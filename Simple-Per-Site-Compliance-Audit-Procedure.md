# Simple Per-Site Compliance Audit & Remediation Procedure
**For Brochure-Type Websites — Post SITE-GUIDE Update**

**Applies to:** Simple brochure-style sites after SITE-GUIDE propagation.  
**Goal:** Lightweight compliance focused on the essentials.

---

## Step-by-Step Instructions

### 1. Strict Sync with Upstream (First Step)
```bash
git pull --ff-only origin main
```

**If blocked:** Stop and report the exact error + `git status`. Safest fix is usually `git stash` → pull → `git stash pop`.

### 2. Audit Against Latest Site Guide
Review the site against the current `SITE-GUIDE.md` requirements. Focus on:

- Security headers (HSTS, X-Frame-Options, etc.)
- CSP alignment (no unsafe-inline where possible)
- CORS origin restriction
- Removal of inline JS handlers/scripts
- Core accessibility (WCAG basics, ARIA, keyboard nav)
- Core SEO/technical launch gates (meta, sitemap, canonicals)

### 3. Apply All Required Missing Updates
Implement **every** missing control listed in the site guide. Prioritize centralized fixes (shared components, global config) over per-page changes.

### 4. Validate Changes
Run available checks:
- Lighthouse (Accessibility + SEO scores)
- Browser console for CSP violations
- `securityheaders.com` or `curl -I` for headers
- Manual spot-check of key pages

### 5. Commit & Push
```bash
git add -A
git commit -m "chore: simple SITE-GUIDE compliance updates

- Headers, CSP, CORS, inline JS, accessibility & SEO gates addressed
- Refs: central SITE-GUIDE"
git push origin main
```

### 6. Return Short Summary
Provide:
- **Changes made** (list of files or key updates)
- **Validation results** (pass/fail highlights)
- **Any follow-ups** needed (manual steps, stakeholder review, etc.)

**If git pull --ff-only is blocked:** Report the exact blocker and the safest next step (usually stash first).

---

**Remember:** Keep it simple and focused. Aim for clean, maintainable fixes that satisfy the core launch gates without over-engineering.

---

## Mandatory End-of-Run Follow-Through (Required)

After fixes are implemented, validated, committed, and pushed, run these live checks yourself before returning final results. Do not leave these to the user unless blocked by access.

### 1. Production Headers + Redirects
```bash
curl -sSI https://www.example.com/
curl -sSI https://example.com/
curl -sSI https://www.example.com/contact/
curl -sSI https://www.example.com/cart/
```

Confirm:
- Canonical redirect behavior is correct.
- Required security headers and restricted CORS are live.

### 2. Production HTML Spot Checks
```bash
curl -sL https://www.example.com/ | rg -n "robots|\?v=|site-announcer"
curl -sL https://www.example.com/contact/ | rg -n "data-validate-form|aria-required=\"true\"|form__honeypot|\?v="
curl -sL https://www.example.com/cart/ | rg -n "robots|\?v="
curl -sL https://www.example.com/404.html | rg -n "robots|\?v="
```

Confirm:
- Versioned assets are present in live output.
- Correct `robots` directives are present (including cart/error noindex requirements).
- Required form/accessibility markup is present where applicable.

### 3. Safe Live Form Check (If Site Has Contact Form)
Use a non-delivery-safe path (such as honeypot) when available:

```bash
curl -sS -D - -o /tmp/site-contact-check.out -X POST https://www.example.com/contact/ \
	--data-urlencode 'name=Test User' \
	--data-urlencode 'email=test@example.com' \
	--data-urlencode 'subject=General' \
	--data-urlencode 'message=Compliance verification test' \
	--data-urlencode 'website=bot-filled'
```

Confirm:
- Endpoint responds successfully with expected security headers.
- Test path avoids unintended outbound notifications when possible.

### 4. Required Final Report Content
Include:
- Live-check commands run.
- Key evidence lines from responses.
- Pass/fail for each live check.
- Any truly manual/account-locked items that could not be completed.

Default behavior: complete the post-audit follow-through yourself and return finished verification, not a to-do list for the user.