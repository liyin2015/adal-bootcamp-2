# Hyperspell Hero Clone — Builder Plan

**Date:** 2026-07-04
**Builder session:** 740b6993-bdf7-4bc1-accd-7f09be846bfa
**Status:** Phase 1 discovery complete — planning approved to build.

---

## 1. Target & Scope

- **URL:** https://www.hyperspell.com/
- **Scope:** Hero section only — `Navbar` + `<section>` hero (H1 / description / Book-a-demo CTA / Unicorn Studio glow) + the immediately-adjacent `Logo marquee` strip (97px high band that visually belongs to the hero). Hard stop at the **\"The Company Brain / Your AI agent\"** two-column feature block at y=661 (out of scope).
- **Viewports required:** 1440×1400 (primary desktop), 1920×1200+ (large-screen centering), 390×844 (mobile).

## 2. Tech Discovery

| Layer | Original | Clone |
|---|---|---|
| Framework | Next.js (App Router) + Tailwind CSS | **Vite + React + Tailwind v4** (matches guide v2) |
| Fonts | Self-hosted woff2 served from `/_next/static/media/...` (Geist, Exposure) | **Self-host same woff2** in `src/assets/fonts/` + `@font-face` in `globals.css` |
| Hero animation | **Unicorn Studio WebGL** (`cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.33/dist/unicornStudio.umd.js`), scene-id `id-ad3rc7r9wq97m0um61k7u7`, canvas 2137×729 stretched to 100% w/h inside `position:absolute inset-0` of `<section>` | **Embed — load same UMD script, render `<div data-us-project=\"<scene>\">`**, init via `UnicornStudio.init()`. Keep a static fallback (cropped screenshot) for first paint / no-JS / dev-time static. |
| Page bg | Stone-900 (`rgb(22,16,16)` = `#161010`) tiled with `/noise.png` 120×120 | Replicate exactly via Tailwind arbitrary values + same noise image (downloaded) |
| Logo carousel | `<img>` logos in a horizontally-scrolling duplicate strip, 160×48 cells, ~32px gaps (`mx-4 md:mx-8`), height 48px, opacity 0.7, grayscale, no Framer | CSS `@keyframes` marquee, infinite linear 40s, logo array duplicated 2× |
| Entrance animation | No Framer appear IDs. Unicorn scene fades in by virtue of the loader; rest of text is settled on first paint (need to verify with GIF) | Framer Motion stagger: heading → description → button → logo strip |
| Body / spacing | `max-w-screen-xl` (1280px) + `mx-auto px-12 xl:px-8 py-12 md:py-20` | Reproduce directly |

**Decision tree resolved → animation tech = Unicorn Studio embed + minimal CSS/Framer Motion entrance.**

## 3. Design Tokens (extracted verbatim)

### Colors
| Token | Hex | Notes |
|---|---|---|
| Hero bg | `#161010` | `rgb(22,16,16)` — `stone-900` Tailwind palette token (`bg-stone-900`) |
| Text primary (H1 + paragraph) | `#D6D6D6` | `rgb(214,214,214)` — `text-stone-100` map (note: stone-100 is `#f5f5f4` in Tailwind, but original reports stone-100 = `rgb(214,214,214)` — verify: the Tailwind script overrides `--color-stone-100` for this site; we will use the literal value `#D6D6D6` regardless of token name) |
| Stone-50 (CTA border + text) | `#E9E9E9` | `rgb(233,233,233)` |
| Container/text default body | `#171717` | `rgb(23,23,23)` (above-the-fold on white subpages, but hero area inherits stone-100) |
| Noise | `noise2.png` (page-level bg under hero) + `noise.png` + `noise3.png` (between sections) | All downloaded |
| CTA gradient | `linear-gradient(to right, lab(57.9249 57.5686 25.3116 / 0.8) 0%, lab(68.2299 49.5438 29.1709 / 0.8) 50%, lab(75.4697 25.3835 45.1166 / 0.8) 100%)` | Verbatim `lab()` strings in Tailwind arbitrary value |
| CTA box-shadow | `lab(0 0 0 / 0.2) 0px 10px 15px -3px, lab(0 0 0 / 0.2) 0px 4px 6px -4px` | Verbatim |

