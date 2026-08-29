# EcoLoop Backend — API Contract

Base URL (local): `http://127.0.0.1:5000`

All responses are JSON. CORS is enabled for `*` (local dev).

---

## GET /api/health

Health check + Gemini configuration status.

**Response 200**
```json
{
  "status": "ok",
  "service": "EcoLoop Backend",
  "gemini_configured": true,
  "gemini_status": "ok",
  "model": "gemini-2.5-flash"
}
```

**cURL**
```bash
curl http://127.0.0.1:5000/api/health
```

---

## POST /api/analyze

Analyze a waste image with Gemini Vision. **Multi-class** — returns one entry per distinct waste object.

### Request
- Content-Type: `multipart/form-data`
- Field: `image` (file)
- Supported: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- Max size: `10 MB` (configured via `MAX_IMAGE_SIZE_MB`)

**cURL**
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "image=@plastic_bottle.jpg"
```

**JS fetch**
```js
const fd = new FormData();
fd.append("image", file); // File from <input type="file">
const res = await fetch("http://127.0.0.1:5000/api/analyze", {
  method: "POST",
  body: fd
});
const data = await res.json();
```

### Success Response 200
```json
{
  "success": true,
  "items": [
    {
      "item": "Plastic bottle",
      "material": "PET plastic",
      "class": "Recyclable",
      "confidence": 94,
      "disposal": "Recyclable / Dry Waste",
      "points": 10,
      "waste_diverted_kg": 0.02,
      "co2_saved_kg": 0.08,
      "explanation": "Clean PET bottle suitable for dry waste recycling.",
      "box_2d": [120, 200, 800, 600]
    },
    {
      "item": "Vegetable scraps",
      "material": "Biodegradable organic matter",
      "class": "Biogas",
      "confidence": 96,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "Suitable for the EcoLoop organic recovery pathway.",
      "box_2d": [210, 120, 680, 610]
    }
  ],
  "summary": {
    "total_items": 2,
    "classes_detected": ["Biogas", "Recyclable"],
    "dominant_class": "Biogas"
  },
  "image": {
    "width": 1706,
    "height": 959
  },
  "model": "gemini-2.5-flash",
  "latency_ms": 1820
}
```

### Item Fields
| Field | Type | Notes |
|-------|------|-------|
| `item` | string | Short object name |
| `material` | string | Inferred material |
| `class` | enum | `Recyclable` \| `Biogas` \| `Non-Recyclable` \| `Others` \| `E-Waste/Hazardous` |
| `confidence` | int 0-100 | Model confidence, clamped |
| `disposal` | string | Human-readable disposal route |
| `points` | int | Demo EcoPoints (deterministic: Recyclable 10, Biogas 15, Non-Recyclable 5, Others 0, E-Waste 25) |
| `waste_diverted_kg` | float | Demo impact (Recyclable 0.02, Biogas 0.10, E-Waste 0.15, others 0) |
| `co2_saved_kg` | float | Demo impact (Recyclable 0.08, Biogas 0.05, E-Waste 0.20, others 0) |
| `explanation` | string | One-sentence reasoning |
| `box_2d` | [ymin,xmin,ymax,xmax] | Optional, normalized 0-1000. Omit if not localizable. Validation: ints 0-1000, ymin<ymax, xmin<xmax. Frontend converts: `top=ymin/10%`, `left=xmin/10%` etc. |
| `mask` | [[x,y],...] | Optional polygon, normalized 0-1000 |

### Summary Fields
- `total_items`: number of items
- `classes_detected`: sorted unique classes
- `dominant_class`: most frequent class (tie-break by confidence)

### Error Responses
All errors: `{ "success": false, "error": { "code": "...", "message": "..." } }`

| HTTP | code | When |
|------|------|------|
| 400 | `IMAGE_REQUIRED` | No file / empty filename / field not `image` |
| 400 | `IMAGE_EMPTY` | Zero-byte file |
| 400 | `IMAGE_INVALID` | Not decodable by Pillow |
| 413 | `IMAGE_TOO_LARGE` | >10 MB |
| 500 | `GEMINI_NOT_CONFIGURED` | `GEMINI_API_KEY` missing |
| 429 | `GEMINI_RATE_LIMITED` | Gemini quota/rate hit |
| 422 | `GEMINI_SAFETY_BLOCK` | Safety filter blocked image |
| 502 | `GEMINI_ERROR` | Other Gemini failure |
| 500 | `ANALYSIS_FAILED` | Unexpected |

**Example error**
```json
{
  "success": false,
  "error": {
    "code": "IMAGE_REQUIRED",
    "message": "Please upload an image. Field name must be 'image'."
  }
}
```

---

## GET /api/stats

Demo aggregate stats (static seed + in-memory session scans). No DB.

**Response 200**
```json
{
  "eco_points": 2480,
  "items_recycled": 47,
  "waste_diverted_kg": 12.4,
  "co2_saved_kg": 8.7
}
```
After scans in this session, values increase:
```json
{
  "eco_points": 2510,
  "items_recycled": 49,
  "waste_diverted_kg": 12.52,
  "co2_saved_kg": 8.83,
  "scans_this_session": 2
}
```

**cURL**
```bash
curl http://127.0.0.1:5000/api/stats
```

---

## Frontend Integration Notes

- **Expect `items` array** — never assume single classification. Render 0..N boxes.
- **Bounding boxes**: `box_2d` is optional. If present, draw: `top=ymin/10%`, `left=xmin/10%`, `width=(xmax-xmin)/10%`, `height=(ymax-ymin)/10%`. Never fabricate boxes; hide if missing.
- **Biogas is key differentiator** — surface it prominently when `class === "Biogas"`.
- **CORS**: `Access-Control-Allow-Origin: *` for local dev. No auth needed Round-1.
- **Latency**: watch `latency_ms`; show spinner while waiting.

## Environment

 Backend reads `backend/.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash   # single source of truth, change without code edits
HOST=127.0.0.1
PORT=5000
```

`.env` is gitignored. Copy `backend/.env.example`.

---

## Running Locally (uv)

> All commands use **uv** — do NOT use plain `pip`/`venv`. `uv` manages the `.venv` and pins via `uv.lock`.

```bash
# 1. Create venv (Python 3.14) — creates .venv at repo root
uv venv --python 3.14
# Activate only if you need a shell (uv run is preferred):
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

# 2. Install deps (pick ONE)
uv sync --no-install-project        # from pyproject.toml (recommended)
# or
uv pip install -r backend/requirements.txt

# 3. Configure key
cp backend/.env.example backend/.env
# edit backend/.env -> set GEMINI_API_KEY=...
# (backend/.env is gitignored — never commit)

# 4. Run — always via uv run so .venv + .env are respected
uv run python backend/app.py
# -> http://127.0.0.1:5000

# Alternative: uv run with explicit module
uv run python -m backend.app
```

Test:
```bash
curl http://127.0.0.1:5000/api/health
curl -F "image=@test.jpg" http://127.0.0.1:5000/api/analyze

# Or via uv run Python test client (no curl needed)
uv run python -c "from backend.app import create_app; app=create_app(); print(app.test_client().get('/api/health').json)"
```
