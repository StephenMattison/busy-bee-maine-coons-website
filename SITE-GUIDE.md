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
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(self), usb=(), interest-cohort=(), accelerometer=(), gyroscope=(), magnetometer=(), ambient-light-sensor=(), autoplay=(self), encrypted-media=(), fullscreen=(self)
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
- Only widen ACAO to `*` for a specific path prefix that is genuinely a public API (e.g. `/api/public/*`) — never globally.
- After deploy, verify: `curl -sI https://<canonical-domain>/ | grep -i access-control` — it must show your domain, not `*`.

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
- **Hreflang** (if multilingual): Proper implementation.

### 3.3 Technical SEO (Foundation for Crawlability & Rankings)
- **Core Web Vitals** (must pass "Good" thresholds):
  - LCP ≤ 2.5s (optimize hero images, critical CSS, font-display:swap, preconnect).
  - INP (Interaction to Next Paint, replacing FID) ≤ 200ms (minimize main-thread work, defer non-critical JS, use web workers).
  - CLS ≤ 0.1 (reserve space for images/ads, avoid layout shifts from fonts/animations).
- **Page Speed**:
  - Lighthouse Performance ≥95 (ideally 100). Use CDN (Cloudflare, Fastly, Akamai), Brotli/Gzip, image optimization (Squoosh, ImageOptim, Cloudinary), critical CSS inlining, JS code-splitting, tree-shaking.
  - Preload key resources (`<link rel="preload">` for fonts, LCP image).
  - HTTP/3, early hints where supported.
- **Mobile-First & Responsive**: Google uses mobile index primarily. Test on real devices. Touch targets ≥44x44px, no horizontal scroll at 320px.
- **Crawlability**:
  - `robots.txt` allows all important paths, blocks admin/login.
  - XML Sitemap (auto-generated, submitted via Search Console, <50k URLs or split).
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
1. **Local Development**: Dockerized environments, hot reload, linting (ESLint + Stylelint + Prettier), TypeScript strict mode.
2. **CI/CD Pipeline** (GitHub Actions / GitLab CI):
   - Automated tests (unit, integration, E2E with Playwright/Cypress — include a11y and visual regression).
   - Security scanning (SAST, dependency, container).
   - Lighthouse CI + axe-core in pipeline (fail build on regression).
   - Accessibility + SEO + Security audits on every PR.
3. **Staging Environment**: Mirror production exactly. Full manual + automated QA including screen reader, keyboard, performance under load.
4. **Production Deployment**: Blue-green or canary. Feature flags for risky changes. Rollback <5 min.
5. **Post-Launch**: 24/7 monitoring, weekly audits, monthly comprehensive review (WCAG, security headers, SEO health, Core Web Vitals trends).

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