# EcoLoop — Backend OpenCode Build Prompt

## ROLE

You are the **Backend Lead** for the EcoLoop Round-1 prototype.

You are working on a separate laptop from the frontend developer. Your implementation must be clean, reliable, simple to run, and easy for the frontend to integrate.

The human developer is the project owner. Do not invent new architecture unless necessary.

---

# 1. PROJECT GOAL

Build the working backend for **EcoLoop**, an outcome-based waste behaviour platform.

The Round-1 demonstration must prove this core loop:

USER
→ uploads / captures a waste image
→ Gemini Vision analyzes it
→ EcoLoop identifies the waste/material/category
→ EcoLoop recommends the correct disposal route
→ EcoLoop calculates demo EcoPoints
→ EcoLoop estimates environmental impact
→ frontend displays the result beautifully

This is a prototype, NOT a production system.

Prioritize:
1. Reliability
2. Fast demo performance
3. Simple architecture
4. Clean API contract
5. Easy frontend integration
6. Extensibility if time remains

Do NOT over-engineer.

---

# 2. TECHNOLOGY — LOCKED

Use:

- Python 3.14
- Flask
- Flask-CORS
- `google-genai`
- python-dotenv
- Pillow
- standard Python libraries where possible

Do NOT introduce:

- React
- Node backend
- Docker
- PostgreSQL
- MongoDB
- Redis
- Celery
- microservices
- authentication systems
- blockchain
- unnecessary ML frameworks

For Round 1, Gemini is the vision intelligence layer.

Gemini is intentionally being used instead of training a custom computer-vision model. Gemini supports native multimodal image understanding/classification.

---

# 3. REQUIRED PROJECT STRUCTURE

Keep backend limited to:

backend/
├── app.py
├── gemini.py
├── requirements.txt
└── .env.example

The repository may also contain:

frontend/
docs/
README.md

Do not modify frontend files.

Do not restructure the repository without a strong reason.

---

# 4. ENVIRONMENT

The API key must NEVER be hardcoded.

Use:

GEMINI_API_KEY=...

from `.env`.

`.env` must be ignored by Git.

Create `.env.example`:

GEMINI_API_KEY=your_gemini_api_key_here

The application should fail gracefully with a useful error if the API key is missing.

---

# 5. GEMINI MODEL

Use a current Gemini Flash model that supports image understanding and is available to the configured API account.

Keep the model name in one obvious configuration constant/environment variable so it can be changed without rewriting the application.

Do not hardcode the model name in multiple files.

---

# 6. GEMINI ANALYSIS CONTRACT

The Gemini prompt must make the model behave like **EcoLoop Waste Intelligence**.

Analyze ALL clearly visible waste items in the image, not just one item.

EcoLoop is intentionally a MULTI-CLASS waste intelligence system. One uploaded image may contain one item or several different waste items.

For example, an image could contain:
- plastic bottle → Recyclable
- banana peel → Biogas
- dirty multilayer wrapper → Non-Recyclable
- broken electronic device → E-Waste/Hazardous
- unclear miscellaneous object → Others

Return a structured JSON response containing an `items` array.

Primary EcoLoop classes for Round 1:

1. `Recyclable`
   Examples: PET bottles, clean paper/cardboard, metal cans, glass bottles, clean recyclable packaging.

2. `Biogas`
   This is the MOST IMPORTANT class.
   Use this for biodegradable/wet organic waste that is suitable for an organic-waste/biogas pathway.
   Examples: food scraps, vegetable/fruit waste, kitchen waste, many biodegradable food residues.
   The system should clearly surface this class in the UI because it is a key differentiator of EcoLoop.

3. `Non-Recyclable`
   Examples: heavily contaminated packaging, certain multilayer wrappers, contaminated mixed waste, items that cannot reasonably enter the recyclable/organic stream.

4. `Others`
   Use when an item does not confidently fit the supported operational streams.

5. `E-Waste/Hazardous`
   Use this optional fifth class for electronics, batteries, bulbs, chemicals, medical/domestic hazardous items, etc. This class should be treated as a special handling stream rather than normal recyclable waste.

