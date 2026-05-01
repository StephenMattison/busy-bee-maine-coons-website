# Strict Per-Site Compliance Audit & Remediation Procedure
**Post SITE-GUIDE Update**

**Applies to:** Every target site folder / repository after a SITE-GUIDE propagation.  
**Strict Mode:** Uses `git pull --ff-only` to guarantee linear history and immediate failure on any divergence.

---

## Prerequisites
- You are in the **root of the specific site folder**.
- The central `StephenMattison/site-guide` Propagate workflow has completed successfully (green) and Sync PRs have been merged.
- You have the latest `SITE-GUIDE.md` (either pulled via the sync PR or present locally).

---

## Step-by-Step Instructions

### 1. Sync with Upstream (Mandatory First Step)
```bash
git pull --ff-only origin main
```

**If blocked by local changes (Step 7):**
- **STOP immediately.**
- Report the exact error message.
- Safest resolution path:
  1. `git status` to identify conflicting files.
  2. Stash or commit local work: `git stash` or `git commit -am "WIP: local changes before SITE-GUIDE sync"`.
  3. Re-run `git pull --ff-only origin main`.
  4. Re-apply stashed changes if needed: `git stash pop`.
- Only proceed after a clean fast-forward pull.

### 2. Full Compliance Audit
Perform a **complete audit** against the latest `SITE-GUIDE.md` (or the propagated controls).

**Key Control Areas (no omissions allowed):**
- Security headers hardening (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, etc.)
- CSP alignment (Content-Security-Policy – strictest viable policy, no `'unsafe-inline'` or `'unsafe-eval'` where avoidable)
- Removal of inline event handlers (`onclick`, `onload`, etc.) and inline `<script>` / `<style>` blocks
- CORS origin restriction (whitelist only trusted origins; no `*` in production)
- Accessibility launch-gate requirements (WCAG 2.2 AA minimum, ARIA labels, keyboard navigation, color contrast, focus management)
- SEO / Technical launch-gate requirements (meta tags, structured data, canonical URLs, sitemap, robots.txt, Core Web Vitals readiness)
- Any required JS / HTML / config refactors (e.g., nonce-based scripts, externalized handlers, environment-specific configs)

**Audit Method:**
- Use automated scanners where available (Lighthouse, axe-core, CSP evaluator, securityheaders.com, etc.).
- Manual code review of all changed files from the sync.
- Cross-reference every requirement listed in `SITE-GUIDE.md`.

### 3. Implement All Required Controls
- Address **every** failing or missing control.
- Make **no omissions** — even if a control seems minor.
- Prefer centralized solutions (e.g., shared header component, global CSP meta or HTTP header config) over per-page fixes.
- Document any intentional deviations with clear justification in code comments or a `COMPLIANCE.md` note.

### 4. Thorough Validation & Reporting
For **each check**, report **Pass / Fail** with evidence:

| Check Category                  | Status | Evidence / Notes                          | Remediation Applied                  |
|---------------------------------|--------|-------------------------------------------|--------------------------------------|
| Security Headers                |        |                                           |                                      |
| CSP Policy                      |        |                                           |                                      |
| No Inline Handlers/Scripts      |        |                                           |                                      |
| CORS Configuration              |        |                                           |                                      |
| Accessibility (WCAG 2.2 AA)     |        |                                           |                                      |
| SEO / Technical Launch Gates    |        |                                           |                                      |
| JS/HTML/Config Refactors        |        |                                           |                                      |
| Other SITE-GUIDE Requirements   |        |                                           |                                      |

**Validation Tools Recommended:**
- `securityheaders.com` or `curl -I` for headers
- Lighthouse CI (accessibility + SEO + performance)
- CSP violation reports in browser console / Reporting API
- Manual keyboard + screen-reader testing
- `git diff` to confirm only intended changes

### 5. Commit & Push Fixes
```bash
git add -A
git commit -m "chore: SITE-GUIDE compliance remediation (strict)

- Security headers hardened
- CSP aligned (no unsafe-inline)
- Inline handlers removed
- CORS restricted
- Accessibility & SEO gates passed
- Refs: <link to central SITE-GUIDE PR or commit>
"
git push origin main
```

