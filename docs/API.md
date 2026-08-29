# EcoLoop Backend — API Contract (Frontend Ready)

> **For frontend coder on separate laptop — copy/paste ready.** No auth, CORS open, `items[]` is stream-area zones (2-6 boxes) with Biogas priority.

Base URL (local): `http://127.0.0.1:5000`  
All responses JSON. `Access-Control-Allow-Origin: *` for local dev.

---

## 0. Quick Connect (30s)

**Frontend does NOT need `GEMINI_API_KEY`.** Backend already has `backend/.env` with `gemini-2.5-flash`.

```bash
# Backend already running via uv (from backend/gemini branch):
uv sync --no-install-project
uv run python backend/app.py
# -> http://127.0.0.1:5000
```

**Test from frontend machine** (same Wi-Fi or localhost):
```bash
curl http://127.0.0.1:5000/api/health
# {"status":"ok","gemini_configured":true,"model":"gemini-2.5-flash"}
```

**Pick any image and POST:**
```bash
curl -X POST http://127.0.0.1:5000/api/analyze -F "image=@backend/image.png"
```

If you get `GEMINI_NOT_CONFIGURED`, backend `.env` missing — tell backend lead.

---

## 1. GET /api/health

Health + Gemini status. Poll this before `/api/analyze`.

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

**JS**
```js
const r = await fetch("http://127.0.0.1:5000/api/health");
const { gemini_configured, model } = await r.json();
if (!gemini_configured) showError("Backend Gemini not configured");
```

---

## 2. POST /api/analyze

**Stream-area detection** — returns 2-6 **zones** (not per-object). Each zone = contiguous waste area of one operational class. One image → multiple zones (e.g., Recyclable heap + Biogas heap + Non-Recyclable heap). **Biogas is max priority**: if an area could be biodegradable *or* Biogas, backend returns Biogas.

### Request
- Content-Type: `multipart/form-data`
- Field: `image` (file) — name must be exactly `image`
- Supported: `image/jpeg`, `image/png`, `image/webp`, `image/gif`
- Max: `10 MB` (`MAX_IMAGE_SIZE_MB` at `backend/config.py:19`)
- CORS: `*` — no headers needed, no auth

