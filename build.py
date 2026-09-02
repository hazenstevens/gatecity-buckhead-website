#!/usr/bin/env python3
"""
Assembles the GateCity Buckhead site from partials/ + pages/ into plain HTML
at the repo root. No dependencies. Run:  python3 build.py

Edit content in pages/ and partials/ -- never the generated .html at the root,
those get overwritten. Every outbound URL lives in LINKS below, so a changed
Zoom link or Church Center form is a one-line edit here.
"""
import os, re, datetime, shutil, hashlib, html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))

# --- Every outbound link, in one place ------------------------------------
BASE = "https://gatecitybuckhead.com"   # canonical site URL (Netlify primary domain)
CC = "https://gatecity-buckhead.churchcenter.com"

LINKS = {
    "GIVE":            CC + "/giving",
    "GIVE_GENERAL":    CC + "/giving/to/general-tithes-offering",
    "GIVE_99":         CC + "/giving/to/99-for-the-1",
    "GIVE_MISSIONS":   CC + "/giving/to/missions",
    "GIVE_BENEV":      CC + "/giving/to/benevolence",
    "GIVE_PRAYER":     CC + "/giving/to/building-fund",   # PCO fund slug (still "building-fund" until renamed in Planning Center)
    "FORM_VISIT":      CC + "/people/forms/888536",
    "FORM_SERVE":      CC + "/people/forms/856748",
    "FORM_CONNECT":    CC + "/people/forms/912170",
    "FORM_FORMATION":  CC + "/people/forms/1282880",
    "FORM_MEMBER":     CC + "/people/forms/858540",
    "FORM_BAPTISM":    CC + "/people/forms/888611",
    "FORM_KIDS":       CC + "/people/forms/888536",
    "FORM_KIDS_SN":    CC + "/people/forms/1076599",
    "FORM_COHORT":     CC + "/people/forms/1114259",
    "FORM_NEWSLETTER": CC + "/people/forms/920146",
    "ZOOM_PRAYER":     "https://us02web.zoom.us/j/83273443236",
    "ZOOM_FORUM":      "https://us02web.zoom.us/j/89552182099",
    "ZOOM_FORMATION":  "https://us02web.zoom.us/j/83897703242",
    "YT":              "https://www.youtube.com/@GateCityBuckhead",
    "POD_SPOTIFY":     "https://open.spotify.com/show/1vmVEsCNhoT7lfYynqWhnm",
    "POD_APPLE":       "https://podcasts.apple.com/us/podcast/gatecity-buckhead/id1797576803",
    "POD_YOUTUBE":     "https://www.youtube.com/playlist?list=PLZe6ANQOBlot8XAn-yYmKIyASu4-dkc86",
    "BLOG_SUBSCRIBE":  CC + "/people/forms/920146",   # TODO: swap for Mailchimp signup once decided
    "MAPS":            "https://maps.google.com/?q=2890+N+Fulton+Dr+NE,+Atlanta,+GA+30305",
    "PCL":             "https://presencecenteredlife.com/",
    "BIBLE_PLANS":     "https://www.bible.com/organizations/9853fe56-6a51-48d4-b050-a3b562cdb22d",
    "AMZ_DETOX":       "https://www.amazon.com/dp/B0H8GDKBY4",
    "AMZ_MANIFEST":    "https://www.amazon.com/dp/B0H4S8Z9S8",
    "AMZ_STRONG":      "https://www.amazon.com/dp/B0GM97RPG1",
    "AMZ_BLESSED":     "https://www.amazon.com/dp/B0G2FGMHMB",
    "AMZ_CONVERSATIONS": "https://www.amazon.com/dp/B0F8J7F553",
    "AMZ_TRANSFORMED": "https://www.amazon.com/dp/B0DZCRD4C2",
    "AMZ_SEVEN_SEEDS": "https://www.amazon.com/dp/B0DX5244NC",
    "AMZ_KOC":         "https://www.amazon.com/dp/0802424899",
    "YV_KOC":          "https://my.bible.com/reading-plans/31471-know-own-change-journeying-towards-gods-heart-for",
    "OG_IMAGE":        BASE + "/assets/img/hero.jpg",  # link-preview image; must be absolute
}

