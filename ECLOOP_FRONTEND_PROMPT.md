# EcoLoop — Frontend OpenCode Build Prompt

## ROLE

You are the **Frontend Lead** for the EcoLoop Round-1 prototype.

You are working on a separate laptop from the backend developer.

Build a visually exceptional but technically simple web prototype using:

- HTML
- CSS
- Vanilla JavaScript

Do NOT introduce React, Vue, Next.js, Tailwind, TypeScript, or a frontend framework.

The goal is to make judges immediately feel that EcoLoop is a polished, credible environmental technology product.

---

# 1. PROJECT IDEA

EcoLoop is an outcome-based waste behaviour platform.

The central loop is:

SCAN WASTE
→ AI UNDERSTANDS IT
→ CORRECT DISPOSAL GUIDANCE
→ ECOPOINT REWARD
→ ENVIRONMENTAL IMPACT
→ USER IS MOTIVATED TO REPEAT

The prototype must make that loop visually obvious.

The core demo flow:

LANDING
→ DASHBOARD
→ SCAN WASTE
→ UPLOAD/CAPTURE IMAGE
→ ANALYZING STATE
→ AI RESULT
→ ECOPOINT REWARD
→ IMPACT UPDATE

This is Round 1.

Do not build unnecessary product features until the core flow is polished.

---

# 2. VISUAL REFERENCE — IMPORTANT

The supplied EcoLoop reference image is the primary visual direction.

Study its overall feel:

- deep forest-black background
- real/natural botanical imagery
- subtle green atmospheric depth
- premium glass panels
- thin technical/HUD-style borders
- pale warm-white typography
- muted olive/grey secondary text
- electric yellow-green/lime used sparingly for data and active states
- restrained gradients
- large editorial typography
- lots of breathing room
- technical coordinate/grid details used subtly
- environmental imagery combined with futuristic data visualization

The reference feels like:

NATURE × INTELLIGENCE × DATA × PREMIUM PRODUCT

It should NOT feel like:
- a generic green NGO website
- a typical SaaS dashboard
- a crypto dashboard
- a gaming UI
- a template with excessive neon

---

# 3. VISUAL LANGUAGE

Use this hierarchy.

## Background

Use a near-black green:

#071009 / #08120B range

The exact values can be adjusted.

Use:
- subtle gradients
- very subtle grain/noise if achievable with CSS
- optional botanical/forest imagery with heavy dark overlay

The background must remain dark enough for text and panels.

---

## Primary text

Warm off-white / ivory.

Avoid pure white everywhere.

Use approximately:

#F2F0DF

---

## Secondary text

Muted green-grey:

#9DA89A

---

## Accent

Use a restrained acid-lime / chartreuse:

#D7FF3F

This accent should communicate:
- active
- success
- environmental progress
- data
- reward

Do NOT paint the entire UI lime.

---

# 4. TYPOGRAPHY

Use a premium modern sans-serif.

Preferred stack:

Inter,
Manrope,
Arial,
sans-serif

Headlines should be large, clean and editorial.

Avoid:
- cartoon fonts
- excessive rounded fonts
- overly futuristic sci-fi fonts

The design should look like a serious climate-tech product.

---

# 5. CORE LAYOUT

Desktop-first but responsive.

Create:

frontend/
├── index.html
├── style.css
└── script.js

Keep JavaScript organized into small functions.

No build step.

The prototype should run with a simple local server.

---

# 6. LANDING / HERO

Create a cinematic opening screen.

Large title:

EcoLoop

Supporting line:

Outcome-based behavior for a circular world.

Alternative copy is allowed if stronger.

Primary CTA:

SCAN YOUR WASTE

Secondary CTA:

VIEW IMPACT

Visual direction:

- full viewport
- dark botanical background
- subtle glass overlay
- thin technical lines
- tiny coordinate-style labels
- large typography
- small "LIVE ECO INTELLIGENCE" / "AI WASTE INTELLIGENCE" indicator

The hero should immediately communicate:

This is not just a recycling app.
It measures behaviour and outcomes.

---

# 7. DASHBOARD

Build a premium command-center dashboard inspired by the supplied reference image.

Header:

ECOLOOP
AI WASTE INTELLIGENCE

Navigation:

Overview
Scan
Impact
Community

Right side:

EcoPoints
Profile/avatar placeholder

---

# 8. DASHBOARD HERO

Show:

YOUR ECO IMPACT

Large metrics:

