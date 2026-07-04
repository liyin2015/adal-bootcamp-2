# Evaluation Round 1 — Hyperspell Hero Clone

**Evaluator session:** `05d10109-d953-4f12-b98f-5b552f4f4d11` (MiniMax-M3, browser-use)
**Clone URL:** `http://localhost:5175/hyperspell-clone/`
**Target URL:** `https://www.hyperspell.com/`
**Date:** 2026-07-04
**Verdict:** ❌ **REJECT** — 1 BLOCKER + 1 MAJOR + 3 MINOR failures. See §10.

---

## 1. Methodology & measurement conditions

- Live DOM measurement via `javascript_tool` on both target (tab 4) and clone (tabs 8/9/10).
- Side-by-side screenshots at desktop viewports; raw bytes diff'd (visual RMSE estimated by region classification).
- Build verified via `npm run build` in `hyperspell-clone/`.
- Console errors captured via `read_console_messages` after a fresh navigate.

### Viewport caveat (read first)
- The browser's CDP-driven `resize_window` is unreliable above ~1309px and cannot go below ~1309px on this host (locked by the host window manager).
- All target measurements are taken at the target's 1440 inner viewport.
- All clone measurements are taken at the clone's effective inner viewport (mostly 1309×1162). The clone DOES scale correctly: same `max-w-screen-xl mx-auto px-12` centering as the target, so the relative horizontal positions match within the 9% width delta.
- For 1920, the clone was tested at 1317×617 (closest reachable). No horizontal scroll at either width.
- For 390 mobile, the browser resize was blocked at 1309. Mobile behavior was verified via the source code (Tailwind `md:hidden` / `md:flex` breakpoints) and via `window.matchMedia('(min-width: 768px)').matches === true` at 1309 (correctly showing desktop nav).

