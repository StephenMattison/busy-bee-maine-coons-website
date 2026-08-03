# Busy Bee Hive — newsletter setup (emails + drip)

## What the site does now

1. **Footer / mid-page “Join the Hive”** on every page that includes the newsletter block.
2. **Exit-intent popup** (“Before you go…”) on desktop mouse-leave, plus a mobile soft prompt after scroll + time.
3. Browser posts to **`POST /api/subscribe`** (Cloudflare Pages Function in `public/functions/api/subscribe.js`).

Until you connect an ESP (email service), signups only hit the Function logs (and optional KV). Wire the steps below once so you can **export every address** and run **drip automations**.

---

## Recommended stack (easiest for you)

| Layer | Tool | Why |
|-------|------|-----|
| **List + drip automations** | **[MailerLite](https://www.mailerlite.com/)** (free tier is enough to start) | Simple UI, groups, automations, CSV export — best “non-dev” drip tool |
| **Edge API** | Cloudflare Pages Function (already live) | Captures email from the site |
| **Optional backup list** | Cloudflare **KV** binding `NEWSLETTER` | Same pattern as CertPeptides; exportable backup |
| **Optional instant ping** | **Resend** → your inbox | Email yourself on every signup |
| **Optional welcome email** | Resend (`NEWSLETTER_SEND_WELCOME=1`) | One-time welcome from a verified domain |

**Not required:** Supabase, Zoho (unless you already live in Zoho Mail for campaigns).  
**Zoho** is fine for reading mail; it is *not* the easiest drip automation layer for this funnel.  
**Supabase** is overkill just to store newsletter emails when MailerLite already is the CRM.

---

## Step 1 — MailerLite (primary: where you “access all emails”)

1. Create a free MailerLite account.
2. **Subscribers → Groups** → create group e.g. `Busy Bee Hive`.
3. Copy the **Group ID** (in group settings / URL — numeric string).
4. **Integrations → API** → create an API token.
5. In **Cloudflare Dashboard**:
   - Pages → project **`busy-bee-maine-coons-website`** (or your exact project name)
   - **Settings → Environment variables** (Production):

| Variable | Value |
|----------|--------|
| `MAILERLITE_API_KEY` | your API token |
| `MAILERLITE_GROUP_ID` | group id (optional but recommended) |

6. **Save** and **retry deployment** (or push any commit) so Functions pick up env vars.

### Where you access contacts

- MailerLite → **Subscribers** (filter by group `Busy Bee Hive`)
- Export: Subscribers → **Export** → CSV anytime
- **Automations** → create a drip (e.g. Day 0 welcome, Day 2 care guide, Day 5 litter alert tip, Day 10 shop offer)

---

## Step 2 — Optional Cloudflare KV backup

Same idea as CertPeptides:

1. Cloudflare → **Workers & Pages → KV** → Create namespace `busybee-newsletter`.
2. Pages project → **Settings → Functions → KV namespace bindings**:
   - Variable name: **`NEWSLETTER`**
   - Namespace: `busybee-newsletter`
3. Redeploy.

Keys look like: `Busy_Bee_Hive:person@email.com`  
Values: JSON with `email`, `source` (`footer` / `exit`), `path`, `subscribedAt`, etc.

Export: Workers KV → open namespace → list/export via dashboard or API.

---

## Step 3 — Optional Resend (notify you + welcome email)

You already use Resend on other sites (e.g. Lunar contact).

| Variable | Purpose |
|----------|---------|
| `RESEND_API_KEY` | Send mail |
| `NEWSLETTER_NOTIFY_TO` | Your address — get a ping on each signup |
| `NEWSLETTER_FROM` | Verified sender, e.g. `Busy Bee Hive <hello@yourdomain.com>` |
| `NEWSLETTER_SEND_WELCOME` | Set to `1` to email the subscriber a welcome |

Verify the sending domain in Resend first (SPF/DKIM).

---

## Step 4 — Test

1. Open https://cooncatcentral.com/  
2. Join with a real email in the gold Hive strip.  
3. Confirm success message.  
4. Check MailerLite subscribers.  
5. Clear site data / private window: move mouse out top of page → exit popup should appear once per session.  
6. Cart/account pages suppress the popup so checkout is not interrupted.

---

## Privacy / compliance notes

- Footer + popup say free, no sell, unsubscribe anytime — keep that accurate.
- In MailerLite, enable **double opt-in** if you want stricter GDPR practice (optional for US-only).
- Do not promise “10% off” unless the shop code exists and works; current copy says **welcome offer** — set a real code in MailerLite welcome email when ready.

---

## Architecture (one glance)

```
Visitor form / exit popup
        │
        ▼
POST /api/subscribe   (Pages Function)
        │
        ├──► MailerLite  (list + drips)  ← you work here daily
        ├──► KV NEWSLETTER (optional backup)
        └──► Resend (optional: notify you / welcome email)
```

If only one thing is set up, make it **MailerLite** — that is where you manage communication and drip campaigns.