12.4 KG
WASTE DIVERTED

47
CORRECT SORTS

8.7 KG
CO₂ IMPACT AVOIDED

2,480
ECOPOINTS

Use large typography.

Each metric should have:
- tiny label
- subtle trend indicator
- minimal technical decoration

Do not make every card look identical.

---

# 9. DATA VISUALIZATION

The reference image has a strong data-dashboard quality.

Create a section:

THE LOOP IN NUMBERS

Use a clean horizontal/stacked visualization showing:

Segregation Accuracy
35%

Organic Recovery
25%

Contamination Reduction
20%

Overflow Prevention
10%

Participation
10%

These are prototype/demo values.

Make them visually elegant:
- horizontal bars
- thin borders
- lime fill
- dark translucent cards

Animate bars when the dashboard loads.

---

# 10. COMMUNITY / LEADERBOARD

Create a panel inspired directly by the reference phone/leaderboard.

Title:

NEIGHBORHOOD LEADERBOARD

Example:

01  Greenridge Terrace     2450 pts
02  Maple Grove             2100 pts
03  Cedar Valley            1950 pts
04  Oakwood Park            1800 pts
05  Haw Rahar               1850 pts

Use subtle trend lines/arrows.

The leaderboard should feel like a real community outcome system.

---

# 11. SCAN EXPERIENCE — MOST IMPORTANT

The scan screen is the primary demo interaction.

Create:

SCAN YOUR WASTE

Large glass upload area.

States:

1. Idle
2. Image selected
3. Analyzing
4. Result
5. Error

Idle state:

DROP WASTE IMAGE
or
OPEN CAMERA

Buttons:

UPLOAD IMAGE
USE CAMERA

If camera implementation becomes unreliable, prioritize image upload.

---

# 12. ANALYZING ANIMATION

When the user submits an image, do NOT immediately jump to the result.

Create a 1–2 second premium analysis animation.

Display:

ANALYZING WASTE

Then sequentially:

● Detecting object
● Identifying material
● Determining waste stream
● Calculating impact

Use subtle scan-line / glow / progress animation.

Do not make it cheesy.

---

# 13. AI RESULT SCREEN

This is the WOW moment.

Example:

PLASTIC BOTTLE

94% CONFIDENCE

RECYCLABLE

Material
PET Plastic

Correct disposal
DRY / RECYCLABLE WASTE

Then:

+10 ECOPOINTS

0.08 KG
estimated CO₂ impact avoided

0.02 KG
waste diverted

Add a short explanation:

"This appears to be a PET plastic bottle. Place it in the dry/recyclable stream after emptying and rinsing it."

Use:
- large item title
- lime category indicator
- elegant metric cards
- image preview
- subtle animated reveal

---

# 14. REWARD ANIMATION

After the result appears:

+10 ECOPOINTS

Animate the number.

Then show:

LOOP COMPLETE

SCAN
→ SORT
→ RECOVER
→ IMPACT

This is an important product moment.

---

# 15. IMPACT PAGE

Create a dedicated impact view.

Title:

YOUR IMPACT

Show:

47
Items correctly sorted

12.4 kg
Waste diverted

8.7 kg
CO₂ impact avoided

2,480
EcoPoints

Then show a visual timeline or circular loop:

YOUR ACTION
↓
CORRECT SEGREGATION
↓
RECOVERY
↓
MEASURABLE IMPACT

The UI should make the "outcome-based behavior" idea obvious.

---

# 16. COMMUNITY PAGE

Show:

COMMUNITY IMPACT

Example:

1,248 kg
Waste diverted

824 kg
Organic recovered

412 kg
Recyclables recovered

86%
Segregation accuracy

Then leaderboard.

Use demo data initially.

---

# 17. API INTEGRATION

The backend exposes:

POST /api/analyze

Request:

multipart/form-data
image=<file>

Expected response:

{
  "success": true,
  "result": {
    "item": "Plastic Bottle",
    "material": "PET Plastic",
    "category": "Recyclable",
    "confidence": 94,
    "disposal": "Dry/Recyclable Waste",
    "points": 10,
    "waste_diverted_kg": 0.02,
    "co2_saved_kg": 0.08,
    "explanation": "..."
  }
}

Implement the frontend so the scan page sends the selected image to:

http://127.0.0.1:5000/api/analyze

Make the API base URL a single JavaScript constant so it can be changed easily.

---

