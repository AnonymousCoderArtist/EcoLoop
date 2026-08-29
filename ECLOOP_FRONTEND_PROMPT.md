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


---

# 29. VISUAL ENHANCEMENT — REAL-TIME DATA INGESTION

The supplied second EcoLoop reference image is now an additional visual direction.

Use the idea of:

## REAL-TIME DATA INGESTION

Do NOT literally copy the slide.

Translate the visual language into the web application.

The visual concept combines:

NATURAL ENVIRONMENT
+
TECHNICAL TELEMETRY
+
AI COMPUTER VISION
+
LIVE WASTE CLASSIFICATION

This should make EcoLoop feel like an actual intelligent infrastructure platform rather than only a recycling website.

---

# 30. AI VISION HIGHLIGHT OVERLAY — IMPORTANT

When the backend returns `box_2d` coordinates, draw bounding boxes over the uploaded image.

For example:

Image contains:

- vegetable scraps
- battery
- plastic bottle

The image should show subtle technical bounding boxes:

┌────────────────────────────┐
│ Vegetable scraps → BIOGAS  │
│ 94% CONFIDENCE             │
└────────────────────────────┘

and:

┌────────────────────┐
│ Battery            │
│ SPECIAL HANDLING   │
└────────────────────┘

Use the reference image as inspiration.

The highlight style should be:

- thin lime/olive technical corners
- small label
- confidence percentage
- class
- restrained glow
- dark translucent label background
- tiny technical metadata

Do NOT use giant colored rectangles over the image.

The actual waste image must remain visible.

---

# 31. MULTI-OBJECT RESULT

If the backend returns:

items: [
  Recyclable,
  Biogas,
  Non-Recyclable
]

the UI must show all detected objects.

Example top-level result:

3 OBJECTS DETECTED

Then show:

[ BIOGAS ]
Vegetable scraps
94%

[ RECYCLABLE ]
Plastic bottle
91%

[ NON-RECYCLABLE ]
Wrapper
88%

The most important class should receive stronger visual emphasis.

If `Biogas` is detected, make it the primary outcome panel:

BIOGAS PATHWAY

Organic waste detected
→ Recovery
→ Biogas
→ Energy

This is one of EcoLoop's strongest differentiators.

---

# 32. "REAL-TIME DATA INGESTION" DASHBOARD PANEL

Add a premium technical panel somewhere in the dashboard.

Title:

REAL-TIME DATA INGESTION

Inside, show:

AI VISION
● ACTIVE

OBJECTS DETECTED
03

CLASSIFICATION
LIVE

CONFIDENCE
94%

DATA STREAM
OPERATIONAL

Use subtle telemetry-like labels.

This is a visual simulation of the platform's intelligence layer.

Do not falsely claim that actual sensors are connected unless they really are.

Use wording such as:

AI STREAM
LIVE

rather than:

ESP32 CONNECTED

unless hardware actually exists.

---

# 33. OPTIONAL FUTURE SENSOR PANEL

If there is enough space, add a small "EDGE TELEMETRY" panel as a future/infrastructure visualization.

Example:

EDGE TELEMETRY

FILL LEVEL       72%
MASS             5.4 KG
STATUS           NOMINAL
STREAM           BIOGAS

Mark it clearly as:

SIMULATED TELEMETRY

or:

DEMO STREAM

Do not imply physical sensor data is real.

This panel should be secondary to the AI scan experience.

---

# 34. TECHNICAL HUD DETAILS

Borrow the reference's subtle technical details:

Examples:

AI/VISION: 94.2
STREAM: ECO-01
LATENCY: 1.42s
CLASSIFIER: ACTIVE
DATA: INGESTING
NODE: LOCAL

Use tiny uppercase monospace text.

Place these around panels sparingly.

Do not fill the screen with random numbers.

Every technical label should reinforce the feeling of an intelligent system.

---

