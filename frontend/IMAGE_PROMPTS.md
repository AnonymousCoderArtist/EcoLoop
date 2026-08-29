# EcoLoop — Image Prompts (Swiss Editorial + Futuristic) — One MD for ChatGPT Image

> **Generate all images with IDENTICAL style, lighting, palette, and camera.** This ensures the whole website feels like one premium climate-tech product, not a collage.
> Export: PNG, 1280×720, 16:9, 300 DPI, no text in image (text added via HTML).

---

## 0. GLOBAL DESIGN SYSTEM — APPLY TO EVERY PROMPT

```
Style: Swiss editorial + futuristic minimal — 12-column grid, 1px borders (#f4f4f0 @ 8% opacity), 11px solid corner squares, light wash fills (15% alpha), mono typography (SF Mono), generous negative space, thin lime accent, glass morphism subtle blur 12px
Palette LOCKED: black #080808, ivory #F4F4F0, lime #CCFF00 (accent + corner squares), amber #CA8A04 (Biogas priority), red #DC2626 (Non-Recyclable), violet #9333EA (E-Waste), grey #8A8A82 / #6B7280
Lighting LOCKED: soft diffused studio key (5600K) from 45° top-left + lime rim light #CCFF00 at 15% intensity from back edge + subtle amber fill for Biogas areas, shallow depth of field f/2.8, 85mm lens equivalent, 8k photorealistic, raw, --no over-sharpened, --no HDR halos, subtle grain 3%
Camera LOCKED: eye-level or 15° top-down, centered grid, subject at 60% frame, negative space 40%, rule of thirds
Futuristic touches: holographic 1px line, subtle glow on borders (outer glow 4px rgba(204,255,0,0.15)), dark glass panels (backdrop-blur 12px, rgba(8,8,8,0.82))
Negative: no cartoon, no 3D clay, no stock watermark, no text/letters, no lens flare, no trash cliché over-saturation, no cartoon bins, keep premium documentary realism
```

Add this suffix to EVERY prompt below: `, Swiss editorial grid, futuristic glass, 1px borders, 11px corner squares, lime rim light, soft studio 5600K, 85mm f/2.8, 8k photorealistic raw, palette #080808 #F4F4F0 #CCFF00 #CA8A04 #DC2626 --ar 16:9 --style raw --no text --no logo`

---

## 1. HERO — End Result User Wants + Without Fear They Avoid

**Goal:** Show clean, rewarded home (want) vs crossed-out landfill guilt (fear removed). Above-the-fold, hero-bg layer.

**Prompt H1 — Hero Master (use as hero-bg):**
```
Bright pristine Scandinavian kitchen, morning soft diffused light from window (same 5600K key + lime rim), three Swiss waste bins in a row — matte green Recyclable (#16a34a), amber Biogas (#ca8a04) glowing subtly, red Non-Recyclable (#dc2626) — all lids closed, no overflow, family of 3 smiling in background slightly blurred (f/2.8), floating holographic EcoPoints badge "+15 PTS" lime #CCFF00 above Biogas bin, background far landfill blurred and crossed with thin lime line (visual metaphor "without"), Swiss grid negative space right 40%, premium climate-tech, futuristic glass counter, --no trash pile, --no contamination, --no guilt
```

**Prompt H2 — Hero Alternative (foreground.png replacement):**
```
Zero-waste counter top-down, sorted waste perfectly arranged on dark slate #080808 with 1px grid, PET bottles + aluminum cans in green zone, vegetable peels + coffee grounds in amber Biogas zone, masks + wrappers in red zone — each zone has thin lime corner brackets visible, light wash fill, editorial top-down, same lighting as H1
```

---

## 2. SOCIAL PROOF — Trust, Numbers, Logos

**Prompt S1 — Metrics strip (background for proof section, uses background 2.png slot):**
```
Dark editorial data wall, four metric cards on 1px grid (1,248kg/824kg/4.8★/2,480 pts) in mono SF Mono, Swiss, lime accent on numbers, same global style + lighting, background subtle bokeh of community, premium
```

