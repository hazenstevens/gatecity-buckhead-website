// Finds the newest Sunday message on the GateCity Buckhead YouTube channel.
// Served at /api/latest-message and cached on Netlify's CDN for an hour.
//
// Reads two public RSS feeds (no API key needed): the channel uploads feed and
// the current series "Message Only" playlist feed. A message is any video whose
// title follows the house convention "<Series> | Part N: <Title>" and is not a
// Short, a worship cut, or a combined Worship & Message service.
//
// Optional env var MESSAGE_PLAYLIST overrides the series playlist (set it when
// a new series starts; it only matters if the message has already fallen out of
// the channel feed's last 15 uploads).

const CHANNEL = "UCPCYw3AOeXT5GInwE2RcRXA";
const DEFAULT_PLAYLIST = "PLKiguYVKo9yE"; // Incense & Oil | Message Only

export default async () => {
  const playlist = process.env.MESSAGE_PLAYLIST || DEFAULT_PLAYLIST;
  const feeds = [
    "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL,
    "https://www.youtube.com/feeds/videos.xml?playlist_id=" + playlist,
  ];
  let entries = [];
  for (const url of feeds) {
    try {
      const r = await fetch(url, { headers: { "user-agent": "gatecitybuckhead.com latest-message" } });
      if (r.ok) entries = entries.concat(parse(await r.text()));
    } catch (e) { /* skip a feed that fails */ }
  }
  const messages = entries.filter(isMessage).sort((a, b) => (a.published < b.published ? 1 : -1));
  if (!messages.length) return json({ error: "no message found" }, 404);
  const m = messages[0];
  const parts = m.title.split("|").map(s => s.trim());
  const series = parts.length > 1 ? parts[0] : "";
  const rest = parts.length > 1 ? parts.slice(1).join(" | ") : m.title;
  const pm = rest.match(/^Part\s*(\d+)\s*:\s*(.+)$/i);
  return json({
    videoId: m.id,
    url: "https://www.youtube.com/watch?v=" + m.id,
    title: m.title,
    series,
    part: pm ? Number(pm[1]) : null,
    messageTitle: pm ? pm[2].trim() : rest,
    published: m.published,
    thumbnail: "https://i.ytimg.com/vi/" + m.id + "/maxresdefault.jpg",
    thumbnailFallback: "https://i.ytimg.com/vi/" + m.id + "/hqdefault.jpg",
    updated: new Date().toISOString(),
  });
};

function isMessage(e) {
  const t = e.title;
  if (/#?shorts/i.test(t)) return false;
  if (/worship\s*&\s*message/i.test(t) || /worship\s*&amp;\s*message/i.test(t)) return false;
  if (/GateCity (Buckhead )?Worship/i.test(t)) return false;
  if (/^Ministry Time/i.test(t)) return false;
  return /\|\s*Part\s*\d+\s*:/i.test(t);
}

function parse(xml) {
  const out = [];
  const re = /<entry>([\s\S]*?)<\/entry>/g;
  let m;
  while ((m = re.exec(xml))) {
    const e = m[1];
    const id = (e.match(/<yt:videoId>([^<]+)<\/yt:videoId>/) || [])[1];
    const title = decode((e.match(/<title>([^<]*)<\/title>/) || [])[1] || "");
    const published = (e.match(/<published>([^<]+)<\/published>/) || [])[1] || "";
    if (id && title) out.push({ id, title, published });
  }
  return out;
}

function decode(s) {
  return s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
}

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

export const config = { path: "/api/latest-message" };
