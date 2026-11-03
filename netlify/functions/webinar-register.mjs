// Walking with Jesus webinar registration: hands a website signup to Planning Center.
// The browser saves the registration in Supabase (rpc webinar_register) and gets an id,
// then POSTs {id} here. This function reads it back from Supabase (nothing from the
// browser is trusted), submits it to the PCO form "I'm interested in the Digital
// Discipleship Cohort!" (1114259) so the existing workflow and emails fire, adds a note
// that they registered for the webinar, and records the result.
// Zoom link email: to be added once the webinar date and link are set.

const SB = "https://egccpqcdpmvkkgdunpuc.supabase.co";
const SB_KEY = "sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda";
const FORM = process.env.PCO_WEBINAR_FORM_ID || "1114259";
const F_PHONE = "8794467", F_TZ = "8794829", F_CONN = "8794852", F_COMMIT = "8794892";
const TZ = { Eastern: "9674410", Central: "9674411", Pacific: "9674412" };
const CONN = { "Online Sunday Services": "9674428", "Virtual Prayer Gatherings": "9674429", "Digital Content (YouTube/Social Media)": "9674430", "In-person occasionally": "9674431", "New, exploring": "9674432" };
const COMMIT_LEARN_MORE = "9674475";
const NOTE_CATEGORY = process.env.PCO_VISIT_NOTE_CATEGORY || "248939";
const PCO = "https://api.planningcenteronline.com/people/v2";

async function rpc(fn, body) {
  const r = await fetch(`${SB}/rest/v1/rpc/${fn}`, { method: "POST", headers: { apikey: SB_KEY, "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`supabase ${fn} ${r.status}`);
  const t = await r.text(); return t ? JSON.parse(t) : null;
}

export default async (req) => {
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let id; try { ({ id } = await req.json()); } catch { return json({ error: "bad request" }, 400); }
  if (!/^[0-9a-f-]{36}$/i.test(id || "")) return json({ error: "bad id" }, 400);
  const v = await rpc("webinar_registration_get", { p_id: id }).catch(() => null);
  if (!v) return json({ error: "not found" }, 404);
  const appId = process.env.PCO_APP_ID, secret = process.env.PCO_SECRET;
  if (!appId || !secret) { await rpc("webinar_registration_mark", { p_id: id, p_status: "failed", p_detail: "PCO not configured" }).catch(() => {}); return json({ error: "not configured" }, 503); }
  const headers = { Authorization: "Basic " + Buffer.from(appId + ":" + secret).toString("base64"), "Content-Type": "application/json" };

  const val = (f, value) => ({ type: "FormSubmissionValue", attributes: { form_field_id: f, value } });
  // Checkbox and dropdown answers take the option id as a plain string.
  const valueSets = [
    [val(F_PHONE, { number: v.phone, location: "Mobile" }), val(F_TZ, TZ[v.time_zone]), val(F_COMMIT, COMMIT_LEARN_MORE), ...(CONN[v.connection] ? [val(F_CONN, CONN[v.connection])] : [])],
  ];
  const person_attributes = { first_name: v.first_name, last_name: v.last_name, emails_attributes: [{ address: v.email, location: "Home" }] };
  let sub = null, lastErr = "";
  outer: for (const values of valueSets) {
    for (const pa of [person_attributes, { first_name: v.first_name, last_name: v.last_name, email: v.email }]) {
      const r = await fetch(`${PCO}/forms/${FORM}/form_submissions?include=person`, { method: "POST", headers, body: JSON.stringify({ data: { type: "FormSubmission", attributes: { person_attributes: pa } }, included: values }) });
      if (r.ok) { sub = await r.json(); break outer; }
      lastErr = `${r.status} ${(await r.text()).slice(0, 300)}`;
      if (r.status !== 422 && r.status !== 400) break outer;
    }
  }
  if (!sub) { await rpc("webinar_registration_mark", { p_id: id, p_status: "failed", p_detail: lastErr }).catch(() => {}); return json({ error: "planning center" }, 502); }

  const personId = sub.data?.relationships?.person?.data?.id;
  const lines = [`Registered for the free Walking with Jesus webinar (website). Time zone: ${v.time_zone}.`];
  if (v.connection) lines.push(`Connected through: ${v.connection}.`);
  if (v.questions) lines.push("Questions: " + v.questions);
  let noteOk = true;
  if (personId) {
    const r = await fetch(`${PCO}/people/${personId}/notes`, { method: "POST", headers, body: JSON.stringify({ data: { type: "Note", attributes: { note: lines.join("\n"), note_category_id: NOTE_CATEGORY } } }) });
    noteOk = r.ok;
  }
  await rpc("webinar_registration_mark", { p_id: id, p_status: "sent", p_detail: `submission ${sub.data?.id} person ${personId || "?"}${noteOk ? "" : " (note failed)"}` }).catch(() => {});
  return json({ ok: true });
};

function json(body, status = 200) { return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } }); }
export const config = { path: "/api/webinar-register" };
