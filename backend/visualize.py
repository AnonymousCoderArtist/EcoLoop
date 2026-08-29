"""
EcoLoop Visual Test — Bounding Box Overlay Generator

Uses backend/image.png -> calls /api/analyze (Gemini) -> draws boxes
with index, class, confidence, points. Saves to backend/ only.

Run:
  uv run python backend/visualize.py                 # analyze live + save
  uv run python backend/visualize.py --cached        # use last JSON without calling Gemini
  uv run python backend/visualize.py --input backend/image.png --output backend/image_annotated.png

Stored outputs:
  backend/image_annotated.png        (latest)
  backend/image_annotated_timestamp.png
  backend/last_result.json           (raw Gemini JSON for debugging)
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

# Support both direct and module run
try:
    from config import GEMINI_MODEL  # type: ignore
except ImportError:
    from backend.config import GEMINI_MODEL  # type: ignore

# ── Style map — Swiss editorial palette ───────────────────────────
CLASS_COLORS: dict[str, tuple[str, str, str]] = {
    # (box_color, text_bg, light_fill_rgba_hex)
    "Recyclable": ("#16a34a", "#14532d", "#16a34a18"),        # green, fill ~15% alpha
    "Biogas": ("#ca8a04", "#713f12", "#eab30822"),            # amber, Biogas priority highlighted
    "Non-Recyclable": ("#dc2626", "#7f1d1d", "#ef444418"),
    "E-Waste/Hazardous": ("#9333ea", "#581c87", "#a855f722"),
    "Others": ("#6b7280", "#1f2937", "#9ca3af18"),
}

FALLBACK_COLOR = ("#0891b2", "#0c4a6e", "#06b6d422")

# Convert hex with alpha to RGBA tuple
def _hex_to_rgba(hex_str: str) -> tuple[int, int, int, int]:
    h = hex_str.lstrip("#")
    if len(h) == 8:  # RRGGBBAA
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
    if len(h) == 6:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    return (0, 0, 0, 0)

# ── Helpers ──────────────────────────────────────────────────────────

def get_font(size: int = 14) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try DejaVu / Arial, fallback to default."""
    candidates = [
        "DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf",
        "arial.ttf",
        "Arial.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    # Search PIL bundled
    try:
        # PIL ships with DejaVu in some installs
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        pass
    return ImageFont.load_default()


def box_to_pixels(box_2d: list[int], img_w: int, img_h: int) -> tuple[int, int, int, int]:
    """Convert [ymin,xmin,ymax,xmax] 0-1000 -> (x1,y1,x2,y2) pixels."""
    ymin, xmin, ymax, xmax = box_2d
    # Clamp 0-1000 already done in schemas, but re-clamp
    ymin = max(0, min(1000, ymin))
    xmin = max(0, min(1000, xmin))
    ymax = max(0, min(1000, ymax))
    xmax = max(0, min(1000, xmax))
    x1 = int(xmin / 1000 * img_w)
    y1 = int(ymin / 1000 * img_h)
    x2 = int(xmax / 1000 * img_w)
    y2 = int(ymax / 1000 * img_h)
    # Ensure x1<x2, y1<y2
    if x1 >= x2:
        x2 = min(img_w, x1 + 20)
    if y1 >= y2:
        y2 = min(img_h, y1 + 20)
    return x1, y1, x2, y2


def draw_swiss_corners(draw: ImageDraw.ImageDraw, x1, y1, x2, y2, color, light_fill, width=2, corner_box=12, bracket_len=22):
    """Swiss editorial: light wash inside + thin border + small solid squares at corners + L brackets."""
    # Light wash inside (semi-transparent)
    draw.rectangle([x1, y1, x2, y2], fill=light_fill, outline=None)
    # Thin main border
    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
    # Small solid squares at 4 corners (Swiss grid)
    sq = corner_box
    for (cx, cy) in [(x1, y1), (x2 - sq, y1), (x1, y2 - sq), (x2 - sq, y2 - sq)]:
        draw.rectangle([cx, cy, cx + sq, cy + sq], fill=color, outline="white", width=1)
        # inner tiny dot
        draw.rectangle([cx + 4, cy + 4, cx + sq - 4, cy + sq - 4], fill="white")
    # Subtle L brackets extending beyond squares
    bl = bracket_len
    bw = 2
    # Top-left beyond square
    draw.line([(x1 + sq + 2, y1), (x1 + sq + 2 + bl, y1)], fill=color, width=bw)
    draw.line([(x1, y1 + sq + 2), (x1, y1 + sq + 2 + bl)], fill=color, width=bw)
    # Top-right
    draw.line([(x2 - sq - 2 - bl, y1), (x2 - sq - 2, y1)], fill=color, width=bw)
    draw.line([(x2, y1 + sq + 2), (x2, y1 + sq + 2 + bl)], fill=color, width=bw)
    # Bottom-left
    draw.line([(x1 + sq + 2, y2), (x1 + sq + 2 + bl, y2)], fill=color, width=bw)
    draw.line([(x1, y2 - sq - 2 - bl), (x1, y2 - sq - 2)], fill=color, width=bw)
    # Bottom-right
    draw.line([(x2 - sq - 2 - bl, y2), (x2 - sq - 2, y2)], fill=color, width=bw)
    draw.line([(x2, y2 - sq - 2 - bl), (x2, y2 - sq - 2)], fill=color, width=bw)


def annotate_image(
    input_path: Path,
    result: dict[str, Any],
    output_path: Path,
) -> Path:
    """Draw all boxes from result onto image and save."""
    img = Image.open(input_path).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    items = result.get("items", [])
    summary = result.get("summary", {})
    model = result.get("model", GEMINI_MODEL)

    # Fonts
    font_small = get_font(12)
    font_med = get_font(14)
    font_large = get_font(16)
    font_tick = get_font(11)

    # ── Draw each zone box ─────────────────────────────────────────
    for idx, item in enumerate(items, start=1):
        box = item.get("box_2d")
        if not box:
            continue
        klass = item.get("class", "Others")
        # Unpack 3-tuple
        try:
            box_color, bg_color, light_hex = CLASS_COLORS.get(klass, FALLBACK_COLOR)
        except ValueError:
            box_color, bg_color = CLASS_COLORS.get(klass, FALLBACK_COLOR)[:2]
            light_hex = "#ffffff18"
        light_fill = _hex_to_rgba(light_hex)
        x1, y1, x2, y2 = box_to_pixels(box, w, h)

        # Swiss: light wash + thin border + small corner squares
        draw_swiss_corners(draw, x1, y1, x2, y2, box_color, light_fill, width=2, corner_box=11, bracket_len=18)

        # ── Swiss label above box (uppercase, tracking) ─────────────
        item_name = item.get("item", "?")[:30]
        confidence = item.get("confidence", 0)
        points = item.get("points", 0)
        # Swiss typographic caps with dot separators
        label = f"#{idx:02d}  {item_name.upper()}  ·  {klass.upper()}  ·  {confidence}%  ·  +{points} PTS"

        try:
            bbox = draw.textbbox((0, 0), label, font=font_med)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except Exception:
            text_w, text_h = draw.textlength(label, font=font_med), 14

        pad_x, pad_y = 10, 5
        label_w = text_w + pad_x * 2
        label_h = text_h + pad_y * 2

        # Position: above box if space, else inside top with offset for corner squares
        lx1 = x1
        ly1 = y1 - label_h - 8
        if ly1 < 0:
            ly1 = y1 + 14  # below corner squares
        lx2 = lx1 + label_w
        ly2 = ly1 + label_h
        if lx2 > w:
            lx2 = w
            lx1 = max(0, lx2 - label_w)

        # Swiss label: solid bg, 1px border, small left accent bar
        draw.rectangle([lx1, ly1, lx2, ly2], fill=bg_color, outline=box_color, width=1)
        # Left accent bar (4px)
        draw.rectangle([lx1, ly1, lx1 + 4, ly2], fill=box_color)
        draw.text((lx1 + pad_x + 4, ly1 + pad_y), label, fill="white", font=font_med)

        # ── Small Swiss index badge (square, not circle) ────────────
        # Top corner already has 11px squares; add numbered square badge just inside
        badge_sz = 22
        bx1, by1 = x1 + 16, y1 + 16
        if ly1 == y1 + 14:
            by1 = ly2 + 8
        # Ensure inside box
        draw.rectangle([bx1, by1, bx1 + badge_sz, by1 + badge_sz], fill=box_color, outline="white", width=1)
        idx_text = f"{idx:02d}"
        try:
            tb = draw.textbbox((0, 0), idx_text, font=font_small)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
        except Exception:
            tw, th = 10, 10
        draw.text((bx1 + (badge_sz - tw) / 2, by1 + (badge_sz - th) / 2 - 1), idx_text, fill="white", font=font_small)

        # ── Bottom Swiss disposal strip (monospace, subdued) ───────
        disposal = item.get("disposal", "")[:40]
        if disposal:
            disp_label = disposal.upper()
            try:
                db = draw.textbbox((0, 0), disp_label, font=font_tick)
                dw, dh = db[2] - db[0], db[3] - db[1]
            except Exception:
                dw, dh = len(disp_label) * 5, 10
            dh += 6
            dw += 10
            dx1, dy1 = x1, y2 - dh - 4
            dx2, dy2 = min(x2, x1 + dw + 8), y2 - 4
            if dy1 < y1:
                dy1, dy2 = y2 + 4, y2 + dh + 4
            # Swiss: white/90 with thin top rule
            draw.rectangle([dx1, dy1, dx2, dy2], fill=(255, 255, 255, 230), outline=box_color, width=1)
            draw.rectangle([dx1, dy1, dx2, dy1 + 2], fill=box_color)
            draw.text((dx1 + 6, dy1 + 3), disp_label, fill="#111827", font=font_tick)

    # ── Footer summary bar ─────────────────────────────────────────
    total_items = summary.get("total_items", len(items))
    classes_detected = summary.get("classes_detected", [])
    dominant = summary.get("dominant_class", "-")
    total_points = sum(i.get("points", 0) for i in items)
    total_diverted = sum(i.get("waste_diverted_kg", 0) for i in items)
    total_co2 = sum(i.get("co2_saved_kg", 0) for i in items)

    footer_h = 72
    # Expand canvas to add footer below image (don't obscure)
    new_h = h + footer_h
    out = Image.new("RGB", (w, new_h), "white")
    out.paste(img, (0, 0))
    draw2 = ImageDraw.Draw(out)

    # Footer background
    draw2.rectangle([0, h, w, new_h], fill="#0f172a")  # slate-900
    # Accent line
    draw2.rectangle([0, h, w, h + 4], fill="#a3e635")  # lime

    # Summary text — multiple categories
    left_text = f"EcoLoop  •  {model}  •  {total_items} items  •  {total_points} pts  •  {total_diverted:.2f}kg diverted  •  {total_co2:.2f}kg CO₂"
    right_text = f"Classes: {', '.join(classes_detected) if classes_detected else '—'}   |   Dominant: {dominant}"
    # Draw left
    draw2.text((16, h + 14), left_text, fill="white", font=font_med)
    draw2.text((16, h + 38), right_text, fill="#a3e635", font=font_small)

    # Per-class legend (bottom right small)
    legend_x = w - 16
    # Build legend string
    legend = "  ".join(f"{c}:{CLASS_COLORS.get(c, FALLBACK_COLOR)[0]}" for c in classes_detected)
    # Instead draw colored dots
    lx = w - 16
    for klass in reversed(classes_detected):
        col = CLASS_COLORS.get(klass, FALLBACK_COLOR)[0]
        # Measure
        try:
            tb = draw2.textbbox((0, 0), klass, font=font_tick)
            tw = tb[2] - tb[0]
        except Exception:
            tw = len(klass) * 6
        # Dot
        dot_x = lx - tw - 14
        draw2.ellipse([dot_x - 4, h + 40, dot_x + 6, h + 50], fill=col)
        draw2.text((dot_x + 10, h + 38), klass, fill="white", font=font_tick)
        lx = dot_x - 10

    out.save(output_path, "PNG", optimize=True)
    print(f"[EcoLoop] Saved annotated image -> {output_path} ({w}x{new_h})")
    print(f"  Items: {total_items} | Classes: {classes_detected} | Dominant: {dominant} | Points: {total_points}")
    for i, it in enumerate(items, 1):
        print(f"  #{i:02d} {it.get('item')[:24]:24} | {it.get('class'):18} | {it.get('confidence'):3}% | +{it.get('points')}pts | box={it.get('box_2d')}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="EcoLoop bbox visualizer")
    parser.add_argument("--input", type=str, default="backend/image.png", help="Input image path")
    parser.add_argument("--output", type=str, default="backend/image_annotated.png", help="Output annotated path")
    parser.add_argument("--cached", action="store_true", help="Use backend/last_result.json instead of calling Gemini")
    parser.add_argument("--json", type=str, default="backend/last_result.json", help="Cache JSON path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    json_path = Path(args.json)

    if not input_path.exists():
        print(f"[ERROR] Input not found: {input_path}")
        return 1

    # Ensure output dir exists (backend)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.cached and json_path.exists():
        print(f"[EcoLoop] Using cached {json_path}")
        result = json.loads(json_path.read_text(encoding="utf-8"))
    else:
        # Call Gemini via app test client (no need to run server)
        print(f"[EcoLoop] Analyzing {input_path} with {GEMINI_MODEL} ...")
        try:
            from backend.app import create_app  # type: ignore
        except ImportError:
            from app import create_app  # type: ignore
        app = create_app()
        client = app.test_client()
        with open(input_path, "rb") as f:
            data = f.read()
        resp = client.post("/api/analyze", data={"image": (f := __import__('io').BytesIO(data), input_path.name)})
        # Need to re-create BytesIO correctly
        if resp.status_code != 200:
            print(f"[ERROR] /api/analyze {resp.status_code}: {resp.json}")
            return 1
        result = resp.json
        # Save cache
        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"[EcoLoop] Cached result -> {json_path}")

        # More reliable path: redo with proper file tuple if above missed mimetype
        if not result or not result.get("items"):
            # fallback: direct gemini call already handled; keep result
            pass

    # If still no result, try direct file post again with correct mimetype handling
    if not result or "items" not in result:
        print("[ERROR] No items in result")
        return 1

    # Annotate
    out = annotate_image(input_path, result, output_path)
    # Also save timestamped copy
    ts = time.strftime("%Y%m%d_%H%M%S")
    ts_path = output_path.parent / f"image_annotated_{ts}.png"
    Image.open(out).save(ts_path)
    print(f"[EcoLoop] Also saved timestamped -> {ts_path}")

    # Verify correct indices
    items = result.get("items", [])
    # Check all boxes valid and indices sequential
    for i, it in enumerate(items, 1):
        box = it.get("box_2d")
        if box:
            x1, y1, x2, y2 = box
            valid = (0 <= x1 <= 1000 and 0 <= x2 <= 1000 and 0 <= y1 <= 1000 and 0 <= y2 <= 1000 and x1 < x2 and y1 < y2)
            if not valid:
                print(f"[WARN] #{i} invalid box {box}")

    print("[EcoLoop] Done. Check backend/image_annotated.png for correct index/highlight and per-box points/category.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
