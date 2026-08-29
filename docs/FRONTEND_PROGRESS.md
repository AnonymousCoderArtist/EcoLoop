# EcoLoop Frontend — Progress & Handoff Doc

**Branch:** `frontend/round-1`  
**Last updated:** 2026-08-29  
**Frontend lead:** Vtx  
**Remote:** `origin/frontend/round-1` pushed  

---

## 1. What We Are Building

EcoLoop is an outcome-based waste-behaviour platform. The frontend prototype must make the core loop obvious:

```
SCAN WASTE → AI UNDERSTANDS IT → CORRECT DISPOSAL GUIDANCE → ECOPOINT REWARD → ENVIRONMENTAL IMPACT → USER IS MOTIVATED TO REPEAT
```

For **Round 1** we are not building every feature. We are building a polished, credible demo that feels like a premium climate-tech product, not a school project.

---

## 2. Current Progress

### Completed
- **Branch setup**
  - Created `frontend/round-1` from `main`
  - All frontend work is isolated to `frontend/` only
- **Project structure**
  - `frontend/index.html`
  - `frontend/style.css`
  - `frontend/script.js`
  - `frontend/background 1.png`
  - `frontend/background 2.png`
  - `frontend/foreground.png`
- **Landing / Hero**
  - Full-screen hero using local background assets
  - Base layer = `background 2.png`
  - Foreground transition = `foreground.png`
  - Reveal layer = `background 1.png`
  - Cursor-following spotlight reveals the base layer through a soft circular mask
  - GSAP entrance animations for title/subtitle/actions
  - Hero no longer clips scroll (`overflow: hidden` removed) so page can scroll to dashboard
- **Navigation**
  - Fixed top nav with logo + links
  - Consistent nav across landing, dashboard, scan, impact, community
- **Dashboard**
  - Hero metrics: waste diverted, correct sorts, CO₂ avoided, EcoPoints
  - Loop bars: Segregation Accuracy, Organic Recovery, Contamination Reduction
  - Telemetry panel: AI Vision, Objects Detected, Classification, Confidence
  - Neighborhood leaderboard
- **Scan experience**
  - Drag-and-drop + file upload
  - Camera capture modal with Cancel / Capture
  - Analyzing animation with sequential status lines
  - Multi-object result cards
  - Detection boxes rendered from `box_2d` with technical corner brackets
  - EcoPoints + CO₂ + waste reward panel
- **Impact page**
  - Impact metrics
  - Action loop visual: Action → Segregation → Recovery → Impact
- **Community page**
  - Community metrics
  - Leaderboard
- **API integration**
  - `API_BASE` constant in `script.js`
  - Sends `multipart/form-data` to backend
  - Normalizes both single-result and multi-item responses
  - Demo/fallback mode included
- **Animations**
  - GSAP loaded from CDN
  - ScrollTrigger loaded from CDN
  - Hero zoom, blur-rise, fade-up animations
- **Responsive**
  - Desktop-first with breakpoints for tablet/mobile
  - Nav adapts on smaller screens

### Not Yet Completed / Needs Polish
- Leaderboard SVG chart animation was started but later simplified; current leaderboard is clean but basic
- Camera viewport UX can be improved after core flow is stable
- Scan history page not started
- Real backend not yet connected end-to-end
- No auth/login gate yet
- Mobile hamburger menu not implemented
- Accessibility pass needed (focus states, ARIA, keyboard flow)

---

## 3. Key Design Decisions

- **Single HTML file SPA pattern** — no router, just show/hide `.page` sections
- **Cursor spotlight mechanic**
  - Base layer shows `background 2.png`
  - Foreground layer shows `foreground.png`
  - Reveal layer shows `background 1.png`
  - Canvas draws soft radial gradient at smoothed cursor position
  - `canvas.toDataURL()` is used as `mask-image` on reveal layer
  - Radius: `260px`, lerp factor: `0.1`
- **GSAP usage**
  - Targets `.hero-bg`, `.hero-line`, `.hero-subtitle`, `.hero-actions`
  - ScrollTrigger reserved for future leaderboard animation
- **Styling approach**
  - Swiss editorial + futuristic minimal
  - Dark background, ivory text, lime accent
  - Thin borders, monospace telemetry, lots of negative space
- **No build step**
  - Plain HTML/CSS/JS
  - GSAP via CDN
  - Fonts via Google Fonts

---

## 4. How to Run

```bash
cd frontend
python -m http.server 8080
# Open http://localhost:8080
```

---

## 5. API Contract

