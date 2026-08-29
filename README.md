# EcoLoop — Outcome-Based Waste Behaviour Platform

Round-1 prototype: **Upload waste image → Gemini Vision → Multi-class classification → Disposal route → EcoPoints → Impact → Beautiful frontend**.

---

## Project Structure

```
.
├── backend/               # Flask + Gemini Vision API (this repo's backend)
│   ├── app.py             # Flask factory, routes (/api/health, /api/analyze, /api/stats)
│   ├── gemini.py          # Gemini client, prompt, parsing, sanitization
│   ├── config.py          # Single source of truth (MODEL name, limits, points/impact maps)
│   ├── schemas.py         # Validation helpers (class enum, confidence, bbox, points)
│   ├── requirements.txt   # pip deps
│   └── .env.example       # env template
├── frontend/              # Separate branch / dev laptop
├── docs/
│   ├── API.md             # Full API contract for frontend
│   └── MASTER_PLAN.md
├── pyproject.toml         # uv project (Python 3.14)
├── requirements.txt       # Root mirror of backend deps (for uv pip)
└── README.md
```

## Quick Start (Backend)

### 1. Create environment (uv)

```bash
uv venv --python 3.14
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
```

> `.venv` is already created at repo root via `uv venv`. Activate it before manual `python` calls, or just use `uv run`.

### 2. Install dependencies

```bash
uv pip install -r backend/requirements.txt
# alternative (via pyproject):
uv sync --no-install-project
```

Core deps: `Flask`, `Flask-Cors`, `google-genai`, `python-dotenv`, `Pillow>=11.3.0` (11.1.0 has no cp314 Windows wheels).

### 3. Configure Gemini

```bash
cp backend/.env.example backend/.env
# edit backend/.env:
# GEMINI_API_KEY=your_gemini_api_key_here
# GEMINI_MODEL=gemini-2.0-flash
```

`.env` is gitignored. `GEMINI_MODEL` is the single config constant — change without code edits.

### 4. Run server

```bash
python backend/app.py
# or
uv run python backend/app.py
```

Server at `http://127.0.0.1:5000`

- `GET  /` → service info
- `GET  /api/health` → health + gemini status
- `POST /api/analyze` → multipart `image` field → JSON items (see `docs/API.md`)
- `GET  /api/stats` → demo aggregate stats

### Test

```bash
curl http://127.0.0.1:5000/api/health
curl -F "image=@test.jpg" http://127.0.0.1:5000/api/analyze
```

Expected `GEMINI_NOT_CONFIGURED` if `.env` missing — intentional graceful error.

---

## Tech — Locked (Round-1)

- Python 3.14, Flask, Flask-CORS, `google-genai`, `python-dotenv`, Pillow, stdlib only
- **No** Docker/Postgres/Mongo/Redis/Celery/microservices/auth/blockchain/custom CV model

## Git Branch

Work on `backend/gemini`:

```bash
git checkout backend/gemini
```

Conventional commits: `feat:`, `docs:`, `fix:` etc. Never commit `.env`.

## Frontend Contract

See `docs/API.md` for endpoints, request/response shapes, error codes, cURL examples, and bounding-box conversion (`ymin/xmin/ymax/xmax` 0-1000 → `%`).

The frontend on a separate laptop can integrate independently without waiting.

## Design Philosophy

Premium, environmental, intelligent, measurable — backend exposes `confidence`, `disposal`, `points`, `waste_diverted_kg`, `co2_saved_kg`, and optional `box_2d` for the visual AI detection experience (lime rectangles, badges, LIVE indicators).

## Future (deferred)

- `GET /api/collection/summary`, routing/truck optimization — simple mock heuristic after core pipeline stable
- Telemetry (`fill_percent`, `mass_kg`) via MQTT — keep extensible, don't build Round-1

---

## Troubleshooting

- **Pillow install fails on 3.14 Windows**: use `Pillow>=11.3.0` (we patched `pyproject.toml` + `requirements.txt`). `Pillow==11.1.0` has no cp314 wheels.
- **uv sync build error**: `uv sync --no-install-project` or ensure `[tool.hatch.build.targets.wheel] packages = ["backend"]` in `pyproject.toml`.
- **Imports fail**: `backend/app.py` supports both `python backend/app.py` and `uv run python backend/app.py` via dual `try: from config` / `except: from backend.config`.

---

For full prompt spec see `ECLOOP_BACKEND_PROMPT.md`.
