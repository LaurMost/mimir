# Mimir — Brand

## Wordmark

The wordmark is set in **Berserker Regular** (the God of War display face).
The "M" glyph contains the embedded ᛗ (Mannaz) rune pattern, which doubles as
the standalone mark.

All SVG assets have the glyph paths embedded directly — they do not require
the font file at render time.

## Mark

The standalone mark is the **M from Berserker, isolated**. It is not a
separate symbol — the letterform itself is the rune. Use `logo.svg` for
transparent contexts, `logo-on-dark.svg` / `logo-on-light.svg` when you need
a contained version.

## Color tokens

| Token | Hex | Role |
|---|---|---|
| `--ink` | `#F2EBDD` | Primary fill on dark surfaces (bone-white) |
| `--ink-dark` | `#0B0B0D` | Primary fill on light surfaces |
| `--bg-dark` | `#0B0B0D` | Primary dark surface |
| `--bg-stone` | `#1A1714` | Warm dark stone for app icon canvas |
| `--bg-light` | `#F2EBDD` | Bone background for inverse contexts |

The palette is deliberately small: bone on stone. No accent color.
If a third color is ever needed (status badges, warnings), use system colors
for that surface — don't extend the brand palette.

## Typography pairings

- **Display / wordmark** — Berserker Regular (commercial use: confirm
  licensing if shipping it in a product)
- **Body / docs** — System serif (Georgia, New York, Times). Mimir's lore is
  pre-modern; sans-serif body type fights that.
- **Code / CLI** — JetBrains Mono or SF Mono

## Clear space

Reserve at least the height of one "I" stem around the wordmark on all sides.
The standalone mark needs at least 15% of its own bounding box as padding.

## What not to do

- Don't change the letter spacing of the wordmark — the proportions are tuned
- Don't add a stroke or outline to the mark
- Don't recolor the mark in anything other than the two tokens above
- Don't place the mark on a busy photographic background without a tinted
  overlay — it competes
- Don't rasterize the SVG for any size above 256px — re-render from the SVG

## File map

```
logo/
  logo.svg                       ← rune mark, transparent
  logo-on-dark.svg               ← rune on bg-dark
  logo-on-light.svg              ← inverse rune on bg-light
  logo-mono-dark.svg             ← dark-fill version (transparent)
  wordmark.svg                   ← MIMIR, transparent
  wordmark-on-dark.svg           ← MIMIR on bg-dark
  wordmark-dark.svg              ← MIMIR in ink-dark
  wordmark-stacked.svg           ← rune + MIMIR (vertical)
  wordmark-stacked-on-dark.svg

favicons/
  favicon.ico                    ← multi-resolution (16/32/48)
  favicon.svg                    ← modern browsers
  favicon-16.png, -32.png, -48.png
  apple-touch-icon.png           ← 180px, iOS home screen
  android-chrome-192.png, -512.png
  manifest.webmanifest

app-icon/
  icon-1024.svg                  ← master with macOS squircle baked in
  icon-1024.png
  Mimir.iconset/                 ← all macOS sizes (1x + 2x)
  build-icns.sh                  ← run on macOS to produce Mimir.icns

og/
  og-image-1200x630.png          ← OG / Twitter link preview
  social-preview-1280x640.png    ← GitHub Settings → Social preview
  twitter-card-1200x600.png
  readme-hero-2400x600.png       ← placeholder until DALL-E version
  (matching .svg sources)
```