# --- Newsletter signup ------------------------------------------------------
# Paste the Mailchimp embedded-form action URL here, e.g.
#   "https://gatecityatl.us21.list-manage.com/subscribe/post?u=XXXX&id=YYYY"
# While it's empty the forms fall back to Netlify Forms (submissions show up
# in Netlify -> Forms, and can email-notify), so nothing is ever lost.
MAILCHIMP_ACTION = "https://gatecitybuckhead.us3.list-manage.com/subscribe/post?u=b941189c6bb50530d38f746fd&id=cdb1521460&f_id=00e92be2f0"
MAILCHIMP_TAGS = "10814202,10812749"   # Mailchimp tag ids applied to website sign-ups: Website + GCB Weekly


def newsletter_form(form_id):
    tpl = read("partials/newsletter-form.html")
    if MAILCHIMP_ACTION:
        u = re.search(r"[?&]u=([^&]+)", MAILCHIMP_ACTION)
        i = re.search(r"[?&]id=([^&]+)", MAILCHIMP_ACTION)
        honeypot = ""
        if u and i:
            honeypot = '<div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_%s_%s" tabindex="-1" value=""></div>' % (u.group(1), i.group(1))
        tags = ('<input type="hidden" name="tags" value="%s">' % MAILCHIMP_TAGS) if MAILCHIMP_TAGS else ""
        vals = {"NL_ACTION": MAILCHIMP_ACTION, "NL_ATTRS": ' target="_blank"', "NL_HIDDEN": tags + honeypot}
    else:
        vals = {"NL_ACTION": "/thanks", "NL_ATTRS": ' name="newsletter" data-netlify="true" netlify-honeypot="website"',
                "NL_HIDDEN": '<input type="hidden" name="form-name" value="newsletter"><p class="sr-only" aria-hidden="true"><label>Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label></p>'}
    vals["NL_ID"] = form_id
    for k, v in vals.items():
        tpl = tpl.replace("{{%s}}" % k, v)
    return tpl


# --- 99 for the 1 progress -------------------------------------------------
# Update this number when a new partner joins (individual or church), then
# rebuild. It drives the progress bars on /pledge and /99-for-the-1.
DONORS_99 = 1


# --- Images. All local now (nothing depends on Squarespace). -------------
IMAGES = {
    "LOGO":   "/assets/img/logo.png",
    "HERO":   "/assets/img/hero.jpg",          # Easter 2026, 417A6646 (Eden)
    "HERO_M": "/assets/img/hero-1400.jpg",     # same, mobile size
    "AIS":    "/assets/img/ais.jpg",
    "PEOPLE": "/assets/img/people.jpg",        # Easter 2026, 417A6449 (Eden)
    "PRAYER": "/assets/img/worship.jpg",       # Easter 2026, 417A6831 (Eden)
    "KIDS":   "/assets/img/kids.jpg",          # Easter 2026, 417A6307 (Eden) - parent + toddler
    "FORUM":  "/assets/img/sunday-forum.jpg",
    "TEAM":   "/assets/img/team.jpg",
    "T_HAZEN":    "/assets/img/team/hazen.jpg",
    "T_HANNAH":   "/assets/img/team/hannah.jpg",
    "T_SON":      "/assets/img/team/son.jpg",
    "T_ANDREW":   "/assets/img/team/andrew.jpg",
    "T_HALIMA":   "/assets/img/team/halima.jpg",
    "T_KARISSA":  "/assets/img/team/karissa.jpg",
    "T_KENNAH":   "/assets/img/team/kennah.jpg",
    "T_SARAH":    "/assets/img/team/sarah.jpg",
    "T_ANGEL":    "/assets/img/team/angel.jpg",
}

