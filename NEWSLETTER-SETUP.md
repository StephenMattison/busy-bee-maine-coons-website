# Busy Bee Hive — newsletter (Klaviyo) — keep it simple

## Already done

| Item | Status |
|------|--------|
| Site forms + exit-intent popup | Live on cooncatcentral.com |
| Subscribe API | Live |
| Klaviyo list **Busy Bee Hive** | You created it |
| List ID | **`SzVGkq`** (built into the site as default) |

---

## One thing left (you)

Add **one** secret in Cloudflare. That’s it.

### Cloudflare (~2 minutes)

1. [dash.cloudflare.com](https://dash.cloudflare.com) → **Workers & Pages**
2. Open the Busy Bee / **cooncatcentral** Pages project  
3. **Settings → Environment variables** → **Production** → **Add**

| Name | Value |
|------|--------|
| `KLAVIYO_API_KEY` | Your Klaviyo **private** API key (`pk_…`) |

Where to get the key: Klaviyo → **Settings → API keys** → Private API key  
(Same key you use for Revenge Works is fine.)

4. **Save** → **Deployments → Retry deployment** (so the Function sees the key)

You do **not** need to set `KLAVIYO_LIST_ID` unless you change lists later — the site already uses **`SzVGkq`**.

---

## Test (30 seconds)

1. https://cooncatcentral.com/ → Join the Hive with your email  
2. Klaviyo → **Audience → Lists → Busy Bee Hive** → you should appear  

---

## Drips later (optional)

When you want automation: Klaviyo → **Flows** → trigger **Added to list → Busy Bee Hive**.

---

## Reminder

Until `KLAVIYO_API_KEY` is on Cloudflare, signups won’t reach Klaviyo. After that one env var + redeploy, you’re done.
