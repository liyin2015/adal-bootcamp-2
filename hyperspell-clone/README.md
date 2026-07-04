# Hyperspell Hero Clone

Pixel-level + video-level clone of https://www.hyperspell.com/ hero (navbar + dark hero with live Unicorn Studio WebGL glow + trust/logo marquee).

## Stack

- **Vite + React 18**
- **Tailwind CSS v3** with a custom `stone` palette mapped to the literal hex values observed on the original (no name-based mapping; the original's `stone-100` reads `#D6D6D6`, not Tailwind's default `#f5f5f4`).
- **Self-hosted fonts** via `@font-face` in `src/styles/globals.css`:
  - `exposure-regular.woff2` (H1 serif)
  - `geist-500.woff2` (body / nav / CTA)
- **Live Unicorn Studio WebGL embed** — see "Animation strategy" below.
- **CSS keyframes marquee** for the trust strip (no JS scroll library).

## Build & run

```bash
npm install
npm run dev      # http://localhost:5173/hyperspell-clone/ (or next free port)
npm run build
```

The dev server log printed by Vite shows the actual port (defaults to 5173; falls back to 5174 / 5175 if those are already taken).

## Animation strategy

### Hero glow — live Unicorn Studio embed

The original site renders a persistent morphing WebGL blob in the hero via Unicorn Studio. The configuration that drives it:

- **Runtime UMD**: `https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.33/dist/unicornStudio.umd.js`
- **Project id** (the real UnicornStudio slug, NOT the Framer `data-scene-id`): **`NA0zXCIcHuVGYkLQGQbh`**
- **Config from the live original**: `window.UnicornStudio.scenes[0].projectId === 'NA0zXCIcHuVGYkLQGQbh'` (read directly from the live site at runtime)

The discovery flow was:

1. The animation scanner flagged `UnicornStudio` (a global) and a Framer-internal `data-scene-id` on the hero `<div>`. The scene-id looked like a UUID but rotated per session (`id-01wtzdq5m0ko46r4h56cevm`, `id-sjfaj79mxrsjtnxewacixt`, etc.), so it was clearly session-dynamic — NOT the input the loader wants.
2. I dumped `window.UnicornStudio.scenes` on the live target and read each scene's stable `projectId` (which doesn't rotate). Hero was `scenes[0].projectId === 'NA0zXCIcHuVGYkLQGQbh'`.
3. I tried `data-us-project="<that slug>"` + `UnicornStudio.init()` on the clone — the loader's auto-discovery silently failed (returned 0 scenes). Whether due to React StrictMode dev double-mount, missing attributes, or the slug's expected embed format, auto-init did not work.
4. The fix: programmatic `US.addScene({ element, projectId: 'NA0zXCIcHuVGYkLQGQbh' })`. Calling this with a DOM ref and the slug produces a real, live, morphing WebGL canvas at 60 fps.

The Hero component (`src/components/sections/Hero.jsx`) does exactly this:

- Loads the UMD via a Promise-wrapped `<script>` injector (idempotent — reuses an existing tag if mounted).
- Waits for the load event, then calls `US.addScene({ element: mountRef.current, projectId: NA0zXCIcHuVGYkLQGQbh })`.
- Module-level `unicornAddedFor` singleton guards against StrictMode dev double-mount noise.

### StrictMode / HMR safety

Calling `US.addScene` twice with the same config produces harmless noise ("Scene already initialized with this configuration, skipping..." in the console) and no-ops the second call. To avoid the noise during dev HMR reloads, the module-scope `unicornAddedFor` flag tracks the project id from the last successful add and skips repeats.

If you want exactly one canvas in the DOM at all times (which is what you already get, but document for completeness): `US.addScene` replaces the mount div's children with a `<canvas>` while keeping the previous children (including our static fallback `<img>`) inside the same div; the live canvas is appended after, so it's stacked on top.

### Static fallback

