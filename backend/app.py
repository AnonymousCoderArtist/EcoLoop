"""
EcoLoop Flask Backend — Modular Factory
Endpoints:
  GET  /api/health
  POST /api/analyze  (multipart/form-data, field: image)
  GET  /api/stats
"""

from __future__ import annotations

import io
import logging
import os
import time
from typing import Any

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image
from werkzeug.exceptions import RequestEntityTooLarge
from pathlib import Path
import json as _json

# Support both direct run (`python backend/app.py`) and module run (`uv run`)
try:
    from config import (  # type: ignore
        ALLOWED_MIME_TYPES,
        MAX_IMAGE_SIZE_BYTES,
        MAX_IMAGE_SIZE_MB,
    )
    from gemini import analyze_image, check_api_key  # type: ignore
except ImportError:
    from backend.config import (  # type: ignore
        ALLOWED_MIME_TYPES,
        MAX_IMAGE_SIZE_BYTES,
        MAX_IMAGE_SIZE_MB,
    )
    from backend.gemini import analyze_image, check_api_key  # type: ignore

# ── In-memory scan history (for /api/stats) ────────────────────────
_scan_history: list[dict[str, Any]] = []

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    # Allow all origins for local dev; tighten in production if needed
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_SIZE_BYTES

    # ── Helpers ──────────────────────────────────────────────────

    def error_response(code: str, message: str, status: int = 400):
        return jsonify({"success": False, "error": {"code": code, "message": message}}), status

    # ── Routes ───────────────────────────────────────────────────

    @app.get("/")
    def root():
        return jsonify(
            {
                "service": "EcoLoop Backend",
                "version": "0.1.0",
                "endpoints": ["/api/health", "/api/analyze", "/api/stats"],
            }
        )

    @app.get("/api/health")
    def health():
        ok, msg = check_api_key()
        return jsonify(
            {
                "status": "ok",
                "service": "EcoLoop Backend",
                "gemini_configured": ok,
                "gemini_status": msg,
                "model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            }
        )

    # ── Demo: serve annotated Swiss image & cached zones (loader + points) ──
    @app.get("/api/demo")
    def demo_info():
        """Return demo options: annotated Swiss image vs live upload."""
        backend_dir = Path(__file__).resolve().parent
        last_json = backend_dir / "last_result.json"
        annotated = backend_dir / "image_annotated.png"
        has_annotated = annotated.exists()
        # Read points/classes from cache if exists, else static demo
        if last_json.exists():
            try:
                data = _json.loads(last_json.read_text(encoding="utf-8"))
                items = data.get("items", [])
                total_points = sum(i.get("points", 0) for i in items)
                classes = data.get("summary", {}).get("classes_detected", [])
            except Exception:
                total_points, classes = 45, ["Biogas", "Recyclable", "Non-Recyclable"]
        else:
            total_points, classes = 45, ["Biogas", "Recyclable", "Non-Recyclable"]
        return jsonify({
            "options": [
                {
                    "id": "annotated",
                    "label": "Swiss Zones Demo",
                    "description": "Pre-analyzed Swiss editorial zones (Biogas priority) - instant demo with loader",
                    "image_url": "/api/demo/image",
                    "thumbnail_url": "/api/demo/image",
                    "available": has_annotated,
                    "points": total_points,
                    "classes": classes,
                    "hint": "Click to simulate 1.2s loader -> zone boxes -> points added"
                },
                {
                    "id": "live",
                    "label": "Upload Your Image",
                    "description": "Live Gemini Vision analysis via /api/analyze",
                    "image_url": None,
                    "available": True,
                    "points": None,
                    "classes": None,
                    "hint": "POST /api/analyze with multipart image"
                }
            ],
            "live": True,
            "annotated_exists": has_annotated
        })

    @app.get("/api/demo/image")
    def demo_image():
        """Serve Swiss annotated image (backend/image_annotated.png)."""
        backend_dir = Path(__file__).resolve().parent
        annotated = backend_dir / "image_annotated.png"
        fallback = backend_dir / "image.png"
        target = annotated if annotated.exists() else fallback
        if not target.exists():
            return jsonify({"success": False, "error": {"code": "DEMO_IMAGE_MISSING", "message": "Run uv run python backend/visualize.py first"}}), 404
        # CORS already enabled; ensure correct mimetype
        return send_file(target, mimetype="image/png", max_age=0)

    @app.get("/api/demo/result")
    def demo_result():
        """Return cached demo JSON instantly (for frontend to preload)."""
        backend_dir = Path(__file__).resolve().parent
        last_json = backend_dir / "last_result.json"
        if not last_json.exists():
            return jsonify({"success": False, "error": {"code": "DEMO_CACHE_MISSING", "message": "No last_result.json — run visualize.py"}}), 404
        try:
            data = _json.loads(last_json.read_text(encoding="utf-8"))
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"success": False, "error": {"code": "DEMO_CACHE_ERROR", "message": str(e)}}), 500

    @app.post("/api/demo/analyze")
    def demo_analyze():
        """Demo loader: sleep 1.2s then return cached zones + add to points."""
        backend_dir = Path(__file__).resolve().parent
        last_json = backend_dir / "last_result.json"
        # Optional JSON body {demo:"annotated"} ignored — only one demo set
        # Simulate loader
        time.sleep(1.2)
        if not last_json.exists():
            return jsonify({"success": False, "error": {"code": "DEMO_CACHE_MISSING", "message": "Run uv run python backend/visualize.py first"}}), 404
        try:
            result = _json.loads(last_json.read_text(encoding="utf-8"))
        except Exception as e:
            return jsonify({"success": False, "error": {"code": "DEMO_CACHE_ERROR", "message": str(e)}}), 500
        # Add to points (same as /api/analyze)
        try:
            items = result.get("items", [])
            points_total = sum(i.get("points", 0) for i in items)
            diverted_total = sum(i.get("waste_diverted_kg", 0) for i in items)
            co2_total = sum(i.get("co2_saved_kg", 0) for i in items)
            _scan_history.append({
                "timestamp": time.time(),
                "items_count": len(items),
                "points_total": points_total,
                "waste_diverted_kg": diverted_total,
                "co2_saved_kg": co2_total,
                "classes": result.get("summary", {}).get("classes_detected", []),
            })
            if len(_scan_history) > 100:
                _scan_history.pop(0)
            result["latency_ms"] = 1200
            result["demo"] = True
        except Exception:
            pass
        return jsonify(result), 200

    @app.get("/api/stats")
    def stats():
        """Demo stats — aggregated from in-memory history + static seed."""
        # Static seed for demo before any scans
        seed = {"eco_points": 2480, "items_recycled": 47, "waste_diverted_kg": 12.4, "co2_saved_kg": 8.7}
        if not _scan_history:
            return jsonify(seed)

        total_points = seed["eco_points"] + sum(s.get("points_total", 0) for s in _scan_history)
        total_items = seed["items_recycled"] + sum(s.get("items_count", 0) for s in _scan_history)
        total_diverted = seed["waste_diverted_kg"] + sum(s.get("waste_diverted_kg", 0) for s in _scan_history)
        total_co2 = seed["co2_saved_kg"] + sum(s.get("co2_saved_kg", 0) for s in _scan_history)

        return jsonify(
            {
                "eco_points": total_points,
                "items_recycled": total_items,
                "waste_diverted_kg": round(total_diverted, 2),
                "co2_saved_kg": round(total_co2, 2),
                "scans_this_session": len(_scan_history),
            }
        )

    @app.post("/api/analyze")
    def analyze():
        start = time.time()

        # ── 1. Validate file presence (works even without API key) ─

        if "image" not in request.files:
            return error_response("IMAGE_REQUIRED", "Please upload an image. Field name must be 'image'.", 400)

        file = request.files["image"]
        if not file or file.filename == "" or file.filename is None:
            return error_response("IMAGE_REQUIRED", "Please upload an image. No file selected.", 400)

        # ── 3. Validate size (Flask also enforces MAX_CONTENT_LENGTH) ─
        # Read bytes
        try:
            image_bytes = file.read()
        except Exception as e:
            return error_response("IMAGE_READ_ERROR", f"Could not read uploaded file: {e}", 400)

        if len(image_bytes) == 0:
            return error_response("IMAGE_EMPTY", "Uploaded file is empty.", 400)

        if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
            return error_response(
                "IMAGE_TOO_LARGE",
                f"Image is too large ({len(image_bytes) / 1024 / 1024:.1f} MB). Maximum is {MAX_IMAGE_SIZE_MB} MB.",
                413,
            )

        # ── 4. Validate MIME / image decodability ────────────────
        mime_type = file.mimetype or file.content_type or "image/jpeg"
        # Some browsers send octet-stream; we will infer from Pillow
        if mime_type not in ALLOWED_MIME_TYPES and mime_type != "application/octet-stream":
            # Still allow if Pillow can open it, but warn
            logger.warning("Unusual MIME type: %s for file %s", mime_type, file.filename)

        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()  # verify without full decode
            # Re-open after verify (verify closes)
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            # Convert format to mime if needed
            fmt = (img.format or "JPEG").lower()
            mime_map = {"jpeg": "image/jpeg", "jpg": "image/jpeg", "png": "image/png", "webp": "image/webp", "gif": "image/gif"}
            inferred_mime = mime_map.get(fmt, mime_type)
            if mime_type == "application/octet-stream":
                mime_type = inferred_mime
        except Exception as e:
            return error_response(
                "IMAGE_INVALID",
                f"Uploaded file is not a valid image (JPG/PNG/WEBP). Error: {e}",
                400,
            )

        # ── 5. Validate API key (after file validation so IMAGE_REQUIRED works) ─
        ok, msg = check_api_key()
        if not ok:
            return error_response(
                "GEMINI_NOT_CONFIGURED",
                f"Server is not configured with a Gemini API key: {msg}. Add GEMINI_API_KEY to backend/.env",
                500,
            )

        # ── 6. Call Gemini ───────────────────────────────────────
        try:
            result = analyze_image(image_bytes, mime_type=mime_type, original_width=width, original_height=height)
        except RuntimeError as e:
            msg = str(e)
            # Map to HTTP status
            if "GEMINI_API_KEY" in msg or "API key" in msg:
                return error_response("GEMINI_NOT_CONFIGURED", msg, 500)
            if "rate-limited" in msg or "quota" in msg.lower():
                return error_response("GEMINI_RATE_LIMITED", msg, 429)
            if "safety" in msg.lower() or "blocked" in msg.lower():
                return error_response("GEMINI_SAFETY_BLOCK", msg, 422)
            return error_response("GEMINI_ERROR", msg, 502)
        except Exception as e:
            logger.exception("Unexpected analyze failure")
            return error_response("ANALYSIS_FAILED", f"Analysis failed: {e}", 500)

        # ── 7. Update in-memory stats ────────────────────────────
        try:
            items = result.get("items", [])
            points_total = sum(i.get("points", 0) for i in items)
            diverted_total = sum(i.get("waste_diverted_kg", 0) for i in items)
            co2_total = sum(i.get("co2_saved_kg", 0) for i in items)
            _scan_history.append(
                {
                    "timestamp": time.time(),
                    "items_count": len(items),
                    "points_total": points_total,
                    "waste_diverted_kg": diverted_total,
                    "co2_saved_kg": co2_total,
                    "classes": result.get("summary", {}).get("classes_detected", []),
                }
            )
            # Keep last 100 scans
            if len(_scan_history) > 100:
                _scan_history.pop(0)
        except Exception:
            pass

        result["latency_ms"] = int((time.time() - start) * 1000)
        return jsonify(result), 200

    # ── Error handlers ──────────────────────────────────────────

    @app.errorhandler(RequestEntityTooLarge)
    def handle_too_large(e):
        return error_response(
            "IMAGE_TOO_LARGE", f"Image exceeds {MAX_IMAGE_SIZE_MB} MB limit.", 413
        )

    @app.errorhandler(404)
    def handle_404(e):
        return error_response("NOT_FOUND", "Endpoint not found.", 404)

    @app.errorhandler(500)
    def handle_500(e):
        logger.exception("Internal error")
        return error_response("INTERNAL_ERROR", "Internal server error.", 500)

    return app


# ── Entrypoint ──────────────────────────────────────────────────────
app = create_app()

if __name__ == "__main__":
    try:
        from config import HOST, PORT  # type: ignore
    except ImportError:
        from backend.config import HOST, PORT  # type: ignore

    ok, msg = check_api_key()
    if not ok:
        print(f"[EcoLoop] WARNING: {msg} — /api/analyze will return GEMINI_NOT_CONFIGURED until .env is set.")
        print(f"[EcoLoop] See backend/.env.example")
    print(f"[EcoLoop] Starting backend on http://{HOST}:{PORT}")
    print(f"[EcoLoop] Model: {os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')}")
    app.run(host=HOST, port=PORT, debug=True)
