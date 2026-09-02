"""One-time converter: Squarespace blog dump -> posts/<slug>.html source files.

Each output file has a small front-matter header followed by clean HTML.
build.py renders them. Re-running this overwrites posts/ — only meant for the
initial migration.
"""
import json, re, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
posts = json.load(open(os.path.join(ROOT, "blog-src", "dump.json")))["posts"]
OUT = os.path.join(ROOT, "posts")
os.makedirs(OUT, exist_ok=True)


def clean_html(s):
    # drop attributes we don't want
    s = re.sub(r'\s(style|class|id|data-rte-preserve-empty|data-rte-list)="[^"]*"', "", s)
    # underline spans -> <u>
    s = re.sub(r"<span>\s*</span>", "", s)
    s = s.replace("<span>", "").replace("</span>", "")
    # empty paragraphs (Squarespace uses them as spacing)
    s = re.sub(r"<p>\s*(<br\s*/?>)?\s*</p>", "", s)
    s = re.sub(r"<p>\s*(&nbsp;|\s)*</p>", "", s)
    # trailing <br> at end of a paragraph
    s = re.sub(r"(<br\s*/?>\s*)+</p>", "</p>", s)
    # external links open in new tab
    s = re.sub(r'<a href="(https?://[^"]+)"(?![^>]*target)', r'<a href="\1" target="_blank" rel="noopener"', s)
    # promote h4 -> h3 (site only styles h2/h3 in prose)
    s = s.replace("<h4>", "<h3>").replace("</h4>", "</h3>")
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def yt_id(src):
    m = re.search(r"youtube\.com%2Fembed%2F([A-Za-z0-9_-]+)", src) or re.search(r"v%3D([A-Za-z0-9_-]+)", src)
    return m.group(1) if m else None


for p in posts:
    slug = p["path"].split("/")[-1]
    parts = []
    k = 0
    for b in p["blocks"]:
        if b["t"] == "html":
            parts.append(clean_html(b["html"]))
        elif b["t"] == "hr":
            parts.append("<hr>")
        elif b["t"] == "quote":
            parts.append("<blockquote>%s</blockquote>" % clean_html(b["html"]))
        elif b["t"] == "img":
            k += 1
            name = "inline-%s-%d" % (slug, k)
            ext = "png" if os.path.exists(os.path.join(ROOT, "assets/img/blog", name + ".png")) else "jpg"
            cap = ("<figcaption>%s</figcaption>" % html.escape(b["cap"])) if b.get("cap") else ""
            parts.append('<figure><img src="/assets/img/blog/%s.%s" alt="%s" loading="lazy">%s</figure>' % (name, ext, html.escape(b.get("alt", "")), cap))
        elif b["t"] == "embed":
            vid = yt_id(b.get("src", "") + b.get("url", ""))
            if vid:
                parts.append('<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/%s" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>' % vid)
        elif b["t"] == "button":
            parts.append('<p><a class="btn btn-primary" href="%s">%s</a></p>' % (b["href"], html.escape(b["text"])))
    body = "\n\n".join(x for x in parts if x)
    # first block is usually an italic subtitle line; keep as-is.
    date = p["pub"][:10]
    ext = "png" if os.path.exists(os.path.join(ROOT, "assets/img/blog", "cover-%s.png" % slug)) else "jpg"
    desc = html.unescape(p["desc"]).replace("\n", " ").strip()
    if len(desc) > 300:
        desc = desc[:297].rsplit(" ", 1)[0] + "…"
    fm = [
        "title: " + p["title"].strip(),
        "date: " + date,
        "author: " + (p["author"] or "GateCity Buckhead"),
        "cover: /assets/img/blog/cover-%s.%s" % (slug, ext),
        "description: " + desc,
    ]
    with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write("---\n" + "\n".join(fm) + "\n---\n" + body + "\n")
    print(date, slug)
print(len(posts), "posts written")