# page slug -> (output path, <title>, meta description, solid header?)
PAGES = {
    "index":             ("index.html",                    "GateCity Buckhead | Sundays at 11am in Buckhead, Atlanta", "A presence-centered church in Buckhead. We gather Sundays at 11am at Atlanta International School. Plan your first visit.", False),
    "new-here":          ("new-here/index.html",            "Plan a Visit | GateCity Buckhead",        "Everything you need for your first Sunday at GateCity Buckhead — what to expect, parking, kids, and how to get connected.", True),
    "our-beliefs":       ("our-beliefs.html",               "Our Beliefs | GateCity Buckhead",         "What we believe: the fifteen statements of faith that shape GateCity Buckhead.", True),
    "our-team":          ("our-team.html",                  "Our Team | GateCity Buckhead",            "Meet the leadership team at GateCity Buckhead in Atlanta.", True),
    "buckcity-kids":     ("buckcity-kids.html",             "BuckCity Kids | GateCity Buckhead",       "Safe, joy-filled kids ministry for ages 1–12, every Sunday at 11am. Pre-register your child before your first visit.", True),
    "digital-community": ("digital-community.html",         "Digital Community | GateCity Buckhead",   "Virtual prayer, Sunday Forum, Formation Nights and the Discipleship Cohort — ways to belong between Sundays.", True),
    "resources":         ("resources/index.html",           "Resources | GateCity Buckhead",           "Podcast, books, YouVersion reading plans, music and more from GateCity Buckhead.", True),
    "location":          ("location.html",                  "Where We Meet | GateCity Buckhead",       "GateCity Buckhead meets at Atlanta International School, 2890 N Fulton Dr NE. Directions and parking.", True),
    "pledge":            ("pledge.html",                    "Give | GateCity Buckhead",                "Give to GateCity Buckhead — one-time or recurring, and become one of the 99 partners helping us reach the one.", False),
    "99-for-the-1":      ("99-for-the-1.html",              "99 for the 1 | GateCity Buckhead",        "Jesus left the 99 to go after the one. We're believing for 99 partners — 90 individuals and 9 churches — to sustain and expand GateCity Buckhead.", False),
    "thanks":            ("thanks.html",                    "Thanks for Subscribing | GateCity Buckhead", "You're on the GCB Weekly list.", True),
    "404":               ("404.html",                       "Page Not Found | GateCity Buckhead",      "That page doesn't exist.", True),
}


def fill(text, extra=None):
    vals = {}
    vals.update(LINKS)
    vals.update(IMAGES)
    vals["YEAR"] = str(datetime.date.today().year)
    vals["DONORS_99"] = str(DONORS_99)
    vals["DONORS_99_PCT"] = str(round(min(DONORS_99, 99) / 99 * 100, 1))
    # Cache-busting: short content hash of site.css / site.js so browsers
    # pick up new styles immediately after a deploy.
    for name in ("site.css", "site.js"):
        with open(os.path.join(ROOT, "assets", name), "rb") as f:
            vals[name.upper().replace(".", "_") + "_V"] = hashlib.md5(f.read()).hexdigest()[:8]
    if extra:
        vals.update(extra)
    text = re.sub(r"\{\{NL_FORM:([a-z0-9-]+)\}\}", lambda m: newsletter_form(m.group(1)), text)
    for _ in range(3):  # allow one level of nesting
        for k, v in vals.items():
            text = text.replace("{{%s}}" % k, v)
    return text


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


# --- Blog -----------------------------------------------------------------
# Posts live in posts/<slug>.html: a front-matter header (title/date/author/
# cover/description) between --- lines, then the post body as plain HTML.
# Each renders to blog/<slug>.html (served at /blog/<slug>, matching the old
# Squarespace URLs) plus blog/index.html and the "From the Blog" cards.

