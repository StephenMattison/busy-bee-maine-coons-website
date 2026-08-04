/**
 * POST /api/subscribe — Busy Bee Hive newsletter
 *
 * Primary ESP: Klaviyo (same pattern as Revenge Works).
 * Cloudflare Pages → Settings → Environment variables (Production):
 *   KLAVIYO_API_KEY   Private API key (pk_…) — only required secret
 *   KLAVIYO_LIST_ID   Optional; defaults to Busy Bee Hive list SzVGkq
 *
 * Optional:
 *   NEWSLETTER         KV binding — backup store + rate limit
 *   RESEND_API_KEY / NEWSLETTER_NOTIFY_TO / NEWSLETTER_FROM — email you on signup
 *   NEWSLETTER_SEND_WELCOME=1 — optional Resend welcome (Klaviyo Flow is better)
 *
 * Full setup: NEWSLETTER-SETUP.md
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
// Klaviyo API revision used on Revenge Works (stable for subscription bulk create)
const KLAVIYO_REVISION = '2023-12-15';

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    },
  });
}

// Busy Bee Hive list (klaviyo.com) — override with env KLAVIYO_LIST_ID if needed
const DEFAULT_KLAVIYO_LIST_ID = 'SzVGkq';

async function addKlaviyo(env, email, fields) {
  const apiKey = (env.KLAVIYO_API_KEY || '').trim();
  const listId = (env.KLAVIYO_LIST_ID || DEFAULT_KLAVIYO_LIST_ID || '').trim();
  if (!apiKey) return { skipped: true, reason: 'missing_api_key' };
  if (!listId) return { skipped: true, reason: 'missing_list_id' };

  let res;
  try {
    res = await fetch(
      'https://a.klaviyo.com/api/profile-subscription-bulk-create-jobs/',
      {
        method: 'POST',
        headers: {
          Authorization: 'Klaviyo-API-Key ' + apiKey,
          'Content-Type': 'application/json',
          Accept: 'application/json',
          revision: KLAVIYO_REVISION,
        },
        // Match Revenge Works payload shape (proven on same account pattern)
        body: JSON.stringify({
          data: {
            type: 'profile-subscription-bulk-create-job',
            attributes: {
              custom_source: 'Busy Bee Hive website',
              profiles: {
                data: [
                  {
                    type: 'profile',
                    attributes: {
                      email,
                      // Note: profile-subscription-bulk-create-jobs rejects `properties`
                      // on this revision — keep payload aligned with Revenge Works.
                      subscriptions: {
                        email: {
                          marketing: {
                            consent: 'SUBSCRIBED',
                            consented_at: new Date().toISOString(),
                          },
                        },
                      },
                    },
                  },
                ],
              },
            },
            relationships: {
              list: { data: { type: 'list', id: listId } },
            },
          },
        }),
      }
    );
  } catch (err) {
    console.error('[subscribe] Klaviyo fetch failed', err);
    return { ok: false, status: 0, body: String(err && err.message ? err.message : err) };
  }

  if (res.ok || res.status === 202 || res.status === 409) {
    return { ok: true, status: res.status };
  }
  const text = await res.text();
  console.error('[subscribe] Klaviyo error', res.status, text.slice(0, 500));
  return { ok: false, status: res.status, body: text.slice(0, 400) };
}

async function notifyAdmin(env, email, fields) {
  if (!env.RESEND_API_KEY || !env.NEWSLETTER_NOTIFY_TO) return;
  const from = env.NEWSLETTER_FROM || 'Busy Bee Hive <onboarding@resend.dev>';
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [env.NEWSLETTER_NOTIFY_TO],
      subject: `Hive signup: ${email}`,
      text: [
        'New Busy Bee Hive subscriber',
        `Email: ${email}`,
        `Source: ${fields.source || 'unknown'}`,
        `Path: ${fields.path || ''}`,
        `Time: ${new Date().toISOString()}`,
      ].join('\n'),
    }),
  }).catch((err) => console.error('[subscribe] notify failed', err));
}

export async function onRequestPost({ request, env }) {
  let payload;
  try {
    payload = await request.json();
  } catch {
    return json({ ok: false, error: 'Invalid request.' }, 400);
  }

  const email = String(payload?.email || '').trim().toLowerCase();
  const list = String(payload?.list || 'Busy_Bee_Hive').trim() || 'Busy_Bee_Hive';
  const source = String(payload?.source || 'inline').slice(0, 40);
  const path = String(payload?.path || '').slice(0, 200);

  if (!EMAIL_RE.test(email)) {
    return json({ ok: false, error: 'Please enter a valid email address.' }, 422);
  }

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const ua = (request.headers.get('User-Agent') || '').slice(0, 200);
  const record = {
    email,
    list,
    source,
    path,
    subscribedAt: new Date().toISOString(),
    ip,
    ua,
  };

  if (env.NEWSLETTER) {
    try {
      const rateKey = `ratelimit:${ip}`;
      const rateData = await env.NEWSLETTER.get(rateKey, { type: 'json' });
      if (rateData && rateData.count >= 8) {
        return json({ ok: false, error: 'Too many requests. Please try again later.' }, 429);
      }
      const existingKey = `${list}:${email}`;
      const existing = await env.NEWSLETTER.get(existingKey);
      if (!existing) {
        await env.NEWSLETTER.put(existingKey, JSON.stringify(record));
      }
      const newCount = rateData ? rateData.count + 1 : 1;
      await env.NEWSLETTER.put(rateKey, JSON.stringify({ count: newCount }), {
        expirationTtl: 3600,
      });
    } catch (err) {
      console.error('[subscribe] KV error', err);
    }
  } else {
    console.log('[subscribe]', JSON.stringify(record));
  }

  const klaviyo = await addKlaviyo(env, email, { source, path });
  if (klaviyo.skipped) {
    console.warn('[subscribe] Klaviyo skipped:', klaviyo.reason || 'missing config');
    if (!env.NEWSLETTER) {
      return json({
        ok: false,
        error: 'Newsletter is not configured yet. Please try again later.',
        code: klaviyo.reason || 'klaviyo_skipped',
      }, 503);
    }
  } else if (klaviyo.ok === false) {
    // Still succeed if KV stored; otherwise fail so visitor can retry
    if (!env.NEWSLETTER) {
      return json({
        ok: false,
        error: 'We could not complete your subscription right now. Please try again.',
        code: 'klaviyo_error',
        klaviyoStatus: klaviyo.status || 0,
        // Safe short hint for dashboard debugging (no API key). Remove once stable.
        detail: typeof klaviyo.body === 'string' ? klaviyo.body.slice(0, 240) : '',
      }, 502);
    }
  }

  try {
    await Promise.race([
      notifyAdmin(env, email, { source, path }),
      new Promise((r) => setTimeout(r, 2000)),
    ]);
  } catch { /* ignore */ }

  return json({ ok: true, message: 'Subscribed' });
}

export async function onRequest() {
  return json({ ok: false, error: 'Method not allowed.' }, 405);
}