# 35. IMAGE ANALYSIS SCREEN — MAKE THIS THE WOW MOMENT

When analysis begins:

Large image in the center.

Around it:

AI VISION / LIVE
CLASSIFIER ACTIVE
INGESTING IMAGE

Then animate:

1. Image appears
2. subtle scan line moves across it
3. object boxes appear
4. labels resolve one by one
5. confidence values appear
6. classification cards slide in
7. final impact calculation appears

Example:

ANALYZING...

01 / OBJECT DETECTED
02 / MATERIAL IDENTIFIED
03 / WASTE STREAM RESOLVED
04 / IMPACT CALCULATED

This should feel like an intelligent computer-vision system.

Keep animation around 1–2 seconds so the demo remains fast.

---

# 36. SENSOR / HARDWARE STORY — FUTURE EXPANSION ONLY

The supplied reference shows an ESP32 + ultrasonic sensor + load cell + MQTT concept.

We may eventually expand EcoLoop into:

SMART BIN
→ FILL LEVEL
→ MASS
→ AI WASTE CLASSIFICATION
→ LIVE DATA INGESTION
→ COLLECTION DEMAND
→ ROUTE OPTIMIZATION

For Round 1:

DO NOT implement the hardware stack.

Instead, make the UI architecture capable of showing it later.

If time permits after the AI scan + dashboard + integration are perfect, we can create a small simulated telemetry demo.

---

# 37. VISUAL PRIORITY ORDER

When deciding what to spend time on:

1. AI image scanning
2. Multi-object highlight boxes
3. Biogas classification
4. Beautiful result screen
5. Dashboard metrics
6. Real-time ingestion visual
7. Impact visualization
8. Community/leaderboard
9. Simulated telemetry
10. Future routing/truck UI

Never sacrifice 1–5 for 9–10.

---

# 38. IMPORTANT — DO NOT OVERDO THE EFFECT

The new technical look is an accent, NOT the entire design.

Keep the original EcoLoop identity:

NATURE × DATA × INTELLIGENCE

Use:

- botanical imagery
- dark green atmosphere
- glass panels
- thin borders
- lime highlights
- technical labels

But maintain large empty spaces and strong typography.

The result should feel closer to a premium climate-tech command center than a cyberpunk dashboard.

---

# 39. BACKEND CONTRACT FOR HIGHLIGHTS

When available, the frontend expects:

{
  "success": true,
  "items": [
    {
      "item": "Vegetable scraps",
      "material": "Organic matter",
      "class": "Biogas",
      "confidence": 94,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "...",
      "box_2d": [210, 120, 680, 610]
    }
  ],
  "summary": {
    "total_items": 1,
    "classes_detected": ["Biogas"],
    "dominant_class": "Biogas"
  }
}

If `box_2d` is missing, gracefully render the result without an overlay.

Never let a missing bounding box break the scan flow.


---

# 29. VISUAL AI DETECTION OVERLAY — IMPORTANT

The newly supplied EcoLoop reference image adds an important visual direction.

Do not make the uploaded image a plain rectangular preview.

The image-analysis experience should feel like a **real-time AI waste-classification camera system**.

Reference characteristics to borrow:

- thin lime/olive detection rectangles
- four-corner technical brackets rather than heavy borders
- small floating labels attached to detected objects
- confidence percentages
- tiny `REC` / `LIVE` indicator
- tiny system telemetry labels
- subtle scanning line
- dark translucent image frame
- lime highlight for active detection
- small technical typography
- restrained HUD/data visualization

The effect should feel like:

**AI COMPUTER VISION × ENVIRONMENTAL SENSOR × PREMIUM CLIMATE-TECH**

NOT:

- gaming HUD
- sci-fi movie UI
- excessive neon
- cyberpunk
- cartoon AR filters

---

# 30. IMAGE DETECTION VIEW

When the user uploads an image, place it inside:

`.detection-stage`

Structure conceptually:

