// Christ Formed Kids printables gate.
// Protects the Holiday Series printables page and its PDFs with the password
// printed in the book. The password lives only in the Netlify env var
// CFK_PASSWORD (never in page code). A correct entry sets a cookie for 30 days.
const COOKIE = "cfk_access";

async function token(pw) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode("cfk-holiday:" + pw));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function page(error) {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Holiday Series Printables | Christ Formed Kids</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gelasio:wght@500;700&display=swap">
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#fff;font-family:Gelasio,Georgia,serif;color:#1d2a24}
.box{max-width:420px;width:90%;text-align:center;padding:2rem}.box img{width:150px;margin-bottom:1rem}h1{color:#225d3f;font-size:1.6rem;margin:.25rem 0 .75rem}p{line-height:1.55}
input{width:100%;box-sizing:border-box;font:inherit;font-size:1.1rem;padding:.8rem 1rem;border:2px solid #bad1c6;border-radius:12px;margin:.75rem 0;text-align:center}
button{font:inherit;font-size:1.05rem;font-weight:700;background:#225d3f;color:#fff;border:0;border-radius:999px;padding:.8rem 1.8rem;cursor:pointer}.err{color:#b3261e;font-weight:700}a{color:#225d3f}</style></head>
<body><form class="box" method="post"><img src="/assets/cfk/cfk-crest-holiday.png" alt="Christ Formed Kids"><h1>Holiday Series Printables</h1>
<p>Enter the password printed under the QR code on the "Your Printables" page of your book.</p>
${error ? '<p class="err">That password didn\'t match. Please try again.</p>' : ""}
<input name="password" type="password" autocomplete="off" aria-label="Password" required autofocus><button type="submit">Open the printables</button>
<p style="margin-top:1.5rem;font-size:.95rem">Don't have the book? <a href="/cfk-printables">Learn about the Holiday Series</a></p></form></body></html>`;
}

export default async (req, context) => {
  const pw = Netlify.env.get("CFK_PASSWORD");
  if (!pw) return new Response("Printables are temporarily unavailable.", { status: 503 });
  const good = await token(pw);
  if (context.cookies.get(COOKIE) === good) return context.next();

  if (req.method === "POST") {
    const form = await req.formData().catch(() => null);
    if (form && String(form.get("password") || "").trim() === pw) {
      const url = new URL(req.url);
      return new Response(null, {
        status: 303,
        headers: {
          Location: url.pathname,
          "Set-Cookie": `${COOKIE}=${good}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`,
        },
      });
    }
    return new Response(page(true), { status: 401, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
  }
  return new Response(page(false), { status: 401, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
};

export const config = {
  path: ["/cfk-printables-holiday", "/cfk-printables-holiday.html", "/cfk-printables-holiday/", "/assets/cfk/*.pdf"],
};
