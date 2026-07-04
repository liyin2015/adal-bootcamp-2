# Test Plan — Hyperspell Hero Clone (Adversarial Evaluation)

**Evaluator:** this worker (session `05d10109-d953-4f12-b98f-5b552f4f4d11`)
**Builder session:** `740b6993-bdf7-4bc1-accd-7f09be846bfa`
**Target URL:** https://www.hyperspell.com/
**Scope:** Hero section only — `<nav>` + dark hero section + trust/logo marquee. Hero ends where the next section (\"The Company Brain\") begins.
**Viewports required:** 1440×1400 (primary), 1920×1200+ (large), 390×844 (mobile).

---

## 0. Ground Truth (extracted from live target — session 05d10109)

### 0.1 Layout geometry (1440 desktop, settled)

| Element | x | y | w | h | Notes |
|---|---|---|---|---|---|
| `<nav>` | 0 | 0 | 1425 | 77 | sticky, transparent bg, no border-bottom |
| Brand `<a href=\"/\">` | 73 | 28 | 128 | 20 | contains `<img src=\"/wordmark-light.svg\" width=\"128\" height=\"32\">` |
| `Resources ▾` (nav link) | 1089 | 28 | 107 | 20 | Geist 14px, letter-spacing 0.7px, color `rgb(214,214,214)`, with chevron SVG `w-3 h-3` |
| `Book a demo →` (nav link) | 1228 | 28 | 124 | 20 | same style as Resources, with `→` glyph |
| Hero `<section>` | 0 | 77 | 1425 | 487 | bg `rgb(22, 16, 16)` (stone-900) + tiled noise2.png (240×240) at 120px; `border-b border-onyx` (1px) |
| H1 | 105 | 157 | 730 | 70 | text \"A brain for your company.\" — `exposure` 64/400, letter-spacing -3.84px, line-height 70.4px, color `rgb(214,214,214)` |
| Description `<p>` | 105 | 252 | 768 | 72 | \"Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read.\" — Geist 30/400, -0.72px, 36px, `rgb(214,214,214)` |
| CTA `Book a demo` | 105 | 372 | 288 | 64 | 24px Geist, letter-spacing -0.72px, color `rgb(233,233,233)`, **bg `linear-gradient(to right, lab(57.92 57.57 25.31/0.8) 0%, lab(68.23 49.54 29.17/0.8) 50%, lab(75.47 25.38 45.12/0.8) 100%)`**, 1px solid `rgb(233,233,233)`, padding 16/32/14, border-radius 0, box-shadow (3 lab(0 0 0 / 0.2) layers) |
| Trust marquee strip | 0 | 565 | 1425 | 97 | bg `rgb(22,16,16)` + noise3.png, `border-b border-onyx`, `py-2`, infinite-scroll logos (each 160×48 cell, ~64px gap) |
| Unicorn Studio canvas (hero) | 0 | 77 | 1425 | 486 | scene id `id-<dynamic>` (e.g. `id-jqugmrgh3sdhrgtwp8vgw`), pixel size 2137×729 rendered at 1425×486 |

**Hero bottom = y 564 + trust strip bottom = y 662.** Hero scope ends at y=662.

### 0.2 Mobile layout (390 viewport)

| Element | x | y | w | h | Notes |
|---|---|---|---|---|---|
| `<nav>` | 0 | 0 | ~390 | 77 | brand left, hamburger right (24×24, three 4-px stroke lines) |
| Brand | 32 | 30 | 128 | 20 | same wordmark image |
| Hamburger button | 366 (right) | 28 | 24 | 24 | aria-label likely \"Open menu\" or similar |
| Hero `<section>` | 0 | 77 | full | larger (vertically wraps to ~2x) | same dark bg + noise |
| H1 | 48 | 129 | 389 | 106 | wraps to **2 lines** (\"A brain for your / company.\") — font-size likely 40–48px (computed at this breakpoint) |
| Description `<p>` | 48 | ~270 | ~389 | ~120 | wraps to ~3 lines |
| CTA `Book a demo` | 48 | 403 | 389 | 64 | **full-width** on mobile (not 288px) |
| Trust marquee | 0 | below CTA | full | 97 | unchanged |
| Unicorn Studio canvas | full | hero area | full | hero h | smaller blob, less prominent |

**Critical mobile rules:**
- Brand + hamburger only (Resources + Book a demo collapsed into hamburger menu)
- H1 wraps to 2 lines
- CTA becomes full-width

### 0.3 Fonts

| Family | Weights | Source | Loaded by |
|---|---|---|---|
| `exposure` (display serif — looks like a high-contrast didone) | 400 (regular), 400 italic | Commercial — not on Google Fonts | hyperspell.com via Framer (CSS `@font-face`) |
| `Geist` (sans) | 400, 500, 600 | Vercel — not on Google Fonts | hyperspell.com via Framer |

**Builder must self-host these or use a documented closest-alt.** The `exposure` "Fallback" shim in `getComputedStyle` is a Framer placeholder — the real font is loaded by `@font-face`. Same for `Geist Fallback`. `document.fonts` shows `exposure` weight 400 as **loaded** on the live site.

### 0.4 Colors (exact)

| Token | Value | Source |
|---|---|---|
| Page background (above hero) | `rgb(255,255,255)` | body |
| Hero section background | `rgb(22, 16, 16)` | Tailwind `bg-stone-900` |
| Trust strip background | `rgb(22, 16, 16)` | same as hero |
| Border between hero and trust, and below trust | `border-onyx` = `rgb(23, 23, 23)`, 1px | Tailwind token |
| H1 / desc text | `rgb(214, 214, 214)` | --color-text or literal |
| CTA text | `rgb(233, 233, 233)` | lighter than H1 |
| CTA border | `rgb(233, 233, 233)` 1px | matches CTA text |
| CTA background | `linear-gradient(to right, lab(57.92 57.57 25.31 / 0.8) 0%, lab(68.23 49.54 29.17 / 0.8) 50%, lab(75.47 25.38 45.12 / 0.8) 100%)` | a coral/salmon-to-amber gradient with alpha 0.8 — keep lab() strings verbatim in arbitrary value |
| Nav link text | `rgb(214, 214, 214)` | matches H1 |
| Nav "Book a demo →" | underlined? — check (likely subtle hover) | Framer default |
| Noise overlay | `noise2.png` (hero) / `noise3.png` (trust) | 240×240 tiled at `bg-[length:120px_120px]` |

**Trust marquee logo colors** (extracted SVG names — assume all logos are SVG on a dark bg → light/white strokes or fills). Logos in order: **Eragon, Entelligence AI, micro, HOBBES, Bear, ScaleAgentic, virio, SuperMe** (8 logos confirmed from network, marquee loops infinitely).

### 0.5 Animation tech

| Stack element | Result |
|---|---|
| `<canvas>` WebGL | **YES** — Unicorn Studio runtime (https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.33/dist/unicornStudio.umd.js) |
| `window.UnicornStudio.init` | exists |
| `data-scene-id` (Framer-managed) | `id-jqugmrgh3sdhrgtwp8vgw` for hero (changes per session) |
| `data-us-project` (legacy) | null on this site — uses Framer-native init |
| CSS `@keyframes` | 0 detected |
| Framer entrance animations | Likely — Framer Motion not detected on window, but Framer site uses its own built-in scroll/appear animations |
| gsap / three / lottie / rive / spline / pixi | none |
| Inline `<video>` | none |
| SMIL SVG | none |

**Entrance animation observed (settled-state vs early frames from entrance GIF):**
- The Unicorn Studio canvas renders the **abstract noise/glow blob** in the right-half of the hero. The blob is dynamic and morphs over time. The blob is not pre-rendered; it's a live WebGL shader.
- No text fades, no stagger animation visible within the first 6s of capture. The H1, desc, CTA, nav appear immediately (or the page was past the entrance).
- Trust marquee scrolls left at a constant rate.

**Trust marquee animation:**
- Horizontal scroll, infinite loop. Speed not measured precisely — appears ~30-40 px/sec.
- 8 logos × (160w + 64gap) = 1792px per cycle; the strip is 1425px wide.

### 0.6 Extracted assets

| Asset | URL | Status |
|---|---|---|
| Wordmark logo | `/wordmark-light.svg` (577×91 viewBox) | fetched — full SVG available |
| Hero noise | `/noise2.png` (240×240 RGBA) | fetched — 240×240 tile |
| Trust noise | `/noise3.png` (240×240 RGBA) | fetched — 240×240 tile |
| Trust logos (8×) | `https://images.ctfassets.net/j1of1zsvj8cu/...` (Contentful CDN) | URLs known — Eragon, Entelligence, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe |
| Unicorn Studio hero scene | `id-<dynamic>` per session | builder should call `UnicornStudio.init()` programmatically with the scene-id, OR embed the same div `data-scene-id` and load the runtime script |

---

## 1. Visual Fidelity Matrix (Element-by-Element Assertions)

All measurements must match within **±2px** on x/y/w/h unless otherwise stated. All hex/rgb/lab values must be **byte-exact**.

### 1.1 Navigation bar (1440 viewport)

| # | Element | Assertion | Pass condition |
|---|---|---|---|
| N1 | nav height | 77px (±2) | `getBoundingClientRect().height` |
| N2 | nav position | sticky top, z-index above hero content | `getComputedStyle.nav.position === 'sticky'` |
| N3 | nav bg | transparent (lets dark hero show through), no backdrop-blur | `backgroundColor === 'rgba(0, 0, 0, 0)'` and no `backdrop-filter` |
| N4 | nav bottom border | none | no `border-bottom` |
| N5 | brand anchor | `<a href=\"/\">` at x=73 y=28, contains `<img>` 128×32 loading `/wordmark-light.svg` | measure and src check |
| N6 | wordmark src | exactly `/wordmark-light.svg` (or absolute `https://www.hyperspell.com/wordmark-light.svg`) | DOM inspection |
| N7 | Resources link | text \"Resources ▾\" at x=1089 y=28, font Geist 14/400, letter-spacing 0.7px, color `rgb(214,214,214)` | text + computed style |
| N8 | Book a demo (nav) | text \"Book a demo →\" at x=1228 y=28, same style as Resources | text + computed style |
| N9 | Resources chevron | inline SVG `w-3 h-3` stroke-only, path `M3 4.5 6 7.5 9 4.5` | DOM check |
| N10 | nav link right alignment | nav links cluster to right (Resources + Book a demo both on right side) | visual |

### 1.2 Hero section (1440 viewport)

| # | Element | Assertion | Pass condition |
|---|---|---|---|
| H1 | hero section rect | y=77, h=487, w=full | measure |
| H2 | hero bg | `rgb(22, 16, 16)` solid + tiled noise2.png at 120×120 | computed + bg image |
| H3 | hero bottom border | 1px `rgb(23,23,23)` (onyx) | `borderBottomWidth === '1px'` and `borderBottomColor` |
| H4 | content wrapper | `mx-auto max-w-screen-xl px-12 py-12 md:py-20` Tailwind classes | DOM check |
| H5 | Unicorn canvas | `<div data-scene-id=\"…\">` containing `<canvas>` filling 1425×486 at y=77 | exists, scene-id non-empty |
| H6 | canvas z-index | behind content (canvas has lower z, or content has higher z) | `z-index` or DOM order |
| H7 | H1 text | exactly \"A brain for your company.\" (capital A, period at end) | textContent |
| H8 | H1 position | x=105 (±2), y=157 (±2), w=730 (±4), h=70 (±4) | measure |
| H9 | H1 font | `exposure` (or alt), size 64px, weight 400, letter-spacing -3.84px, line-height 70.4px, color `rgb(214,214,214)` | computed style |
| H10 | H1 alignment | left-aligned (not center) | computed `text-align` |
| H11 | description text | exactly \"Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read.\" | textContent |
| H12 | description position | x=105, y=252, w=768, h=72 (±2) | measure |
| H13 | description font | Geist 30/400, -0.72px, 36px, `rgb(214,214,214)` | computed style |
| H14 | description alignment | left | text-align |
| H15 | CTA text | exactly \"Book a demo\" (no `→` on the body CTA — only on nav) | textContent |
| H16 | CTA position | x=105, y=372, w=288, h=64 (±2) | measure |
| H17 | CTA bg | linear-gradient `to right, lab(57.92 57.57 25.31 / 0.8) 0%, lab(68.23 49.54 29.17 / 0.8) 50%, lab(75.47 25.38 45.12 / 0.8) 100%)` — **lab() strings must be kept verbatim** | computed backgroundImage |
| H18 | CTA border | 1px solid `rgb(233, 233, 233)` | computed |
| H19 | CTA text color | `rgb(233, 233, 233)`, Geist 24/400, -0.72px | computed |
| H20 | CTA padding | 16px top / 32px sides / 14px bottom (16 32 14) | computed padding |
| H21 | CTA border-radius | 0px (sharp corners — not rounded!) | computed |
| H22 | CTA box-shadow | 5+ layer string including `lab(0 0 0 / 0.2) 0px 10px 15px -3px, lab(0 0 0 / 0.2) 0px 4px 6px -4px` | computed box-shadow |
| H23 | CTA href | `https://cal.com/conor-brennan-burke/30-minute` | href attr |

### 1.3 Trust marquee (1440 viewport)

| # | Element | Assertion | Pass condition |
|---|---|---|---|
| T1 | strip rect | x=0, y=565, w=full, h=97 | measure |
| T2 | strip bg | `rgb(22, 16, 16)` + tiled noise3.png at 120×120 | computed |
| T3 | strip border-bottom | 1px `rgb(23,23,23)` (onyx) | computed |
| T4 | strip padding | py-2 (8px top/bottom) | computed padding |
| T5 | logo count visible | 5 logos visible at any moment at 1440w (matches screenshot) | DOM count |
| T6 | logo set | Eragon, Entelligence AI, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe (8 distinct, then loops) | src URLs |
| T7 | each logo | 160×48, SVG format (from Contentful CDN or local copy) | img natural size + tag |
| T8 | marquee animation | continuous left-scroll, no jump on loop, speed ~30-40px/s | visual + animation timing |
| T9 | logo color treatment | logos appear light/white on dark bg (inverted, not original brand colors) | visual |
| T10 | logo loading | all 8 logos load successfully (no broken `<img>`) | naturalWidth > 0 |

### 1.4 Unicorn Studio WebGL canvas (1440)

| # | Element | Assertion | Pass condition |
|---|---|---|---|
| U1 | canvas present | `<canvas>` inside hero, fills 1425×486 | exists |
| U2 | canvas pixel size | ≥ 1900px wide on retina (e.g. 2137 or 2857) for sharpness | `canvas.width` |
| U3 | script loaded | `https://cdn.jsdelivr.net/gh/hiunicornstudio/.../unicornStudio.umd.js` in DOM | script tag |
| U4 | `UnicornStudio.init` called | `window.UnicornStudio` exists, hero scene initialized | `typeof UnicornStudio.init === 'function'` |
| U5 | data-scene-id present | non-empty `data-scene-id` attr on canvas wrapper | DOM check |
| U6 | StrictMode guard | if React StrictMode is on, canvas is initialized exactly once (no duplicate `addScene` calls) | code review + console check |
| U7 | visible blob | hero shows colored noise/glow blob in right half (NOT a static gradient — must animate) | visual |
| U8 | noise overlay still visible | tiled noise2.png is visible over the dark bg, even where canvas is | visual |

---

## 2. Animation Verification Plan

| # | Animation | What to verify | How |
|---|---|---|---|
| A1 | Hero entrance (text) | Nav + H1 + desc + CTA visible at t=0 (or fade in within ~300ms — verify with builder what's promised) | record 5s on load, look for fades |
| A2 | Trust marquee loop | Scrolls left, no visible jump, ~5 logos visible at any time at 1440w, no pause on hover, speed steady | record 8s, scrub |
| A3 | Unicorn canvas render | Live WebGL — produces morphing/noise blob, NOT a static gradient | visual confirm frames differ frame-to-frame |
| A4 | CTA hover | likely a subtle lift/glow on hover — record the hover state at the 2 viewports | hover + screenshot |
| A5 | Nav link hover | underline or color shift on Resources/Book a demo hover | hover + screenshot |
| A6 | Resources dropdown | if builder implements the menu, must match the Blog + Documentation links | open menu + screenshot |
| A7 | Hamburger menu (mobile) | if builder implements, must open a sheet/overlay with Resources + Book a demo | tap + screenshot |
| A8 | Scroll behavior | nav becomes sticky with dark backdrop (or stays transparent) — verify against original | scroll + screenshot |

**Build rule:** the builder may promise **entrance text animations are minimal/instant** if the original has no visible stagger. The clone's settled state at t=2s must match the target's settled state at t=2s. The marquee and canvas must keep animating forever.

---

## 3. Content Exactness Checks (verbatim)

| # | String | Source | Must be |
|---|---|---|---|
| C1 | brand alt | `<img alt=\"Logo\">` | `Logo` (capital L) |
| C2 | H1 | `<h1>` | `A brain for your company.` |
| C3 | description | `<p>` | `Hyperspell connects your tools, builds a context graph, and surfaces it as a filesystem any agent can read.` |
| C4 | CTA body | button | `Book a demo` (no arrow) |
| C5 | nav \"Resources\" | link | `Resources` (with chevron) |
| C6 | nav \"Book a demo →\" | link | `Book a demo →` (with `→` glyph) |
| C7 | document title | `<title>` | `Hyperspell - Your company brain` (or similar) |

---

## 4. Design-Token Assertions (file-level)

The clone must define tokens that match. A `tailwind.config.js` (or CSS vars) must have at minimum:

```js
// Required
stone-900: '#161010'  // hero bg
onyx: '#171717'       // border
text-primary: 'rgb(214, 214, 214)'  // H1, desc, nav links
text-cta: 'rgb(233, 233, 233)'      // CTA text/border

// Required font families
fontFamily: {
  display: ['exposure', 'serif'],
  sans: ['Geist', 'system-ui', 'sans-serif'],
}

// Required spacing
container max-w: 1280px (max-w-screen-xl)
px-12 (48px) horizontal padding in hero content wrapper
py-12 mobile, py-20 desktop
```

If the builder uses a Google Fonts **closest-alt** for `exposure`, document it. Likely candidates: `Playfair Display`, `DM Serif Display`, `Cormorant Garamond`. Visual mismatch > 4px on cap-height = failure.

If `Geist` is replaced, candidates: `Inter`, `Manrope`. Visual mismatch = failure.

---

## 5. Responsive Edge Cases

| # | Viewport | What to check |
|---|---|---|
| R1 | 1440×1400 | full desktop (H1 left, canvas blob right, marquee 5 logos) |
| R2 | 1920×1200 | hero content stays at x=105 (left-aligned, NOT centered to 1920w) — verify with screenshot diff. Canvas spans full width. |
| R3 | 390×844 | hamburger menu, H1 wraps to 2 lines, CTA becomes full-width, smaller canvas blob |
| R4 | 768×1024 (tablet) — out of scope but should not break | verify no horizontal scroll, layout sane |
| R5 | 2400×1200 (ultra-wide) | hero content stays at x=105 (left-aligned), canvas spans full width, no horizontal overflow |

---

## 6. Code-Review Risks (the things that always break)

| # | Risk | What to look for |
|---|---|---|
| CR1 | **StrictMode double-mount on Unicorn Studio** | If the Builder uses React 18 + StrictMode, `useEffect` runs twice. The Unicorn Studio runtime's `addScene` may double-register → console warnings, broken canvas, or two scenes stacked. **Builder must guard** with a `useRef` or a `if (initRef.current) return;` check. |
| CR2 | **Fixed-margin centering** instead of `max-w-[…] mx-auto` | Anti-pattern from §3 of guide. Check: no `ml-[Npx]` or `left-[Npx]` magic numbers. Use `max-w-screen-xl mx-auto px-12`. |
| CR3 | **Wrong font self-hosting** | If builder uses Google Fonts `Playfair Display` for `exposure` and doesn't document it, that's a silent failure. Check the loaded font name via `getComputedStyle(h1).fontFamily` and verify it matches. |
| CR4 | **CTA border-radius wrong** | Original has `0px` (sharp corners). If builder uses Tailwind `rounded-md` or `rounded-lg`, instant fail. |
| CR5 | **CTA gradient simplified to hex** | The `lab(…)` values must remain `lab(…)` strings in the clone. If builder converts to `#E0…` hex, the salmon-amber gradient will look noticeably different. |
| CR6 | **Trust logos are not SVG / not from CDN** | If builder uses placeholder rectangles, the marquee will look empty. Verify the 8 logo URLs are reachable or the SVGs are saved locally. |
| CR7 | **Marquee speed wrong** | If marquee scrolls too fast or jitters, fails A2. |
| CR8 | **Missing noise overlay** | The dark hero bg without `noise2.png` looks flat / too clean. The original has visible film-grain noise. |
| CR9 | **Missing `border-onyx`** between hero and trust strip, or between trust and next section. |
| CR10 | **H1 font-weight wrong** | If builder sets `font-semibold` (600) instead of `font-normal` (400) for `exposure`, the H1 will look too heavy. |
| CR11 | **Mobile: H1 wraps to wrong line** | Original wraps \"A brain for your / company.\" If builder uses different font size, may wrap to \"A brain for / your company.\" — fail. |
| CR12 | **Mobile: CTA not full-width** | Original: 389px wide on 390 viewport. If builder keeps the desktop 288px width, fail. |
| CR13 | **Mobile: nav still shows Resources + Book a demo** | Should be brand + hamburger only. |
| CR14 | **Canvas not initialized on mount** | If builder forgets to call `UnicornStudio.init()` after the runtime script loads, hero is just black. |
| CR15 | **Hero content covered by canvas** | Canvas should be z-0 or have `z-0` while content is `z-10`. If reversed, text disappears. |

---

## 7. What Would PROVE the Clone BROKEN

Any **one** of these = automatic REJECT:

1. **Hero canvas missing or static** — no WebGL blob in the right half of the hero.
2. **H1 font is not exposure** and the builder has not documented a closest-alt with a visible fidelity match.
3. **CTA gradient does not contain `lab(` strings** (e.g. converted to hex or simplified to plain color).
4. **CTA has rounded corners** (border-radius > 0).
5. **Trust marquee shows fewer than 5 logos or missing one of {Eragon, Entelligence, micro, HOBBES, Bear, ScaleAgentic, Virio, SuperMe}**.
6. **Mobile CTA is not full-width** (i.e. keeps 288px desktop width).
7. **Mobile nav shows Resources + Book a demo instead of hamburger**.
8. **Noise overlay missing on hero or trust strip** (looks like a flat solid color).
9. **`border-onyx` divider missing** between hero and trust strip.
10. **H1 text differs from `A brain for your company.`** (extra space, missing period, wrong punctuation).
11. **Console errors on load** (`UnicornStudio is not defined`, font 404, image 404).
12. **StrictMode double-mount causes two canvases** stacked.
13. **Hero content positioned wrong by more than 5px** at 1440 viewport (H1 not at x=105, CTA not at x=105 y=372).
14. **Layout uses `ml-[Npx]` or fixed `left-[Npx]`** (centering anti-pattern from §3 of guide).
15. **Layout breaks at 1920 viewport** — content doesn't extend with the canvas, or extra horizontal scrollbar appears.

---

## 8. Acceptance Criteria (the final pass/fail)

The clone **PASSES** iff:

- **A.** All 23 hero assertions in §1.2 pass within ±2px / byte-exact.
- **B.** All 10 nav assertions in §1.1 pass.
- **C.** All 10 trust marquee assertions in §1.3 pass.
- **D.** All 8 canvas assertions in §1.4 pass.
- **E.** Animation A2 (marquee) + A3 (canvas) verified running.
- **F.** All 7 content exactness strings in §3 match verbatim.
- **G.** All 3 viewport responsive edge cases in §5 verified.
- **H.** No code-review risks from §6 (especially CR1, CR2, CR5, CR11, CR12).
- **I.** `npm run build` succeeds, no console errors on load, no horizontal scroll at any of 1440/1920/390.

The clone **FAILS** (REJECT) on any of the 15 conditions in §7.

---

## 9. Evidence to be Captured at Evaluation Time

When the builder reports done, the evaluator will:

1. Open clone at `http://localhost:5173/hyperspell-clone/` in a fresh tab.
2. Open `https://www.hyperspell.com/` in a separate tab.
3. For each viewport (1440, 1920, 390), screenshot BOTH and run `javascript_tool` to extract the same tokens measured above.
4. Compute diffs (x, y, w, h ± px; colors byte-exact; text verbatim).
5. Re-record the entrance GIF on the clone, side-by-side with the target GIF in `screenshots/target-entrance-animation.gif`.
6. Open console on clone, verify no errors and no double canvas mount.
7. Write `team-log/eval_round_1.md` with: PASS/FAIL per assertion, severity (BLOCKER / MAJOR / MINOR), evidence (screenshot path + measurement), and the file+line to fix.
8. Iterate: send failures to builder → builder fixes → evaluator re-runs.

**Reference screenshots saved:**
- `team-log/screenshots/target-desktop-1440-settled.jpeg` (canvas glow visible)
- `team-log/screenshots/target-desktop-1440-midmarquee.jpeg` (mid-marquee, no glow)
- `team-log/screenshots/target-desktop-1920.jpeg` (large viewport)
- `team-log/screenshots/target-mobile-390.jpeg` (mobile, hamburger)
- `team-log/screenshots/target-entrance-animation.gif` (7 frames over ~8s)

---

## 10. Out-of-Scope (for completeness)

- The \"Company Brain\" two-column section below the trust strip.
- The \"Adaptive Memory\" grid further down.
- Any footer or bottom-of-page content.
- The mobile menu open state (verify Resources dropdown, hamburger open state is **NOT** required to match — only the closed state must).
- Hover states for nav links (out of scope unless trivially implemented).
