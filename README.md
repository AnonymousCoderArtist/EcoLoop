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

## Quick Start (Backend) — uv

> **Use `uv` for everything** — `uv venv` + `uv sync`/`uv pip` + `uv run`. Do not use plain `pip`/`venv`.

### 1. Create environment

```bash
uv venv --python 3.14   # creates .venv at repo root (Python 3.14.7)
# Only if you need an interactive shell:
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
# Preferred: just prefix every command with `uv run`
```

`.venv` is already created at repo root via `uv venv`.

### 2. Install dependencies

```bash
# Recommended — from pyproject.toml + uv.lock
uv sync --no-install-project

# Or via pip requirements mirror
uv pip install -r backend/requirements.txt
# (Root requirements.txt mirrors backend/requirements.txt)
```

Core deps: `Flask==3.1.0`, `Flask-Cors==5.0.0`, `google-genai==1.21.0`, `python-dotenv==1.0.1`, `Pillow>=11.3.0` (11.1.0 has no cp314 Windows wheels — patched).

### 3. Configure Gemini

```bash
cp backend/.env.example backend/.env
# edit backend/.env:
# GEMINI_API_KEY=your_gemini_api_key_here   # never commit — .gitignore covers .env/*.env
# GEMINI_MODEL=gemini-2.5-flash             # single source of truth in backend/config.py:7
```

`.env` is gitignored. `GEMINI_MODEL` is the single config constant — change without code edits.

### 4. Run server

```bash
uv run python backend/app.py   # preferred — uses .venv + loads backend/.env
# alt: uv run python -m backend.app
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

# Without curl:
uv run python -c "from backend.app import create_app; app=create_app(); c=app.test_client(); print(c.get('/api/health').json)"
```

Expected `GEMINI_NOT_CONFIGURED` if `.env` missing — intentional graceful error. With a valid `GEMINI_API_KEY` in `backend/.env:1`, `/api/analyze` calls Gemini and returns `items[]`.

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

## Frontend Contract (Updated — Stream-Area Zones)

See `docs/API.md` for **frontend quick-connect** ( `uv run` + `curl` + JS `fetch` copy/paste), zone-based `items[]` (2-6 areas, Biogas max priority), Swiss box rendering (`box_2d` → `%`), error codes, and summary dashboard.

The frontend on a separate laptop can integrate independently without waiting — **CORS `*`, no auth**, `POST /api/analyze` with `FormData image` returns `items[]` zones ready to render. Visual reference: `uv run python backend/visualize.py` → `backend/image_annotated.png`.

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
