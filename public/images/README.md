# Image assets needed

Drop the following files into this folder before launch. Filenames are referenced by the HTML / manifest / sitemap.

## Required
- `logo.png`             — 512×512, transparent PNG (Organization JSON-LD)
- `og-default.jpg`       — 1200×630, JPG (Open Graph / Twitter card fallback)
- `favicon.ico`          — 32×32 + 16×16 multi-res ICO (legacy browsers / Google snippet)
- `apple-touch-icon.png` — 180×180, PNG (iOS home-screen)
- `icon-192.png`         — 192×192, PNG (PWA manifest)
- `icon-512.png`         — 512×512, PNG (PWA manifest)

## Recommended (per page hero / cards)
- `hero-maine-coon.webp`        — 1600×1200, WebP, < 200 KB
- `hero-maine-coon@2x.webp`     — 3200×2400 (for retina `<source srcset>`)
- `kitten-{name}-{1..4}.webp`   — 1200×900 product/kitten gallery shots
- `product-{slug}.webp`         — 1200×1200 shop product images

## Standards
- Format priority: **AVIF → WebP → JPG fallback**
- All raster assets compressed via Squoosh or `cwebp -q 78`
- Every `<img>` already has descriptive `alt` text in the HTML — match it when shooting/sourcing photos
- Include `loading="lazy"` and explicit `width`/`height` to preserve CLS = 0
