// Spiritual Gifts Assessment: hands a finished assessment to Mailchimp so the full results email goes out.
// The browser saves the submission in Supabase (rpc gifts_assessment_submit, which scores the answers
// on the server and returns an id), then POSTs {id} here. This function reads the row back from
// Supabase (nothing the browser sends is trusted), adds or updates the person in the GateCity Buckhead
// audience with their results in merge fields (GIFT1/GIFT2 = gift keys for the email's conditional
// content, GIFT1N/GIFT2N = names, GSYN = how the two gifts work together, GPARTS = strongest gift in
// each part), then applies two tags: "spiritual-gifts" (stays on the contact, for segmenting) and
// "gifts-results-send" (the trigger). Adding the trigger tag starts the Mailchimp flow
// "Spiritual Gifts Assessment: Full Results", which sends the results email and then removes the
// trigger tag, so someone retaking the assessment gets a fresh email. Website, GCB Weekly and Widest
// Audience tags match every other website signup (Hazen, Nov 11). Needs MAILCHIMP_API_KEY in Netlify.
import { createHash } from "node:crypto";
import { GIFTS, PARTS } from "./data.mjs";

const SB = "https://egccpqcdpmvkkgdunpuc.supabase.co";
const SB_KEY = "sb_publishable_THG77diuxLtHQ_BpN2SvVw_Z2w9XHda";
const MC_LIST = process.env.MAILCHIMP_LIST_ID || "cdb1521460";
const TAG = "spiritual-gifts";
const TRIGGER = "gifts-results-send";
const FIELDS = [
  ["GIFT1", "Gifts: top gift key"], ["GIFT2", "Gifts: second gift key"],
  ["GIFT1N", "Gifts: top gift"], ["GIFT2N", "Gifts: second gift"],
  ["GSYN", "Gifts: how they work together"], ["GPARTS", "Gifts: strongest per part"],
];
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "Content-Type": "application/json", "cache-control": "no-store" } });

async function rpc(fn, body) {
  const r = await fetch(`${SB}/rest/v1/rpc/${fn}`, { method: "POST", headers: { apikey: SB_KEY, "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error(`supabase ${fn} ${r.status}`);
  const t = await r.text(); return t ? JSON.parse(t) : null;
}

let fieldsReady = false;
async function ensureFields(api, headers) {
  if (fieldsReady) return;
  const r = await fetch(`${api}/merge-fields?count=100&fields=merge_fields.tag`, { headers });
  const have = new Set(((await r.json().catch(() => ({}))).merge_fields || []).map((f) => f.tag));
  for (const [tag, name] of FIELDS) {
    if (have.has(tag)) continue;
    await fetch(`${api}/merge-fields`, { method: "POST", headers, body: JSON.stringify({ tag, name, type: "text", public: false, options: { size: 255 } }) });
  }
  fieldsReady = true;
}

function synergy(a, b) {
  const A = GIFTS[a], B = GIFTS[b];
  const tail = A.kind !== B.kind
    ? "One is a speaking gift and one a serving gift (1 Peter 4:11), a strong pair: you can both say it and live it."
    : A.kind === "speaking"
      ? "Both are speaking gifts (1 Peter 4:11), so watch for chances to put words into action alongside others."
      : "Both are serving gifts (1 Peter 4:11), so you may build up the church most through what you do, and your words will carry that weight.";
  return `With ${A.name}, ${A.with}. With ${B.name}, ${B.with}. ${tail}`.slice(0, 255);
}

export default async (req) => {
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let id; try { ({ id } = await req.json()); } catch { return json({ error: "bad request" }, 400); }
  if (!/^[0-9a-f-]{36}$/i.test(id || "")) return json({ error: "bad id" }, 400);
  const v = await rpc("gifts_assessment_get", { p_id: id }).catch(() => null);
  if (!v || !GIFTS[v.top1] || !GIFTS[v.top2]) return json({ error: "not found" }, 404);
  const key = process.env.MAILCHIMP_API_KEY;
  if (!key) { await rpc("gifts_assessment_mark", { p_id: id, p_status: "failed", p_detail: "MAILCHIMP_API_KEY missing" }).catch(() => {}); return json({ error: "not configured" }, 503); }
  const dc = key.split("-")[1] || "us3";
  const api = `https://${dc}.api.mailchimp.com/3.0/lists/${MC_LIST}`;
  const member = `${api}/members/${createHash("md5").update(v.email.toLowerCase()).digest("hex")}`;
  const headers = { Authorization: "Basic " + Buffer.from("gcb:" + key).toString("base64"), "Content-Type": "application/json" };
  try {
    await ensureFields(api, headers);
    const parts = PARTS.map((p) => `${p.name}: ${GIFTS[v.part_tops?.[p.id]]?.name || ""}`).join(" | ").slice(0, 255);
    const merge = { FNAME: String(v.first_name).slice(0, 60), GIFT1: v.top1, GIFT2: v.top2, GIFT1N: GIFTS[v.top1].name, GIFT2N: GIFTS[v.top2].name, GSYN: synergy(v.top1, v.top2), GPARTS: parts };
    if (v.last_name) merge.LNAME = String(v.last_name).slice(0, 60);
    const r = await fetch(member, { method: "PUT", headers, body: JSON.stringify({ email_address: v.email, status_if_new: "subscribed", merge_fields: merge }) });
    const m = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(`member ${r.status} ${(m.detail || "").slice(0, 160)}`);
    // TRIGGER is removed by the flow after the email sends, so the next retake adds it fresh.
    const t = await fetch(`${member}/tags`, { method: "POST", headers, body: JSON.stringify({ tags: [TAG, TRIGGER, "Website", "GCB Weekly", "Widest Audience"].map((name) => ({ name, status: "active" })) }) });
    if (!t.ok) throw new Error(`tags ${t.status}`);
    await rpc("gifts_assessment_mark", { p_id: id, p_status: "sent", p_detail: `mailchimp ok, member ${m.status}, tags ${TAG} + ${TRIGGER}` }).catch(() => {});
    return json({ ok: true });
  } catch (e) {
    await rpc("gifts_assessment_mark", { p_id: id, p_status: "failed", p_detail: String(e.message || e) }).catch(() => {});
    return json({ error: "mailchimp" }, 502);
  }
};
export const config = { path: "/api/gifts-results" };
