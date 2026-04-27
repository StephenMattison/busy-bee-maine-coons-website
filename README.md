# Busy Bee Maine Coons — busybeemainecoons.com

Premier digital platform connecting buyers with ethical, health-tested Maine Coon breeders, plus a curated store of giant-breed-specific products.

## Source-of-truth documents

All work on this site **must** strictly follow these files:

1. [BUSY-BEE-BUSINESS-PLAN.md](BUSY-BEE-BUSINESS-PLAN.md) — partnerships, revenue model, growth roadmap.
2. [BUSY-BEE-DESIGN.md](BUSY-BEE-DESIGN.md) — brand, palette, typography, navigation, page structure.
3. [BUSY-BEE-BLOG-POST.md](BUSY-BEE-BLOG-POST.md) — required template for every blog post.
4. [SITE-GUIDE.md](SITE-GUIDE.md) — universal WCAG 2.2 AA, security, and SEO standards.

## Project structure

```
.
├── BUSY-BEE-*.md           # business / design / blog source-of-truth
├── SITE-GUIDE.md           # universal site standard
├── README.md
└── public/                 # ← Cloudflare Pages build output directory
    ├── index.html          # Home
    ├── kittens.html        # Available Kittens
    ├── the-breed.html      # The Breed
    ├── care.html           # Care Guides
    ├── stories.html        # Coon Cat Stories (blog)
    ├── community.html
    ├── tools.html          # Useful Tools
    ├── shop.html
    ├── about.html
    ├── contact.html
    ├── cart.html
    ├── account.html
    ├── privacy.html
    ├── terms.html
    ├── accessibility.html
    ├── ethics.html         # Ethical breeding & health-testing standards
    ├── css/style.css
    ├── js/{script,cart,newsletter}.js
    ├── images/             # (add assets here)
    ├── functions/api/      # Cloudflare Pages Functions
    ├── _headers            # Security + caching headers
    ├── _redirects          # Apex/clean-URL redirects
    ├── robots.txt
    └── sitemap.xml
```

## Cloudflare Pages deployment

| Setting                  | Value     |
|--------------------------|-----------|
| Build command            | *(blank)* |
| Build output directory   | `public`  |
| Root directory           | `/`       |
| Production branch        | `main`    |

This matches the Network-wide standard for static sites (every site uses `public/` so the workflow stays identical across the network).

## Local preview

```bash
cd public && python3 -m http.server 8080
# → http://localhost:8080
```

## Quality gates (must pass before launch)

- Lighthouse 100/100 across Performance, Accessibility, Best Practices, SEO
- WCAG 2.2 AA (manual keyboard + screen-reader pass)
- A+ on SSL Labs, SecurityHeaders.com, Mozilla Observatory
- Zero broken links, valid sitemap submitted to Google Search Console
- All schema validates in Google Rich Results Test