```text
┌──────────────────────────────────────────┐
│ AI WASTE CLASSIFIER                  REC │
│                                          │
│      ┌───────────────┐                   │
│      │ vegetable     │                   │
│      │ scraps        │                   │
│      └───────────────┘                   │
│      BIOGAS · 94%                        │
│                                          │
│                    ┌────────┐            │
│                    │ battery│            │
│                    └────────┘            │
│                    E-WASTE · 91%         │
│                                          │
│  AI ACTIVE                    1.45s      │
└──────────────────────────────────────────┘
```

The actual uploaded image should remain visible underneath.

---

# 31. GEMINI BOUNDING BOX RENDERING

The backend returns Gemini's documented normalized coordinates:

```text
box_2d = [ymin, xmin, ymax, xmax]
```

where values are normalized from `0–1000`. citeturn0search0turn0search2

Convert them into CSS percentages:

```javascript
const [ymin, xmin, ymax, xmax] = item.box_2d;

const top = ymin / 10;
const left = xmin / 10;
const width = (xmax - xmin) / 10;
const height = (ymax - ymin) / 10;
```

Then create an absolutely positioned detection box:

```text
position: absolute
top: `${top}%`
left: `${left}%`
width: `${width}%`
height: `${height}%`
```

IMPORTANT:
The image and detection overlay must use the same containing element and the same rendered aspect ratio.

Do NOT use arbitrary pixel coordinates.

Use percentage coordinates so the boxes remain aligned when the image is resized.

---

# 32. DETECTION BOX DESIGN

Do not use a normal thick rectangular border.

Build a technical corner-bracket effect using CSS pseudo-elements or nested elements.

Example visual hierarchy:

```text
       ┌───────────────┐
       │               │
       │   WASTE ITEM  │
       │               │
       └───────────────┘
```

But only the corners should be strongly visible.

Use:
- 1–2px lime lines
- short corner segments
- subtle glow
- transparent center
- small label badge

The box should animate in when detection finishes.

---

# 33. CLASS-SPECIFIC HIGHLIGHTING

Keep the palette restrained.

Suggested mapping:

`Biogas`
→ lime/green highlight

`Recyclable`
→ yellow-lime highlight

`Non-Recyclable`
→ muted warm/grey highlight

`E-Waste/Hazardous`
→ controlled amber/red accent

`Others`
→ muted grey

Do NOT turn the entire screen into multiple colors.

The primary EcoLoop visual identity should remain dark + ivory + lime.

---

# 34. FLOATING DETECTION LABEL

Each detected item should have a compact label:

```text
Vegetable scraps
BIOGAS · 94%
```

or:

```text
Plastic bottle
RECYCLABLE · 96%
```

Position the label near the top of the corresponding box.

If the box is too close to the top edge, automatically place the label inside/below the box so it stays visible.

If multiple labels overlap:
- intelligently offset them
- or place a compact list on the right
- never allow labels to become unreadable

---

# 35. SCANNING ANIMATION

Before results appear:

1. Display uploaded image.
2. Add subtle moving horizontal scan line.
3. Show:

`AI WASTE CLASSIFIER`

4. Show small telemetry:

`OBJECT DETECTION ACTIVE`

`MATERIAL ANALYSIS`

`STREAM CLASSIFICATION`

5. Reveal detection boxes one-by-one.
6. Reveal labels.
7. Reveal confidence.
8. Show final classification summary.

Keep total animation around 1–2 seconds.

It should feel fast and intelligent, not like the user is waiting for a fake loading screen.

---

# 36. DETECTION SUMMARY

After the boxes appear, show a compact panel:

```text
DETECTION SUMMARY

03 OBJECTS DETECTED

01  BIOGAS
01  RECYCLABLE
01  E-WASTE
```

Then:

```text
PRIMARY RECOVERY PATH
BIOGAS
```

This makes the multi-class capability immediately visible to judges.

---