### 6. Final Report (Return This Information)
After completion, provide:

**Exact files changed:**
- List every modified/added/deleted file with short description.

**Validation results:**
- Full table from Step 4 (all Pass after remediation).

**Residual risks:**
- Any controls that could not be fully automated or that have known limitations.
- Any manual follow-ups required (e.g., DNS changes, CDN config, stakeholder sign-off).

**Manual follow-ups:**
- Items that require human action outside this repo (e.g., updating external services, re-running CI after merge, notifying team).

---

## Strict Blocker Handling (git pull --ff-only)

**If the command fails** (typical messages):
- `fatal: Not possible to fast-forward, aborting.`
- `error: Your local changes to the following files would be overwritten by merge:`

**STOP immediately** and report in your response:
1. The **exact full error message**.
2. Output of `git status`.
3. Output of `git log --oneline -5` (shows any divergence).

**Safest resolution path (preferred order):**

1. **Uncommitted local changes present** (most common):
   ```bash
   git stash push -m "WIP: before strict SITE-GUIDE pull"
   git pull --ff-only origin main
   git stash pop
   ```

2. **Local branch has diverged** (you have extra commits):
   - **Do NOT force anything.**
   - Create safety branch first: `git branch backup/pre-strict-$(date +%Y%m%d-%H%M)`
   - Then decide: stash + reset, or rebase, or ask maintainer.

3. **After any resolution**, re-run the full compliance steps from the top.

**Golden Rule:**  
Never use `--force` or `git push --force` during SITE-GUIDE propagation unless you have explicit written authorization from the repository owner.

---

**Remember:** The goal is **100% compliance with zero omissions** and a **clean linear history**. The `--ff-only` flag protects the entire fleet from messy merge commits. Treat every SITE-GUIDE control as a hard launch gate.

---

## Mandatory Post-Audit Follow-Through (Do Not Skip)

After remediation, validation, commit, and push are complete, perform the live checks below yourself and include evidence in the final report. Do not hand these steps back to the user unless blocked by permissions.

### A. Verify Production Headers and Redirects
Run checks against the canonical production domain:

```bash
curl -sSI https://www.example.com/
curl -sSI https://example.com/
curl -sSI https://www.example.com/contact/
curl -sSI https://www.example.com/cart/
```

Confirm and report:
- Apex to www redirect behavior is correct.
- Hardened headers are present (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, CORP, restricted CORS, Vary: Origin).

### B. Verify Live HTML Output on Key Pages
Check homepage, contact page, cart page, and one error page in production HTML output:

```bash
curl -sL https://www.example.com/ | rg -n "robots|\?v=|data-validate-form|site-announcer"
curl -sL https://www.example.com/contact/ | rg -n "robots|\?v=|data-validate-form|aria-required=\"true\"|form__honeypot"
curl -sL https://www.example.com/cart/ | rg -n "robots|\?v="
curl -sL https://www.example.com/404.html | rg -n "robots|\?v="
```

Confirm and report:
- Correct `robots` directives (cart + error pages `noindex, nofollow`).
- Versioned assets are present in live markup (`?v=` hashes).
- Accessibility/form markup changes are present where required.

### C. Safely Verify Live Form Endpoint (If Present)
For contact/lead endpoints, perform a safe verification that does not send real notifications when possible (for example, honeypot path):

```bash
curl -sS -D - -o /tmp/site-contact-check.out -X POST https://www.example.com/contact/ \
   --data-urlencode 'name=Test User' \
   --data-urlencode 'email=test@example.com' \
   --data-urlencode 'subject=General' \
   --data-urlencode 'message=Compliance verification test' \
   --data-urlencode 'website=bot-filled'
```

Confirm and report:
- Endpoint responds successfully.
- Security headers remain present on dynamic response.
- No unintended email/notification side effect occurred (or explicitly state if not avoidable).

### D. Final Closeout Requirement
Your final response must include:
- Commands executed for live verification.
- Key response lines (status codes, critical headers, and key HTML evidence lines).
- Pass/fail for each live check.
- Anything truly not automatable from repo context (for example, account-locked external consoles).

Default rule: complete as much post-audit follow-through as possible yourself before returning results.