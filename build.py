#!/usr/bin/env python3
"""
Assembles the GateCity Buckhead site from partials/ + pages/ into plain HTML
at the repo root. No dependencies. Run:  python3 build.py

Edit content in pages/ and partials/ -- never the generated .html at the root,
those get overwritten. Every outbound URL lives in LINKS below, so a changed
Zoom link or Church Center form is a one-line edit here.
"""
import os, re, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# --- Every outbound link, in one place ------------------------------------
CC = "https://gatecity-buckhead.churchcenter.com"
IMGBASE = "https://images.squarespace-cdn.com/content/v1/6646144cd2db59376f6958ff/"

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
    "BIBLE_PLANS":     "https://www.bible.com/search/plans",
    "OG_IMAGE":        "https://www.gatecitybuckhead.com/assets/img/hero.jpg",  # link-preview image; must be absolute
}

# --- Images. Swap these for /assets/img/... once files are committed. ------
IMAGES = {
    "LOGO":   IMGBASE + "6eafc964-cc88-4715-804d-906eddde6219/gcb-green%2Bwhite-horiztonal.png?format=750w",
    "HERO":   "/assets/img/hero.jpg",          # Easter 2026, 417A6646 (Eden)
    "HERO_M": "/assets/img/hero-1400.jpg",     # same, mobile size
    "AIS":    IMGBASE + "419f67fe-c699-4129-9aae-fb55ee325529/Atlanta-International-School-Buckhead-Atlanta-AIS.jpg?format=1500w",
    "PEOPLE": "/assets/img/people.jpg",        # Easter 2026, 417A6449 (Eden)
    "PRAYER": "/assets/img/worship.jpg",       # Easter 2026, 417A6831 (Eden)
    "KIDS":   "/assets/img/kids.jpg",          # Easter 2026, 417A6307 (Eden) - parent + toddler
    "FORUM":  IMGBASE + "d5fc60c2-6da7-4fb4-8ba2-d150a806f758/sunday-forum.jpg?format=1000w",
    "TEAM":   IMGBASE + "556588b2-9b68-4cdc-939a-adc6e9c0ac53/GCB+TEAM+PHOTO.jpg?format=2500w",
    "T_HAZEN":    IMGBASE + "61210430-491e-4dc9-ba1a-077374b4245a/hazen.jpg?format=800w",
    "T_HANNAH":   IMGBASE + "7150436b-a70f-4696-9cf8-eaa652b3d453/hannah.jpg?format=800w",
    "T_SON":      IMGBASE + "6de32b77-f496-4d0b-a853-1155f4dfe880/son.jpg?format=800w",
    "T_ANDREW":   IMGBASE + "5027a4c8-544c-48e5-b922-371f04571981/IMG_9722_jpg+2.JPG?format=800w",
    "T_HALIMA":   IMGBASE + "5240778c-23dd-4600-88d9-c49d303b4ba7/IMG_9707_jpg.JPG?format=800w",
    "T_KARISSA":  IMGBASE + "9baacc57-2c84-4305-b649-4494db9157f1/karissa.jpg?format=800w",
    "T_KENNAH":   IMGBASE + "45f88d30-98ba-4d88-87d4-25c0ed7707fb/IMG_9752_jpg+2.JPG?format=800w",
    "T_GRETCHEN": IMGBASE + "38609c40-a6c9-4be1-8bbc-bab008f5ca63/gretchen.jpg?format=800w",
    "T_SARAH":    IMGBASE + "12cd8dbe-b6cd-417d-8bf9-f79025a67d81/sarah-headshot.jpg?format=800w",
    "T_ANGEL":    IMGBASE + "71e0bfb0-7cde-4fb9-9d2c-9a37a544515e/IMG_4042.JPG?format=800w",
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
