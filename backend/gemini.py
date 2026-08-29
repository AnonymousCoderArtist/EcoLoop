"""
EcoLoop Gemini Waste Intelligence Service.

Handles:
- Gemini client init & graceful missing-key errors
- Multi-class waste prompt with bounding boxes
- Structured JSON parsing with fallbacks
- Sanitization via schemas helpers
"""

from __future__ import annotations

import base64
import json
import logging
import mimetypes
import re
import traceback
from io import BytesIO
from typing import Any

from PIL import Image

# Support both `python backend/app.py` and `uv run` / package imports
try:
    from config import GEMINI_API_KEY, GEMINI_MODEL  # type: ignore
    from schemas import build_summary, sanitize_item  # type: ignore
except ImportError:
    from backend.config import GEMINI_API_KEY, GEMINI_MODEL  # type: ignore
    from backend.schemas import build_summary, sanitize_item  # type: ignore

logger = logging.getLogger(__name__)

# ── EcoLoop System Prompt ──────────────────────────────────────────

ECOLOOP_SYSTEM_PROMPT = """You are EcoLoop Waste Intelligence — a precise, honest waste-material classifier for the EcoLoop outcome-based waste behaviour platform.

TASK:
Detect contiguous waste AREAS / ZONES by operational stream — NOT individual objects. This is a STREAM-AREA detection task. One image must return 2-6 large zone boxes, one per operational stream area (e.g., one Recyclable zone covering the bottle/can heap, one Biogas zone covering the organic heap, one Non-Recyclable zone covering the bottom mixed waste). Each zone box must tightly enclose a spatially contiguous accumulation of waste of the SAME class. If a pile contains mixed classes that are visually separable, split into separate zones. Do NOT return 20+ tiny per-object boxes — merge into zones.

ECO-LOOP CLASSES (assign exactly one per zone):
1. "Recyclable" — clean paper/cardboard, PET bottles, metal cans, glass bottles, clean recyclable packaging.
2. "Biogas" — MOST IMPORTANT CLASS. Maximum priority. Use for ANY biodegradable/wet organic waste that is suitable for the organic-waste/biogas pathway: food scraps, vegetable/fruit waste, kitchen waste, biodegradable food residues, coffee grounds, leaves suitable for biogas. If an item/area could be described as biodegradable OR Biogas, ALWAYS choose Biogas. If suitable for biogas, Biogas wins over Others/Non-Recyclable. Only use Others if truly not suitable for biogas.
3. "Non-Recyclable" — heavily contaminated packaging, multilayer wrappers, contaminated mixed waste that cannot reasonably enter recyclable/organic streams.
4. "Others" — zone does not confidently fit the supported operational streams or is unclear. Use sparingly.
5. "E-Waste/Hazardous" — electronics, batteries, bulbs, chemicals, medical/domestic hazardous items. Special handling stream.

RULES:
- Return 2-6 ZONES (areas), not per-object instances. Merge adjacent same-class items into ONE zone box.
- Ignore people, hands, furniture, plants, walls, phones, background non-waste objects. Focus ONLY on waste/material zones.
- Never claim certainty when image is unclear. Keep explanations short (one sentence). Include representative contents in explanation (e.g., "Recyclable zone: PET bottles + aluminum cans").
- For each zone return: item (zone name, e.g., "Recyclable heap" or "Biogas zone — vegetable peels + coffee grounds"), material (composite, e.g., "PET, aluminum, cardboard" or "Organic food waste"), class, confidence (0-100 integer), disposal (use: "Recyclable / Dry Waste" for Recyclable, "Organic / Biogas Feedstock" for Biogas, "Non-Recyclable / Landfill (Last Resort)" for Non-Recyclable, "Others / Manual Sorting Required" for Others, "E-Waste / Hazardous - Special Handling" for E-Waste/Hazardous), points (Recyclable 10, Biogas 15, Non-Recyclable 5, Others 0, E-Waste/Hazardous 25), waste_diverted_kg & co2_saved_kg (use conservative demo values: Recyclable 0.02/0.08, Biogas 0.10/0.05, E-Waste/Hazardous 0.15/0.20, others 0/0), explanation.
- BIO GAS PRIORITY: If any doubt between Biogas vs Others/Non-Recyclable for organic matter, choose Biogas. Biogas is the key differentiator of EcoLoop — surface it prominently.
- For every zone, return bounding box "box_2d": [ymin, xmin, ymax, xmax] normalized to 0-1000 (Gemini 0-1000 convention, relative to original image). Box must cover the whole zone area, not a single item. Do NOT invent boxes. Slightly loose box is better than precisely wrong. Validate ymin < ymax and xmin < xmax. Do not return duplicate overlapping zones for same class — merge them.
- Return structured JSON only.

OUTPUT JSON SHAPE (zones):
{
  "items": [
    {
      "item": "Biogas zone — vegetable peels",
      "material": "Organic food waste",
      "class": "Biogas",
      "confidence": 98,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "Biogas zone: vegetable peels + coffee grounds suitable for biogas.",
      "box_2d": [120, 200, 800, 600]
    }
  ]
}

If image contains no waste or is unclear, return {"items": []} with empty array. Never return free-form text outside JSON.
"""

# JSON schema hint for model — used in structured output where supported
RESPONSE_JSON_SCHEMA_HINT = """Respond with valid JSON matching this TypeScript type:
{
  items: Array<{
    item: string;
    material: string;
    class: "Recyclable" | "Biogas" | "Non-Recyclable" | "Others" | "E-Waste/Hazardous";
    confidence: number; // 0-100
    disposal: string;
    points: number;
    waste_diverted_kg: number;
    co2_saved_kg: number;
    explanation: string;
    box_2d?: [number, number, number, number];
  }>
}
"""

