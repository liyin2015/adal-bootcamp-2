# Contract — Hyperspell Hero Clone

**Status:** Approved to Build
**Engineer:** session a3de2709 (supervisor)
**Builder:** adal-worker-56ef7bda (minimax-MiniMax-M3, browser-use)
**Evaluator:** adal-worker-f7f3b0d4 (minimax-MiniMax-M3, browser-use)
**Target:** https://www.hyperspell.com/ — hero section only (nav + dark hero + trust/logo marquee). Hard stop at the "The Company Brain" section.
**Output dir:** `hyperspell-clone/`
**Fidelity:** PIXEL LEVEL + VIDEO LEVEL (animation, content, font, color, styling, all effects) — exactly the same.

---

## Engineer Adjudications (resolved conflicts)

1. **Entrance animation = minimal/instant.** The evaluator's ground truth shows NO visible text entrance stagger on the original (nav/H1/desc/CTA visible at t=0). The clone must match the original's settled state at t≈0–2s. Do NOT add a Framer Motion stagger the original lacks. Only the Unicorn Studio canvas intro (handled by its own runtime) and the infinite marquee are animated. `useReducedMotion` not needed since no entrance anim is added.
2. **Large-screen positioning = match original, do not impose centering.** Evaluator measured hero content staying left-anchored (x≈105) even at 1920. The builder must re-verify the original's actual x-position at 1920×1200 and MATCH it. If the original left-anchors, the clone left-anchors. If it centers, it centers. Do not blindly apply `mx-auto` if the original doesn't. No `ml-[Npx]` / `left-[Npx]` magic numbers either way — use the same container classes the original uses.
3. **Unicorn Studio scene ID = verify + fallback.** The scene-id may be session-dynamic. Builder must confirm the embedded `<div data-us-project="...">` actually renders the live WebGL blob on the clone. If the hardcoded ID fails to load, fall back to a cropped static screenshot of the orb (`src/assets/media/hero-orb-fallback.png`) so the hero is never a flat black box. Document which path shipped.
4. **Marquee = CSS keyframes auto-scroll is acceptable** for this infinite non-draggable strip (the rAF-drag adaptation rule applies to *draggable* marquees, not this one). Must be seamless (duplicate logo set), ~30–40 px/s, no jump on loop.
5. **StrictMode double-mount guard is mandatory** for the Unicorn Studio init (useRef guard) — no duplicate canvases.
6. **lab() color strings must remain verbatim** in the CTA gradient + box-shadow. Do not convert to hex.
7. **CTA border-radius = 0** (sharp corners). No Tailwind rounded utility.

---

## Scope (explicit)

**In scope:** Navbar (logo wordmark + Resources ▾ + Book a demo → on desktop; brand + hamburger on mobile), Hero section (dark stone-900 bg + noise2.png tile + Unicorn Studio WebGL canvas + H1 + description + Book-a-demo CTA), Trust/logo marquee strip (8 logos, infinite scroll, noise3.png bg, onyx border).

**Out of scope:** "The Company Brain" two-column section and everything below it, footer, mobile menu open-state, nav-link hover styling (unless trivial), tablet-specific tuning, SEO/a11y deep work.

**Viewports:** 1440×1400 (primary), 1920×1200+ (large), 390×844 (mobile).

---

## Implementation Tasks (from builder_plan, accepted)

