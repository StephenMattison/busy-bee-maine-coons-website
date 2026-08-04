# Busy Bee Maine Coons — agent instructions

You are working in **one** website repo. Push only to this remote.

- **GitHub:** `StephenMattison/busy-bee-maine-coons-website` (`origin`)
- **Branch:** usually `main`
- **After every meaningful change:** commit and push here only

## Hosting (production)

- **Host:** Cloudflare Pages (static)
- **Pages project:** `busy-bee-maine-coons-website`
- **Live site:** https://cooncatcentral.com
- **Canonical domain:** `https://cooncatcentral.com` (set in `_build.py` as `SITE`)
- **Legacy / brand domain:** busybeemainecoons.com may be marketing name only; do **not** use it as live canonical unless DNS is pointed here
- **What ships:** everything under `public/` (HTML, CSS, JS, images, `_headers`, `_redirects`, sitemap, robots, `llms.txt`)
- **Deploy path:** `git push origin main` → Pages auto-build (~1–3 min). Verify **live** `cooncatcentral.com` after push
- **Wrangler CLI:** optional for this static site; use for Pages Functions/Workers only. Auth notes: `~/.grok/rules/deploy-and-auth.md`

## Binding standards

1. Follow **`SITE-GUIDE.md`** in this repo root (copy of canonical `StephenMattison/site-guide`).
2. Always-on digest: Grok rules `site-guide-core`. **Open `SITE-GUIDE.md`** for a11y, SEO, security, Google Reviews, performance, cache-busting, or new UI.
3. **Never edit** `SITE-GUIDE.md` here. Edit canonical site-guide, then run `./sync-guide.sh`.
4. Brand / product docs (content only; SITE-GUIDE still wins on a11y/SEO/security):
   - `BUSY-BEE-BUSINESS-PLAN.md`
   - `BUSY-BEE-DESIGN.md`
   - `BUSY-BEE-BLOG-POST.md` (template for stories/articles)

## Layout

| Path | Role |
|------|------|
| `_build.py` | **Source of truth** for shared chrome + page bodies; regenerates `public/*.html` |
| `public/` | Live static output (Cloudflare Pages root) |
| `public/css/style.css` | Shared CSS |
| `public/js/*.js` | Shared JS (`script.js` = chrome + reviews + filters) |
| `public/images/` | Assets (prefer `kittens/`, `cats/`, `review/` — no spaces in paths) |
| `functions/api/` | Cloudflare Pages Functions (repo root; e.g. newsletter) |
| `public/_headers`, `_redirects` | Edge headers / redirects |
| `public/llms.txt` | Mandatory agent discovery file |
| `scripts/check-site-guide-compliance.py` | Title/meta uniqueness gate |
| `sync-guide.sh` | Refresh `SITE-GUIDE.md` from local canonical clone |

## Newsletter / Hive list

- **UI:** footer Hive strip + **exit-intent popup** (`newsletter.js`)
- **API:** `functions/api/subscribe.js` → `POST /api/subscribe`
- **ESP:** **Klaviyo** list **Busy Bee Hive** id `SzVGkq` (default in subscribe.js); only env required: `KLAVIYO_API_KEY`
- **Optional:** KV binding `NEWSLETTER`; Resend notify (`RESEND_API_KEY`, `NEWSLETTER_NOTIFY_TO`)
- Full wire-up: **`NEWSLETTER-SETUP.md`**

## Implementation habits

- Prefer editing **`_build.py`**, then `python3 _build.py`, for nav/footer/meta/chrome so all pages stay consistent
- Surgical CSS/JS edits; match existing class names
- Bust CSS/JS/image `?v=` via `ASSET_V` in `_build.py` when those assets change
- Google review URL + QR: `GOOGLE_REVIEW_URL` / `GOOGLE_REVIEW_QR` in `_build.py` (also exposed as `window.BUSYBEE`)
- Real photos under `public/images/kittens/` and `public/images/cats/` — do not ship emoji-only hero/cards when photos exist
- Finish = implemented + SITE-GUIDE-aligned for touched areas + committed + pushed + live spot-check

## Domain / config constants (`_build.py`)

- `SITE` — canonical origin
- `ASSET_V` — cache-bust query for CSS/JS/icons/OG
- `GOOGLE_REVIEW_URL` — official review destination (update when Place ID known)
- `BRAND`, `TAGLINE`, `NAV`

## New chat sessions

User often hits **+** only to reset context. On short prompts (“continue”, “next”), use git status/log + files; apply rules above. Do not ask them to restate SITE-GUIDE / commit-push / caveman.