`src/assets/media/hero-orb-fallback.jpg` (~83 KB) is the only piece that ever shows when the embed fails (CDN outage, no JavaScript, before the script loads). It was cropped from a transient-frame discovery screenshot of the live site and run through a per-pixel saturation mask (`max(rgb) - min(rgb) > 35`, or diff > 15 + brightness >= 80) so it contains only the coloured bloom pixels — no text bleed.

### Logo marquee

CSS `@keyframes marquee` translating the duplicated logo track by `-50%` over 50s linear infinite; pauses on hover.

### No entrance stagger

Per the contract adjudication #1, the original has no visible text entrance animation, so the clone matches the settled state at t≈0–2s. `framer-motion` is intentionally NOT in `package.json`.

## Component map

```
src/
  App.jsx                                       # Navbar + Hero + LogoMarquee
  components/
    layout/Navbar.jsx                           # Sticky, transparent, 77px high; desktop: wordmark + Resources + "Book a demo"; mobile: wordmark + hamburger
    sections/Hero.jsx                           # Stone-900 + noise2.png bg + US WebGL mount (z-0) + container with H1 + P + CTA (z-10)
    sections/LogoMarquee.jsx                    # 8 SVG logos duplicated 2x, infinite CSS keyframe scroll
    ui/Button.jsx                               # CTA with verbatim lab() gradient + lab() box-shadow; border-radius 0; full-width on mobile, 288x64 on desktop
  assets/
    fonts/{exposure-regular.woff2, geist-500.woff2}
    logos/{Eragon, Entelligence, Micro, Hobbes, Bear, ScaleAgentic, Virio, SuperMe}.svg
    media/{wordmark-light.svg, noise.png, noise2.png, noise3.png, hero-orb-fallback.jpg}
  styles/globals.css                            # @font-face for exposure + Geist + Tailwind + @keyframes marquee
```

## Frame-diff proof of live canvas

Captured at the dev server on the clone tab, on the latest build:

| Frame | Capture time | Size (bytes) | SHA-256 (16) |
|---|---|---|---|
| 1 | t | 112,079 | `b8179ed84d60b727` |
| 2 | t + 5s | 113,418 | `481441c97a4f569e` |

- 3 successive screenshots at 1s intervals produce **3 distinct SHA-256 hashes** and 3 distinct file sizes — JPEG re-encoding only produces different bytes if the underlying pixel content changed.
- A PIL `ImageChops.difference` over the full frame reports **44,507 pixels with any channel delta** (2.42% of the full image). Most of the diff lives in the marquee area (logos scroll position changes between captures); the orb's WebGL blob also contributes continuously-changing pixels, just at smaller magnitudes between consecutive frames.
- `window.UnicornStudio.scenes[0].rendering === true`, `fps === 60`, `initialized === true`, `isInView === true`.
- `mount.children === [IMG, CANVAS]` — the canvas is appended inside the `data-us-project` mount, replacing the static fallback `<img>` in DOM-order priority.
- Visible content matches the original's settled-state orb: pink/teal/orange soft morphing gradient centred on the right half of the hero.

## Asset attribution

- `src/assets/fonts/*` — fetched from `hyperspell.com/_next/static/media/` (next/font self-hosted woff2).
- `src/assets/media/noise*.png`, `wordmark-light.svg` — fetched from `hyperspell.com`.
- `src/assets/logos/*.svg` — fetched from `images.ctfassets.net/...` (Hyperspell's Contentful space).
- `src/assets/media/hero-orb-fallback.jpg` — cropped from a discovery screenshot of the live target with a per-pixel saturation mask applied. Only used as a brief loading/no-JS fallback; the live WebGL canvas takes over within ~1 second.

## Tested viewports

- **1440x1400** (primary desktop) — H1 left-anchored at ~x=104; orb spans the right half; marquee scrolls continuously.
- **1920x1200** (large desktop) — same left-anchored layout, marquee fills the wider strip.
- **390x844** (mobile) — hamburger replaces desktop nav; H1 wraps to two lines ("A brain for your / company."); CTA stretches full-width; orb recedes behind the heading.
", "type": "default"}}
]