def load_posts():
    posts = []
    pdir = os.path.join(ROOT, "posts")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".html"):
            continue
        raw = read("posts/" + fn)
        m = re.match(r"---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit("posts/%s: missing front matter" % fn)
        meta = {}
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        meta["slug"] = fn[:-5]
        meta["body"] = m.group(2).strip()
        meta["draft"] = meta.get("draft", "").lower() in ("true", "yes", "1")
        posts.append(meta)
    posts = [p for p in posts if not p["draft"]]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def post_card(p, heading="h3"):
    return (
        '<a class="card post-card" href="/blog/%s">'
        '<div class="card-img wide"><img src="%s" alt="" loading="lazy"></div>'
        '<div class="card-body"><div class="card-when">%s &middot; %s</div>'
        '<%s>%s</%s><p>%s</p>'
        '<span class="card-link">Read <span class="arrow">&rarr;</span></span></div></a>'
        % (p["slug"], p["cover"], nice_date(p["date"]), _html.escape(p["author"]),
           heading, _html.escape(p["title"]), heading, _html.escape(p.get("description", "")))
    )


def render_blog(head, header, footer):
    posts = load_posts()
    post_tpl = read("pages/_post.html")
    index_tpl = read("pages/_blog-index.html")
    outs = []
    for i, p in enumerate(posts):
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        nav = ""
        if older:
            nav += '<a class="post-nav-link" href="/blog/%s"><span>&larr; Older</span><strong>%s</strong></a>' % (older["slug"], _html.escape(older["title"]))
        if newer:
            nav += '<a class="post-nav-link next" href="/blog/%s"><span>Newer &rarr;</span><strong>%s</strong></a>' % (newer["slug"], _html.escape(newer["title"]))
        path = "/blog/" + p["slug"]
        extra = {
            "TITLE": p["title"] + " | GateCity Buckhead Blog",
            "DESC": p.get("description", ""),
            "PATH": path,
            "OG_IMAGE": BASE + p["cover"],
            "POST_TITLE": _html.escape(p["title"]),
            "POST_DATE": nice_date(p["date"]),
            "POST_ISO": p["date"],
            "POST_AUTHOR": _html.escape(p["author"]),
            "POST_COVER": p["cover"],
            "POST_BODY": p["body"],
            "POST_NAV": nav,
        }
        doc = (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n%s</head>\n<body class=\"solid-header\">\n%s\n%s\n%s\n</body>\n</html>\n"
            % (fill(head, extra), fill(header), fill(post_tpl, extra), fill(footer))
        )
        dest = os.path.join(ROOT, "blog", p["slug"] + ".html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(doc)
        outs.append(("blog/" + p["slug"] + ".html", p["date"]))
    # index
    cards = "\n".join(post_card(p) for p in posts)
    extra = {"TITLE": "Blog | GateCity Buckhead", "DESC": "Weekly teaching and reflections from the pastors and team at GateCity Buckhead.",
             "PATH": "/blog/", "BLOG_CARDS": cards, "BLOG_COUNT": str(len(posts))}
    doc = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n%s</head>\n<body class=\"solid-header\">\n%s\n%s\n%s\n</body>\n</html>\n"
        % (fill(head, extra), fill(header), fill(index_tpl, extra), fill(footer))
    )
    with open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    outs.append(("blog/", posts[0]["date"] if posts else datetime.date.today().isoformat()))
    latest = "\n".join(post_card(p) for p in posts[:3])
    return outs, latest


def main():
    head = read("partials/head.html")
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    built = []
    blog_outs, blog_latest = render_blog(head, header, footer)
    for slug, (out, title, desc, solid) in PAGES.items():
        body = read("pages/%s.html" % slug).replace("{{BLOG_LATEST}}", blog_latest)
        path = "/" + out.replace("index.html", "")
        page_head = fill(head, {"TITLE": title, "DESC": desc, "PATH": path})
        body_class = "solid-header" if solid else ""
        doc = (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n%s</head>\n<body class=\"%s\">\n%s\n%s\n%s\n</body>\n</html>\n"
            % (page_head, body_class, fill(header), fill(body), fill(footer))
        )
        dest = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(doc)
        built.append(out)

    # sitemap
    urls = []
    for slug, (out, _t, _d, _s) in PAGES.items():
        if slug in ("404", "thanks"):
            continue
        urls.append(BASE + "/" + out.replace("index.html", ""))
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (u, today))
    for out, d in blog_outs:
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (BASE + "/" + out.replace("index.html", "").replace(".html", ""), d))
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")

    print("Built %d pages:" % len(built))
    for b in built:
        print("  " + b)
    print("  sitemap.xml")


if __name__ == "__main__":
    main()