If an image contains multiple items, return one entry per clearly identifiable item.

Example:

{
  "success": true,
  "items": [
    {
      "item": "Plastic bottle",
      "material": "PET plastic",
      "class": "Recyclable",
      "confidence": 94,
      "disposal": "Recyclable / Dry Waste",
      "points": 10
    },
    {
      "item": "Vegetable scraps",
      "material": "Biodegradable organic matter",
      "class": "Biogas",
      "confidence": 96,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15
    }
  ],
  "summary": {
    "total_items": 2,
    "classes_detected": ["Recyclable", "Biogas"],
    "dominant_class": "Biogas"
  }
}

IMPORTANT BIOGAS RULE:
Do not classify something as Biogas merely because it is biodegradable in a broad sense. The class means the item is reasonably suitable for the EcoLoop organic/biogas pathway. If uncertain, use Others or explain the uncertainty.

For each item return:
- item
- material
- class
- confidence (0-100)
- disposal
- points
- waste_diverted_kg
- co2_saved_kg
- short explanation

If bounding boxes are practical with the selected Gemini capability, optionally return:
- box_2d: [ymin, xmin, ymax, xmax], normalized 0-1000

This can later allow the frontend to draw labels around individual waste objects. Do not make bounding boxes a blocker for the Round-1 build.

Use Gemini structured JSON output / schema validation where supported rather than relying only on free-form text parsing. Gemini officially supports structured outputs and object detection/segmentation for image understanding. citeturn0search0turn0search2

Important:
- Never claim certainty when the image is unclear.
- Do not invent precise material information.
- Do not force every object into a supported class.
- Keep explanations short.
- Validate every returned class against the allowed enum.
- Validate confidence is 0-100.
- Sanitize all model output before returning it to the frontend.
- If Gemini returns malformed output, return a clean structured API error rather than crashing.

---

# 7. DEMO POINT LOGIC

EcoPoints are prototype gamification values.

Use deterministic defaults based on category:

Organic: 15
Compostable: 15
Recyclable: 10
E-Waste: 25
Hazardous: 20
General Waste: 5
Unknown: 0

If Gemini produces an unreasonable value, the backend should use the deterministic category value.

The purpose is to demonstrate the behavioural feedback loop, not to claim a real-world reward economy.

---

# 8. DEMO IMPACT LOGIC

Use conservative prototype estimates.

The values are illustrative, not scientific guarantees.

For Round 1:

Recyclable:
- waste_diverted_kg ≈ 0.02
- co2_saved_kg ≈ 0.08

Organic:
- waste_diverted_kg ≈ 0.10
- co2_saved_kg ≈ 0.05

Compostable:
- waste_diverted_kg ≈ 0.10
- co2_saved_kg ≈ 0.05

E-Waste:
- waste_diverted_kg ≈ 0.15
- co2_saved_kg ≈ 0.20

Hazardous:
- waste_diverted_kg ≈ 0.05
- co2_saved_kg ≈ 0.10

General Waste:
- waste_diverted_kg = 0
- co2_saved_kg = 0

These are demo metrics only.

Do not present them as certified environmental measurements.

---

# 9. API ENDPOINTS

Implement:

## GET /api/health

Return:

{
  "status": "ok",
  "service": "EcoLoop Backend"
}

---

## POST /api/analyze

Accept:

multipart/form-data

Field:

image

Supported common image formats:
- JPG/JPEG
- PNG
- WEBP

Validate:
- file exists
- MIME/type is reasonable
- size is reasonable

Return HTTP 200:

{
  "success": true,
  "items": [
    {
      "item": "...",
      "material": "...",
      "class": "Biogas",
      "confidence": 96,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "..."
    }
  ],
  "summary": {
    "total_items": 1,
    "classes_detected": ["Biogas"],
    "dominant_class": "Biogas"
  }
}

For errors:

{
  "success": false,
  "error": {
    "code": "IMAGE_REQUIRED",
    "message": "Please upload an image."
  }
}

