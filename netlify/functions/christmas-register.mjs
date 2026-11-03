// Christmas Eve registration: hands a website registration to Planning Center.
// The browser saves the registration in Supabase (rpc christmas_register) and
// gets an id, then POSTs {id} here. This function reads it back from Supabase
// (nothing the browser sends is trusted), submits it to the Planning Center
// Christmas Eve form (which sends the guest's thank-you email, notifies staff,
// and starts the workflow), adds a note with the party size, and records the result.
//
// Set PCO_CHRISTMAS_FORM_ID in Netlify once the Planning Center form exists.
// Until then registrations are saved in Supabase and marked "waiting".

const SB = "https://egccpqcdpmvkkgdunpuc.supabase.co";
const SB_KEY = "sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda";
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

  const v = await rpc("christmas_registration_get", { p_id: id }).catch(() => null);
  if (!v) return json({ error: "not found" }, 404);

  const form = process.env.PCO_CHRISTMAS_FORM_ID;
  const appId = process.env.PCO_APP_ID, secret = process.env.PCO_SECRET;
  if (!form || !appId || !secret) {
    await rpc("christmas_registration_mark", { p_id: id, p_status: "waiting", p_detail: form ? "PCO not configured" : "no PCO form yet" }).catch(() => {});
    return json({ ok: true, saved: true });
  }
  const auth = "Basic " + Buffer.from(appId + ":" + secret).toString("base64");
  const headers = { Authorization: auth, "Content-Type": "application/json" };

  const shapes = [
    { first_name: v.first_name, last_name: v.last_name, emails_attributes: [{ address: v.email, location: "Home" }] },
    { first_name: v.first_name, last_name: v.last_name, email: v.email },
  ];
  let sub = null, lastErr = "";
  for (const person_attributes of shapes) {
    const r = await fetch(`${PCO}/forms/${form}/form_submissions?include=person`, {
      method: "POST", headers,
      body: JSON.stringify({ data: { type: "FormSubmission", attributes: { person_attributes } } }),
    });
    if (r.ok) { sub = await r.json(); break; }
    lastErr = `${r.status} ${(await r.text()).slice(0, 300)}`;
    if (r.status !== 422 && r.status !== 400) break;
  }
  if (!sub) {
    await rpc("christmas_registration_mark", { p_id: id, p_status: "failed", p_detail: lastErr }).catch(() => {});
    return json({ error: "planning center" }, 502);
  }

  const personId = sub.data?.relationships?.person?.data?.id;
  const note = `Christmas Eve 2026 (website): saved a spot for ${v.adults} adult${v.adults == 1 ? "" : "s"} and ${v.kids} kid${v.kids == 1 ? "" : "s"}.` + (v.phone ? ` Phone: ${v.phone}.` : "");
  let noteOk = true;
  if (personId) {
    const r = await fetch(`${PCO}/people/${personId}/notes`, {
      method: "POST", headers,
      body: JSON.stringify({ data: { type: "Note", attributes: { note, note_category_id: NOTE_CATEGORY } } }),
    });
    noteOk = r.ok;
  }
  await rpc("christmas_registration_mark", { p_id: id, p_status: "sent", p_detail: `submission ${sub.data?.id} person ${personId || "?"}${noteOk ? "" : " (note failed)"}` }).catch(() => {});
  return json({ ok: true });
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
}

export const config = { path: "/api/christmas-register" };
