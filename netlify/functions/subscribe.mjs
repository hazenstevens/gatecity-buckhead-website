// Newsletter signup: the website's email forms POST {email, fname, hp} here.
// We add the person to the GateCity Buckhead Mailchimp audience through the API
// (no Mailchimp captcha page), so the browser always lands on /thanks, where the
// Google Ads "Email signup" conversion fires. Bot protection: a hidden honeypot field,
// a minimum time on page before submit, and a check that the email's domain can
// actually receive mail (MX record). No confirmation email (Hazen, Nov 11): new contacts
// are subscribed right away. Existing contacts keep their status. Tagged "Website".
// Needs MAILCHIMP_API_KEY in Netlify.
import { createHash } from "node:crypto";
import { resolveMx } from "node:dns/promises";
const MC_LIST = process.env.MAILCHIMP_LIST_ID || "cdb1521460";
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "Content-Type": "application/json" } });

export default async (req) => {
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let b; try { b = await req.json(); } catch { return json({ error: "bad request" }, 400); }
  if (b.hp) return json({ ok: true }); // honeypot filled: pretend success, do nothing
  if (typeof b.t === "number" && b.t < 3000) return json({ ok: true }); // submitted under 3s after load: a bot
  const email = String(b.email || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || email.length > 200) return json({ error: "Please enter a valid email address." }, 400);
  const mx = await resolveMx(email.split("@")[1]).catch(() => []);
  if (!mx.length) return json({ error: "That email address doesn't look right. Please check it and try again." }, 400);
  const key = process.env.MAILCHIMP_API_KEY;
  if (!key) return json({ error: "not configured" }, 503);
  const dc = key.split("-")[1] || "us3";
  const base = `https://${dc}.api.mailchimp.com/3.0/lists/${MC_LIST}/members/${createHash("md5").update(email.toLowerCase()).digest("hex")}`;
  const headers = { Authorization: "Basic " + Buffer.from("gcb:" + key).toString("base64"), "Content-Type": "application/json" };
  const merge = {}; if (b.fname) merge.FNAME = String(b.fname).slice(0, 60);
  const r = await fetch(base, { method: "PUT", headers, body: JSON.stringify({ email_address: email, status_if_new: "subscribed", merge_fields: merge }) });
  if (!r.ok) { const t = await r.json().catch(() => ({})); return json({ error: t.detail || "signup failed" }, 502); }
  await fetch(base + "/tags", { method: "POST", headers, body: JSON.stringify({ tags: [{ name: "Website", status: "active" }] }) }).catch(() => {});
  return json({ ok: true });
};
export const config = { path: "/api/subscribe" };