**Prompt S2 — SVG Icon Set (generate as SVG, not photo):**
> **SKIP — NOT GENERATING (use inline SVG already in site at `frontend/index.html` + `style.css`)**
```
Minimal line SVG icon set on black #080808: shield-check, users-group, leaf, trophy, bar-chart — 2px stroke, lime #CCFF00, 24×24 grid, Swiss, futuristic thin glow, consistent line weight
```

**Prompt S3 — Community photo:**
```
Diverse urban neighborhood (4 people, 20s-40s) holding phone showing EcoLoop leaderboard "Greenridge Terrace 2,450 pts", authentic smile, soft diffused same lighting, Swiss, lime accent on phone border, shallow depth, background blurred street, editorial documentary
```

**Prompt S4 — Logo strip:**
> **SKIP — NOT GENERATING (use text logos already in site)**
```
Five minimal climate-tech logotypes in grey #8a8a82 on black, 1px border grid, "As seen in" label mono 10px, Swiss editorial, same palette, horizontal strip
```

---

## 3. PROBLEM — Real Cost (show urgency, make them feel it)

**Prompt P1 — Landfill (background for problem card 1, muted):**
```
Aerial landfill at golden hour muted desaturated (same 5600K but desaturated -30%), methane haze thin #6b7280, seagulls small, vast, editorial documentary, 1px red top rule #DC2626, same Swiss grid, premium — show scale of overflow
```

**Prompt P2 — Ocean / Microplastic:**
```
Close-up ocean surface, microplastic particles floating, subtle turtle silhouette far blurred, editorial muted, 1px orange rule, same lighting desaturated, premium, not dramatic horror — quiet cost
```

**Prompt P3 — Contamination (kitchen bin confusion):**
```
Kitchen bin top-down, mixed contamination: vegetable peels + plastic wrapper + face mask + battery all tossed together in one bin, cross-contamination, labels confused, health hazard, same studio lighting + red rim light, Swiss thin border, premium documentary
```

**Prompt P4 — Cost infographic (generate as background, text via HTML):**
```
Dark Swiss infographic wall, three large numbers mono: "$12B landfill cost" "8% global CO2 from organic" "91% plastic never recycled" — lime accent on numbers, same global style, background subtle landfill bokeh 10% opacity
```

**Prompt P5 — Alt mixed pile urgency (optional):**
```
Premium waste pile with dirty multilayer wrapper + e-waste battery leaking + medical mask, mixed materials clearly wrong stream, desk light same 5600K + red fill, Swiss corner squares faint, editorial urgency without gore
```

---

## 4. SOLUTION — Better by Design (5-8 Features, each = feature + benefit + visual)

Generate each as 600×400 card header image (still same global style) + benefit text via HTML.

**F1 — AI Swiss Zones (uses background 2.png slot):**
```
Gemini Vision scanning waste pile top-down, 4 thin lime corner brackets #CCFF00 + 11px solid squares + light wash fill (15% alpha) per zone visible, UI overlay faint holographic, dark slate #080808, same lighting, futuristic, premium — show AI understanding zones not objects
```

**F2 — Biogas Priority (amber hero):**
```
Biogas heap: vegetable peels + coffee grounds + dry leaves clustered center, amber glow #CA8A04 subtle outer glow 8px, small biogas plant silhouette far blurred, methane flame tiny, priority badge amber, same global lighting + amber fill, Swiss
```

**F3 — One-Tap Scan:**
```
Hand holding phone camera over waste, phone screen showing drop-zone UI with dashed lime border, camera modal with Cancel/Capture buttons, Swiss mono "1.2s loader" label, same lighting, premium
```

**F4 — EcoPoints + Impact:**
```
Reward burst holographic: large "+15 PTS" lime #CCFF00, sub-label "0.10kg diverted · 0.05kg CO₂" mono, animated counter blur, dark glass panel backdrop-blur, same style
```

**F5 — Dashboard Telemetry (uses background 1.png slot):**
```
Dark dashboard grid, metrics: 12.4kg waste / 47 sorts / 8.7kg CO₂ / 2,480 pts, live ingestion "Active" lime, loop bars 35/25/20% lime, mono typography, Swiss 1px borders, same lighting, futuristic glass
```

**F6 — Leaderboard & Community:**
```
Neighborhood leaderboard dark panel: Greenridge Terrace 2,450 pts (lime) vs Maple Grove 2,100, trophy line icon, community map faint background bokeh, Swiss grid, same global style
```

