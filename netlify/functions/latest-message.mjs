// Finds the newest Sunday message on the GateCity Buckhead YouTube channel.
// Served at /api/latest-message and cached on Netlify's CDN for an hour.
//
// Reads the current series "Message Only" playlist RSS feed (no API key
// needed), falling back to the channel uploads feed only if the playlist is empty. A message is any video whose
// title follows the house convention "<Series> | Part N: <Title>" and is not a
// Short, a worship cut, or a combined Worship & Message service.
//
// Optional env var MESSAGE_PLAYLIST overrides the series playlist (set it when
// a new series starts). Update DEFAULT_PLAYLIST at each series launch.

const CHANNEL = "UCPCYw3AOeXT5GInwE2RcRXA";
const DEFAULT_PLAYLIST = "PLR3fw1RacPTk"; // Formed for a Purpose | Message Only

export default async () => {
  const playlist = process.env.MESSAGE_PLAYLIST || DEFAULT_PLAYLIST;
  // The Message Only playlist is the source of truth (it holds exactly one
  // video per Sunday, the real message cut). The channel feed is only a
  // fallback, because the channel also carries podcast-style re-uploads and
  // full-service streams that can outrank the message by date.
  const playlistUrl = "https://www.youtube.com/feeds/videos.xml?playlist_id=" + playlist;
  const channelUrl = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL;
  let entries = [];
  try {
    const r = await fetch(playlistUrl, { headers: { "user-agent": "gatecitybuckhead.com latest-message" } });
    if (r.ok) entries = parse(await r.text());
  } catch (e) { /* fall through */ }
  if (!entries.filter(isMessage).length) {
    // RSS feeds don't support newer short playlist IDs, so read the playlist page itself.
    try {
      const r = await fetch("https://www.youtube.com/playlist?list=" + playlist, { headers: { "user-agent": "Mozilla/5.0", "accept-language": "en-US" } });
      if (r.ok) entries = parsePlaylistPage(await r.text());
    } catch (e) { /* fall through */ }
  }
  if (!entries.filter(isMessage).length) {
    try {
      const r = await fetch(channelUrl, { headers: { "user-agent": "gatecitybuckhead.com latest-message" } });
      if (r.ok) entries = parse(await r.text());
    } catch (e) { /* skip */ }
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
    published: m.fromPage ? null : m.published,
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

function parsePlaylistPage(html) {
  const out = [], seen = new Set();
  const pats = [
    /"playlistVideoRenderer":\{"videoId":"([\w-]{11})"[\s\S]*?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"/g,
    /"lockupViewModel":\{"contentImage"[\s\S]*?"contentId":"([\w-]{11})"/g,
  ];
  let m;
  while ((m = pats[0].exec(html))) push(m[1], m[2]);
  if (!out.length) {
    // Newer page format: video IDs and titles in lockupViewModel blocks.
    const re = /"contentId":"([\w-]{11})"/g;
    while ((m = re.exec(html))) {
      const win = html.slice(Math.max(0, m.index - 6000), m.index + 6000);
      const titles = [...win.matchAll(/"title":\{"content":"((?:[^"\\]|\\.)*)"/g)].map(x => x[1]);
      const t = titles.find(x => /\|\s*Part\s*\d+/i.test(x)) || titles[0];
      if (t) push(m[1], t);
    }
  }
  return out;
  function push(id, raw) {
    if (seen.has(id)) return; seen.add(id);
    let title; try { title = JSON.parse('"' + raw + '"'); } catch (e) { title = raw; }
    out.push({ id, title, published: new Date(Date.UTC(2000, 0, 1 + out.length)).toISOString(), fromPage: true });
  }
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
