// Christmas Eve registration: hands a website registration to Planning Center and Mailchimp.
// The browser saves the registration in Supabase (rpc christmas_register) and
// gets an id, then POSTs {id} here. This function reads it back from Supabase
// (nothing the browser sends is trusted), then:
//  1. Submits it to the Planning Center form "Christmas Eve 2026 Registration" (1375690)
//     with phone and party size. That form emails Hazen (notification list) and its
//     automation sends the guest the "Your spot is saved for Christmas Eve" email
//     (PCO email template, from Hazen). A profile note records the party size.
//  2. Adds the guest to the GateCity Buckhead Mailchimp audience (same list and
//     MAILCHIMP_API_KEY as /api/plan-visit): subscribed if new, existing contacts keep
//     their status (so past unsubscribes stay unsubscribed), tagged "Christmas Eve 2026",
//     "Recent Visitors", "GCB Weekly" and "Widest Audience". The form says so under the button.
// Results are recorded on the Supabase row (pco_status / pco_detail).
import { createHash } from "node:crypto";

const SB = "https://egccpqcdpmvkkgdunpuc.supabase.co";
const SB_KEY = "sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda";
const FORM = process.env.PCO_CHRISTMAS_FORM_ID || "1375690";
const F_PHONE = "11014488", F_PARTY = "11014489";
const NOTE_CATEGORY = process.env.PCO_VISIT_NOTE_CATEGORY || "248939"; // General
const PCO = "https://api.planningcenteronline.com/people/v2";
const MC_LIST = process.env.MAILCHIMP_LIST_ID || "cdb1521460";
const MC_TAGS = ["Christmas Eve 2026", "Recent Visitors", "GCB Weekly", "Widest Audience"];

function partySize(v) {
  const a = Number(v.adults) || 1, k = Number(v.kids) || 0;
  return `${a} adult${a == 1 ? "" : "s"}, ${k} kid${k == 1 ? "" : "s"} (party of ${a + k})`;
}

async function addToMailchimp(v) {
  const key = process.env.MAILCHIMP_API_KEY;
  const email = String(v.email || "").trim();
  if (!key) return "mc skipped (no key)";
  if (!email) return "mc skipped (no email)";
  try {
    const dc = key.split("-")[1] || "us3";
    const base = `https://${dc}.api.mailchimp.com/3.0/lists/${MC_LIST}/members/${createHash("md5").update(email.toLowerCase()).digest("hex")}`;
    const headers = { Authorization: "Basic " + Buffer.from("gcb:" + key).toString("base64"), "Content-Type": "application/json" };
    const merge = {};
    if (v.first_name) merge.FNAME = String(v.first_name).slice(0, 60);
    if (v.last_name) merge.LNAME = String(v.last_name).slice(0, 60);
    if (v.phone) merge.PHONE = String(v.phone).slice(0, 40);
    const put = () => fetch(base, { method: "PUT", headers, signal: AbortSignal.timeout(6000),
      body: JSON.stringify({ email_address: email, status_if_new: "subscribed", merge_fields: merge }) });
    let r = await put();
    if (!r.ok && merge.PHONE) { delete merge.PHONE; r = await put(); }
    if (!r.ok) return `mc failed ${r.status}`;
    const m = await r.json().catch(() => ({}));
    const t = await fetch(base + "/tags", { method: "POST", headers, signal: AbortSignal.timeout(6000),
      body: JSON.stringify({ tags: MC_TAGS.map((name) => ({ name, status: "active" })) }) });
    return t.ok ? `mc ${m.status || "ok"}` : `mc ${m.status || "ok"}, tags failed ${t.status}`;
  } catch (e) {
    return "mc error " + String(e && e.name || e).slice(0, 40);
  }
}

async function rpc(fn, body) {
  const r = await fetch(`${SB}/rest/v1/rpc/${fn}`, {
    method: "POST",
    headers: { apikey: SB_KEY, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`supabase ${fn} ${r.status}`);
  const t = await r.text();
  return t ? JSON.parse(t) : null;
}

export default async (req) => {
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let id;
  try { ({ id } = await req.json()); } catch { return json({ error: "bad request" }, 400); }
  if (!/^[0-9a-f-]{36}$/i.test(id || "")) return json({ error: "bad id" }, 400);

  const v = await rpc("christmas_registration_get", { p_id: id }).catch(() => null);
  if (!v) return json({ error: "not found" }, 404);

  const mcP = addToMailchimp(v).catch(() => "mc error");

  const appId = process.env.PCO_APP_ID, secret = process.env.PCO_SECRET;
  if (!appId || !secret) {
    await rpc("christmas_registration_mark", { p_id: id, p_status: "waiting", p_detail: "PCO not configured; " + await mcP }).catch(() => {});
    return json({ ok: true, saved: true });
  }
  const auth = "Basic " + Buffer.from(appId + ":" + secret).toString("base64");
  const headers = { Authorization: auth, "Content-Type": "application/json" };

  const party = partySize(v);
  const values = [{ type: "FormSubmissionValue", attributes: { form_field_id: F_PARTY, value: party } }];
  if (v.phone) values.push({ type: "FormSubmissionValue", attributes: { form_field_id: F_PHONE, value: { number: v.phone, location: "Mobile" } } });

  const shapes = [
    { first_name: v.first_name, last_name: v.last_name, emails_attributes: [{ address: v.email, location: "Home" }] },
    { first_name: v.first_name, last_name: v.last_name, email: v.email },
  ];
  let sub = null, lastErr = "";
  for (const person_attributes of shapes) {
    const r = await fetch(`${PCO}/forms/${FORM}/form_submissions?include=person`, {
      method: "POST", headers,
      body: JSON.stringify({ data: { type: "FormSubmission", attributes: { person_attributes } }, included: values }),
    });
    if (r.ok) { sub = await r.json(); break; }
    lastErr = `${r.status} ${(await r.text()).slice(0, 300)}`;
    if (r.status !== 422 && r.status !== 400) break;
  }
  if (!sub) {
    await rpc("christmas_registration_mark", { p_id: id, p_status: "failed", p_detail: lastErr + "; " + await mcP }).catch(() => {});
    return json({ error: "planning center" }, 502);
  }

  const personId = sub.data?.relationships?.person?.data?.id;
  const note = `Christmas Eve 2026 (website): saved a spot for ${party}.` + (v.phone ? ` Phone: ${v.phone}.` : "");
  let noteOk = true;
  if (personId) {
    const r = await fetch(`${PCO}/people/${personId}/notes`, {
      method: "POST", headers,
      body: JSON.stringify({ data: { type: "Note", attributes: { note, note_category_id: NOTE_CATEGORY } } }),
    });
    noteOk = r.ok;
  }
  await rpc("christmas_registration_mark", { p_id: id, p_status: "sent", p_detail: `submission ${sub.data?.id} person ${personId || "?"}${noteOk ? "" : " (note failed)"}; ${await mcP}` }).catch(() => {});
  return json({ ok: true });
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}

export const config = { path: "/api/christmas-register" };