**cURL**
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "image=@plastic_bottle.jpg"
```

**JS fetch (React / vanilla)**
```js
const fd = new FormData();
fd.append("image", file); // from <input type="file"> or drag-drop
const res = await fetch("http://127.0.0.1:5000/api/analyze", { method: "POST", body: fd });
const data = await res.json();
if (!data.success) { showError(data.error.message); return; }
// data.items -> zones, data.summary -> aggregate
```

**React Dropzone example**
```jsx
const onDrop = async (files) => {
  const fd = new FormData();
  fd.append("image", files[0]);
  const r = await fetch("http://127.0.0.1:5000/api/analyze", { method: "POST", body: fd });
  const j = await r.json();
  setResult(j); // j.items, j.summary, j.image
};
```

### Success Response 200 — Zone-based (current)
```json
{
  "success": true,
  "items": [
    {
      "item": "Recyclable zone — plastic bottles and aluminum cans",
      "material": "PET, aluminum",
      "class": "Recyclable",
      "confidence": 98,
      "disposal": "Recyclable / Dry Waste",
      "points": 10,
      "waste_diverted_kg": 0.02,
      "co2_saved_kg": 0.08,
      "explanation": "Recyclable zone: PET bottles and aluminum cans.",
      "box_2d": [100, 0, 900, 250]
    },
    {
      "item": "Biogas zone — vegetable and fruit peels",
      "material": "Organic food waste",
      "class": "Biogas",
      "confidence": 98,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "Biogas zone: vegetable peels, whole vegetables, and fruit waste suitable for biogas.",
      "box_2d": [100, 250, 900, 500]
    },
    {
      "item": "Biogas zone — cardboard, leaves, and coffee grounds",
      "material": "Organic waste, cardboard",
      "class": "Biogas",
      "confidence": 95,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "Biogas zone: cardboard pieces, dry leaves, and coffee grounds suitable for composting/biogas.",
      "box_2d": [100, 500, 900, 750]
    },
    {
      "item": "Non-Recyclable zone — mixed waste",
      "material": "Mixed plastics, non-recyclable packaging, medical waste",
      "class": "Non-Recyclable",
      "confidence": 98,
      "disposal": "Non-Recyclable / Landfill (Last Resort)",
      "points": 5,
      "waste_diverted_kg": 0.0,
      "co2_saved_kg": 0.0,
      "explanation": "Non-Recyclable zone: plastic packaging, face mask, coffee capsules, and plastic cutlery.",
      "box_2d": [100, 750, 900, 1000]
    }
  ],
  "summary": {
    "total_items": 4,
    "classes_detected": ["Biogas", "Non-Recyclable", "Recyclable"],
    "dominant_class": "Biogas"
  },
  "image": { "width": 1280, "height": 698 },
  "model": "gemini-2.5-flash",
  "latency_ms": 23967
}
```
*Real output from `backend/image.png` (2.0 MB) — 4 Swiss zones. See `backend/visualize.py`.*

### Item (Zone) Fields
| Field | Type | Notes |
|-------|------|-------|
| `item` | string | Zone name (e.g., `Biogas zone — vegetable peels`) — display as title |
| `material` | string | Composite material (e.g., `PET, aluminum` or `Organic food waste`) |
| `class` | enum | `Recyclable` \| `Biogas` \| `Non-Recyclable` \| `Others` \| `E-Waste/Hazardous` — **Biogas max priority** |
| `confidence` | int 0-100 | Clamped; show as `%` badge |
| `disposal` | string | `Recyclable / Dry Waste`, `Organic / Biogas Feedstock`, `Non-Recyclable / Landfill`, `Others / Manual Sorting`, `E-Waste / Hazardous` |
| `points` | int | **Per-zone** EcoPoints: `Recyclable 10`, `Biogas 15`, `Non-Recyclable 5`, `Others 0`, `E-Waste 25` — sum for total |
| `waste_diverted_kg` | float | Per-zone demo: `Recyclable 0.02`, `Biogas 0.10`, `E-Waste 0.15`, else `0` |
| `co2_saved_kg` | float | Per-zone demo: `Recyclable 0.08`, `Biogas 0.05`, `E-Waste 0.20`, else `0` |
| `explanation` | string | 1-sentence zone description |
| `box_2d` | `[ymin,xmin,ymax,xmax]` | **Zone bbox**, normalized `0-1000` (Gemini convention). Optional — omit if not localizable. Validation: ints `0-1000`, `ymin<ymax`, `xmin<xmax`. Frontend converts to `%` (see below). |
| `mask` | `[[x,y],...]` | Optional polygon `0-1000` — future use |

### Rendering `box_2d` (Swiss style reference)
Backend `backend/visualize.py:70` uses this exact math — copy for frontend overlay `<div style="position:relative">` + absolute boxes:

```js
// box_2d [ymin,xmin,ymax,xmax] 0-1000 -> CSS %
function toPct(box, imgW, imgH) { // or use % directly
  const [ymin, xmin, ymax, xmax] = box;
  return {
    top: `${ymin/10}%`,
    left: `${xmin/10}%`,
    width: `${(xmax - xmin)/10}%`,
    height: `${(ymax - ymin)/10}%`,
  };
}
// Or pixels if you have img natural size:
function toPixels(box, imgW, imgH) {
  const [ymin, xmin, ymax, xmax] = box;
  return {
    x: xmin/1000*imgW, y: ymin/1000*imgH,
    w: (xmax-xmin)/1000*imgW, h: (ymax-ymin)/1000*imgH
  };
}
```

**Swiss editorial reference** (from `backend/image_annotated.png`): each box has light wash fill (~15% alpha) + thin border + 11px solid corner squares + `#02 BIOGAS ZONE · BIOGAS · 98% · +15 PTS` label with left accent bar. Colors: `Recyclable #16a34a`, `Biogas #ca8a04` (amber, priority), `Non-Recyclable #dc2626`, `E-Waste #9333ea`, `Others #6b7280`. Frontend may replicate or use its own premium style — contract is `box_2d + class + points`.

**Must:**
- Expect `items[]` length `0..6` zones (handle 0 = no waste).
- `box_2d` optional — hide box if missing, never fabricate.
- Show per-zone `+{points} PTS` and `class` badge inside/above box, plus disposal below.
- Aggregate total: `sum(points)`, `classes_detected`, `dominant_class`.

### Summary Fields
- `total_items`: zone count (`items.length`)
- `classes_detected`: sorted unique classes (e.g., `["Biogas","Recyclable"]`)
- `dominant_class`: most frequent zone class (tie → highest confidence) — highlight prominently (Biogas if present)

### Error Responses
All errors: `{ "success": false, "error": { "code": "...", "message": "..." } }` with meaningful HTTP.

| HTTP | code | When | Frontend action |
|------|------|------|-----------------|
| 400 | `IMAGE_REQUIRED` | No file / wrong field name (`image`) | Show “Please upload an image” |
| 400 | `IMAGE_EMPTY` | 0 bytes | Show “File empty” |
| 400 | `IMAGE_INVALID` | Not JPG/PNG/WEBP (Pillow fails) | Show “Invalid image” |
| 413 | `IMAGE_TOO_LARGE` | >10 MB | Show “Image too large (10MB)” |
| 500 | `GEMINI_NOT_CONFIGURED` | `backend/.env` missing key | Show “Backend not configured — contact backend lead” |
| 429 | `GEMINI_RATE_LIMITED` | Quota hit | Retry after 5s, show “Busy, retrying” |
| 422 | `GEMINI_SAFETY_BLOCK` | Safety filter | Show “Try different image” |
| 502 | `GEMINI_ERROR` | Gemini failure | Show “Analysis failed, retry” |
| 500 | `ANALYSIS_FAILED` | Unexpected | Show generic error |