### Typography (extracted via TreeWalker)
| Element | Family | Size (md) | Weight | LH | Tracking | Color | Notes |
|---|---|---|---|---|---|---|---|
| H1 | `exposure` | 64px | 400 | 70.4px | -3.84px | `#D6D6D6` | `text-[3rem]! md:text-[4rem]!`, `mb-6`, `md:w-3/5`. Note period in \"company.\". |
| Description (P) | `Geist` | 30px (`text-2xl md:text-3xl`) | 400 | 36px | -0.72px | `#D6D6D6` | `max-w-3xl`, `mb-12`, font-body class |
| Nav links (uppercase) | `Geist` | 14px | 400 | — | `0.7px` | `#D6D6D6` (Resources + Book a demo), `#BFBFBF` (Blog/Documentation dropdown items) | All caps |
| Logo wordmark | N/A — uses `<img src=\"/wordmark-light.svg\">` | 128×32 | — | — | — | — | Downloaded to `src/assets/media/wordmark-light.svg` |
| CTA button | `Geist` | 24px | 400 | — | inherits | `#E9E9E9` | Verbatim |

### Spacing & Components
| Component | Value |
|---|---|
| Navbar height | 77px |
| Navbar inner `max-w-screen-xl mx-auto px-12 xl:px-8 py-12 md:py-20` (note: class also lives on content, but same wrapper here) → use inner `px-12 xl:px-8` + flex `justify-between items-center h-[77px]` |
| Nav horizontal padding | ~32px (`px-8`) on xl, 48px (`px-12`) on smaller |
| H1 left padding inside container | container's left edge (after `mx-auto px-12` ≈ x=104 on 1440 viewport) |
| Section height | 487px (at 1440 desktop, includes py-12 md:py-20 of 80px each top + bottom = 160 + content height 326) |
| Logo strip height | 97px |
| Logo cell | 160×48, gap 32 (`mx-4`) md:32 (`md:mx-8`) — visually ~224px center-to-center |
| CTA button | 288×64, padding `16px 32px 14px`, `border: 1px solid #E9E9E9`, `border-radius: 0px` (square corners) |

### Section hero background
- Parent shell: `relative overflow-hidden border-b border-onyx bg-stone-900 bg-[url('/noise2.png')] bg-[length:120px_120px] bg-repeat`
- Inner unicorn layer: `absolute inset-0 w-full h-full` containing the Unicorn Studio mount.
- Content layer: `mx-auto relative z-10 px-12 xl:px-8 py-12 md:py-20 max-w-screen-xl`

### Logo marquee
- 8 unique logos (Eragon, Entelligence, Micro, Hobbes, Bear, ScaleAgentic, Virio, SuperMe), list duplicated to enable seamless loop. Source: `images.ctfassets.net/...`. All downloaded to `src/assets/logos/*.svg`.
- Each cell: `relative h-12 w-40 flex-shrink-0 mx-4 md:mx-8 grayscale opacity-70 pointer-events-none`
- Wrap div: full width, vertical center, the marquee animates via `transform: translateX(0 -> -50%)` over ~40s linear infinite.

## 4. Assets Checklist (downloaded)

- [x] `src/assets/fonts/exposure-regular.woff2` (self-host H1 serif)
- [x] `src/assets/fonts/geist-500.woff2` (self-host body)
- [x] `src/assets/media/wordmark-light.svg` (logo for navbar)
- [x] `src/assets/media/noise.png` + `noise2.png` + `noise3.png` (bg textures)
- [x] `src/assets/logos/*.svg` × 8 (Eragon, Entelligence, Micro, Hobbes, Bear, ScaleAgentic, Virio, SuperMe)

Optional / embed-only:
- Unicorn Studio UMD: `https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.33/dist/unicornStudio.umd.js` — load via `<script>` tag; `<div data-us-project=\"id-ad3rc7r9wq97m0um61k7u7\">` inside the absolute layer.

