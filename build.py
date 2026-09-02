#!/usr/bin/env python3
"""
Assembles the GateCity Buckhead site from partials/ + pages/ into plain HTML
at the repo root. No dependencies. Run:  python3 build.py

Edit content in pages/ and partials/ -- never the generated .html at the root,
those get overwritten. Every outbound URL lives in LINKS below, so a changed
Zoom link or Church Center form is a one-line edit here.
"""
import os, re, datetime, shutil, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))

# --- Every outbound link, in one place ------------------------------------
CC = "https://gatecity-buckhead.churchcenter.com"

LINKS = {
    "GIVE":            CC + "/giving",
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
    "OG_IMAGE":        "https://www.gatecitybuckhead.com/assets/img/hero.jpg",  # link-preview image; must be absolute
}

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
    "404":               ("404.html",                       "Page Not Found | GateCity Buckhead",      "That page doesn't exist.", True),
}


def fill(text, extra=None):
    vals = {}
    vals.update(LINKS)
    vals.update(IMAGES)
    vals["YEAR"] = str(datetime.date.today().year)
    # Cache-busting: short content hash of site.css / site.js so browsers
    # pick up new styles immediately after a deploy.
    for name in ("site.css", "site.js"):
        with open(os.path.join(ROOT, "assets", name), "rb") as f:
            vals[name.upper().replace(".", "_") + "_V"] = hashlib.md5(f.read()).hexdigest()[:8]
    if extra:
        vals.update(extra)
    for _ in range(3):  # allow one level of nesting
        for k, v in vals.items():
            text = text.replace("{{%s}}" % k, v)
    return text


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def main():
    head = read("partials/head.html")
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    built = []
    for slug, (out, title, desc, solid) in PAGES.items():
        body = read("pages/%s.html" % slug)
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
        if slug == "404":
            continue
        urls.append("https://www.gatecitybuckhead.com/" + out.replace("index.html", ""))
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (u, today))
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")

    print("Built %d pages:" % len(built))
    for b in built:
        print("  " + b)
    print("  sitemap.xml")


if __name__ == "__main__":
    main()