Use meaningful HTTP status codes.

---

# 10. OPTIONAL ROUND-1 DEMO ENDPOINT

If it can be implemented without slowing down the core build:

GET /api/stats

Return demo statistics such as:

{
  "eco_points": 2480,
  "items_recycled": 47,
  "waste_diverted_kg": 12.4,
  "co2_saved_kg": 8.7
}

This can initially be static/in-memory prototype data.

No database is required.

---

# 11. FRONTEND INTEGRATION CONTRACT

The frontend developer is working independently.

DO NOT require them to wait for you.

The frontend will call:

POST /api/analyze

and expect exactly the documented structure.

Create/update:

docs/API.md

with:

- endpoint
- request format
- response format
- error format
- example curl request
- example JSON response
- CORS/local-development information

Do not make the frontend guess the contract.

---

# 12. CORS

Enable CORS for local development.

The frontend may run through a simple local server.

Do not introduce authentication or complicated security middleware for Round 1.

---

# 13. ERROR HANDLING

The backend must NEVER crash because:

- Gemini is temporarily unavailable
- malformed model output is returned
- an image is missing
- an unsupported file is uploaded
- the API key is missing
- the image is too large
- the model cannot identify the item

Return a useful JSON error.

The frontend must always have enough information to show a graceful error state.

---

# 14. RUNNING THE BACKEND

The README should contain the exact setup:

Create environment:

uv venv

Activate it.

Install:

uv pip install -r backend/requirements.txt

Create:

backend/.env

Run:

python backend/app.py

The server should be easy to run from the repository root.

Prefer:

http://127.0.0.1:5000

unless there is a strong reason otherwise.

---

# 15. QUALITY REQUIREMENTS

Before declaring complete:

1. Start Flask successfully.
2. `/api/health` works.
3. Upload a real JPG/PNG.
4. Gemini receives the image.
5. Gemini response is parsed.
6. `/api/analyze` returns valid JSON.
7. Invalid/missing images produce clean errors.
8. Missing API key produces a clean error.
9. CORS works.
10. `docs/API.md` matches the actual implementation.

Test at least:
- plastic bottle → Recyclable
- banana/vegetable/food waste → Biogas
- aluminum can → Recyclable
- dirty multilayer wrapper → Non-Recyclable
- an ambiguous/miscellaneous object → Others
- an image containing MULTIPLE waste types in one frame

The multiple-waste image test is important: the API must return multiple `items`, not collapse the image into one classification.

Do not fake successful Gemini results when the real API is configured.

---

# 16. GIT RULES

Work only on the backend branch.

Recommended branch:

backend/gemini

Do not modify or overwrite frontend work.

Make small commits:

- `feat: add Flask backend`
- `feat: integrate Gemini vision analysis`
- `feat: add waste classification response`
- `docs: add backend API contract`

Do not commit `.env`.

---

# 17. DESIGN PHILOSOPHY

The backend should support the visual experience shown in the EcoLoop reference design:

- premium
- environmental
- intelligent
- measurable
- futuristic but credible

The backend should expose enough meaningful data for the frontend to create:
- classification result
- confidence
- disposal recommendation
- EcoPoints
- environmental impact
- progress/impact dashboard

---

# 18. DO NOT DO THESE

Do NOT:

- build blockchain
- build real payments
- build real municipal integrations
- build a complicated database
- train a custom neural network
- build authentication
- build an admin system
- rewrite frontend
- add unnecessary frameworks
- spend time on theoretical architecture

The goal is a convincing working Round-1 prototype.

---

# 19. IF CORE BACKEND IS COMPLETE EARLY

Only after all required tests pass, optionally add:

1. `/api/stats`
2. simple scan history stored in memory
3. category statistics
4. recent scan endpoint
5. better uncertainty handling
6. optional multi-object detection if useful

Never sacrifice reliability for expansion.

---

# FINAL INSTRUCTION

Start by inspecting the repository.

Then implement the backend completely.

Do not merely explain what should be done.

Actually create/edit the files, install the necessary dependencies, run the server, test the API, and fix errors.