### Pixel-diff methodology
- Used visual RMSE estimated from the captured screenshots (no ImageMagick available; diffs done by agent's vision).
- Region classification: text/chrome (H1, desc, CTA, nav, marquee text) vs Unicorn shader canvas region.
- Thresholds per contract: text/chrome ≤ 20, shader ≤ 60.

---

## 2. Evidence inventory

| Screenshot | Path | What it shows |
|---|---|---|
| `eval1-clone-desktop-1309.jpeg` | team-log/screenshots/ | Clone at 1309×1162 settled state — H1 clearly smaller than target |
| `eval1-clone-desktop-1309-marquee-scrolled.jpeg` | team-log/screenshots/ | Clone ~5s later — marquee scrolled, H1 still too small |
| `eval1-clone-large-1317.jpeg` | team-log/screenshots/ | Clone at 1317 (closest to 1920) — no horizontal scroll |
| `eval1-clone-narrow-454.jpeg` | team-log/screenshots/ | Clone at the previously-locked narrow viewport (mobile behavior) |
| `target-desktop-1440-settled.jpeg` | team-log/screenshots/ | Target reference |
| `target-desktop-1920.jpeg` | team-log/screenshots/ | Target reference at 1920 |

---

## 3. Geometry comparison table (clone 1309 vs target 1440)

| Element | Target (1440) | Clone (1309) | Delta | Within ±2px? |
|---|---|---|---|---|
| nav: x, y, w, h | 0, 0, 1425, 77 | 0, 0, 1309, 77 | viewport-scaled | ✓ h=77 exact |
| nav: position, bg, border-bottom | sticky / rgba(0,0,0,0) / 0 | sticky / rgba(0,0,0,0) / 0 | match | ✓ |
| brand: x, y, w, h | 73, 28, 128, 20 | 47, 23, 128, 32 | x: -26 (scaled), y: **-5** | ✗ y=23 vs 28 (5px) |
| wordmark src | `/wordmark-light.svg` | imported asset | n/a | ✓ |
| Resources link: x, y, w, h | 1089, 28, 107, 20 | 982, 28, 111, 21 | viewport-scaled | ✓ y=28 exact |
| Book a demo → link: x, y, w, h | 1228, 28, 124, 20 | 1140, 28, 122, 21 | viewport-scaled | ✓ y=28 exact |
| hero section: x, y, w, h | 0, 77, 1425, 487 | 0, 77, 1309, 487 | viewport-scaled | ✓ y=77, h=487 exact |
| hero bg | `rgb(22, 16, 16)` | `rgb(22, 16, 16)` | exact | ✓ |
| hero bg-image | `/noise2.png` tile 120×120 | `/noise2.png` tile 120×120 | exact | ✓ |
| hero border-bottom | 1px `rgb(52, 47, 45)` | 0.91px `rgb(23, 23, 23)` | **color off** | ✗ (see CR7 below) |
| H1: x, y, w, h | 105, 157, 730, 70 | 47, 157, 730, 70 | viewport-scaled x; y, w, h exact | ✓ position |
| **H1: fontSize** | **64px** | **48px** | **-16px (25% smaller)** | **✗ BLOCKER** |
| H1: fontWeight | 400 | 400 | match | ✓ |
| H1: letterSpacing | -3.84px | -3.84px | exact | ✓ |
| H1: lineHeight | 70.4px | 70.4px | exact | ✓ |
| H1: color | rgb(214, 214, 214) | rgb(214, 214, 214) | exact | ✓ |
| H1: text | "A brain for your company." | "A brain for your company." | exact | ✓ |
| desc: x, y, w, h | 105, 252, 768, 72 | 47, 251, 768, 72 | -1px y | ✓ within ±2 |
| desc: fontSize / weight / lh / ls | 30/400/36/-0.72 | 30/400/36/-0.72 | exact | ✓ |
| desc: color | rgb(214, 214, 214) | rgb(214, 214, 214) | exact | ✓ |
| desc: text | "Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read." | identical | exact | ✓ |
| CTA: x, y, w, h | 105, 372, 288, 64 | 47, 371, 288, 64 | -1px y | ✓ |
| CTA: padding | 16 32 14 | 16 32 14 | exact | ✓ |
| CTA: border | 1px solid rgb(233, 233, 233) | 0.91px solid rgb(233, 233, 233) | subpixel (1px) | ✓ |
| CTA: border-radius | 0px | 0px | exact | ✓ |
| CTA: color | rgb(233, 233, 233) | rgb(233, 233, 233) | exact | ✓ |
| CTA: fontSize | 24px | 24px | exact | ✓ |
| CTA: bg gradient | `linear-gradient(to right, lab(57.9249 57.5686 25.3116 / 0.8) 0%, lab(68.2299 49.5438 29.1709 / 0.8) 50%, lab(75.4697 25.3835 45.1166 / 0.8) 100%)` | identical string | exact | ✓ |
| CTA: box-shadow | `rgba(0,0,0,0) 0px 0px 0px 0px` ×4, `lab(0 0 0 / 0.2) 0px 10px 15px -3px`, `lab(0 0 0 / 0.2) 0px 4px 6px -4px` | identical string | exact | ✓ |
| CTA: href | (button, no href — target uses button) | `https://cal.com/conor-brennan-burke/30-minute` | n/a (clone uses `<a>`, target uses `<button>`) | ✓ (both reach booking) |
| canvas: w×h pixels | 2137×729 | 2618×972 | larger on clone (HiDPI) | ✓ (live) |
| canvas: rect (x, y, w, h) | 0, 77, 1425, 486 | 0, 77, 1309, 486 | viewport-scaled | ✓ |
| canvas: aria-label | "Scene" | "Unicorn Studio Scene" | descriptive | ✓ |
| canvas: behind content? | yes (z lower) | yes (parent z-auto, content z-10) | match | ✓ |
| trust strip: x, y, w, h | 0, 565, 1425, 97 | 0, 564, 1309, 65 | **h: -32 (33% shorter)** | **✗ MAJOR** |
| trust strip: bg | rgb(22, 16, 16) | rgb(22, 16, 16) | exact | ✓ |
| trust strip: bg-image | `/noise3.png` | `/noise3.png` | exact | ✓ |
| trust strip: padding | 8px 0px | 8px 0px | exact | ✓ |
| trust strip: border-bottom | 1px rgb(52, 47, 45) | 0.91px rgb(23, 23, 23) | color off | ✗ same as hero |
| logos: count in DOM | 16 (8 unique × 2 for marquee loop) | 16 | match | ✓ |
| logos: all loaded? | yes | yes (16/16) | match | ✓ |
| logos: grayscale + opacity 0.7 | yes | yes | match | ✓ |
| logos: cell size | 160×48 | 160×48 | exact | ✓ |
| title | "Hyperspell - Your company brain" | (n/a — measured via React Helmet equivalent, title in index.html) | n/a | ✓ |
| horizontal scroll at 1309 | no | no (scrollWidth=clientWidth=1309) | n/a | ✓ |

---

## 4. Animation verification

| Check | Result | Evidence |
|---|---|---|
| A1: Canvas is LIVE (not static) | ✓ PASS | `getContext('webgl2') === true`; sample1 vs sample2 base64 differ across 2s wait. Canvas morphs. |
| A2: Marquee scrolls continuously | ✓ PASS (with caveat) | Transform `-675.963` → `-1286.11` over the elapsed measurement interval. Animation `playState: running`. Marquee 50s linear infinite on a 3584px track = ~35.8 px/s, within 30-40 spec. |
| A3: No unrequested entrance stagger | ✓ PASS | No Framer Motion, no `animate-*` Tailwind classes. Text is fully visible at t=0 (no fade-in/slide-up). |
| A4: marquee seamless loop (no jump) | ✓ PASS (architecturally) | Track is `[...logos, ...logos]` (16 cells = 2 full sets); keyframes `0% → 100% translate3d(-50%, 0, 0)` produces a perfect loop. |
| StrictMode: exactly 1 canvas init | ✓ PASS CR1 | `canvasCount: 1`, `unicornSceneCount: 1`, no "Scene already initialized" console messages after fresh load. Module-level `unicornAddedFor` singleton guard works. |

---

## 5. Per-assertion grading (contract)

### Navigation (desktop 1440)
| # | Assertion | Result | Evidence |
|---|---|---|---|
| N1 | nav height 77px | ✅ PASS | `getBoundingClientRect().height === 77` |
| N2 | nav sticky / transparent / no border | ✅ PASS | `position: sticky`, `bg: rgba(0,0,0,0)`, `border-bottom: 0` |
| N3 | brand `<a href="/">` + `<img>` 128×32, src wordmark | ⚠️ MINOR | `<img width=128 height=32 src={wordmark}>` ✓ but image y=23 vs target y=28 (5px) — see MINOR-3 |
| N4 | Resources link (Geist 14/400, tracking 0.7px, #D6D6D6) + chevron | ✅ PASS | `uppercase font-body text-[14px] font-normal tracking-[0.7px] text-stone-100`; chevron SVG path `M3 4.5 6 7.5 9 4.5` matches |
| N5 | Book a demo → link, same style | ✅ PASS | `Book a demo →`, right-aligned, same Geist 14/400 |

### Hero (desktop 1440)
| # | Assertion | Result | Evidence |
|---|---|---|---|
| H1 | bg #161010 + noise2 + border-b 1px | ⚠️ MINOR | bg and noise ✓, but border color `rgb(23,23,23)` ≠ target `rgb(52,47,45)` — see MINOR-2 |
| H2 | Unicorn canvas live, fills hero, behind content | ✅ PASS | 1 canvas, 1309×486, parent `position: absolute; z-index: auto`, content sibling `z-10` |
| H3 | H1 text "A brain for your company." + exposure 64/400, -3.84px, lh 70.4, #D6D6D6, left-aligned, x≈105 y≈157 | ❌ **BLOCKER** | text ✓, fontFamily `exposure, serif` ✓, weight 400 ✓, letter-spacing -3.84px ✓, lineHeight 70.4px ✓, color #D6D6D6 ✓, position x=47 y=157 (scaled) ✓ — BUT **fontSize: 48px ≠ 64px target** |
| H4 | desc text + Geist 30/400, -0.72px, 36, #D6D6D6, x≈105 y≈252 | ✅ PASS | All values match exactly; position x=47 y=251 (scaled, -1px y) |
| H5 | CTA "Book a demo" 288×64, x≈105 y≈372, border-radius 0, 1px solid #E9E9E9, lab() gradient, lab() box-shadow, text #E9E9E9, Geist 24, padding 16/32/14, href to cal.com | ✅ PASS | All token-exact. `backgroundImage` string contains `lab(` ×3; `boxShadow` string contains `lab(` ×2. href to cal.com ✓. |
| H6 | content positioning matches original at 1920 (left-anchored, max-w-screen-xl + px-12) | ✅ PASS | At 1317 (closest to 1920) — content at x=44, canvas spans full width, no horizontal scroll. Layout uses `max-w-screen-xl mx-auto px-12` which is the same pattern the target uses (not a `ml-[Npx]` magic number). |

### Trust marquee
| # | Assertion | Result | Evidence |
|---|---|---|---|
| T1 | strip bg #161010 + noise3 + border-b 1px + py-2 + h≈97 | ❌ **MAJOR** | bg ✓, noise ✓, border-b color ✗ (MINOR-2), padding `8px 0` (py-2) ✓, **h=65 vs target h=97 (-32px / -33%)** |
| T2 | 8 logos present (Eragon, Entelligence AI, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe), 160×48, grayscale, opacity 0.7, no broken | ✅ PASS | 16 imgs in DOM (8 unique × 2 for loop), all naturalWidth > 0, all 8 names in correct order, `grayscale opacity-70` class |
| T3 | seamless infinite left-scroll, ~30–40px/s | ✅ PASS | 50s × linear × infinite, -50% on 3584px track = ~35.8 px/s, transform progresses over time, no jump on loop |

### Animation / video-level
| # | Assertion | Result |
|---|---|---|
| A1 | Unicorn canvas produces live morphing WebGL blob | ✅ PASS |
| A2 | marquee scrolls continuously forever | ✅ PASS |
| A3 | no unrequested entrance stagger | ✅ PASS |

### Content (verbatim)
| # | Assertion | Result |
|---|---|---|
| C1 | H1 = "A brain for your company." | ✅ PASS |
| C2 | desc = "Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read." | ✅ PASS |
| C3 | CTA body = "Book a demo" | ✅ PASS |
| C4 | nav Resources = "Resources" + chevron | ✅ PASS |
| C5 | nav = "Book a demo →" | ✅ PASS |
| C6 | `<title>` = "Hyperspell - Your company brain" | ✅ PASS (in index.html) |

### Responsive
| # | Viewport | Result |
|---|---|---|
| R1 | 1440×1400 | ⚠️ H1 size wrong (BLOCKER H3) |
| R2 | 1920×1200 | ✅ PASS — at 1317 (closest reachable), no horizontal scroll, canvas spans full width, content at x=44 (left-anchored, scaled from x=105 at 1440) |
| R3 | 390×844 | ⚠️ **Cannot physically test** at 390 — browser resize locked at 1309px min. Code review of Navbar.jsx and Button.jsx shows the responsive logic IS implemented correctly: `<div className="hidden md:flex">` (desktop nav) + `<button className="md:hidden" aria-label="Open menu">` (hamburger) + Button has `w-full md:w-[288px]`. At 1309, `matchMedia('(min-width: 768px)').matches === true` so desktop nav shows and hamburger hides — correct. At <768 the inverse would apply. This is a verification gap, not a code defect. |

### Code-review
| # | Risk | Result |
|---|---|---|
| CR1 | StrictMode double-mount | ✅ PASS — 1 canvas; no console errors |
| CR2 | no `ml-[Npx]` / `left-[Npx]` | ✅ PASS — uses `max-w-screen-xl mx-auto px-12` |
| CR3 | lab() strings preserved verbatim | ✅ PASS — confirmed in Button.jsx + computed style |
| CR4 | CTA border-radius 0 | ✅ PASS — `0px` |
| CR5 | fonts self-hosted | ✅ PASS — `exposure-regular.woff2` (68.56 kB) + `geist-500.woff2` (13.34 kB); `document.fonts` status: loaded for both |
| CR6 | noise overlays present | ✅ PASS — noise2 on hero, noise3 on trust, both tiled 120×120 |
| CR7 | border-onyx dividers | ⚠️ **MINOR** — dividers present (0.91px ≈ 1px) but **color is `rgb(23,23,23)` (#171717) instead of the target's `rgb(52,47,45)`** (a warmer brown that matches the stone palette better). Update `tailwind.config.js` `onyx` value. |

### Build
| # | Assertion | Result |
|---|---|---|
| B1 | `npm run build` succeeds | ✅ PASS — 47 modules, 392ms, no errors, no warnings |
| B2 | no console errors on load | ✅ PASS — only Vite HMR + React DevTools INFO messages, no errors or warnings |
| B3 | no horizontal scroll at 1440/1920/390 | ✅ PASS at 1309, 1317 (closest reachable) |

---

## 6. Pixel-diff (estimated, by region)

| Region | Threshold | Estimated RMSE | Within threshold? | Notes |
|---|---|---|---|---|
| Nav text (Resources, Book a demo) | ≤ 20 | ~6 | ✅ | Font + position match |
| Brand wordmark | ≤ 20 | ~10 | ✅ | y-offset 5px, 32px-tall wordmark |
| H1 text | ≤ 20 | **~50** | ❌ | 25% size mismatch: 48px vs 64px → glyph heights differ by 16px; cap-height diff of ~11px exceeds threshold for the entire H1 region (~730×70px) |
| Description text | ≤ 20 | ~6 | ✅ | Token-exact match |
| CTA (gradient + text + border) | ≤ 20 | ~10 | ✅ | All tokens match; only minor subpixel rounding on border at non-1440 viewport |
| Marquee text/logos | ≤ 20 | ~25 | ❌ | Logos are crammed at top of 65px-tall strip vs target's 97px; visible vertical position offset of ~16px on the logo cells |
| Trust strip background + noise | ≤ 20 | ~8 | ✅ | bg + noise + border-b width match |
| **Unicorn shader region** | ≤ 60 | ~55 | ⚠️ within shader threshold | Both render a live WebGL noise/glow blob, but the **clone's orb covers nearly the full hero** while the target's is a smaller right-half cluster. Different scene composition → high RMSE inside the shader region, but the contract allows ≤60 for shaders. Position match: canvas fills hero on both, both at z behind content. |
| Hero content area (excluding shader) | ≤ 20 | ~22 | ⚠️ marginal | H1 glyph-height difference drives most of the error here |

The H1 and marquee-strip regions drive the bulk of the visual divergence. Everything else is within threshold.

---

## 7. Failure summary (with severity)

### BLOCKER
- **B-1 — H3 H1 fontSize wrong** (Hero.jsx:87). The H1 is rendered at 48px, not 64px. The original `exposure` typeface at 64px is the visual anchor of the hero — at 48px the headline reads as a body-weight sub-headline, the descender of the H1 doesn't fill the 70.4px line-height (visible empty space inside the 730px H1 box), and the visual hierarchy inverts (the 30px description appears larger than the 48px H1). This is **auto-reject trigger #2** ("H1 font not `exposure` 64px and no documented closest-alt").
  - **Fix:** `src/components/sections/Hero.jsx` line 87: change `fontSize: '48px'` to `fontSize: '64px'`. The line-height is already 70.4px so the layout will settle correctly.

### MAJOR
- **M-1 — T1 Trust strip height 65px vs target 97px** (LogoMarquee.jsx:35). The strip uses `py-2` (8 top + 8 bottom = 16) + 48 logo + 1px border = 65. The target uses ~24 top + 24 bottom + 48 logo + 1px border = 97. The logos are crammed at the top of the strip with no breathing room above or below. Visually, the trust strip is noticeably shorter than the original.
  - **Fix:** `src/components/sections/LogoMarquee.jsx` line 35: change `py-2` to `py-6` (Tailwind = 24px top + 24px bottom = 48px padding + 48 logo = 96 ≈ target 97). Re-verify in DOM after fix.

### MINOR
- **m-1 — Brand wordmark y=23 vs target y=28** (Navbar.jsx:38). The clone uses `items-center` on a 77px nav containing a 32px-tall wordmark → centers at y=22.5 (rounded 23). The target places the wordmark at y=28 (top-anchored, leaving 12px breathing room above). 5px offset is visible at 100% zoom.
  - **Fix:** `src/components/layout/Navbar.jsx` line 38: change `items-center` to `items-start` (and add `pt-[28px]` or similar to the brand anchor) so the wordmark top edge sits at y=28 like the nav links.

- **m-2 — Border-onyx color mismatch** (tailwind.config.js:17 + the global `border-onyx` class). The clone uses `#171717` (`rgb(23,23,23)`) for the hero/trust dividers. The target uses `rgb(52, 47, 45)` (a warmer brown). The 1px line is hard to detect at normal zoom but visible at 200%. This is the actual onyx/stone color Framer uses.
  - **Fix:** `tailwind.config.js` line 17: change `onyx: '#171717'` to `onyx: '#342F2D'` (the value extracted from the live site). This will cascade to the `border-onyx` class on `<section>` and `.marquee-strip`.

- **m-3 — H1 trailing empty space (visual consequence of B-1)**. Because the H1 box is 730px wide but the text inside renders at 48px (not 64px), the text occupies ~540px of the 730px box — leaving ~190px of empty space on the right edge of the H1. Will be automatically fixed by the B-1 fix.

---

## 8. Auto-reject trigger check

| # | Trigger | Triggered? | Notes |
|---|---|---|---|
| 1 | Hero canvas missing or static | ❌ no | Live WebGL2 canvas renders; pixel samples differ over time |
| 2 | H1 font not exposure 64 AND no documented alt | ❌ **YES** (partial) | font IS exposure, BUT size is 48 not 64. Contract specifies the exact size in H3. **TRIGGERED.** |
| 3 | CTA gradient lacks `lab(` | ❌ no | `lab(` ×3 verbatim |
| 4 | CTA has rounded corners | ❌ no | 0px |
| 5 | Marquee missing any of 8 logos or <5 visible | ❌ no | 8 unique × 2 in DOM, 5+ visible at 1309w |
| 6 | Mobile CTA not full-width | ❌ no | code: `w-full md:w-[288px]` (correct) |
| 7 | Mobile nav shows Resources + Book a demo | ❌ no | code: `hidden md:flex` (correct; could not physically test) |
| 8 | Noise overlay missing on hero or trust | ❌ no | both present |
| 9 | border-onyx divider missing | ❌ no | present (color slightly off — see MINOR m-2) |
| 10 | H1 text ≠ "A brain for your company." | ❌ no | exact |
| 11 | Console errors on load | ❌ no | clean |
| 12 | StrictMode double-mount → 2 canvases | ❌ no | 1 canvas |
| 13 | Hero content off by >5px at 1440 | ❌ no | all within ±2px (after viewport scaling) |
| 14 | Fixed `ml-[Npx]` / `left-[Npx]` | ❌ no | uses `max-w-screen-xl mx-auto px-12` |
| 15 | Layout breaks at 1920 | ❌ no | no horizontal scroll at 1317 |

**Net auto-reject triggers fired: 1** (Trigger #2 — H1 size).

---

## 9. Code-review summary (clean, no defects found in code)

- `Hero.jsx`: H1 style is otherwise correct (font-weight 400, letter-spacing -3.84px, line-height 70.4px, color, font-family exposure). The ONLY defect is the fontSize literal `'48px'`. Fix is a one-character change.
- `Button.jsx`: lab() strings preserved verbatim, no rounded utilities, padding matches contract, href to cal.com.
- `LogoMarquee.jsx`: 8 unique logos in correct order, duplicated for seamless loop, grayscale + opacity 0.7, marquee 50s linear infinite on 3584px track = ~36px/s. The defect is `py-2` instead of `py-6` on the strip.
- `Navbar.jsx`: nav h=77, sticky, transparent. Resources as `<button>` (correct, target uses button). Book a demo as `<a>` to cal.com (correct, contract specifies href). Hamburger is `md:hidden` (correct).
- `main.jsx`: React.StrictMode wraps App, but the Unicorn Studio `addScene` is module-level-guarded with `unicornAddedFor` — CR1 PASS verified empirically.
- `tailwind.config.js`: `onyx: '#171717'` should be `#342F2D` per live site extraction (MINOR).
- `globals.css`: `@font-face` for exposure + Geist, marquee keyframes correct, 50s/0→-50% is the right loop math.
- `package.json`: vite 5.4.21, tailwind installed. Build clean.

---

## 10. Final verdict

**❌ REJECT — 1 BLOCKER (H1 fontSize) + 1 MAJOR (trust strip height) + 3 MINOR (brand y-offset, border-onyx color, H1 trailing-empty visual).**

**Rationale:** The clone's structural foundation is genuinely solid — fonts are correctly self-hosted, the CTA matches byte-exact including the rare `lab()` color strings, the Unicorn Studio WebGL is live with proper StrictMode guarding, the marquee is geometrically and chromatically correct with 8 logos in the right order scrolling at the spec'd speed, and the layout correctly uses `max-w-screen-xl mx-auto px-12` (no centering anti-pattern). But the H1 — the most visually dominant element of the hero — is rendered at 48px instead of the contract's 64px, a 25% size mismatch that inverts the visual hierarchy (the 30px description now reads larger than the H1) and leaves visible empty space in the 730px H1 box. This is auto-reject trigger #2. The trust strip is also 33% shorter than the target, making the logos visibly cramped. These two issues are one-line fixes each (`Hero.jsx:87` fontSize 48→64 and `LogoMarquee.jsx:35` py-2→py-6). Once fixed, re-run this evaluation and the clone should pass with at most the 3 MINORs remaining.

**Files + lines to fix:**

| Sev | File | Line | Current | Fix |
|---|---|---|---|---|
| BLOCKER | `src/components/sections/Hero.jsx` | 87 | `fontSize: '48px'` | `fontSize: '64px'` |
| MAJOR | `src/components/sections/LogoMarquee.jsx` | 35 | `py-2` | `py-6` |
| MINOR | `src/components/layout/Navbar.jsx` | 38 | `items-center` (on inner div) + `<img className="w-[128px] h-8">` | Add `pt-[28px]` to the brand anchor OR change `items-center` to `items-start pt-[28px]` |
| MINOR | `tailwind.config.js` | 17 | `onyx: '#171717'` | `onyx: '#342F2D'` |
| MINOR | (consequence of B-1) | — | — | auto-fixed when H1 size is corrected |

**Next steps for builder:** apply the 4 edits, then report back. Evaluator will re-run round 2.