**Example error**
```json
{
  "success": false,
  "error": { "code": "IMAGE_REQUIRED", "message": "Please upload an image. Field name must be 'image'." }
}
```

**JS error handling**
```js
const r = await fetch("http://127.0.0.1:5000/api/analyze", { method: "POST", body: fd });
const j = await r.json();
if (!r.ok || !j.success) {
  const code = j.error?.code;
  if (code === "IMAGE_REQUIRED") toast("Upload an image");
  else if (code === "IMAGE_TOO_LARGE") toast("Max 10MB");
  else if (code === "GEMINI_RATE_LIMITED") setTimeout(retry, 5000);
  else toast(j.error.message);
  return;
}
render(j);
```

---

## 3. GET /api/stats

Demo aggregate (static seed + in-memory session). No DB.

**Response 200**
```json
{
  "eco_points": 2480,
  "items_recycled": 47,
  "waste_diverted_kg": 12.4,
  "co2_saved_kg": 8.7
}
```
After your `POST /api/analyze` calls in same session:
```json
{
  "eco_points": 2525,
  "items_recycled": 51,
  "waste_diverted_kg": 12.64,
  "co2_saved_kg": 8.92,
  "scans_this_session": 1
}
```

**Poll for dashboard**
```js
const s = await fetch("http://127.0.0.1:5000/api/stats").then(r=>r.json());
// s.eco_points etc.
```

---

## 4. Frontend Integration Checklist

- [ ] `GET /api/health` → show green if `gemini_configured`
- [ ] `POST /api/analyze` with `FormData image` → handle `items[]` zones (render 0..N boxes)
- [ ] Convert `box_2d` via `ymin/10%` etc.; light wash + corner squares optional
- [ ] Per-zone: title `item`, badge `class` + `confidence%`, `+points PTS`, footer `disposal`, `waste_diverted_kg`/`co2_saved_kg`
- [ ] Summary bar: `total_items`, `classes_detected` (chips), `dominant_class` (hero), `sum(points)` total
- [ ] Handle `!success` errors by `code` (see table) — never crash on malformed Gemini
- [ ] Show `latency_ms` spinner; debounce uploads

**Visual reference:** `backend/image_annotated.png` generated by `uv run python backend/visualize.py` (Swiss: light fill + 11px corner squares). Your frontend can mimic or diverge — API guarantees `box_2d` + `class` + `points`.

---

## 5. Environment (backend only — frontend ignores)

Backend reads `backend/.env` (gitignored):
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash   # single source at backend/config.py:17
HOST=127.0.0.1
PORT=5000
MAX_IMAGE_SIZE_MB=10
```
`.env` never committed. `GEMINI_MODEL` change requires no code edit.

---

## 6. Running Locally (uv — single source)

> All backend commands via `uv` — never plain `pip`.

```bash
# 1. venv (Python 3.14) at repo root
uv venv --python 3.14
# activate only if needed: .venv\Scripts\activate (Win) / source .venv/bin/activate (Unix)

# 2. deps (one of)
uv sync --no-install-project        # from pyproject.toml + uv.lock (preferred)
uv pip install -r backend/requirements.txt

# 3. key
cp backend/.env.example backend/.env
# edit GEMINI_API_KEY

# 4. run (uv ensures .venv + .env)
uv run python backend/app.py
# or: uv run python -m backend.app
# -> http://127.0.0.1:5000

# Visual proof (backend only, not for frontend)
uv run python backend/visualize.py              # live Gemini -> backend/image_annotated.png
uv run python backend/visualize.py --cached     # re-render from backend/last_result.json
```

**Verify**
```bash
curl http://127.0.0.1:5000/api/health
curl -X POST http://127.0.0.1:5000/api/analyze -F "image=@backend/image.png"
uv run python -c "from backend.app import create_app; print(create_app().test_client().get('/api/health').json)"
```

---

## 7. CORS & Deployment Notes

- `Flask-CORS` at `backend/app.py:49` — `origins: *` for `/api/*`. Frontend may run `vite`, `next`, or file:// — all allowed in Round-1.
- No auth, no cookies. For production, tighten `CORS` to frontend origin.
- If frontend and backend on different hosts (e.g., `192.168.x.x`), frontend must fetch `http://<backend-ip>:5000/api/analyze` — ensure backend binds `HOST=0.0.0.0` in `backend/.env`.

**Contact:** Backend branch `backend/gemini` — see `README.md`. For contract drift, check `backend/gemini.py:36` prompt (stream-area, Biogas max) and `backend/schemas.py:8` validation.