# ── Helpers ──────────────────────────────────────────────────────────

def _get_client():
    """Create Gemini client or raise clean error if key missing."""
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Create backend/.env with GEMINI_API_KEY=your_key (see .env.example)."
        )
    try:
        from google import genai

        return genai.Client(api_key=GEMINI_API_KEY)
    except ImportError as e:
        raise RuntimeError(
            "google-genai is not installed. Run: uv pip install -r backend/requirements.txt"
        ) from e


def _extract_json(text: str) -> dict[str, Any]:
    """Robustly extract JSON from model output (handles markdown fences, extra text)."""
    if not text or not text.strip():
        raise ValueError("Empty model response")
    text = text.strip()
    # Strip markdown code fences
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if fence_match:
        text = fence_match.group(1).strip()
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try find outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Model returned malformed JSON: {text[:800]}")


def _image_part_bytes(image_bytes: bytes, mime_type: str) -> dict[str, Any]:
    """Build image part for google-genai. Try new SDK format."""
    # google-genai expects types.Part.from_bytes or inline_data
    # We'll return a dict that caller can adapt; simpler: use PIL + base64 approach
    return {"mime_type": mime_type, "data": image_bytes}


# ── Public API ───────────────────────────────────────────────────────

def analyze_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    original_width: int | None = None,
    original_height: int | None = None,
) -> dict[str, Any]:
    """
    Send image to Gemini and return sanitized EcoLoop result.

    Returns dict with keys: success, items, summary, image (optional), model
    On Gemini error, raises RuntimeError / ValueError with clean message.
    """
    client = _get_client()

    # Prepare prompt with schema hint
    full_prompt = ECOLOOP_SYSTEM_PROMPT + "\n\n" + RESPONSE_JSON_SCHEMA_HINT

    # Determine image MIME if generic
    if mime_type == "application/octet-stream":
        mime_type = "image/jpeg"

    # Build content parts — handle SDK variations gracefully
    # google-genai 1.x: client.models.generate_content(model=..., contents=[Part...])
    # We'll use the most compatible path: base64 + Pillow not needed; SDK handles bytes.

    try:
        from google.genai import types

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

        # Try structured output via response_schema where supported
        # Fallback to plain text JSON if schema not supported by model
        config = None
        try:
            # Attempt to use JSON schema for stricter output
            schema = {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item": {"type": "string"},
                                "material": {"type": "string"},
                                "class": {
                                    "type": "string",
                                    "enum": [
                                        "Recyclable",
                                        "Biogas",
                                        "Non-Recyclable",
                                        "Others",
                                        "E-Waste/Hazardous",
                                    ],
                                },
                                "confidence": {"type": "integer"},
                                "disposal": {"type": "string"},
                                "points": {"type": "integer"},
                                "waste_diverted_kg": {"type": "number"},
                                "co2_saved_kg": {"type": "number"},
                                "explanation": {"type": "string"},
                                "box_2d": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "minItems": 4,
                                    "maxItems": 4,
                                },
                            },
                            "required": [
                                "item",
                                "material",
                                "class",
                                "confidence",
                                "disposal",
                                "points",
                                "waste_diverted_kg",
                                "co2_saved_kg",
                                "explanation",
                            ],
                        },
                    }
                },
                "required": ["items"],
            }
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=schema,
                temperature=0.2,
            )
        except Exception:
            # Older SDK may not support response_json_schema
            try:
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            except Exception:
                config = None

        # Call model
        if config is not None:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[image_part, full_prompt],
                config=config,
            )
        else:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[image_part, full_prompt],
            )

        # Extract text
        text = getattr(response, "text", None)
        if not text:
            # Try candidates
            try:
                text = response.candidates[0].content.parts[0].text  # type: ignore
            except Exception:
                text = str(response)

        parsed = _extract_json(text or "")

    except RuntimeError:
        raise
    except Exception as e:
        logger.error("Gemini call failed: %s\n%s", e, traceback.format_exc())
        # Re-raise as clean error for API layer
        msg = str(e)
        # Map common errors to user-friendly messages
        if "API_KEY" in msg or "API key" in msg or "PERMISSION_DENIED" in msg:
            raise RuntimeError(f"Gemini API key error: {msg}") from e
        if "quota" in msg.lower() or "rate" in msg.lower() or "RESOURCE_EXHAUSTED" in msg:
            raise RuntimeError("Gemini is temporarily rate-limited. Please retry in a moment.") from e
        if "SAFETY" in msg or "blocked" in msg.lower():
            raise RuntimeError("Image was blocked by safety filters. Try a different image.") from e
        raise RuntimeError(f"Gemini analysis failed: {msg}") from e

    # ── Sanitize model output ──────────────────────────────────────
    raw_items = parsed.get("items")
    if raw_items is None:
        # Model may have returned top-level array or different key
        if isinstance(parsed, list):
            raw_items = parsed
        else:
            raw_items = []

    if not isinstance(raw_items, list):
        raw_items = []

    sanitized = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        try:
            sanitized.append(sanitize_item(raw))
        except Exception as e:
            logger.warning("Skipping invalid item %s: %s", raw, e)
            continue

    summary = build_summary(sanitized)

    result: dict[str, Any] = {
        "success": True,
        "items": sanitized,
        "summary": summary,
        "model": GEMINI_MODEL,
    }
    if original_width and original_height:
        result["image"] = {"width": original_width, "height": original_height}

    return result


def check_api_key() -> tuple[bool, str]:
    """Return (ok, message) for health checks."""
    if not GEMINI_API_KEY:
        return False, "GEMINI_API_KEY is not set"
    if len(GEMINI_API_KEY.strip()) < 10:
        return False, "GEMINI_API_KEY looks invalid (too short)"
    return True, "ok"
