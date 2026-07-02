# Site Guide: Building Perfect, Ultra-Secure, WCAG-Compliant, SEO-Optimized Websites for #1 Google Ranking

> **⚠️ Canonical source: [StephenMattison/site-guide](https://github.com/StephenMattison/site-guide)**
> Do **not** edit this file directly in a website repo. All edits must go to the canonical repo above.
> To pull the latest version into this repo, run: `./sync-guide.sh`

**Project Objective**: Create flawless, production-ready websites that achieve:
- **WCAG 2.2 Level AA (and AAA where feasible)** compliance for universal accessibility.
- **Ultra-high security** standards (beyond baseline, including proactive threat mitigation).
- **Perfect SEO** across on-page, technical, off-page, and user-experience signals to secure and maintain Google Page #1 rankings for target keywords.
- **Exceptional performance**, user experience, and long-term maintainability.

This guide is the definitive reference for all development, content, and deployment decisions. All sites must pass automated audits (Lighthouse 100/100 across Performance, Accessibility, Best Practices, SEO) and manual expert reviews before launch.

---

## 1. WCAG 2.2 Compliance Instructions (Accessibility — Non-Negotiable)

All websites **must** meet or exceed WCAG 2.2 Level AA. Aim for AAA on critical user flows. Accessibility is a core ranking factor (Google uses it in quality signals) and a legal requirement in many jurisdictions.

### 1.1 Core Principles (POUR)
- **Perceivable**: Information and UI components must be presentable to users in ways they can perceive.
  - Provide text alternatives for non-text content (images, icons, charts, videos).
  - Provide captions, transcripts, and audio descriptions for time-based media.
  - Create content that can be presented in different ways without losing information (e.g., responsive design, zoom to 200%).
  - Make it easier for users to see and hear content (high contrast, no low-contrast text).

- **Operable**: UI components and navigation must be operable.
  - All functionality available via keyboard (no mouse-only traps).
  - Users have enough time to read and use content (no auto-redirects without warning, adjustable time limits).
  - Do not design content in a way that is known to cause seizures or physical reactions (no flashing >3 times/second).
  - Provide ways to help users navigate, find content, and determine where they are (skip links, clear headings, focus indicators, logical tab order).

- **Understandable**: Information and UI operation must be understandable.
  - Make text content readable and understandable (plain language, define abbreviations, reading level appropriate).
  - Make web pages appear and operate in predictable ways (consistent navigation, no unexpected context changes).
  - Help users avoid and correct mistakes (clear error messages, suggestions, labels, instructions).

- **Robust**: Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.
  - Maximize compatibility with current and future user agents (valid HTML, proper ARIA, no deprecated features).

### 1.2 Implementation Checklist (Mandatory)
- **Semantic HTML5**: Use `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, proper heading hierarchy (one `<h1>` per page, logical H2-H6).
- **Images & Media**:
  - Every `<img>` must have meaningful `alt` text (descriptive, not "image" or filename). Decorative images: `alt=""` + `role="presentation"`.
  - Complex images/charts: `aria-describedby` pointing to detailed description or longdesc.
  - Videos: Captions (WebVTT), transcripts, audio descriptions. Controls must be keyboard accessible.
- **Color & Contrast**:
  - Minimum 4.5:1 contrast for normal text, 3:1 for large text (WCAG AA). AAA: 7:1 / 4.5:1.
  - Do not rely on color alone to convey information (use icons, patterns, text labels).
  - Test with tools: `axe-core`, Lighthouse, WebAIM Contrast Checker, Colour Contrast Analyser.
- **Keyboard & Focus**:
  - Visible focus indicator (never remove `outline` or use `outline: none` without replacement).
  - Logical tab order matching visual/layout order.
  - Skip-to-content link at top.
  - Skip link must be hidden off-screen until focused (do not leave a visible sliver at the top of the viewport).
  - Recommended skip-link CSS baseline:
    ```css
    .skip-link { position: absolute; top: -200px; left: 12px; z-index: 1000; }
    .skip-link:focus { top: 12px; }
    ```
  - No keyboard traps (e.g., modals must trap focus properly with `aria-modal` and focus management).
- **Forms & Input**:
  - Every form control has visible `<label>` (or `aria-label`/`aria-labelledby`).
  - Error identification: Clear, specific messages with suggestions. Use `aria-invalid`, `aria-describedby`.
  - Required fields marked with `aria-required="true"`.
- **ARIA & Assistive Tech**:
  - Use ARIA only when native HTML insufficient (landmarks, live regions for dynamic content, `role`, `aria-*` attributes).
  - Test with screen readers: NVDA (Windows), VoiceOver (macOS/iOS), TalkBack (Android).
- **Responsive & Zoom**: Content reflows at 320px width without horizontal scroll or loss of functionality. Text resizable to 200% without loss.
- **Testing & Validation**:
  - Automated: Lighthouse Accessibility ≥100, axe DevTools, WAVE, Pa11y.
  - Manual: Keyboard-only navigation (Tab, Shift+Tab, Enter, Space, Esc), screen reader testing, high-contrast mode, zoom testing.
  - Document accessibility statement on site (link in footer).

**Failure to meet WCAG AA blocks launch.** Remediation must be completed within 48 hours of any audit finding.

---

## 2. Ultra-Secure Website Architecture

Security is foundational. We build "secure by design" with defense-in-depth. No site launches without passing independent security audit (OWASP ZAP, Burp Suite, Qualys, etc.) and achieving A+ on SSL Labs, SecurityHeaders.com, and Mozilla Observatory.

### 2.0 Social Cards, Favicons, and Third-Party Cache Busting (Mandatory)
- You cannot force Facebook, X, Slack, iMessage, Discord, LinkedIn, or browser favicon caches to purge immediately on demand from your server. Any guide claiming you can is wrong.
- The required solution on every site is versioned asset URLs for all social preview images and favicon references. When any social card image or favicon changes, the URL must also change.
- Every page must reference social preview images and favicon assets with an explicit version query string, for example: `/assets/img/social-cards/share-card.jpg?v=20260619-1` and `/assets/favicons/favicon-32x32.png?v=20260619-1`.
- The web manifest icon `src` values must also carry the same version query string.
- HTML pages must ship with `Cache-Control: public, max-age=0, must-revalidate`.
- Social-card assets and favicon assets must also ship with `Cache-Control: public, max-age=0, must-revalidate` so browsers and intermediaries revalidate aggressively.
- When you replace a favicon or social image, do all of the following before deploy is complete:
  1. Replace the image file.
  2. Bump the shared version string everywhere that references that asset.
  3. Deploy the updated HTML and headers.
  4. If needed, manually request refreshes in platform debuggers such as Facebook Sharing Debugger, LinkedIn Post Inspector, and X Card Validator. These tools help, but versioned URLs are the real fix.
- Never rely on keeping the same asset URL for changed share images or favicons. Some crawlers and clients keep those cached for weeks or months.
- This rule is mandatory for every Stephen Mattison site.

### 2.1 HTTPS & Transport Security (Mandatory)
- Enforce HTTPS site-wide with 301 redirects.
- HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- TLS 1.3 only (disable 1.0/1.1/1.2 where possible; 1.2 minimum with strong ciphers).
- Certificate: Let's Encrypt or higher (Wildcard + EV where branding requires). Auto-renewal via Certbot or equivalent.
- HTTP/2 or HTTP/3 (QUIC) enabled.

### 2.2 Headers & Browser Protections (CSP Required)
Implement these response headers on **every** page/response:
```
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-site
Cross-Origin-Embedder-Policy: require-corp (for isolation where needed)
Access-Control-Allow-Origin: https://your-canonical-domain.com
Vary: Origin
```
- Use `nonce` or hashes for inline scripts/styles to avoid `'unsafe-inline'` where possible.
- Regularly audit and tighten CSP.

#### 2.2.1 CSP — `script-src 'self'` blocks ALL inline `<script>` (including event handlers)
Our standard CSP omits `'unsafe-inline'` from `script-src`. This is correct and mandatory on this network. It also means any inline `<script>…</script>` block, any `onclick="…"`/`onsubmit="…"`/etc. attribute, and any `javascript:` URL is silently blocked by the browser in production. The page renders fine; the feature just does nothing. This is the #1 "works locally, dead in prod" gotcha.

**Hard rule for every new site:**
- `script-src` must **not** include `'unsafe-inline'`. If you see it in a draft `_headers` or CSP config, remove it before launch.
- Put **all** JavaScript in external files under `/js/<feature>.js` and load with `<script src="/js/<feature>.js" defer></script>`.
- Wire up events with `addEventListener` from inside that external file. Never use `onclick=`/`onsubmit=`/`onchange=`/any `on*=` HTML attribute.
- Never use `javascript:` URLs in links or buttons.
- The only inline `<script>` allowed in HTML is `<script type="application/ld+json">…</script>` for structured data.
- If a third-party snippet truly requires inline JS, use a CSP hash or nonce for that exact snippet. Never weaken policy with `'unsafe-inline'`.

**Cloudflare Challenge Platform compatibility (mandatory):**
- Cloudflare may inject inline JS from `/cdn-cgi/challenge-platform/scripts/jsd/main.js`.
- If your `script-src` contains both `'unsafe-inline'` and script hashes/nonces, browsers ignore `'unsafe-inline'`, which can still block Cloudflare-injected inline JS and trigger Lighthouse Best Practices failures (`errors-in-console`, `inspector-issues`).
- Use one strategy per environment:
  1. **Strict CSP strategy (preferred):** keep hashes/nonces and disable JS challenge injection on normal page traffic.
  2. **Compatibility strategy:** keep `'unsafe-inline'` and remove script hashes/nonces from `script-src`.
- Verify after deploy with:
  - `curl -sI https://<canonical-domain>/ | grep -i content-security-policy`
  - Lighthouse Best Practices on the live homepage.

**Standard implementation pattern:**

```html
<form id="size-form" class="tool-form">
  <button type="submit" class="btn btn-primary">Estimate Adult Size</button>
</form>
<script src="/js/tools.js" defer></script>
```

```js
document.getElementById('size-form')?.addEventListener('submit', function (event) {
  event.preventDefault();
  predictSize();
});
```

**Mandatory preflight before every deploy / PR approval:**

```bash
# 1) Fail if any inline event handlers exist in built HTML
rg -n '\son[a-z]+\s*=' public/

# 2) Fail if any inline executable <script> exists
rg -nP '<script(?![^>]*(src=|type="application/ld\+json"))' public/

# 3) Fail if any javascript: URL exists
rg -n 'javascript:' public/
```

Expected result for all three commands: **no output**.

**Verify after deploy:**
- Open the deployed page in Chrome/Firefox DevTools → **Console** tab. CSP violations show as bright-red `Refused to execute inline script because it violates the following Content Security Policy directive…` errors. Zero CSP errors = pass.
- Spot-check the affected interaction in production, not just locally. Static-file previews and local file opens can hide CSP failures that only show up behind the real headers.

**Launch gate:** Any CSP console error or any match from the three `rg` commands above blocks launch until fixed.

#### 2.2.2 CORS — Never ship `Access-Control-Allow-Origin: *`
Cloudflare Pages (and many static hosts) default to `Access-Control-Allow-Origin: *` on static assets. This must be explicitly overridden on **every new site** from day one.

**Mandatory `public/_headers` template — copy this verbatim and substitute `<canonical-domain>`:**

```
/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(self), usb=(), interest-cohort=(), accelerometer=(), gyroscope=(), magnetometer=(), autoplay=(self), encrypted-media=(), fullscreen=(self)
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-site
  Access-Control-Allow-Origin: https://<canonical-domain>
  Vary: Origin
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; media-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
```

**Rules:**
- `Access-Control-Allow-Origin` must be your exact canonical domain — never `*`.
- `Cross-Origin-Resource-Policy: same-site` prevents your assets being hotlinked or embedded by third-party pages.
- `Vary: Origin` tells CDN/proxies to cache responses per origin, which is required alongside a non-wildcard ACAO.
- Do not include deprecated or unrecognized `Permissions-Policy` features (for example `ambient-light-sensor`) because they trigger DevTools issues and can reduce Lighthouse Best Practices.
- Only widen ACAO to `*` for a specific path prefix that is genuinely a public API (e.g. `/api/public/*`) — never globally.
- After deploy, verify: `curl -sI https://<canonical-domain>/ | grep -i access-control` — it must show your domain, not `*`.
- Add an exact-match domain check to catch typos (`growbru.com` vs `growbrew.com` type mistakes):

```bash
EXPECTED_ORIGIN="https://<canonical-domain>"
ACTUAL_ORIGIN="$(curl -sI https://<canonical-domain>/ | tr -d '\r' | awk -F': ' 'tolower($1)=="access-control-allow-origin" {print $2}')"
[[ "$ACTUAL_ORIGIN" == "$EXPECTED_ORIGIN" ]] || { echo "ACAO mismatch: $ACTUAL_ORIGIN"; exit 1; }
```

**Launch gate:** Missing or wildcard ACAO on the global `/*` block = block launch until fixed.

### 2.3 Input Validation, Sanitization & Injection Prevention
- **Server-side validation** for ALL inputs (never trust client).
- Use prepared statements / parameterized queries (never string concatenation for SQL).
- Output encoding / escaping (HTML, JS, URL, CSS contexts).
- Sanitize with libraries (DOMPurify for client, OWASP ESAPI or equivalent server-side).
- Rate limiting on all endpoints (e.g., 5 attempts/min for login).
- Honeypots + reCAPTCHA v3 / Cloudflare Turnstile for forms.
- File uploads: Strict MIME type validation, virus scanning (ClamAV), rename files, store outside web root, size limits.

### 2.4 Authentication & Session Management
- Strong password policy (min 12 chars, complexity, no common passwords — use HaveIBeenPwned API check).
- Multi-Factor Authentication (MFA) **mandatory** for all admin/user accounts with sensitive data.
- Passwordless options: Passkeys (WebAuthn/FIDO2) preferred where supported.
- Session: HttpOnly, Secure, SameSite=Strict cookies. Short timeouts (15-30 min idle), regenerate session ID on login.
- Account lockout after 5 failed attempts (15 min or exponential backoff).
- OAuth 2.1 / OpenID Connect for third-party logins (Google, Apple, Microsoft — with PKCE).

### 2.5 Data Protection & Privacy
- Encrypt sensitive data at rest (AES-256-GCM or better, keys in HSM or KMS like AWS KMS, never in code).
- Never log PII or sensitive data.
- Data minimization: Collect only what is needed.
- Cookie consent banner with granular controls (necessary vs analytics/marketing). Use IAB TCF or equivalent. No cookies before consent where required (GDPR/CCPA).
- Privacy policy + Terms of Service linked in footer, updated regularly.
- Right to be forgotten / data export endpoints (automated where possible).

### 2.6 Infrastructure & Operations Security
- Hosting: Enterprise-grade with SOC 2 Type II, ISO 27001, PCI DSS (if payments), DDoS protection (Cloudflare, AWS Shield, Akamai).
- WAF (Web Application Firewall) with OWASP Top 10 rules enabled and tuned.
- Regular dependency scanning (npm audit, Snyk, Dependabot, Renovate) — zero critical/high vulnerabilities allowed.
- Automated backups (daily full + continuous WAL for DBs) with encryption and 30-day retention. Test restores quarterly.
- Monitoring: Real-time (Datadog, New Relic, Sentry) + SIEM for anomaly detection. 24/7 alerting.
- Penetration testing & red team exercises: Quarterly minimum. Bug bounty program recommended.
- Incident response plan: Documented, tested annually. Breach notification within 72 hours (or sooner per regulation).
- Zero-trust principles: Least privilege access, just-in-time, network segmentation.

### 2.7 Content Management & Third-Party Risks
- If using CMS (WordPress, etc.): Hardened config, minimal plugins, automatic core/plugin updates, security plugins (Wordfence, Sucuri), file integrity monitoring.
- Third-party scripts: Audit all (Google Tag Manager, analytics, chat, ads). Use Subresource Integrity (SRI) hashes. Prefer self-hosted where possible.
- Never load third-party SDKs globally unless the page actively uses them. Load on demand for the exact feature/page to reduce risk surface and avoid unnecessary Lighthouse Best Practices noise.
- No eval(), no dangerous DOM manipulation.

**Security Audit Gate**: Independent third-party audit (or automated + manual by security engineer) required before any production deployment. Remediate all findings (Critical/High = block launch).

---

## 3. Perfect SEO Strategy for Sustained #1 Google Rankings

Goal: Dominate target keywords with helpful, authoritative, technically flawless pages that satisfy user intent and Google's ranking systems (Helpful Content, Core Updates, SpamBrain, etc.).

### 3.1 Keyword Research & Intent Alignment
- Primary + secondary + long-tail keywords mapped to user intent (informational, transactional, navigational, commercial).
- Tools: Google Keyword Planner, Search Console (impressions/clicks), Ahrefs/Semrush (for competitor gaps), AnswerThePublic, AlsoAsked.
- Target "People Also Ask" and featured snippet opportunities.
- Content clusters: Pillar pages + supporting cluster content with internal linking.

### 3.2 On-Page SEO (Every Page Must Pass)
- **Title Tag**: 50-60 characters, primary keyword near front, unique, compelling, brand at end.
- **Meta Description**: 150-160 characters, includes keyword, call-to-action, unique per page.
- **URL Structure**: Short, descriptive, keyword-rich, hyphens (no underscores, no dates unless news), lowercase. Example: `/best-practices/wcag-2-2-compliance-checklist`
- **Headings**: One H1 (main keyword + benefit), H2s for sections (secondary keywords), logical hierarchy. Never skip levels.
- **Content Quality**:
  - Original, in-depth (1,500–4,000+ words for competitive topics), scannable (short paragraphs, bullets, tables, bold key phrases).
  - Answers "Who, What, When, Where, Why, How" thoroughly.
  - E-E-A-T signals: Author byline with credentials/bio, citations to authoritative sources, "Last updated" date, "Reviewed by" expert, About page, Contact/Trust signals.
  - First 100-150 words include primary keyword naturally + answer main query.
  - No thin/duplicate/low-value content. Pass Google's Helpful Content Update test (would you bookmark/share this?).
- **Images**: Unique, optimized (WebP/AVIF primary, fallback), descriptive filenames + alt text (keyword + context), captions where helpful. Lazy load with `loading="lazy"`.
- **Internal Linking**: 3–8 relevant internal links per page, descriptive anchor text (not "click here").
- **Schema Markup** (JSON-LD preferred):
  - Article, FAQPage, HowTo, BreadcrumbList, Organization, WebSite, Person (author), Review, AggregateRating.
  - Validate with Google Rich Results Test.
- **Canonical Tags**: Self-referencing or correct target for duplicates.

#### 3.2.1 Page Title and Meta Description Rules
- Every indexable page must have a unique `<title>` and unique `<meta name="description">`.
- Every indexable page should include `<meta name="robots" content="index,follow">` unless intentionally noindexed.
- Start the title with the most important keyword phrase for that page, then finish with the brand.
- Keep titles readable and specific; do not stuff keywords or repeat the same phrase twice.
- Write descriptions for users first: summarize the page, include the main keyword naturally, and make the benefit or action clear.
- Keep descriptions unique across the site so search engines do not see near-duplicate snippets.
- Match the visible page intent exactly. Product pages should describe the product, collection pages should describe the category, and support pages should describe the support topic.
- Use the same core wording in `<title>`, Open Graph title, and Twitter title so shared links look consistent.
- Keep Open Graph and Twitter descriptions aligned with the page description unless a shorter social version is needed.
- Add a strong canonical URL for every indexable page and make sure the title/description describe that canonical version, not a duplicate.
- For blog posts, lead with the topic or question being answered and end with the brand.
- For product pages, lead with the product type or primary use case, then add the size, format, or benefit, then end with the brand.
- For home pages and collection pages, lead with the main commercial keyword phrase, then describe the offering, then end with the brand.
- Recommended pattern:
  - Title: `Primary Keyword or Topic | Supporting Benefit or Modifier | Brand`
  - Description: `Primary keyword + user benefit + differentiator + call to action`
- Avoid vague titles such as `Home`, `Products`, or `Blog` unless they are supported by strong keyword context.
- Avoid duplicate brand-first titles unless the brand itself is the primary search term for that page.
- If a page targets social sharing, keep the Open Graph image current and use a concise, compelling title/description pair.
- **Hreflang** (if multilingual): Proper implementation.

##### Authoring procedure (mandatory)
- Titles and meta descriptions are an SEO-engineering deliverable, not a content-author chore. They are produced and maintained by whoever is writing the page or running the build, following the patterns above.
- Hand-writing per page is acceptable only on small static sites (roughly under 30 indexable pages). Above that scale, generate them programmatically from a per-page data source (JSON, YAML, CSV, CMS field, product database) plus a template that enforces the recommended pattern. This guarantees uniqueness and keeps every page in sync as data changes.
- Never copy a title or description from one page to another as a starting point. Always derive each from that page's own primary keyword, intent, and differentiator.
- Re-validate titles and descriptions after every content change, every product import, and every template refactor. Bulk imports are the most common source of duplicate-title and duplicate-description regressions.
- The canonical compliance script (`scripts/check-site-guide-compliance.py`, installed via `apply-lighthouse-standard.sh`) enforces presence and uniqueness of `<title>` and `<meta name="description">` across all indexable pages and runs in CI on every adopted repo. A failed compliance run blocks deploy; fix the duplicates or missing entries before retrying.
- When migrating or restructuring a site, run the compliance script locally before pushing — duplicates from a previous iteration must be resolved as part of the migration, not deferred.

### 3.3 Technical SEO (Foundation for Crawlability & Rankings)
#### Core Web Vitals (CWV) – Best-in-Class Requirements (Mandatory for All Sites)

Core Web Vitals are non-negotiable. Every page and component must be engineered for the absolute best possible scores, not merely "good". Target significantly better than Google's thresholds for competitive advantage and superior user experience:

- LCP: Target ≤ 1.8 s (excellent) on both mobile and desktop. Prioritize above-the-fold content, especially product heroes and research request forms.
- INP: Target ≤ 150 ms. Every interactive element (buttons, forms, research request flows, filters) must feel instant.
- CLS: Target ≤ 0.05. Zero unexpected layout shifts on any page, including dynamic Supabase-loaded content and product listings.

These metrics directly impact Google ranking under Page Experience signals and conversion rates. Every new site, page, or component must be built to these elite standards from the first line of code.

Measurement (required on every build):
- Run Lighthouse (performance + accessibility) and PageSpeed Insights on mobile + desktop before any deployment.
- Enable and regularly review Cloudflare Web Analytics real-user metrics.
- Monitor Google Search Console Core Web Vitals report.
- Re-test after any Supabase integration or dynamic content changes.

Platform-agnostic rules (apply to all current and future sites regardless of hosting):
- Mobile-first, responsive design with touch-friendly interactions.
- Optimize all images: proper sizing, modern formats (AVIF/WebP), width/height attributes, native lazy loading, and fetchpriority on LCP elements.
- Critical CSS inlined; all non-critical JavaScript deferred or loaded asynchronously.
- Font loading with font-display: swap and preload of key fonts only.
- Reserve space for all dynamic or loaded elements (images, forms, Supabase data) using aspect-ratio, min-height, or skeleton loaders to eliminate layout shift.
- Minimize render-blocking resources.
- Batch and optimize all API/Supabase calls; avoid blocking the main thread.
- Test and optimize specifically for research request forms, product pages, and e-commerce flows for fast INP and conversion.

Current primary stack optimizations (Cloudflare Pages + Supabase – apply these now and whenever using this stack):
- Use Cloudflare Image Optimization or native responsive images with transformations.
- Leverage Cloudflare edge caching and Cache Rules aggressively for all static assets and, where safe, dynamic responses.
- Consider Pages Functions for proxying or caching Supabase queries at the edge when it improves LCP or INP.
- Take full advantage of global edge delivery for lowest possible latency on all assets and API responses.

This section applies to every website build going forward. No exceptions. Performance must be best-in-class, not average.
- **Mobile-First & Responsive**: Google uses mobile index primarily. Test on real devices. Touch targets ≥44x44px, no horizontal scroll at 320px.
- **Crawlability**:
  - `robots.txt` allows all important paths, blocks admin/login.
  - XML Sitemap: **must explicitly list every indexable URL** — homepage, all product/landing/category pages, shop. Do NOT rely on auto-generation tools without verifying the output URL count matches the actual page count. A sitemap with missing pages is a silent SEO failure: Google will only index what it finds in the sitemap. After every deploy that adds new pages, update the sitemap and re-submit in Search Console.
  - Sitemap URL count check: run `grep -c "<loc>" sitemap.xml` and verify it equals the total number of indexable pages.
  - Clean HTML (no excessive JS rendering for critical content — SSR or SSG preferred for SEO-critical pages).
  - Proper status codes (200 OK, 301/308 for redirects, 404 for missing, 410 for gone).
  - No broken links (internal or external) — monitor with Screaming Frog or Ahrefs.
- **Indexing Control**: `noindex` only on thin/duplicate/paginated/admin pages. Use `canonical` + `noindex` carefully.
- **Structured Data & Rich Results**: Aim for multiple rich result types. Monitor in Search Console Enhancements report.
- **International SEO** (if applicable): Proper hreflang, geo-targeting in Search Console, localized content.

### 3.4 Off-Page SEO & Authority Building
- High-quality backlinks from relevant, authoritative domains (DA 50+). Focus on editorial, guest posts, HARO, digital PR, broken link building, resource pages.
- Brand mentions (unlinked) count toward E-E-A-T.
- Social signals (indirect): Shareable content, engagement on X/LinkedIn/Reddit.
- Local SEO (if applicable): Google Business Profile optimized, citations consistent (NAP), reviews.

### 3.5 Analytics, Monitoring & Iteration
- **Google Search Console**: Verify property, submit sitemap, monitor impressions/clicks/position/Core Web Vitals/Enhancements/Issues. Fix all errors weekly.
- **Google Analytics 4** (server-side tagging preferred for privacy): Track conversions, user journeys, scroll depth, video engagement.
- **Rank Tracking**: Daily/weekly for target keywords (Ahrefs, Semrush, SERP API).
- **Competitor Analysis**: Identify content gaps, backlink opportunities, SERP features.
- **Content Refresh**: Update top-performing pages quarterly with new data, examples, statistics. Re-optimize based on Search Console data.
- **A/B Testing**: For titles, meta, CTAs (Google Optimize or VWO — respect privacy).
- **Negative SEO Protection**: Monitor backlinks for spam, disavow if needed. Secure site to prevent hacking (which can tank rankings).

#### 3.5.1 Mandatory GA4 + Search Console Setup (All Sites)

Run this checklist for every new website and every major relaunch.

1. **Create/verify Google Search Console domain property**
  - Prefer a **Domain property** (`example.com`) via DNS TXT verification so all protocols/subdomains are covered.
  - Keep an HTML verification file in the repo root as a fallback for URL-prefix verification continuity.

2. **Confirm crawl endpoints before submission**
  - Ensure `robots.txt` contains a valid, live sitemap URL (for example `https://www.example.com/sitemap.xml`).
  - Do not reference compressed sitemap paths unless that exact `.gz` file is actually deployed.
  - Ensure the canonical host in sitemap URLs matches the production canonical domain.

3. **Submit sitemap in Search Console**
  - In Search Console → Sitemaps, submit the canonical sitemap URL.
  - After deploys that add major URL groups, re-check sitemap status and coverage.

4. **Set up Google Analytics 4 (GA4)**
  - Create a GA4 property and web data stream for the canonical production domain.
  - Install GA4 via external JavaScript (no inline scripts) to stay compatible with strict CSP.
  - Store the measurement ID (`G-XXXXXXXXXX`) in a single config location so all pages use one source of truth.
  - Enable conversion events for primary business outcomes (purchase, lead, checkout start, contact submit).

5. **Link Google products**
  - Link GA4 to Search Console.
  - Link GA4 to Google Ads if ads are used.
  - Confirm shared timezone/currency settings are correct before reporting periods begin.

6. **Launch validation (same day)**
  - Confirm Search Console verification is active.
  - Confirm sitemap status is `Success`.
  - **Verify sitemap URL count** — run `grep -c "<loc>" sitemap.xml` and confirm it matches the total number of indexable pages. A mismatch means pages are missing and will not be indexed by Google.
  - Confirm GA4 Realtime receives page views from live traffic.
  - Inspect one key URL in Search Console URL Inspection and request indexing if needed.

7. **Weekly operating cadence (mandatory)**
  - Search Console: Coverage, Enhancements, Core Web Vitals, Manual Actions, Security Issues.
  - GA4: conversion trend, landing-page performance, engagement drop-offs, anomalous traffic.
  - Fix critical errors in the same sprint; do not allow unresolved indexing or measurement drift.

Implementation notes:
- Keep analytics scripts external to avoid CSP breakage on production static sites.
- Use one canonical property and one canonical sitemap per production domain.
- No SEO workflow can guarantee a permanent #1 ranking; the repeatable path is superior technical quality, strong content, authority growth, and continuous iteration.

### 3.6 Google Ranking Factors Prioritization (2026+)
1. **Helpful, People-First Content** (E-E-A-T + original research + user satisfaction).
2. **Page Experience** (Core Web Vitals + mobile + HTTPS + no intrusive interstitials).
3. **Technical Excellence** (crawl/index/render speed, structured data).
4. **Authority & Trust** (backlinks, brand, reviews, citations).
5. **User Signals** (dwell time, low pogo-sticking, high engagement — achieved via superior UX/accessibility).

**Launch Gate**: Full SEO audit (technical + on-page + content) with 0 critical issues. Target: Top 3 organic for primary keywords within 90 days of launch, #1 within 6 months via consistent execution.

---

## 4. Performance, UX & Conversion Optimization
- **Design System**: Consistent, accessible components (buttons, forms, cards) with WCAG-compliant states.
- **Animations**: Subtle, purposeful, respect `prefers-reduced-motion`.
- **Loading States**: Skeleton screens, optimistic UI, clear progress.
- **Conversion Focus**: Clear value prop above fold, prominent CTAs, trust signals (testimonials, security badges, guarantees), minimal friction checkout/forms.
- **A/B & Personalization**: Data-driven (but privacy-first).

### 4.1 Asset Cache-Busting (Mandatory for ALL Static Sites)

**Rule**: Every static asset reference (CSS, JS, images, fonts, icons, manifest) must include a content-hash query string (`?v=<hash>`) appended at build time. This is non-negotiable for every site we build.

**Why it's mandatory**:
- Allows aggressive 1-year `immutable` caching at the CDN and in browsers (huge perf win, near-zero repeat-visit latency).
- Eliminates the need to ever manually purge the CDN cache when updating an image, stylesheet, or script — the new hash makes the URL a "new" resource browsers fetch automatically.
- Prevents stale-asset bugs (mismatched CSS/JS, old logos lingering after a brand update).
- This is the same pattern Webpack, Vite, Next.js, Astro, and every modern framework use. There is no scenario where omitting it is correct for a production static site.

**Implementation pattern (Python static-site builder)**:

```python
import hashlib
from pathlib import Path

OUT = Path(__file__).parent / "public"

def asset_v(rel_path: str) -> str:
    """Return ?v=<md5[:10]> for cache-busting an asset under public/.
    Returns empty string if the file doesn't exist (graceful fallback)."""
    f = OUT / rel_path.lstrip("/")
    if not f.exists():
        return ""
    h = hashlib.md5(f.read_bytes()).hexdigest()[:10]
    return f"?v={h}"
```

Use it in every asset reference:

```python
# Inside f-strings (most templates):
f'<link rel="stylesheet" href="/css/style.css{asset_v("/css/style.css")}">'
f'<script src="/js/script.js{asset_v("/js/script.js")}" defer></script>'
f'<img src="/images/logo.webp{asset_v("/images/logo.webp")}" alt="Logo">'

# Inside non-f-string templates, use string concatenation:
'<img src="/images/hero.webp' + asset_v("/images/hero.webp") + '" alt="Hero">'

# For dynamic image fields (cards, listings):
f'<img src="/images/kittens/{k["image"]}{asset_v("/images/kittens/" + k["image"])}" ...>'
```

**Pair with the matching CDN cache headers** (`public/_headers` for Cloudflare Pages):

```
/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=31536000, immutable

/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate
```

HTML is never cached (so new asset hashes propagate instantly); hashed assets are cached for 1 year `immutable`.

**Coverage checklist** — every one of these must use `asset_v()`:
- [ ] All `<link rel="stylesheet">` tags
- [ ] All `<script src=...>` tags
- [ ] All `<img src=...>` tags (hero, logos, cards, content images, OG images)
- [ ] `<link rel="icon">`, apple-touch-icon, manifest icons
- [ ] `<link rel="manifest">` site.webmanifest
- [ ] Preload tags (`<link rel="preload" href=...>`)
- [ ] CSS `url(...)` references (handled separately — version the CSS file itself)
- [ ] Open Graph / Twitter card image URLs (use absolute URL + hash)

**Verification after build**:

```bash
# Confirm hashes appear in built HTML — should show ?v=<hash> on every asset:
grep -oE 'src="[^"]*\?v=[^"]*"' public/index.html | head
grep -oE 'href="[^"]*\.(css|webp|js)\?v=[^"]*"' public/index.html | head

# Confirm no literal {asset_v(...)} leaked into HTML (common bug in non-f-string templates):
! grep -r 'asset_v(' public/ && echo "Clean"
```

**Common pitfall**: When a template uses a plain triple-quoted string (not an f-string), `{asset_v(...)}` will be emitted as literal text and break the URL. Always either (a) make the template an f-string, or (b) use string concatenation as shown above. The verification grep above catches this.

---

## 5. Development Workflow & Quality Gates

### 5.1 Lighthouse CI (Mandatory for Every Repo)

Every site repository **must** include Lighthouse CI, but the default standard is **low-frequency** execution (manual trigger + monthly schedule) so routine commits are not slowed down by long scans.

**Canonical source of truth for repo assets**:
- `templates/lighthouse/.github/workflows/lighthouse.yml`
- `templates/lighthouse/scripts/run-lhci.sh`
- `templates/lighthouse/.lighthouserc.json`
- `templates/compliance/.github/workflows/site-guide-compliance.yml`
- `templates/compliance/scripts/check-site-guide-compliance.py`

Use the canonical adoption script from the `StephenMattison/site-guide` repo to install the shared workflow and helper into a site repo:

```bash
./scripts/apply-lighthouse-standard.sh /absolute/path/to/site-repo
./scripts/apply-lighthouse-standard.sh /absolute/path/to/site-repo public
```

Use the second form for repos that serve built static output from `public/`.

**Shared workflow standard**:

**`.github/workflows/lighthouse.yml`**
```yaml
name: Lighthouse CI

on:
  workflow_dispatch:
  schedule:
    - cron: '0 5 1 * *'

permissions:
  contents: read
  statuses: write
  checks: write
  pull-requests: write

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v5
        with:
          node-version: '22'

      - name: Install Lighthouse CI
        run: npm install -g @lhci/cli@0.14.x

      - name: Run Lighthouse CI
        env:
          LHCI_GITHUB_TOKEN: ${{ github.token }}
        run: ./scripts/run-lhci.sh
```

**`scripts/run-lhci.sh`**
```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${LHCI_GITHUB_TOKEN:-}" && -z "${LHCI_GITHUB_APP_TOKEN:-}" ]] && command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    LHCI_GITHUB_TOKEN="$(gh auth token)"
    export LHCI_GITHUB_TOKEN
  fi
fi

exec npx -y @lhci/cli@0.14.x autorun "$@"
```

**`.lighthouserc.json`** (baseline; customize per site):
```json
{
  "ci": {
    "collect": {
      "staticDistDir": ".",
      "numberOfRuns": 3
    },
    "assert": {
      "preset": "lighthouse:no-pwa",
      "assertions": {
        "categories:performance": ["warn", {"minScore": 0.85}],
        "categories:accessibility": ["warn", {"minScore": 0.90}],
        "categories:best-practices": ["warn", {"minScore": 0.85}],
        "categories:seo": ["warn", {"minScore": 0.95}]
      }
    },
    "upload": {
      "target": "temporary-public-storage",
      "uploadUrlMap": true
    }
  }
}
```

**Notes on configuration**:
- Change `staticDistDir` to `"public"` for sites that build into a `public/` directory.
- Add an explicit `collect.url` array for the 4-6 most important pages once the baseline is stable.
- For sites with a Python or Node build step, add the build step before the `lhci autorun` step.
- The workflow must use GitHub's built-in Actions token for remote status checks. Do not create a separate personal token for each site repo.
- Local runs should use `./scripts/run-lhci.sh` so GitHub CLI auth is reused automatically when available.
- Once the site is remediated and stable, raise accessibility and SEO assertions from `"warn"` to `"error"`.
- Default cadence is monthly plus manual runs on demand. If a specific site needs stricter enforcement, that site can opt into per-PR Lighthouse later.

**Execution model**:
- Default: monthly scheduled run + manual run from Actions tab when you want a fresh audit.
- Optional stricter mode: per-PR/per-push Lighthouse can be enabled on a per-site basis, but is not required by this baseline standard.

**Reading Lighthouse CI results**:
- Each run uploads a public report URL visible in the GitHub Actions log under "Lighthouse CI".
- Each run should also write GitHub status checks like `lhci/url/index.html` when the token setup is correct.
- Click the URL to see the full report with exact scores and specific issues to fix.
- Any `error`-level assertion failure blocks PR merging until fixed.

### 5.2 Continuous Site-Guide Compliance (Mandatory)

Every adopted repo must run a separate compliance workflow for **site-guide sync updates** (plus manual runs) to enforce guide rules without adding noise to routine website PRs.

**`.github/workflows/site-guide-compliance.yml`**
```yaml
name: Site Guide Compliance

on:
  workflow_dispatch:
  pull_request:
    branches: [main]
    paths:
      - 'SITE-GUIDE.md'
      - 'Strict-Per-Site-Compliance-Audit-Procedure.md'
      - 'Simple-Per-Site-Compliance-Audit-Procedure.md'
      - '.github/workflows/site-guide-compliance.yml'
      - 'scripts/check-site-guide-compliance.py'
  push:
    branches: [main]
    paths:
      - 'SITE-GUIDE.md'
      - 'Strict-Per-Site-Compliance-Audit-Procedure.md'
      - 'Simple-Per-Site-Compliance-Audit-Procedure.md'
      - '.github/workflows/site-guide-compliance.yml'
      - 'scripts/check-site-guide-compliance.py'

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Check SITE-GUIDE compliance (titles + meta descriptions)
        run: python3 scripts/check-site-guide-compliance.py
```

**`scripts/check-site-guide-compliance.py`** (enforced automatically):
- All indexable HTML pages must have a non-empty `<title>`.
- All indexable HTML pages must have a non-empty `meta name="description"`.
- `<title>` values must be unique across indexable pages.
- Meta descriptions must be unique across indexable pages.
- Pages with robots `noindex` are excluded from this check.
- Generated sitemap template files under `sitemap/pages/mods/` are excluded so this gate stays focused on real indexable pages.
- Search-engine verification token files (for example `googlexxxxxxxxxxxxxxxx.html` and `Gensw_*.html`) are excluded from this check.

This gate is intentionally strict so title/meta quality does not drift over time.

By default this gate is not run for unrelated day-to-day page edits unless you trigger it manually.

1. **Local Development**: Dockerized environments, hot reload, linting (ESLint + Stylelint + Prettier), TypeScript strict mode.
2. **CI/CD Pipeline** (GitHub Actions / GitLab CI):
   - Automated tests (unit, integration, E2E with Playwright/Cypress — include a11y and visual regression).
   - Security scanning (SAST, dependency, container).
   - Lighthouse CI + axe-core in pipeline (fail build on regression).
   - Accessibility + SEO + Security audits on every PR.
3. **Staging Environment**: Mirror production exactly. Full manual + automated QA including screen reader, keyboard, performance under load.
4. **Production Deployment**: Blue-green or canary. Feature flags for risky changes. Rollback <5 min.
5. **Post-Launch**: 24/7 monitoring, weekly audits, monthly comprehensive review (WCAG, security headers, SEO health, Core Web Vitals trends).

### 5.3 Production Console Hygiene (Mandatory)
- Keep debug logging available in development, but gate it in production (for example by hostname, environment flag, or build mode).
- Do not ship persistent noisy `console.log` output in production application flows.
- A small helper is the preferred pattern:

```js
const DEBUG_LOG = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
const debugLog = (...args) => { if (DEBUG_LOG) console.log(...args); };
```

- Replace non-essential `console.log(...)` calls with `debugLog(...)`.
- Keep `console.error(...)` for real runtime failures that require investigation.

### 5.3.1 Lighthouse Best Practices Recovery Runbook (Mandatory)
- Use this exact flow whenever Best Practices drops below 100 on a live site.

1. Run a live best-practices-only audit and save JSON output.
2. Read failing audit IDs first (`errors-in-console`, `inspector-issues`, `deprecations`, etc.).
3. If `errors-in-console` mentions CSP inline blocking, inspect live `Content-Security-Policy` and match it to source control `_headers`.
4. If `Permissions-Policy` warnings appear, remove deprecated/unrecognized feature tokens.
5. If issues come from `/cdn-cgi/challenge-platform/...`, treat as Cloudflare challenge injection and apply the CSP compatibility rule in section 2.2.1.
6. Trigger a fresh deployment, then purge edge cache.
7. Re-check live headers and rerun Lighthouse on the live domain (not localhost) before sign-off.

Required validation commands:
```bash
curl -sI https://<canonical-domain>/ | rg -i "content-security-policy|permissions-policy|cf-cache-status"
npx --yes lighthouse https://<canonical-domain>/ --only-categories=best-practices --quiet --chrome-flags='--headless=new --no-sandbox'
```

Launch gate: do not close remediation until live-domain Best Practices and console/Issues panel are clean.

### 5.3.2 One-Command Operator Workflow (Recommended Standard)
- To keep operations fast and consistent across all site repos, use one-command shell helpers.
- These helpers improve execution speed and reduce command mistakes; they do not replace CI, code review, or required launch gates.

Required command set:
```bash
siteup
siteaudit
sitepush "clear commit message"
```

Expected behavior:
1. `siteup`: updates local repo from remote default branch (safe pull with autostash/rebase).
2. `siteaudit`: runs repo-defined audit scripts (local compliance + Lighthouse where available).
3. `sitepush`: stages all changes, commits with message, and pushes current branch.

Optional guide-sync command:
```bash
./sync-guide.sh
```
- Use this when a repo maintains `SITE-GUIDE.md` by copying from a local canonical checkout.
- If your workflow distributes guide updates by PR into each website repo, merge PR then run `siteup` in local folders.

Operator sequence per repo:
1. `siteup`
2. make changes
3. `siteaudit`
4. `sitepush "what changed"`

### 5.4 Playwright Rapid Validation Protocol (Mandatory for Fast Web QA)
- Use browser automation (Playwright) as the default first-pass validator after UI edits, bug fixes, and production regressions.
- Goal: reduce manual QA time, catch breakage early, and verify behavior consistently across flows.

#### 5.4.1 When to Use
- After any UI/UX change affecting layout, filters, forms, navigation, cart/checkout, auth, or dashboard interactions.
- When a user reports "it looks broken" or "button does not work" and reproduction is unclear.
- Before and after production deployments when cache/versioning changes are involved.

#### 5.4.2 Cost-Control Rules (Token/Credit Efficiency)
- Start with focused checks: validate only the modified flow first (not full-site sweeps).
- Reuse an open browser page/session whenever possible instead of opening many tabs.
- Prefer short assertions (state text, element visibility, count, URL hash) over large page dumps.
- Escalate in tiers:
1. Smoke check (one happy path).
2. Critical edge path check.
3. Broader regression only if failures are found.
- Stop once acceptance criteria are proven; avoid redundant re-runs.

#### 5.4.3 Standard Fast Validation Sequence
1. Load target page and wait for stable render.
2. Verify versioned assets are current (JS/CSS query versions when relevant).
3. Execute the exact user journey tied to the change.
4. Assert expected UI/output state with specific checks.
5. Capture a concise pass/fail summary with affected components.
6. If failed: fix, rerun the minimal failing step, then rerun the smoke path.

#### 5.4.4 Required Assertions by Change Type
- Data/listing changes: result count, expected item presence, sort order, filter behavior.
- Interaction changes: click handlers, keyboard access, modal open/close, persisted state.
- Responsive changes: at least one mobile-width and one desktop-width check for overflow/wrapping.
- Deployment checks: verify production payload/version and one user-visible behavior.

#### 5.4.5 Reporting Format (Keep It Short)
- Checked flow(s)
- Assertion results (pass/fail)
- Environment checked (local/staging/production)
- Residual risk (if any)

---

### 5.5 Standard Mobile CSS Patterns (Mandatory — Never Reinvent)

These patterns are derived from working production sites (revengeworks.com et al.). Apply them identically on every new site. Deviation requires explicit justification and a mobile overflow test before merge.

#### 5.5.1 Navbar — Required Structure
```css
/* NAVBAR BASE */
.navbar {
  position: sticky; top: 0; z-index: 1000;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.navbar-inner {
  max-width: 1280px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 1.5rem; height: 56px;
}

/* LOGO — must never collapse on mobile */
.logo {
  display: flex; align-items: center; gap: 0.5rem;
  flex-shrink: 0;        /* MANDATORY — prevents logo squishing to 0px */
  margin-right: auto;    /* pushes nav-actions to far right */
}
.logo img { height: 36px; width: auto; display: block; }

/* DESKTOP NAV LINKS — hidden on tablet/phone */
.nav-links { display: flex; gap: 0.25rem; }
@media (max-width: 1024px) {
  .nav-links { display: none; }
  .mobile-toggle { display: block; }
}

/* NAV ACTIONS (cart, account, hamburger) */
.nav-actions { display: flex; align-items: center; gap: 0.5rem; }

/* MOBILE NAV */
@media (max-width: 768px) {
  .navbar-inner { height: 56px; padding: 0 1rem; }
  .nav-actions  { gap: 0.5rem; }
  /* Minimum tap targets */
  .nav-cart, .mobile-toggle, .nav-account {
    min-width: 44px; min-height: 44px;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  /* Mobile menu links — large and readable */
  .mobile-menu a {
    display: block;
    padding: 1rem 1.5rem;
    font-size: 1.1rem; font-weight: 600;
    border-bottom: 1px solid #f1f5f9;
  }
}
```

**Rules:**
- `flex-shrink: 0` + `margin-right: auto` on `.logo` — non-negotiable. Without this the logo collapses to 0px on phones when nav-actions items overflow the flex row.
- Never put more than 3 icon buttons in `.nav-actions` on mobile. If you have X/Twitter, account, cart, AND hamburger, hide the decorative ones (X/Twitter) at `≤1024px`.
- `gap: 0.5rem` minimum between nav-action icons — tighter looks broken.

#### 5.5.2 Hero Section — Mobile Rules
```css
.hero {
  /* Desktop: extra bottom padding to clear absolutely-positioned overlays */
  padding: 3.5rem 1.5rem 8rem;
  position: relative; overflow: hidden;
}
@media (max-width: 768px) {
  .hero { padding: 2.5rem 1.25rem 3rem; }
}
```

**Hard rules:**
1. **Never embed `position: absolute` children that require large padding to avoid overlap.** Testimonial strips, badge rows, trust cards — put them as a *separate section below the hero*, not inside it. On mobile, absolutely positioned elements always become layout liabilities (either they overlap content or, when converted to `position: static` in a media query, they bloat the hero to 1000+ px tall).
2. **Never use `position: static` as a mobile fallback for an element that was `position: absolute`.** If you need to show trust content on mobile, duplicate it outside the hero in a dedicated `<section>`.
3. **Hero image columns with `minmax(520px, 1fr)`** will overflow at any mobile viewport. Use `minmax(min(100%, 520px), 1fr)` and confirm the grid collapses to 1 column at 768px.

#### 5.5.3 Grid Columns — Safe Pattern
```css
/* WRONG — minimum 280px hard-coded causes overflow at narrow viewports */
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));

/* CORRECT — min() clamps to 100% of container before triggering the minimum */
grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
```
Apply this to every grid on every site. The `min(100%, Npx)` pattern is the only safe way to use `minmax` with a pixel floor.

#### 5.5.4 Overflow-X — Global Safety Net
```css
/* Put this in the base CSS of every site */
html { overflow-x: clip; }   /* clips overflow without creating scroll context */
/* Do NOT use: overflow-y: scroll; scrollbar-gutter: stable; */
/* scrollbar-gutter: stable reserves ~15px permanently and collapses headless */
/* browser viewports — wasting debugging time on a non-issue for real phones */
```

#### 5.5.5 Pre-Commit Mobile Overflow Check (Mandatory)
Run this in Playwright or browser console at **375px, 390px, and 768px** after any CSS change:
```js
// PASS = no numbers > 0, FAIL = something is overflowing
document.querySelectorAll('*').forEach(el => {
  if (el.getBoundingClientRect().right > window.innerWidth + 2) {
    console.warn('OVERFLOW:', el.tagName, el.className, Math.round(el.getBoundingClientRect().right));
  }
});
console.log('scrollWidth:', document.documentElement.scrollWidth, 'innerWidth:', window.innerWidth);
```
**Do not commit if `scrollWidth > innerWidth`.** Fix the overflowing element first.

---

### 5.6 Playwright Screenshots vs. Real Phone — Why They Differ (Critical)

Playwright running inside VS Code on a Mac desktop is **not** a real phone. Screenshots can appear "responsive and working" while the actual phone experience is broken. Understand why before trusting any Playwright screenshot.

#### Why Playwright screenshots look narrower than expected
- Playwright headless Chromium defaults to `deviceScaleFactor: 2` (Retina). A viewport set to `width: 390` produces a **780×1688 px PNG**, but `window.innerWidth` may report 275 px, not 390 px, because `scrollbar-gutter: stable` on `html` consumes ~15 px and the headless window has a minimum size constraint.
- `setViewportSize()` calls do not always persist across `page.goto()` in the tool sandbox. Always re-verify `window.innerWidth` after navigation before trusting dimensional checks.
- The tool renders in a desktop Chrome process — no iOS Safari rendering engine, no rubber-band scrolling, no `safe-area-inset` behavior.

#### The #1 failure mode
A Playwright screenshot shows the nav bar, sections, and product grid correctly proportioned. You conclude "responsive is working." Meanwhile, on a real iPhone:
- The hero section is 1,200+ px tall because a CSS rule made an absolutely-positioned element flow statically.
- The horizontal product grid overflows because `minmax(280px, 1fr)` can't fit two columns in 375 px.
- The logo is 0 px wide because `flex-shrink` is not set.

None of these show up in Playwright screenshots if the headless viewport is already narrower than the breakpoint being tested.

#### Required practice
Playwright is the first-pass QA tool; real-device testing is the required final sign-off for mobile responsiveness.

1. **Always test on a real device before declaring mobile "done".** Use Safari > `certpeptides.com` directly, or use Chrome DevTools device emulation on your phone via Remote Debugging.
2. **Use the overflow check script** (§5.5.5) — it catches issues that screenshots miss.
3. **Set `await page.setViewportSize({ width: 390, height: 844 })` AND verify** `window.innerWidth === 390` before trusting any Playwright mobile check. If it reports a different width, the check is invalid.
4. **Do not spend tokens analyzing Playwright screenshot dimensions.** If a screenshot looks wrong, run the JS overflow check and test on a real device. Screenshots are for quick visual confirmation of layout intent, not pixel-accurate mobile QA.

---

## 6. Tools & Resources (Approved Stack)
- **Accessibility**: axe DevTools, WAVE, Lighthouse, Pa11y, NVDA/VoiceOver testing, Stark (Figma plugin).
- **Security**: OWASP ZAP, Burp Suite, Snyk, Dependabot, SSL Labs, SecurityHeaders.com, Mozilla Observatory, Cloudflare.
- **SEO**: Google Search Console, Analytics 4, Lighthouse, Screaming Frog, Ahrefs/Semrush, Schema Markup Generator, Rich Results Test.
- **Performance**: WebPageTest, GTmetrix, Chrome DevTools, Calibre, Treo.sh.
- **Content**: Grammarly (or ProWritingAid), Hemingway Editor, SurferSEO/Frase (content optimization).
- **Hosting/CDN**: Cloudflare (Pages + Workers + R2), Vercel, AWS (Amplify + CloudFront + WAF), Netlify (with functions).

---

## 7. Compliance & Legal
- Accessibility statement + VPAT (Voluntary Product Accessibility Template) available.
- Privacy Policy, Terms, Cookie Policy (updated for latest regulations).
- If e-commerce/payments: PCI DSS SAQ compliance.
- Regular legal review of content (claims, disclaimers).

---

**Final Mandate**: Every line of code, every piece of content, every configuration must contribute to **WCAG perfection**, **military-grade security**, and **unbeatable SEO**. No compromises. Sites built to this standard will rank #1, convert at industry-leading rates, and serve every user equitably while withstanding sophisticated attacks.

**Version**: 2026.04 | **Last Reviewed**: April 28, 2026 (test #5) | **Next Review**: Quarterly or after major Google/Core updates.

*This guide is living — update immediately when Google, W3C, or security standards evolve.*