At the end, report:

- files created/changed
- how to run it
- API endpoint
- test result
- anything the frontend developer must know

Keep the implementation simple and production-clean enough for a hackathon prototype.


---

# 20. FUTURE PHASE — COLLECTION ROUTING / TRUCK OPTIMIZATION

Do NOT implement this before the core multi-class Gemini pipeline is stable.

EcoLoop can later expand from "what is this waste?" to "where should it go and how should it be collected?"

Possible Phase 2 flow:

AI classification
→ waste stream
→ locality / pickup point
→ accumulated quantity
→ collection priority
→ route optimization
→ number/type of trucks required
→ driver/collector route

Potential future backend endpoints:

GET /api/collection/summary
POST /api/collection/route
GET /api/collection/routes
GET /api/collection/trucks

Future route data may include:

{
  "zone": "Zone A",
  "stream": "Biogas",
  "estimated_kg": 420,
  "pickup_points": 12,
  "truck_type": "Organic Waste Carrier",
  "trucks_required": 2,
  "priority": "High",
  "route": [...]
}

This is intentionally deferred.

When the core prototype is complete and there is spare time, implement a simple demo routing layer using static/mock locality data and a straightforward heuristic. Do NOT attempt a production GIS/vehicle-routing system during Round 1.

The long-term product idea is:

CLASSIFY → AGGREGATE → ROUTE → COLLECT → RECOVER → MEASURE IMPACT


---

# 21. VISUAL INTELLIGENCE DATA FOR THE FRONTEND

The frontend will use the AI result to create a visual "real-time ingestion" experience inspired by the supplied EcoLoop reference.

The backend should therefore preserve optional object-level data when Gemini provides it.

For each detected object, support:

- `item`
- `material`
- `class`
- `confidence`
- `disposal`
- `points`
- `waste_diverted_kg`
- `co2_saved_kg`
- `explanation`
- optional `box_2d`

`box_2d` format:

[ymin, xmin, ymax, xmax]

Coordinates are normalized to 0–1000.

Gemini's current image-understanding documentation supports object detection with normalized bounding boxes, so use this capability where supported. citeturn0search4

The frontend can then draw technical highlight boxes around detected waste.

Example:

{
  "item": "Vegetable scraps",
  "class": "Biogas",
  "confidence": 94,
  "box_2d": [210, 120, 680, 610]
}

The backend MUST NOT fail if `box_2d` is unavailable.

Bounding boxes are an enhancement, not a blocker.

---

# 22. FUTURE REAL-TIME INGESTION DATA

The reference design also shows a future hardware/telemetry layer.

Do NOT build ESP32/MQTT/hardware integration in Round 1 unless the core AI pipeline is already finished.

However, keep the architecture extensible for future fields such as:

{
  "telemetry": {
    "fill_percent": 72,
    "mass_kg": 5.4,
    "temperature_c": 21,
    "timestamp": "..."
  }
}

Future architecture:

EDGE SENSOR
→ MQTT
→ ECOLOOP INGESTION API
→ WASTE STREAM AGGREGATION
→ ROUTING / TRUCK OPTIMIZATION

For now, this is only a documented future direction.

Do not add MQTT dependencies just for the sake of the visual.


---

# 21. VISUAL INTELLIGENCE DATA — BOUNDING BOXES ARE REQUIRED IF RELIABLE

The frontend wants to create a visual "AI detection" experience similar to the EcoLoop reference:
- thin lime detection rectangles
- corner brackets
- object labels attached to the rectangle
- class badges
- confidence percentage
- small REC / LIVE / AI status indicators

Gemini officially supports object detection with bounding boxes. Its documented format is:

`box_2d: [ymin, xmin, ymax, xmax]`

with every coordinate normalized to the range `0–1000`. The backend must convert these coordinates to the frontend-friendly form without losing precision. citeturn0search0turn0search2

For every confidently detected waste object, return:

```json
{
  "box_2d": [ymin, xmin, ymax, xmax],
  "label": "Vegetable scraps",
  "class": "Biogas",
  "confidence": 94
}
```