1. Scaffold Vite + React + Tailwind v4 in `hyperspell-clone/`. `vite.config.js` `base: '/hyperspell-clone/'`.
2. Self-host fonts: `exposure-regular.woff2` (H1) + `geist-500.woff2` (body/nav/CTA) via `@font-face` in `src/styles/globals.css`. If `exposure` is commercial/unavailable, use a documented closest-alt (Playfair Display / DM Serif Display) — but self-host the real woff2 first (already downloaded).
3. `Navbar.jsx` — sticky, transparent bg, no border-bottom, h=77px, wordmark `<img>` 128×32, Resources ▾ (Geist 14/400, tracking 0.7px, #D6D6D6) + Book a demo → on right. Mobile: brand + hamburger only.
4. `Hero.jsx` — section bg `#161010` + tiled noise2.png (120×120), `border-b border-onyx` (1px #171717), Unicorn Studio mount (`absolute inset-0`, z-0), content layer (z-10) with H1 + P + CTA. Guard Unicorn init against StrictMode double-mount.
5. `Button.jsx` — CTA 288×64 desktop (full-width on mobile), 1px solid #E9E9E9, border-radius 0, padding 16/32/14, bg = verbatim lab() gradient, box-shadow = verbatim lab() layers, text "Book a demo" (no arrow), Geist 24/400, color #E9E9E9, href `https://cal.com/conor-brennan-burke/30-minute`.
6. `LogoMarquee.jsx` — full-width strip, bg #161010 + noise3.png, border-b border-onyx, py-2, 8 logos (Eragon, Entelligence AI, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe) duplicated 2×, each cell 160×48 grayscale opacity-70, infinite left-scroll CSS keyframes ~30–40px/s, seamless loop.
7. `index.html` — load Unicorn Studio UMD `<script>` (deferred), `<title>Hyperspell - Your company brain</title>`.
8. `README.md` — run/deploy + CDN risk note + font-alt documentation.

## Build Validation (builder self-test before reporting done)

- `npm install` + `npm run build` succeed with no errors.
- `npm run dev` renders at `http://localhost:5173/hyperspell-clone/` with no console errors (no "UnicornStudio is not defined", no font/image 404).
- Builder screenshots the clone at 1440, 1920, 390 and eyeballs against the target screenshots in `team-log/screenshots/` before reporting done. (This is a self-render check, NOT the formal evaluation — the evaluator owns fidelity verdict.)
- Builder does NOT self-evaluate, does NOT write eval reports, does NOT judge pixel fidelity. Reports files changed + build/lint result.

---

## Testable Assertions (evaluator grades against these)

### Navigation (desktop 1440)
- N1: nav height 77px (±2)
- N2: nav sticky, transparent bg, no backdrop-blur, no border-bottom
- N3: brand `<a href="/">` with `<img>` 128×32 loading `/wordmark-light.svg`, alt="Logo"
- N4: "Resources" link (Geist 14/400, tracking 0.7px, #D6D6D6) + chevron SVG, right-aligned
- N5: "Book a demo →" link, same style, right-aligned

### Hero (desktop 1440)
- H1: hero section bg `#161010` + tiled noise2.png (120×120) + border-b 1px #171717
- H2: Unicorn Studio `<canvas>` present, fills hero, behind content (z-0), renders live morphing blob (not static)
- H3: H1 text exactly "A brain for your company." — `exposure` 400, tracking -3.84px, lh 70.4px, #D6D6D6, left-aligned, at x≈105 y≈157. **Responsive fontSize: 48px on mobile (<768px), 64px on md+ (≥768px)** — matches original's `text-[3rem]! md:text-[4rem]!`. lh stays 70.4px at both sizes.
- H4: description exactly "Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read." — Geist 30/400, -0.72px, 36px, #D6D6D6, x≈105 y≈252
- H5: CTA "Book a demo" (no arrow), 288×64, x≈105 y≈372, border-radius 0, 1px solid #E9E9E9, bg = verbatim lab() gradient, box-shadow = verbatim lab() layers, text #E9E9E9 Geist 24/400, padding 16/32/14, href to cal.com
- H6: content positioning matches original at 1920 (left-anchored OR centered — match whatever the original does; builder verifies)

### Trust marquee (desktop 1440)
- T1: strip bg #161010 + noise3.png, border-b 1px #171717, py-2, h≈97
- T2: all 8 logos present (Eragon, Entelligence AI, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe), 160×48, grayscale, opacity 0.7, no broken images
- T3: infinite seamless left-scroll, ~30–40px/s, no jump on loop

### Animation / video-level
- A1: Unicorn canvas produces a live morphing WebGL blob (frames differ over time) — not a static gradient or flat color
- A2: marquee scrolls continuously forever
- A3: no unrequested entrance stagger added (settled state at t≈2s matches original's settled state)

### Content (verbatim)
- C1: H1 = "A brain for your company."
- C2: description = "Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read."
- C3: CTA body = "Book a demo"
- C4: nav Resources = "Resources" + chevron
- C5: nav = "Book a demo →"
- C6: `<title>` = "Hyperspell - Your company brain"

### Responsive
- R1: 1440×1400 — full desktop matches
- R2: 1920×1200 — content positioning matches original (verified), canvas spans full width, no horizontal scroll
- R3: 390×844 — hamburger nav (brand + hamburger only, NO Resources/Book-a-demo links), H1 wraps to 2 lines ("A brain for your / company."), CTA full-width, no horizontal scroll

### Code-review (must not break)
- CR1: StrictMode double-mount guarded — exactly one Unicorn canvas init
- CR2: no `ml-[Npx]` / `left-[Npx]` centering anti-pattern
- CR3: lab() strings preserved verbatim (not converted to hex)
- CR4: CTA border-radius = 0
- CR5: fonts self-hosted (real woff2) or closest-alt documented
- CR6: noise overlays present (noise2 on hero, noise3 on trust)
- CR7: border-onyx dividers present

### Build
- B1: `npm run build` succeeds
- B2: no console errors on load
- B3: no horizontal scroll at 1440/1920/390

---

## Auto-Reject (any one = REJECT)

1. Hero canvas missing or static (no live WebGL blob)
2. H1 font not `exposure` and no documented closest-alt
3. CTA gradient lacks `lab(` strings (converted to hex)
4. CTA has rounded corners
5. Marquee missing any of the 8 logos or shows <5 visible
6. Mobile CTA not full-width
7. Mobile nav shows Resources + Book a demo (should be hamburger)
8. Noise overlay missing on hero or trust
9. border-onyx divider missing
10. H1 text ≠ "A brain for your company."
11. Console errors on load
12. StrictMode double-mount → two canvases
13. Hero content off by >5px at 1440
14. Fixed `ml-[Npx]`/`left-[Npx]` centering
15. Layout breaks at 1920 (horizontal scroll or content mispositioned)

---

## Pixel-diff thresholds (from adaptation memory)

- Text/chrome regions: RMSE ≤ 20
- Unicorn Studio WebGL shader region: RMSE ≤ 60 (irreducible GPU rasterization + subpixel AA noise floor — perfect pixel-match is mathematically unrealistic for live shaders)
- The evaluator MUST use these relaxed thresholds for the canvas region and report both the raw RMSE and the region classification.

---

## Process

1. Builder builds to this contract, self-tests (build + lint + dev render + eyeball vs target screenshots), reports done with files changed.
2. Evaluator runs adversarial eval against this contract, writes `team-log/eval_round_1.md` with PASS/FAIL per assertion, severity, evidence, file+line to fix.
3. Engineer sends failures to builder → builder fixes → evaluator re-verifies. Iterate until ACCEPT.
4. Only after evaluator ACCEPT: commit + push.
