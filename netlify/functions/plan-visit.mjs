// Plan a Visit: hands a website signup to Planning Center.
// The browser first saves the signup in Supabase (rpc plan_visit_submit) and
// gets back an id. It then POSTs {id} here. This function reads the signup
// back from Supabase (so nothing the browser sends is trusted), submits it to
// the Planning Center form "I'm Coming On A Sunday!" (888536), which fires the
// same emails and workflow card as a Church Center submission, adds a note
// with kids/notes to the person's profile, and records the result.
//
// Uses the same PCO_APP_ID / PCO_SECRET env vars as /api/n99.

const SB = "https://egccpqcdpmvkkgdunpuc.supabase.co";
const SB_KEY = "sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda";
const FORM = process.env.PCO_VISIT_FORM_ID || "888536";
const F_PHONE = "6951825", F_DATE = "6951629";
const NOTE_CATEGORY = process.env.PCO_VISIT_NOTE_CATEGORY || "248939"; // General
const PCO = "https://api.planningcenteronline.com/people/v2";

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

  const v = await rpc("plan_visit_get", { p_id: id }).catch(() => null);
  if (!v) return json({ error: "not found" }, 404);

  const appId = process.env.PCO_APP_ID, secret = process.env.PCO_SECRET;
  if (!appId || !secret) {
    await rpc("plan_visit_mark", { p_id: id, p_status: "failed", p_detail: "PCO not configured" }).catch(() => {});
    return json({ error: "not configured" }, 503);
  }
  const auth = "Basic " + Buffer.from(appId + ":" + secret).toString("base64");
  const headers = { Authorization: auth, "Content-Type": "application/json" };

  const values = [{ type: "FormSubmissionValue", attributes: { form_field_id: F_DATE, value: v.visit_date } }];
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
    await rpc("plan_visit_mark", { p_id: id, p_status: "failed", p_detail: lastErr }).catch(() => {});
    return json({ error: "planning center" }, 502);
  }

  const personId = sub.data?.relationships?.person?.data?.id;
  const kids = Array.isArray(v.kids) ? v.kids : [];
  const lines = [`Plan a Visit (website): coming Sunday ${v.visit_date}, ${v.adults} adult${v.adults == 1 ? "" : "s"}.`];
  if (kids.length) {
    lines.push("Kids:");
    for (const k of kids) {
      const bits = [k.name, k.birthday && `born ${k.birthday}`, k.grade && `grade ${k.grade}`, k.medical && `allergies/medical: ${k.medical}`].filter(Boolean);
      lines.push("- " + bits.join(", "));
    }
  }
  if (v.notes) lines.push("They shared: " + v.notes);
  let noteOk = true;
  if (personId && (kids.length || v.notes || v.adults > 1)) {
    const r = await fetch(`${PCO}/people/${personId}/notes`, {
      method: "POST", headers,
      body: JSON.stringify({ data: { type: "Note", attributes: { note: lines.join("\n"), note_category_id: NOTE_CATEGORY } } }),
    });
    noteOk = r.ok;
  }
  await rpc("plan_visit_mark", { p_id: id, p_status: "sent", p_detail: `submission ${sub.data?.id} person ${personId || "?"}${noteOk ? "" : " (note failed)"}` }).catch(() => {});
  return json({ ok: true });
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}

export const config = { path: "/api/plan-visit" };