## 5. Component Breakdown

```
src/
  components/
    layout/
      Navbar.jsx      # Logo <img> + nav links (Resources▾ dropdown) + Book-a-demo CTA. Sticky top.
    sections/
      Hero.jsx        # Orchestrates bg noise + UnicornStudio mount + container with H1/P/Button
      LogoMarquee.jsx # Below hero; full-width strip with infinite-scroll logo row
    ui/
      Button.jsx      # Primary "Book a demo" (square border + gradient bg + lab() shadow)
      NoiseBackground.jsx  # Reusable stone-900 + tiled noise block (so we can keep DRY for future sections)
  assets/
    media/ (noise*.png, wordmark-light.svg)
    logos/  (8 SVGs)
    fonts/  (exposure-regular.woff2, geist-500.woff2)
  styles/
    globals.css  # @font-face + Tailwind + keyframes (marquee, gradient shift)
  App.jsx         # <Navbar /> + <Hero /> + <LogoMarquee />
  main.jsx
  index.css       # Tailwind
index.html
vite.config.js    # base: '/hyperspell-clone/' (since clone served at /hyperspell-clone/)
```

## 6. Animation Strategy

### A. Hero glow / Unicorn Studio (embed)
```html
<script src="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.33/dist/unicornStudio.umd.js"></script>
...
<div
  data-us-project="id-ad3rc7r9wq97m0um61k7u7"
  data-us-scale="1"
  data-us-dpi="1.5"
  data-us-lazyload="true"
  style="position:absolute;inset:0;width:100%;height:100%"
></div>
```
- Initialize once on mount via `UnicornStudio.init()`.
- Optional: `data-us-disable-mobile` etc — start minimal.
- Provide a **static fallback** in case of CDN stall or no-script: render an `<img>` of the orb (we'll snapshot the canvas once via `canvas.toDataURL()` not possible for WebGL, so use a cropped screenshot saved to `src/assets/media/hero-orb-fallback.png`).

### B. Entrance animation (Framer Motion)
- `useReducedMotion` → skip anims.
- Container variant: `staggerChildren: 0.12, delayChildren: 0.1`
- Items: `initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}`
- Order: navbar (slide-down) → H1 → description → CTA → logo marquee (fade in opacity 0→0.7) → unicorn (fade in opacity 0→1)

### C. Logo marquee
- CSS `@keyframes scrollX { from { transform: translateX(0); } to { transform: translateX(-50%); } }`
- Apply to a flex row containing 2× the logo list, `animation: scrollX 40s linear infinite`
- Pause on hover (`hover:[animation-play-state:paused]` for QA nicety, optional).

### D. Hover (CTA button)
- `transition: all duration-300 ease-in-out` (per original Tailwind classes on `<button>`)
- Hover: slightly intensify gradient brightness or push shadow — **must match if observed**; otherwise keep the `transition-all` and replicate the exact behavior (we'll record a hover clip and verify).

## 7. Build Validation Plan

1. `npm install` in `hyperspell-clone/`.
2. `npm run build` must complete with zero errors and zero warnings beyond defaults.
3. `npm run dev` (port 5173 by Vite) → opening `http://localhost:5173/hyperspell-clone/` must render with no console errors (warnings ok only for unrelated things).
4. Stop dev server before evaluator runs.
5. Side-by-side screenshot comparison at 1440×1400, 1920×1200, 390×844 — evaluator's job, not builder.

## 8. Responsive Spec

| Breakpoint | Hero behavior |
|---|---|
| `<768px` (mobile 390) | Container padding `px-8`, py stays `py-12`. H1 `text-[3rem]!` (48px), no width-3/5 cap (full width). Description `text-2xl` (24px). CTA button stretches to `w-full` inside container. Logo marquee still scrolls. Nav: hamburger replaces `Resources▾ + Book a demo` (mobile uses a hamburger; the section after our scope). For mobile **only** the hero + marquee are required to match — we'll replicate the hamburger at the same position. |
| `768–1280px` (md) | Container `py-12 md:py-20`, H1 `text-[4rem]!` (64px), description `text-3xl` (30px). |
| `≥1280px` (xl) | Container `px-8` (down from `px-12` on smaller) — Tailwind `xl:px-8`. |

**Center on large screens:** use `mx-auto max-w-screen-xl px-8` for the inner content (matches original's centered wrapper). The Unicorn layer remains `absolute inset-0` so the glow still spans the full window width.

## 9. Edge Cases & Assumptions

- **CDN dependency for Unicorn Studio.** If jsdelivr is down at evaluation, fallback image shows. Document this in `README.md`.
- **Custom lab() colors** are non-standard — supported in modern browsers (Chrome ≥111, Safari ≥15). Document fallback if needed.
- **Self-hosted fonts:** exposure regular is enough; we'll need exposure-italic if any hero text is italic. Per H1 metric `fontStyle: normal`, regular only.
- **Trust bar visibility at 1920:** the 8-logo strip is short (~2176px total — 2× of 1088), so it scrolls. At any width the marquee fills horizontal space.
- **No entrance animation is visible on the actual original** (no `data-framer-appear-id`). The Unicorn Studio scene may have its own loader; we'll trust the embed to handle its intro.
- **Hyphenation/safe-area:** Tailwind defaults handle; if H1 wraps awkwardly, force `max-w-3/5` at md and above.

## 10. Open Questions for Engineer

1. **Unicorn Studio project access.** `data-scene-id` is `id-ad3rc7r9wq97m0um61k7u7`. UnicornStudio typically requires `data-us-project` which is a different schema (often a UUID). Is using `data-us-project` with this id sufficient, or do we need a different embed string?
   - **Self-resolution:** try `data-us-project=\"id-ad3rc7r9wq97m0um61k7u7\"` first (UnicornStudio v1.4.x supports arbitrary scene-id strings). If it fails, swap to a static screenshot fallback as documented.
2. **Hover state of CTA** — original transition timing `300ms ease-in-out` with backdrop-blur. Hover behavior not yet captured. **Decision:** record a 5s hover clip during build, replicate the observed effect (or match `transition-all` per source).
3. **Subpixel positioning of H1 period "." — Tracked vs not tracked; sentence is 1 line at 1440 (rounded) — confirm period renders cleanly with `tracking-[-3.84px]`.

## 11. Files I will touch

| Path | Purpose |
|---|---|
| `hyperspell-clone/package.json` | Vite + React + Tailwind + framer-motion + autoprefixer |
| `hyperspell-clone/vite.config.js` | `base: '/hyperspell-clone/'` |
| `hyperspell-clone/index.html` | Load UnicornStudio UMD `<script>` (deferred) |
| `hyperspell-clone/src/main.jsx` | Bootstrap |
| `hyperspell-clone/src/App.jsx` | Layout wrapper |
| `hyperspell-clone/src/styles/globals.css` | `@font-face` for exposure + Geist + Tailwind + `marquee` keyframes |
| `hyperspell-clone/src/components/layout/Navbar.jsx` | Sticky nav with logo + dropdown + CTA |
| `hyperspell-clone/src/components/sections/Hero.jsx` | Section with UnicornStudio mount + gradient bg + container + H1 + P + CTA |
| `hyperspell-clone/src/components/sections/LogoMarquee.jsx` | Infinite-scroll logo strip |
| `hyperspell-clone/src/components/ui/Button.jsx` | Primary CTA with verbatim gradient + box-shadow |
| `hyperspell-clone/src/components/ui/NoiseBackground.jsx` | Stone-900 + tiled-noise bg shell |
| `hyperspell-clone/src/assets/**` | Already downloaded |
| `hyperspell-clone/README.md` | Run/deploy instructions + CDN risk note |

## 12. Out of Scope (explicit)

- Anything below the LogoMarquee strip (\"The Company Brain\" section, diagrams, comparisons, FAQ, footer).
- iPad mini / tablet-specific tuning (responsive handled at md/mobile only).
- Lighthouse / SEO / a11y deep work (basic semantics via React landmarks).