# 18. DEVELOPMENT WITHOUT BACKEND

Do NOT wait for the backend.

Create a development fallback.

If the API cannot be reached, allow a demo/mock mode that produces realistic sample results.

Example:

Plastic bottle:
- Recyclable
- PET Plastic
- 94%
- +10 points

Banana peel:
- Organic
- 96%
- +15 points

Aluminium can:
- Recyclable
- 97%
- +10 points

The UI should make it easy to switch between:

REAL API
and
DEMO MODE

Do not display "fake AI" to the user as if it were real. This is only a development fallback.

When the real backend works, use it automatically.

---

# 19. RESPONSIVE DESIGN

Desktop is the primary presentation environment.

Also make it usable at:
- 1440px
- 1280px
- 1024px
- mobile width

On smaller screens:
- stack cards
- preserve hierarchy
- keep buttons usable
- avoid horizontal overflow

---

# 20. MICRO-INTERACTIONS

Use subtle motion.

Allowed:

- fade-in
- slide-up
- bar growth
- number counting
- hover border glow
- image reveal
- scanning line
- progress indicator
- button hover
- page transitions

Avoid:

- excessive particles
- spinning everything
- huge 3D effects
- distracting animations
- excessive glass blur

Motion should communicate state, not decoration.

---

# 21. REFERENCE IMAGE DETAILS TO PRESERVE

The supplied reference has:

- large editorial title
- botanical background
- translucent rectangular panels
- thin technical borders
- subtle coordinate markers
- lime data visualization
- leaderboard
- analytical metrics
- dark environmental atmosphere

Translate these ideas into the website.

Do NOT copy the exact layout.

Build a more usable web product inspired by the same visual language.

---

# 22. CONTENT STYLE

Use confident, concise language.

Examples:

"SCAN. SORT. RECOVER."

"Turn everyday disposal into measurable impact."

"Your waste has an outcome."

"Every correct sort closes the loop."

"AI-powered waste intelligence."

Avoid corporate filler such as:

"Revolutionizing the future of sustainability through innovative solutions."

---

# 23. ACCESSIBILITY

Ensure:

- readable contrast
- visible focus states
- buttons have labels
- images have alt text
- keyboard navigation works
- upload controls are accessible

---

# 24. PERFORMANCE

Do not load huge background assets.

If using an image:
- optimize it
- use an overlay
- keep the UI responsive

Avoid unnecessary external libraries.

Use CSS and vanilla JS wherever possible.

---

# 25. GIT RULES

Work only on:

frontend/prototype

Do not modify backend implementation.

Commit logically:

- `feat: create EcoLoop landing page`
- `feat: add dashboard`
- `feat: add waste scanning experience`
- `feat: add AI result UI`
- `feat: connect scan to backend API`

Do not rewrite backend files.

---

# 26. DEMO FLOW MUST WORK

Before declaring complete, manually test:

1. Open landing page.
2. Click Scan.
3. Select image.
4. Show preview.
5. Click Analyze.
6. Show analyzing animation.
7. Receive API result OR demo fallback.
8. Show classification.
9. Show EcoPoints.
10. Show environmental impact.
11. Navigate to Impact.
12. Return to Dashboard.
13. Confirm the dashboard reflects the scan where practical.

The complete demo should take roughly 60–90 seconds.

---

# 27. EXPANSION PLAN

Only after the core flow is polished and working, consider:

Priority 1:
- camera capture
- scan history
- dynamic dashboard statistics
- category filters

Priority 2:
- community map
- richer leaderboard
- achievements
- streaks

Priority 3:
- collection scheduling
- nearby recycling points
- advanced analytics

Do not build these until the core experience is stable.

---

# 28. FINAL QUALITY BAR

The final UI should make a judge think:

"How did they build this so quickly?"

It should feel like a polished climate-tech product, not a school project.

The most important visual principle is:

## NATURE × DATA × INTELLIGENCE

Use the supplied reference image as the emotional and visual direction.

---

# FINAL INSTRUCTION

Do not merely describe the implementation.

Actually create/edit the frontend files.

Start by inspecting the existing repository and existing API documentation.

Implement the complete Round-1 frontend.

If the backend is not ready, use the documented API contract plus a development fallback.

Run the site locally and test the full user journey.

Fix visual and functional issues before stopping.

At the end, report:
- files created/changed
- how to run the frontend
- API integration status
- demo flow tested
- remaining issues
- optional expansion ideas only if the core is complete
