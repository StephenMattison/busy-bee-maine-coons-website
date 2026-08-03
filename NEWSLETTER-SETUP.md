# Busy Bee Hive → Klaviyo (simple)

**List already created:** Busy Bee Hive · List ID **`SzVGkq`** (site uses this automatically).

**You only need to add one secret in Cloudflare:** `KLAVIYO_API_KEY`

---

## Part A — Get your Klaviyo private API key (2 minutes)

1. Open **[https://www.klaviyo.com](https://www.klaviyo.com)** and sign in.
2. Click your **account menu** (bottom-left or top-right, depending on the new UI).
3. Go to **Settings**.
4. Open **API keys** (sometimes under **Account → API keys**).
5. Under **Private API Keys**:
   - If you already have a private key for Revenge Works / other sites, you can **reuse that same key** (copy it if you still have it saved; Klaviyo often won’t show the full key again after creation).
   - If not: click **Create Private API Key**.
     - Name it e.g. `Cloudflare Pages – Busy Bee`.
     - Access: prefer **Full Access** for simplicity, or grant **Lists, Profiles, Subscriptions** write access.
     - Create → **copy the key immediately** (starts with `pk_`).
6. Paste it somewhere temporary (Notes) until Cloudflare is done. Treat it like a password.

---

## Part B — Add the key in Cloudflare (the important part)

### B1. Open the right project

1. Open **[https://dash.cloudflare.com](https://dash.cloudflare.com)** and sign in (Stephen’s account).
2. In the left sidebar, click **Workers & Pages**  
   (If you don’t see it: click the **three-line menu** or search “Workers” in the top search bar.)
3. Click the **Pages** tab (or the list of projects — look for Pages sites).
4. Find and open the project for **Busy Bee / cooncatcentral.com**.  
   Likely name: **`busy-bee-maine-coons-website`**  
   (If unsure: open each project → **Custom domains** until you see **cooncatcentral.com**.)

### B2. Environment variables

1. Inside that project, click **Settings** (top tabs: Overview · Deployments · Metrics · Settings, etc.).
2. In the Settings left menu (or page sections), open **Environment variables**  
   (may appear under **Variables and Secrets** or **Functions** → **Environment variables** — Cloudflare renames this occasionally).
3. Make sure you are editing **Production** (not only Preview), if the UI offers both.
4. Click **Add** / **Add variable** / **Add environment variable**.
5. Enter exactly:

| Field | What to type |
|--------|----------------|
| **Variable name** | `KLAVIYO_API_KEY` |
| **Value** | your private key starting with `pk_…` |
| **Type** | **Secret** (if offered — hides the value later) or Encrypt / Encrypt and deploy |

6. **Do not** add `KLAVIYO_LIST_ID` unless you change lists later — the site already defaults to **`SzVGkq`**.
7. Click **Save** / **Save and deploy** if that button appears.

### B3. Make the Function use the new variable (required)

Environment variables often apply only after a **new deploy**.

Pick **one**:

**Option 1 — Retry last deploy (easiest)**  
1. Open the **Deployments** tab.  
2. On the latest Production deployment, open the **⋯** menu.  
3. Click **Retry deployment** (or **Redeploy**).  
4. Wait until status is **Success** (usually 1–3 minutes).

**Option 2 — Push any small commit**  
Any `git push` to `main` also redeploys (agents often do this for you).

### B4. Confirm it worked

1. Open **[https://cooncatcentral.com/](https://cooncatcentral.com/)** in a private/incognito window.
2. Scroll to the gold **Busy Bee Hive** box (or use the exit popup).
3. Subscribe with **your own email**.
4. You should see a success message on the site.
5. In Klaviyo: **Audience → Lists & segments → Busy Bee Hive** → open the list → your email should appear within a minute or two.

If the site says success but Klaviyo is empty:

- Confirm the variable name is exactly `KLAVIYO_API_KEY` (all caps, underscores).
- Confirm it’s on **Production**, not only Preview.
- Confirm you **redeployed** after saving.
- Cloudflare → project → **Deployments** → open the latest deploy → **Functions** / logs and look for `Klaviyo error` or `KLAVIYO_API_KEY … not set`.

---

## What you do **not** need

- MailerLite  
- Supabase  
- Zoho for the list  
- A second Klaviyo “mailer” account — one account, one list (**Busy Bee Hive**) is enough  
- Setting `KLAVIYO_LIST_ID` (unless you rename/recreate the list)

---

## Later (optional): drip emails

When you want automated follow-ups:

1. Klaviyo → **Flows** → **Create flow**  
2. Trigger: **Added to list** → **Busy Bee Hive**  
3. Add emails (welcome, care tip, litter alert, etc.) and turn the flow **Live**

No Cloudflare changes needed for flows.

---

## One-line summary

**Cloudflare → Workers & Pages → Busy Bee project → Settings → Environment variables → Production → add `KLAVIYO_API_KEY` = your `pk_…` key → Redeploy → test signup on cooncatcentral.com → check list Busy Bee Hive in Klaviyo.**
