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

Analyze the primary waste item visible in the image.

Return structured JSON with:

{
  "item": "Plastic bottle",
  "material": "PET plastic",
  "category": "Recyclable",
  "confidence": 94,
  "disposal": "Dry/Recyclable Waste",
  "points": 10,
  "waste_diverted_kg": 0.02,
  "co2_saved_kg": 0.08,
  "explanation": "Short human-readable explanation."
}

Allowed categories:

- Organic
- Recyclable
- Compostable
- E-Waste
- Hazardous
- General Waste
- Unknown

Important:

- Never claim certainty when the image is unclear.
- If confidence is low, return `Unknown` or explain uncertainty.
- Do not invent precise material information that cannot reasonably be inferred.
- Keep the explanation short.
- Keep the response suitable for displaying directly in a UI.
- The backend must validate/sanitize the model response before returning it.

If Gemini returns malformed JSON, attempt a safe extraction/parse strategy. If that still fails, return a structured API error rather than crashing.

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
  "result": {
    "item": "...",
    "material": "...",
    "category": "...",
    "confidence": 94,
    "disposal": "...",
    "points": 10,
    "waste_diverted_kg": 0.02,
    "co2_saved_kg": 0.08,
    "explanation": "..."
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
- plastic bottle
- banana peel/organic waste
- aluminum can

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
