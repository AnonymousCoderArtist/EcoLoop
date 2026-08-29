"""EcoLoop Backend Configuration — single source of truth."""

import os

from dotenv import load_dotenv

load_dotenv()

# ── Gemini ──────────────────────────────────────────────────────────
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# ── Server ──────────────────────────────────────────────────────────
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "5000"))
FLASK_ENV: str = os.getenv("FLASK_ENV", "development")

# ── Upload validation ───────────────────────────────────────────────
MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
MAX_IMAGE_SIZE_BYTES: int = MAX_IMAGE_SIZE_MB * 1024 * 1024

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ── EcoLoop domain constants ────────────────────────────────────────
ALLOWED_CLASSES = [
    "Recyclable",
    "Biogas",
    "Non-Recyclable",
    "Others",
    "E-Waste/Hazardous",
]

# Deterministic demo points (Section 7)
CATEGORY_POINTS: dict[str, int] = {
    "Recyclable": 10,
    "Biogas": 15,
    "Non-Recyclable": 5,
    "Others": 0,
    "E-Waste/Hazardous": 25,
}

# Conservative demo impact (Section 8)
# (waste_diverted_kg, co2_saved_kg)
CATEGORY_IMPACT: dict[str, tuple[float, float]] = {
    "Recyclable": (0.02, 0.08),
    "Biogas": (0.10, 0.05),
    "Non-Recyclable": (0.0, 0.0),
    "Others": (0.0, 0.0),
    "E-Waste/Hazardous": (0.15, 0.20),
}

DISPOSAL_MAP: dict[str, str] = {
    "Recyclable": "Recyclable / Dry Waste",
    "Biogas": "Organic / Biogas Feedstock",
    "Non-Recyclable": "Non-Recyclable / Landfill (Last Resort)",
    "Others": "Others / Manual Sorting Required",
    "E-Waste/Hazardous": "E-Waste / Hazardous - Special Handling",
}
