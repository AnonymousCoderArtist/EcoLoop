# EcoLoop — Outcome-Based Waste Behaviour Platform

Round-1 prototype: **Upload waste image → Gemini Vision → Multi-class classification → Disposal route → EcoPoints → Impact → Beautiful frontend**.

---

## Project Structure

```
.
├── backend/               # Flask + Gemini Vision API
│   ├── app.py             # Flask factory, /api/health, /api/analyze, /api/stats + /api/demo/* (loader + points)
│   ├── gemini.py          # Gemini prompt — stream-area 2-6 zones, Biogas max priority
│   ├── config.py          # Single source GEMINI_MODEL=gemini-2.5-flash, loads backend/.env
│   ├── schemas.py         # sanitize_item, box validation, points/impact maps
│   ├── visualize.py       # Swiss editorial overlay — light wash + 11px corners, saves backend/image_annotated.png
│   ├── image.png          # demo input (gitignored, 1280x698)
│   ├── image_annotated.png # Swiss zones output (gitignored, 1280x770)
│   ├── last_result.json   # cached demo JSON (gitignored)
│   ├── requirements.txt   # Flask 3.1, Flask-Cors, google-genai, dotenv, Pillow>=11.3
│   └── .env.example       # GEMINI_API_KEY template
├── frontend/              # Landing + Dashboard + Scan + Impact + Community (SPA, no build)
│   ├── index.html         # 8-section landing: hero (end-result without fear) → proof → problem → solution 8 bento (no text over images, 16/9 contain) → how it works 4 → FAQ → CTA → footer
│   ├── style.css          # Swiss editorial + futuristic — lime #ccff00, dark #080808, 1px borders, glass blur, hero glass for readability
│   ├── script.js          # SPA nav, scan + demo (loadDemoImageAndAnalyze), box_2d → %, stats refresh, GSAP hero
│   ├── IMAGE_PROMPTS.md   # Detailed prompts (same 5600K + lime rim, 85mm, 8k) — F8 real, S2/S4 skip, 7 real images already in repo
│   ├── hero-bg.png, landfill.png, biogas.png, imagescan.png, metrics-strip.png, communiity.png, foreground-bg.png + background 1/2.png
│   └── ...
├── docs/
│   ├── API.md             # Frontend-ready contract — quick connect, zones, demo loader, Swiss render, errors, uv
│   └── FRONTEND_PROGRESS.md
├── ECLOOP_BACKEND_PROMPT_SIMPLE.md # 10-step agent guide
├── pyproject.toml         # uv project (Python 3.14, hatch packages=["backend"])
├── requirements.txt       # root mirror
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
- `POST /api/analyze` → multipart `image` → zones `items[]` + `summary` + `box_2d` (Swiss, Biogas max)
- `GET  /api/stats` → demo aggregate stats
- `GET  /api/demo` → demo options (Swiss annotated vs live)
- `GET  /api/demo/image` → final `image_annotated.png` (Swiss light wash + 11px corners)
- `POST /api/demo/analyze` → 1.2s loader → 4 zones 45 pts + adds to stats
- `GET  /api/demo/result` → cached JSON instant

### Test (backend + visual proof)

```bash
curl http://127.0.0.1:5000/api/health
curl -F "image=@backend/image.png" http://127.0.0.1:5000/api/analyze
curl http://127.0.0.1:5000/api/demo --output demo.json
curl http://127.0.0.1:5000/api/demo/image --output demo.png

# Without curl:
uv run python -c "from backend.app import create_app; app=create_app(); c=app.test_client(); print(c.get('/api/health').json)"

# Visual proof — 4 Swiss zones 45 pts:
uv run python backend/visualize.py              # live Gemini -> backend/image_annotated.png
uv run python backend/visualize.py --cached     # re-render from backend/last_result.json
```

Expected `GEMINI_NOT_CONFIGURED` if `.env` missing — intentional. With valid `GEMINI_API_KEY` at `backend/.env:1`, `/api/analyze` returns `items[]` zones.

### 5. Run frontend (integrated)

```bash
cd frontend && python -m http.server 8080  # http://localhost:8080
# Home now scrollable: hero (clean without fear, glass backdrop) → proof → problem (landfill.png, no heavy tint) → solution 8 bento (images 16/9 contain, no text over) → how it works 4 → FAQ → CTA → footer
# Scan page: Demo Quick Start → Try Demo — Swiss Zones (loads /api/demo/image, 1.2s loader → annotated + 45 pts) vs Upload/Camera → POST /api/analyze
```

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
