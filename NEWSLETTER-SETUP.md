# Busy Bee Hive — newsletter setup (Klaviyo)

**Status as of last code deploy:** Site UI + API are ready.  
**Still needs you (when you have 10 minutes):** create a Klaviyo list + paste 2 secrets into Cloudflare.

You can skip this for now. Signups still work on the site; without the Klaviyo keys they only hit Cloudflare Function logs until you connect the account.

---

## Already done (no action)

- Footer **Hive** signup strip (benefits + form)
- **Exit-intent** popup (“Before you go…”)
- `POST /api/subscribe` on Cloudflare Pages
- Code pushes profiles to **Klaviyo** when env vars exist (same pattern as Revenge Works)

---

## When you have time (checklist)

### 1. Klaviyo.com (~3 min)

1. Log in at [klaviyo.com](https://www.klaviyo.com)
2. **Audience → Lists & segments → Create list**  
   Name: **Busy Bee Hive** (keep it separate from Revenge Works)
3. Open that list → copy the **List ID** (short code in settings/URL)
4. **Settings → API keys → Create Private API key**  
   Or reuse your existing account private key (`pk_…`) if it already has list/profile permissions

### 2. Cloudflare (~3 min)

1. [Cloudflare Dashboard](https://dash.cloudflare.com) → **Workers & Pages**
2. Open the Busy Bee project (`busy-bee-maine-coons-website` / cooncatcentral)
3. **Settings → Environment variables** → Production → **Add**:

| Name | Value |
|------|--------|
| `KLAVIYO_API_KEY` | your private key (`pk_…`) |
| `KLAVIYO_LIST_ID` | Busy Bee Hive list ID |

4. Save, then **Deployments → Retry deployment** (or any git push) so Functions see the new vars

### 3. Quick test (~2 min)

1. Open https://cooncatcentral.com/
2. Join the Hive with a real email you control
3. In Klaviyo → **Audience → Profiles** (or the list) → confirm the email appears
4. Optional: **Flows** → new flow triggered when someone is **added to list “Busy Bee Hive”** (welcome drip later)

---

## Where emails live once connected

| Want | Where |
|------|--------|
| All Hive emails | Klaviyo → list **Busy Bee Hive** / Profiles |
| Export CSV | List → export |
| Drip / welcome series | Klaviyo → **Flows** |
| One-off blasts | Klaviyo → **Campaigns** |

---

## Optional later (not required)

| Extra | Why |
|-------|-----|
| Cloudflare KV binding named `NEWSLETTER` | Backup store + rate limit |
| Resend `RESEND_API_KEY` + `NEWSLETTER_NOTIFY_TO` | Email *you* on each signup |

Drips are better as **Klaviyo Flows** than Resend one-offs.

---

## Architecture (for later)

```
Site form / exit popup
        →  POST /api/subscribe  (Pages Function)
        →  Klaviyo list “Busy Bee Hive”  ← you work here
```

**Bottom line:** Nothing critical is blocked. When you’re free, do the Klaviyo list + 2 Cloudflare env vars above and the Hive is fully live.
