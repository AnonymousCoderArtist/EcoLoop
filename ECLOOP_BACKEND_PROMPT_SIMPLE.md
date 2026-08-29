# EcoLoop Backend — Simple Agent Prompt

> **For Backend AI Agent — follow step-by-step, no guesswork.**

## 1. Goal
Demo loop: **Upload image → Gemini Vision → Zones (Biogas priority) → Disposal → EcoPoints → Impact → JSON**. Prototype, not prod.

## 2. Locked Tech
- Python 3.14, Flask, Flask-CORS, `google-genai`, `python-dotenv`, `Pillow`, stdlib
- No Docker/DB/Redis/auth/blockchain

## 3. Structure
```
backend/
  app.py              Flask factory, /api/* routes
  gemini.py           Gemini prompt + sanitize (Biogas max, stream-area 2-6 zones)
  config.py           GEMINI_MODEL single source
  schemas.py          sanitize_item, box validation
  visualize.py        Swiss bbox overlay (light wash + corner squares)
  image.png           demo input (user supplied, gitignored)
  image_annotated.png demo output (Swiss zones, gitignored)
  last_result.json    cached demo JSON (gitignored)
  .env / .env.example GEMINI_API_KEY
```

## 4. Env
- `uv venv --python 3.14` → `uv sync --no-install-project`
- `backend/.env`: `GEMINI_API_KEY=...`, `GEMINI_MODEL=gemini-2.5-flash` (900+ models, 2.5 stable)
- `backend/.env` gitignored, `config.py:9` loads it explicitly (`Path(__file__).parent / ".env"`)

## 5. Gemini Prompt (copy to gemini.py)
```
Detect contiguous waste AREAS/ZONES by stream — NOT per-object. 2-6 large boxes, one per class.
Classes: Recyclable(10pts), Biogas(15pts MAX PRIORITY — if biodegradable→Biogas), Non-Recyclable(5), Others(0), E-Waste(25).
Merge same-class piles into one zone. Return box_2d [ymin,xmin,ymax,xmax] 0-1000 per zone.
```
See full at `backend/gemini.py:36`.

## 6. API (must implement exactly)
- `GET /api/health` → `{status, gemini_configured, model}`
- `POST /api/analyze` multipart `image` → `{success:true, items:[{item,material,class,confidence,disposal,points,waste_diverted_kg,co2_saved_kg,explanation,box_2d}], summary:{total_items,classes_detected,dominant_class}, image, model, latency_ms}` + `box_2d` optional
- `GET /api/stats` → `{eco_points, items_recycled, waste_diverted_kg, co2_saved_kg}`
- **Demo additions** (for frontend loader/demo):
  - `GET /api/demo` → `{options: [{id:"annotated", label:"Swiss Zones Demo", image_url:"/api/demo/image", thumbnail_url:"/api/demo/image", points:45, classes}] , live:true}`
  - `GET /api/demo/image` → serves `backend/image_annotated.png` (Swiss light wash + corner squares, per-zone `+PTS` badge)
  - `POST /api/demo/analyze` `{"demo":"annotated"}` → sleep 1.2s (loader) → return cached `last_result.json` + add to `_scan_history` → points increment at `GET /api/stats`

## 7. Validation
- Never crash: missing image → `IMAGE_REQUIRED`, invalid → `IMAGE_INVALID`, large → `IMAGE_TOO_LARGE`, no key → `GEMINI_NOT_CONFIGURED`, Gemini 404 → map to 502 etc. (see `app.py:54` error_response)
- Sanitize: `schemas.py` clamps `0-100`, validates enum, `box_2d` `0-1000`, points `Biogas 15` etc.

## 8. Run & Test
```bash
uv sync --no-install-project
uv run python backend/app.py # http://127.0.0.1:5000
curl http://127.0.0.1:5000/api/health
curl -F "image=@backend/image.png" http://127.0.0.1:5000/api/analyze
uv run python backend/visualize.py # -> backend/image_annotated.png (4 zones, 45pts)
uv run python backend/visualize.py --cached
curl http://127.0.0.1:5000/api/demo/image --output demo.png
```

## 9. Demo Flow for Frontend (loader + points)
1. Frontend shows 2 cards: **Swiss Zones Demo** (uses `/api/demo/image`) + **Upload Your Image** (calls `/api/analyze`)
2. User clicks Demo → frontend shows loader 1.2s → `POST /api/demo/analyze` → receives 4 zones (Biogas priority) → renders Swiss boxes → calls `GET /api/stats` → points `2480 → 2525`
3. User uploads own image → `POST /api/analyze` → loader → result → points auto-added

## 10. Branch
`backend/gemini` — `git add backend/*` (not `.env`, not `image*.png` nor `last_result.json` per `.gitignore:14-17`) → commit → push

Keep it simple: reliability > performance > clean contract.
