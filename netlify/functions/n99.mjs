// Counts unique donors to the "99 for the 1" fund in Planning Center Giving.
// Served at /api/n99 and cached on Netlify's CDN for an hour.
//
// Needs two environment variables in Netlify (Project configuration ->
// Environment variables), created from a Planning Center Personal Access
// Token at https://api.planningcenteronline.com/oauth/applications :
//   PCO_APP_ID   - the token's Application ID
//   PCO_SECRET   - the token's Secret
// Optional: N99_FUND_ID (default 470170), N99_SINCE (default 2025-10-22).

export default async () => {
  const id = process.env.PCO_APP_ID, secret = process.env.PCO_SECRET;
  if (!id || !secret) {
    return json({ error: "not configured" }, 503);
  }
  const FUND = process.env.N99_FUND_ID || "470170";
  const SINCE = process.env.N99_SINCE || "2025-10-22";
  const auth = "Basic " + Buffer.from(id + ":" + secret).toString("base64");
  const donors = new Set();
  let url = "https://api.planningcenteronline.com/giving/v2/donations?include=designations&per_page=100&order=-received_at";
  let pages = 0, stop = false;
  while (url && !stop && pages < 60) {
    const r = await fetch(url, { headers: { Authorization: auth } });
    if (!r.ok) return json({ error: "planning center " + r.status }, 502);
    const j = await r.json();
    const desig = new Map((j.included || []).filter(i => i.type === "Designation").map(i => [i.id, i]));
    for (const d of j.data || []) {
      const a = d.attributes || {};
      if ((a.received_at || "") < SINCE) { stop = true; break; }
      if (a.refunded) continue;
      if (!["succeeded", "pending"].includes(a.payment_status)) continue;
      const pid = d.relationships?.person?.data?.id;
      if (!pid) continue;
      const hits = (d.relationships?.designations?.data || [])
        .map(x => desig.get(x.id))
        .some(x => x && x.relationships?.fund?.data?.id === FUND && (x.attributes?.amount_cents || 0) > 0);
      if (hits) donors.add(pid);
    }
    url = j.links?.next;
    pages++;
  }
  return json({ count: donors.size, goal: 99, updated: new Date().toISOString() });
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "public, max-age=300",
      "netlify-cdn-cache-control": "public, max-age=3600, stale-while-revalidate=86400",
    },
  });
}

export const config = { path: "/api/n99" };