**F7 — Non-Recyclable Intelligence (red):**
```
Contaminated face mask + multilayer packaging flagged red #DC2626 zone, thin red border + 11px corner squares + "Landfill Last Resort" mono label, clear guidance, same lighting + red fill 15%, Swiss
```

**F8 — Swiss Annotated Final (hero for demo, 1280×770):**
> **USE REAL — NOT GENERATING (use `backend/image_annotated.png` real AI output, served at `/api/demo/image`)**
```
Full annotated waste image 1280×770 with 4 zones, each with light wash fill, thin border, 11px corner squares, per-zone label "#02 BIOGAS ZONE · 98% · +15 PTS" with amber bg, footer slate #0F172A, lime top rule, premium Swiss editorial, same lighting as all above — this is the final proof judges touch
```

---

## 5. HOW IT WORKS — 3-4 Steps (Swiss numbered)

Generate each step as 400×400 icon + photo combo, same style.

**Step 01 — Snap:**
```
Phone drop zone: hand dropping waste image into dashed lime border, arrow thin lime, dark bg, step number "01" mono top-left, same global lighting + Swiss 1px border
```

**Step 02 — AI Zones:**
```
Four Swiss zones with corner squares + amber Biogas glow, 1.2s loader line scanning, dark bg, same style
```

**Step 03 — Earn & Track:**
```
EcoPoints +15 badge + dashboard update: points counter + waste/CO₂ numbers rising, lime accent, same style
```

**Step 04 — Repeat & Lead (optional):**
```
Community leaderboard + hands holding sorted bins, repeat habit loop arrow, Swiss grid, same lighting
```

---

## 6. FAQ — Icons (SVG)

```
Minimal line SVG icons: question mark in circle, shield-check, leaf, clock, coins/points — 2px stroke lime #CCFF00 on black #080808, 24×24, Swiss grid, futuristic glow, consistent weight
```

---

## 7. CTA — Final Push

**Prompt CTA — Wide (uses foreground.png slot, blurred):**
```
Wide CTA: hands holding three clean sorted bins (green/amber/red) forward, bright soft diffused same 5600K + lime rim, background foreground.png blurred bokeh, dark overlay 30%, Swiss, CTA button "Start Scanning — Free" lime #CCFF00 on black, premium hopeful
```

---

## 8. FOOTER — Brand

**Prompt Footer — Subtle:**
```
EcoLoop wordmark + tagline "Outcome-based waste intelligence", background 1.png at 10% opacity overlay on black #080808, Swiss 1px top border, mono footer links, same global style, premium minimal
```

---

## Export Checklist (for ChatGPT Image)

- [ ] All prompts include suffix: `, Swiss editorial grid, futuristic glass, 1px borders, 11px corner squares, lime rim light, soft studio 5600K, 85mm f/2.8, 8k photorealistic raw, palette #080808 #F4F4F0 #CCFF00 #CA8A04 #DC2626 --ar 16:9 --style raw --no text --no logo`
- [ ] Keep lighting identical across H1-P1-F1 — same 45° key + lime rim, so scroll feels continuous.
- [ ] Keep palette identical — black/ivory/lime/amber/red/violet/grey only, no new colors.
- [ ] Generate each as PNG 1280×720 (F1-F8 as 600×400 crops from same), then place: hero H1 → hero-bg, social S1 → proof section bg, problem P1-P3 → problem cards, solution F1-F8 → solution card headers, how-it-works steps → step icons, CTA → CTA bg.
- [ ] No text in image — all labels via HTML (mono SF Mono, 11px system-label) to keep Swiss typography crisp.
- [ ] Futuristic touches: glass morphism 12px blur, outer glow 4px rgba(204,255,0,0.15), holographic thin line on hero.

## Website Overall Landing Order (for reference)

Hero (end result without fear) → Social Proof (trust) → Problem (real cost) → Solution (5-8 features + benefit + visual) → How It Works (01-04) → FAQ → CTA → Footer

All sections use same editorial Swiss + futuristic system — see `frontend/style.css` `.landing-section`, `.hero-*`, `.panel`, `var(--accent)` #CCFF00, `var(--black)` #080808.