# 37. REFERENCE IMAGE STYLE DETAILS

The new reference should influence the frontend in these specific ways:

### Large typography
Keep the strong oversized page titles.

### Technical coordinates
Add tiny labels such as:

`H/W_FLW: 39.52 · -87.85`

`S/N_FLW: 48.12 · -85.15`

These are decorative telemetry only. Do not pretend they are real GPS/sensor values.

Better alternatives:

`AI_SCAN: 01.42s`

`VISION_STATUS: ACTIVE`

`OBJECTS: 03`

### System labels

Use tiny uppercase text:

`ECOLOOP VISION`

`AI WASTE CLASSIFIER`

`SYSTEM STATUS: OPERATIONAL`

### Image panels

Use large rounded-but-not-overly-rounded glass panels with thin borders.

### Bottom technical status

Use small telemetry such as:

`MODEL: GEMINI VISION`

`LATENCY: 1.45s`

`DATA FLOW: LIVE`

Only show real latency if we measure it. Otherwise use clearly demo-oriented UI text.

---

# 38. DO NOT OVERDESIGN

The reference looks sophisticated because it has restraint.

Therefore:

- large typography
- few strong panels
- lots of negative space
- subtle borders
- limited accent color
- controlled animation

Do not add:
- dozens of cards
- huge neon glows
- random floating particles
- excessive gradients
- unnecessary 3D elements
- noisy dashboards

---

# 39. CAMERA-STYLE MODE

If time permits after the upload flow works, make the scan panel look like a camera viewport.

Possible top status:

`● REC`

Possible bottom controls:

`CAPTURE`

`ANALYZE`

But image upload remains the reliable Round-1 fallback.

---

# 40. MULTI-OBJECT RESULT UI

The frontend must NOT assume there is only one item.

Loop through:

```javascript
result.items
```

For every item:
- render a bounding box if `box_2d` exists
- render a detection label
- render class
- render confidence
- render result card

The dashboard should summarize all detected classes.

Example:

```text
3 OBJECTS DETECTED

BIOGAS          01
RECYCLABLE      01
E-WASTE         01
```

This is a key feature and should be visible in the demo.

---

# 41. FUTURE ROUTING VISUALIZATION

Do not implement the actual routing engine yet.

However, structure the frontend so a future page can display:

```text
COLLECTION INTELLIGENCE

ZONE A
────────────────────────

BIOGAS
420 kg

COLLECTION POINTS
12

TRUCKS REQUIRED
2

PRIORITY
HIGH

[ OPTIMIZE ROUTE ]
```

This can later become the bridge from:

AI CLASSIFICATION
→ WASTE AGGREGATION
→ TRUCK PLANNING
→ ROUTE OPTIMIZATION

Only build this if the Round-1 core is complete.

---

# 42. DEMO WOW MOMENT

The ideal judge-facing sequence is:

1. Upload an image containing multiple types of waste.
2. Image appears in the dark camera-style frame.
3. `AI WASTE CLASSIFIER` appears.
4. Scan line moves across the image.
5. 2–4 detection boxes appear.
6. Each object gets a small label.
7. One of them prominently shows:

`BIOGAS · 94%`

8. Summary appears:

`03 OBJECTS DETECTED`

9. EcoPoints animate upward.
10. Impact numbers update.
11. Dashboard shows the measurable outcome.

This should be the centerpiece of the prototype.

---

# 43. TECHNICAL IMPLEMENTATION RULE

Do not create a separate computer-vision model merely to draw boxes.

Gemini already provides documented normalized bounding boxes for object detection. citeturn0search0turn0search11

Use Gemini's coordinates.

If bounding boxes are unavailable for a particular model/API configuration:
- do not fake them
- fall back to classification cards
- keep the architecture ready for `box_2d`
- test with the configured Gemini model before adding fallback complexity

The bounding box feature is a visual enhancement, not a reason to destabilize the core scan flow.
