"""Validation & sanitization helpers for EcoLoop items."""

from __future__ import annotations

from collections import Counter
from typing import Any

try:
    from config import (  # type: ignore
        ALLOWED_CLASSES,
        CATEGORY_IMPACT,
        CATEGORY_POINTS,
        DISPOSAL_MAP,
    )
except ImportError:
    from backend.config import (  # type: ignore
        ALLOWED_CLASSES,
        CATEGORY_IMPACT,
        CATEGORY_POINTS,
        DISPOSAL_MAP,
    )


def sanitize_class(raw: str | None) -> str:
    """Validate class against enum, fallback to Others."""
    if not raw or not isinstance(raw, str):
        return "Others"
    # Normalize common aliases from model
    normalized = raw.strip()
    aliases = {
        "organic": "Biogas",
        "compostable": "Biogas",
        "biodegradable": "Biogas",
        "recyclable": "Recyclable",
        "non-recyclable": "Non-Recyclable",
        "non_recyclable": "Non-Recyclable",
        "general waste": "Non-Recyclable",
        "general_waste": "Non-Recyclable",
        "e-waste": "E-Waste/Hazardous",
        "e_waste": "E-Waste/Hazardous",
        "hazardous": "E-Waste/Hazardous",
        "e-waste/hazardous": "E-Waste/Hazardous",
        "others": "Others",
        "unknown": "Others",
        "other": "Others",
    }
    lower = normalized.lower()
    if normalized in ALLOWED_CLASSES:
        return normalized
    if lower in aliases:
        return aliases[lower]
    return "Others"


def clamp_confidence(value: Any) -> int:
    try:
        iv = int(float(value))
    except Exception:
        return 0
    return max(0, min(100, iv))


def validate_box(box: Any) -> list[int] | None:
    """Validate box_2d: [ymin, xmin, ymax, xmax] 0-1000, ymin<ymax etc."""
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        return None
    try:
        coords = [int(float(c)) for c in box]
    except Exception:
        return None
    # Clamp 0-1000
    coords = [max(0, min(1000, c)) for c in coords]
    ymin, xmin, ymax, xmax = coords
    if ymin >= ymax or xmin >= xmax:
        return None
    return coords


def get_points(klass: str, raw_points: Any) -> int:
    """Return deterministic points; override unreasonable model values."""
    expected = CATEGORY_POINTS.get(klass, 0)
    try:
        p = int(float(raw_points))
        # If model returns wildly off (e.g., negative or >100), use deterministic
        if 0 <= p <= 100 and abs(p - expected) <= 30:
            # Allow model variance within 30, otherwise clamp to expected?
            # Spec says: if unreasonable, use deterministic. We'll enforce expected
            # strictly for demo consistency.
            return expected
        return expected
    except Exception:
        return expected


def get_impact(klass: str, raw_diverted: Any, raw_co2: Any) -> tuple[float, float]:
    """Return deterministic impact; ignore model values and use category."""
    diverted, co2 = CATEGORY_IMPACT.get(klass, (0.0, 0.0))
    # We intentionally use deterministic values per spec to avoid invented science.
    return diverted, co2


def sanitize_item(raw: dict[str, Any]) -> dict[str, Any]:
    klass = sanitize_class(raw.get("class") or raw.get("category"))
    confidence = clamp_confidence(raw.get("confidence", 0))
    points = get_points(klass, raw.get("points"))
    waste_diverted, co2_saved = get_impact(
        klass, raw.get("waste_diverted_kg"), raw.get("co2_saved_kg")
    )
    disposal = raw.get("disposal") or DISPOSAL_MAP.get(klass, "Others / Manual Sorting Required")
    # Ensure disposal matches expected mapping if model invents something weird
    if klass in DISPOSAL_MAP and disposal not in DISPOSAL_MAP.values():
        # Keep model disposal if it looks reasonable (contains known keywords), else map
        if not any(kw in disposal.lower() for kw in ["recycl", "biogas", "organic", "hazard", "e-waste", "landfill", "others"]):
            disposal = DISPOSAL_MAP[klass]

    item: dict[str, Any] = {
        "item": str(raw.get("item") or raw.get("label") or "Unknown waste item")[:120],
        "material": str(raw.get("material") or "Unknown material")[:120],
        "class": klass,
        "confidence": confidence,
        "disposal": str(disposal)[:120],
        "points": points,
        "waste_diverted_kg": waste_diverted,
        "co2_saved_kg": co2_saved,
        "explanation": str(raw.get("explanation") or raw.get("reason") or "")[:300],
    }

    box = validate_box(raw.get("box_2d") or raw.get("box"))
    if box is not None:
        item["box_2d"] = box

    # Optional mask — keep if looks like list of [x,y]
    mask = raw.get("mask")
    if isinstance(mask, list) and len(mask) >= 3:
        # Validate polygon
        valid = True
        for pt in mask:
            if not isinstance(pt, (list, tuple)) or len(pt) != 2:
                valid = False
                break
            try:
                x, y = int(float(pt[0])), int(float(pt[1]))
                if not (0 <= x <= 1000 and 0 <= y <= 1000):
                    valid = False
                    break
            except Exception:
                valid = False
                break
        if valid:
            item["mask"] = [[int(float(x)), int(float(y))] for x, y in mask]

    return item


def build_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    if not items:
        return {"total_items": 0, "classes_detected": [], "dominant_class": "Others"}
    classes = [i["class"] for i in items]
    counter = Counter(classes)
    # Dominant = most frequent; tie-break by highest confidence
    most_common = counter.most_common()
    max_count = most_common[0][1]
    tied = [c for c, cnt in most_common if cnt == max_count]
    if len(tied) == 1:
        dominant = tied[0]
    else:
        # highest confidence among tied
        best = None
        best_conf = -1
        for it in items:
            if it["class"] in tied and it["confidence"] > best_conf:
                best_conf = it["confidence"]
                best = it["class"]
        dominant = best or tied[0]

    return {
        "total_items": len(items),
        "classes_detected": sorted(set(classes)),
        "dominant_class": dominant,
    }
