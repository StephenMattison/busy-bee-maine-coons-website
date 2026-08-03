/**
 * POST /api/subscribe — Busy Bee Hive newsletter
 *
 * Stores + routes signups so you can run drip campaigns.
 *
 * Cloudflare Pages → Settings → Environment variables (Production):
 *   MAILERLITE_API_KEY     (recommended for lists + automations/drips)
 *   MAILERLITE_GROUP_ID    (optional group/list id)
 *   RESEND_API_KEY         (optional: admin notify + confirmation email)
 *   NEWSLETTER_NOTIFY_TO   (optional: your inbox, e.g. stephen@…)
 *   NEWSLETTER_FROM        (optional: verified Resend from, e.g. Hive <hello@cooncatcentral.com>)
 *
 * Optional KV binding (Functions → Bindings):
 *   Variable name: NEWSLETTER  →  a KV namespace
 *   Keys: Busy_Bee_Hive:{email}  →  JSON subscriber record
 *
 * Full setup: NEWSLETTER-SETUP.md in repo root.
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    },
  });
}

async function addMailerLite(env, email, fields) {
  if (!env.MAILERLITE_API_KEY) return { skipped: true };
  const payload = {
    email,
    status: 'active',
    fields: {
      source: fields.source || 'website',
      path: fields.path || '',
      brand: 'Busy Bee Maine Coons',
    },
  };
  if (env.MAILERLITE_GROUP_ID) {
    payload.groups = [env.MAILERLITE_GROUP_ID];
  }
  const res = await fetch('https://connect.mailerlite.com/api/subscribers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      Authorization: `Bearer ${env.MAILERLITE_API_KEY}`,
    },
    body: JSON.stringify(payload),
  });
  // 200/201 created/updated, 409 often already exists
  if (res.ok || res.status === 409) {
    return { ok: true, status: res.status };
  }
  const text = await res.text();
  console.error('[subscribe] MailerLite error', res.status, text.slice(0, 400));
  return { ok: false, status: res.status, body: text.slice(0, 200) };
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
        `New Busy Bee Hive subscriber`,
        `Email: ${email}`,
        `Source: ${fields.source || 'unknown'}`,
        `Path: ${fields.path || ''}`,
        `Time: ${new Date().toISOString()}`,
      ].join('\n'),
    }),
  }).catch((err) => console.error('[subscribe] notify failed', err));
}

async function sendWelcome(env, email) {
  if (!env.RESEND_API_KEY || env.NEWSLETTER_SEND_WELCOME !== '1') return;
  const from = env.NEWSLETTER_FROM || 'Busy Bee Hive <onboarding@resend.dev>';
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from,
      to: [email],
      subject: 'Welcome to the Busy Bee Hive 🐝',
      text: [
        'Welcome to the Busy Bee Hive!',
        '',
        'You’re on the list for:',
        '• First look at new Maine Coon litters (before public posts)',
        '• Practical care tips for giant-breed cats',
        '• A welcome offer on oversized gear in our shop',
        '',
        'Browse available kittens: https://cooncatcentral.com/kittens',
        'Care guides: https://cooncatcentral.com/care',
        '',
        'You can unsubscribe anytime from future emails.',
        '— Busy Bee Maine Coons',
      ].join('\n'),
    }),
  }).catch((err) => console.error('[subscribe] welcome failed', err));
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

  // Optional KV store (exportable backup + rate limit)
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

  // Primary ESP for drips / campaigns
  const ml = await addMailerLite(env, email, { source, path });
  if (ml && ml.ok === false && env.MAILERLITE_API_KEY) {
    // Still accept signup locally; surface soft error only if nothing else stored
    if (!env.NEWSLETTER) {
      return json({
        ok: false,
        error: 'We could not complete your subscription right now. Please try again.',
      }, 502);
    }
  }

  // Fire-and-forget admin + optional welcome
  const side = Promise.all([
    notifyAdmin(env, email, { source, path }),
    sendWelcome(env, email),
  ]);
  // Workers may cut off after response; await briefly
  try {
    await Promise.race([
      side,
      new Promise((r) => setTimeout(r, 2500)),
    ]);
  } catch { /* ignore */ }

  return json({ ok: true, message: 'Subscribed' });
}

export async function onRequest() {
  return json({ ok: false, error: 'Method not allowed.' }, 405);
}
