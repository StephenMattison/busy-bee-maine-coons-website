# Busy Bee Hive — newsletter (Klaviyo)

## Short answer

**Yes — Klaviyo is the right tool for this.**  
You already use it on **Revenge Works** (`KLAVIYO_API_KEY` + `KLAVIYO_LIST_ID` on that Pages project). Busy Bee’s subscribe API is now wired the same way.

**I could not find your Klaviyo private key or list IDs in this repo** (they should live only in Cloudflare env / Klaviyo dashboard — good). You paste them into the Busy Bee Pages project once.

---

## What the site does

1. Footer **Hive** signup + **exit-intent** popup  
2. `POST /api/subscribe` (Cloudflare Pages Function)  
3. Creates/updates a **Klaviyo profile**, marks **email marketing consented**, adds them to your **list**

---

## Cloudflare env vars (Busy Bee project)

Pages → **`busy-bee-maine-coons-website`** (or your exact project) → **Settings → Environment variables** (Production):

| Variable | Value |
|----------|--------|
| `KLAVIYO_API_KEY` | Private API key from Klaviyo (starts with `pk_`) |
| `KLAVIYO_LIST_ID` | List ID for a list e.g. **Busy Bee Hive** |

Optional:

| Variable | Purpose |
|----------|---------|
| KV binding `NEWSLETTER` | Backup store + rate limit |
| `RESEND_API_KEY` + `NEWSLETTER_NOTIFY_TO` | Email *you* on each signup |
| `NEWSLETTER_FROM` | Verified Resend from-address |

Redeploy after saving env vars (or push any commit).

---

## Where to get keys in Klaviyo

1. **API key**  
   Klaviyo → **Settings → API keys** → Create **Private** API key  
   Scopes needed (minimum): profiles write, lists write, subscriptions write (or a full private key while testing)

2. **List ID**  
   **Audience → Lists & segments** → create list **Busy Bee Hive** (or use an existing list)  
   Open the list → **Settings** (or URL) → copy **List ID** (short alphanumeric)

You can reuse the **same private API key** as Revenge Works if that key is account-wide; use a **separate list** for Busy Bee so drips stay clean.

---

## Where you access contacts + drips

| Need | In Klaviyo |
|------|------------|
| See everyone | **Audience → Profiles** or your list |
| Export | List → **Manage list → Export** |
| Drip / welcome series | **Flows** → trigger = **Added to list** (Busy Bee Hive) or **Subscribed to email marketing** |
| Campaigns | **Campaigns** → send to that list |

Recommended first flow: **Welcome / Hive** — Day 0 welcome, Day 2 care guide link, Day 5 litter-alert pitch, Day 10 shop gear.

---

## Test checklist

1. Set env vars + redeploy  
2. Sign up on https://cooncatcentral.com with a real email  
3. Klaviyo → Profiles → find email, confirm list membership + email marketing = subscribed  
4. Exit-intent once per session (mouse out top of page)

---

## Architecture

```
Site form / exit popup
        │
        ▼
POST /api/subscribe  (Pages Function)
        │
        ├──► Klaviyo list + profile (drips/flows live here)
        ├──► KV NEWSLETTER (optional backup)
        └──► Resend notify (optional)
```

**MailerLite is not required** if you stay on Klaviyo.