The frontend can convert to percentages:

```text
top    = ymin / 10 %
left   = xmin / 10 %
bottom = ymax / 10 %
right  = xmax / 10 %
```

Example:

```text
box_2d = [220, 140, 650, 710]

top    = 22%
left   = 14%
height = 43%
width  = 57%
```

Return the coordinates relative to the ORIGINAL uploaded image dimensions, following Gemini's documented 0–1000 coordinate convention.

IMPORTANT:
- Never fabricate coordinates.
- Do not return a box if the object cannot be localized reasonably.
- A slightly loose box is preferable to a confidently wrong precise box.
- Validate every coordinate is an integer from 0 to 1000.
- Validate `ymin < ymax` and `xmin < xmax`.
- Clamp out-of-range values.
- If multiple objects overlap, return separate boxes.
- Do not let bounding-box failure break classification. If detection succeeds but localization fails, return the item without a box.

---

# 22. OPTIONAL SEGMENTATION MASK

If the selected Gemini model/API path reliably supports segmentation, optionally return:

```json
"mask": [[x1,y1], [x2,y2], [x3,y3]]
```

with polygon coordinates normalized to 0–1000.

This can later create an even more advanced glowing contour around waste objects.

DO NOT make segmentation a Round-1 blocker.

Bounding boxes are the priority.

---

# 23. RECOMMENDED API RESULT SHAPE FOR VISUAL SCANNING

The preferred result is:

```json
{
  "success": true,
  "items": [
    {
      "item": "Vegetable scraps",
      "material": "Biodegradable organic waste",
      "class": "Biogas",
      "confidence": 94,
      "disposal": "Organic / Biogas Feedstock",
      "points": 15,
      "waste_diverted_kg": 0.10,
      "co2_saved_kg": 0.05,
      "explanation": "Suitable for the EcoLoop organic recovery pathway.",
      "box_2d": [220, 140, 650, 710]
    }
  ],
  "summary": {
    "total_items": 1,
    "classes_detected": ["Biogas"],
    "dominant_class": "Biogas"
  }
}
```

The backend should preserve the original image dimensions in the response if useful:

```json
"image": {
  "width": 1706,
  "height": 959
}
```

This is optional because the frontend can also read the dimensions from the uploaded image.

---

# 24. AI DETECTION PROMPT BEHAVIOR

Ask Gemini to:

1. Detect all prominent waste objects.
2. Identify the object.
3. Assign exactly one EcoLoop operational class.
4. Determine confidence.
5. Return a bounding box for each object.
6. Avoid duplicate boxes for the same object.
7. Ignore irrelevant background objects such as plants, tables, hands, people, phones, walls, etc.
8. Focus on waste/material objects.
9. Prefer the Biogas class for clearly identifiable organic food/kitchen waste suitable for the organic recovery pathway.
10. Return `Others` when the object cannot confidently fit the operational streams.

Suggested instruction:

"Detect all prominent waste objects in the uploaded image. Ignore people, hands, furniture, background scenery and non-waste objects. For each waste object, identify its material and assign exactly one EcoLoop class: Recyclable, Biogas, Non-Recyclable, E-Waste/Hazardous, or Others. Return a [ymin,xmin,ymax,xmax] bounding box normalized to 0-1000 for every localized object. Do not invent objects or boxes."

Use structured JSON output/schema where supported so the backend receives predictable fields. Gemini documents JSON schema structured outputs for this purpose. citeturn0search7

---

# 25. ROUND-1 VISUAL DETECTION PRIORITY

The desired demo is:

UPLOAD IMAGE
        ↓
"AI WASTE CLASSIFIER"
        ↓
DETECTION SCAN
        ↓
BOX 1 → Vegetable scraps → BIOGAS 94%
BOX 2 → Battery → E-WASTE 91%
BOX 3 → Bottle → RECYCLABLE 96%
        ↓
CLASSIFICATION SUMMARY
        ↓
ECOPOINTS + IMPACT

This should be treated as one of the highest-value backend features after basic classification.