**Endpoint**
```
POST http://127.0.0.1:5000/api/analyze
```

**Request**
```
multipart/form-data
image=<file>
```

**Expected response**
```json
{
  "success": true,
  "result": {
    "item": "Plastic Bottle",
    "material": "PET Plastic",
    "class": "Recyclable",
    "confidence": 94,
    "disposal": "Dry/Recyclable Waste",
    "points": 10,
    "waste_diverted_kg": 0.02,
    "co2_saved_kg": 0.08,
    "explanation": "..."
  }
}
```

**Multi-object variant**
```json
{
  "success": true,
  "items": [...],
  "summary": {
    "total_items": 3,
    "classes_detected": ["Biogas", "Recyclable"],
    "dominant_class": "Biogas"
  }
}
```

**Box coordinates**
```json
"box_2d": [ymin, xmin, ymax, xmax]   // normalized 0-1000
```

Frontend converts to percentages:
```js
const top = ymin / 10;
const left = xmin / 10;
const width = (xmax - xmin) / 10;
const height = (ymax - ymin) / 10;
```

---

## 6. Demo Flow (Target)

1. Open landing page
2. See Lithos hero with spotlight reveal
3. Click nav or CTA to Dashboard
4. See metrics, loop bars, telemetry, leaderboard
5. Go to Scan
6. Upload image or open camera
7. See preview
8. Click Analyze Waste
9. See analyzing animation
10. See result cards + detection boxes + reward
11. Dashboard and Impact update with new values
12. Navigate to Impact and Community

---

## 7. Known Issues

| Issue | Status |
|-------|--------|
| GSAP `.hero-fade` selector error | Fixed |
| Camera modal visible on load | Fixed |
| No Cancel button in camera modal | Fixed |
| Hero background images reversed | Fixed |
| Hero scroll clipped by overflow | Fixed |
| Spotlight too heavy on low-end devices | Not started |
| Mobile hamburger menu missing | Not started |
| Scan history missing | Not started |
| Real backend not tested end-to-end | Not started |

---

## 8. Next Steps

### Priority 1 — Core Polish
- [ ] Test full demo flow end-to-end
- [ ] Polish scan result cards and detection boxes
- [ ] Ensure dashboard updates persist during session
- [ ] Add subtle grain texture to hero only

### Priority 2 — Navigation & UX
- [ ] Add mobile hamburger menu
- [ ] Improve camera capture UX
- [ ] Add loading/skeleton states
- [ ] Add error state UI for API failures

### Priority 3 — Expansion
- [ ] Scan history page
- [ ] Dynamic dashboard statistics
- [ ] Category filters
- [ ] Community map
- [ ] Achievements / streaks

---

## 9. Git Workflow

- Work only on `frontend/round-1`
- Do not modify backend implementation
- Commit logically:
  - `feat: create EcoLoop landing page`
  - `feat: add dashboard`
  - `feat: add waste scanning experience`
  - `feat: add AI result UI`
  - `feat: connect scan to backend API`

---

## 10. Files Reference

| File | Purpose |
|------|---------|
| `frontend/index.html` | Main SPA structure |
| `frontend/style.css` | All styles |
| `frontend/script.js` | All logic |
| `frontend/background 1.png` | Reveal hero image |
| `frontend/background 2.png` | Base hero image |
| `frontend/foreground.png` | Hero foreground transition |
| `docs/API.md` | Backend API docs |
| `docs/MASTER_PLAN.md` | Project master plan |
| `ECLOOP_FRONTEND_PROMPT.md` | Original frontend brief |

---

## 11. Quick Context for New Laptop

If you are switching to another laptop:
1. Pull branch `frontend/round-1`
2. Work only inside `frontend/`
3. Run `python -m http.server 8080` from `frontend/`
4. Open `http://localhost:8080`
5. If backend is not running, use **DEMO MODE** on the Scan page
6. GSAP and ScrollTrigger are loaded from CDN — internet required for animations

## 12. Latest Push Status

- Branch `frontend/round-1` has been pushed to remote
- Remote URL: `https://github.com/AnonymousCoderArtist/EcoLoop.git`
- PR link: `https://github.com/AnonymousCoderArtist/EcoLoop/pull/new/frontend/round-1`
- Latest commit includes:
  - Swapped hero base/reveal images
  - Removed `overflow: hidden` from hero to allow scrolling
  - Cleaned up Swiss editorial styles
  - Fixed GSAP selector targets
  - Fixed camera modal open/close behavior

---

*Document generated by Vtx. Update this file as frontend progresses.*
