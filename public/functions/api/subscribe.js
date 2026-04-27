/**
 * POST /api/subscribe
 * Newsletter signup endpoint (Cloudflare Pages Function).
 *
 * Wire up an actual ESP later (ConvertKit / Mailchimp / Resend) by reading
 * env.ESP_API_KEY from Pages → Settings → Environment variables.
 */
export async function onRequestPost({ request, env }) {
  const headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
  };

  let payload;
  try {
    payload = await request.json();
  } catch {
    return new Response(JSON.stringify({ ok: false, error: 'invalid_json' }), { status: 400, headers });
  }

  const email = (payload?.email || '').trim().toLowerCase();
  // RFC-5322-lite, sufficient for client + server validation.
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  if (!valid) {
    return new Response(JSON.stringify({ ok: false, error: 'invalid_email' }), { status: 422, headers });
  }

  // TODO: forward to ESP. For now, log and accept.
  console.log('[subscribe]', email);

  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}

export function onRequest() {
  return new Response('Method Not Allowed', { status: 405, headers: { Allow: 'POST' } });
}
