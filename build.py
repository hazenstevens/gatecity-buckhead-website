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
    "FORM_CONNECT":    CC + "/people/forms/854046",   # "I Want To Learn More!" form
    "FORM_PRAYER":     CC + "/people/forms/912170",   # "Virtual Prayer" form
    "FORM_FORMATION":  CC + "/people/forms/1331359",
    "FORM_MEMBER":     CC + "/people/forms/858540",
    "FORM_BAPTISM":    CC + "/people/forms/888611",
    "FORM_KIDS":       CC + "/people/forms/888536",
    "FORM_KIDS_SN":    CC + "/people/forms/1076599",
    "FORM_COHORT":     CC + "/people/forms/1114259",
    "FORM_NEWSLETTER": CC + "/people/forms/920146",
    "ZOOM_PRAYER":     "https://us02web.zoom.us/j/83273443236?pwd=nOpbkxVsb64EkVEeYX81XsgnFiZDPH.1",   # passcode 212 embedded
    "ZOOM_FORUM":      "https://us02web.zoom.us/j/89552182099?pwd=NZStXMlLrbSG5Vkuh5JnjEC2QmKRXd.1",
    "ZOOM_FORMATION":  "https://us02web.zoom.us/j/83897703242?pwd=nenTjKEiuIJuAlJEhZNLKg3zgoW5Gv.1",
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
    "AMZ_LEGACY":      "https://www.amazon.com/dp/B0FMLMGGCN",
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
# Extra tags a specific form can add, by name: {{NL_FORM:some-id:brief}}
MAILCHIMP_EXTRA_TAGS = {
    "brief": "10812754",   # "Parent Newsletter" = the BuckCity Brief (Kids page form)
}


def newsletter_form(form_id, extra=None):
    tpl = read("partials/newsletter-form.html")
    if MAILCHIMP_ACTION:
        u = re.search(r"[?&]u=([^&]+)", MAILCHIMP_ACTION)
        i = re.search(r"[?&]id=([^&]+)", MAILCHIMP_ACTION)
        honeypot = ""
        if u and i:
            honeypot = '<div style="position:absolute;left:-5000px" aria-hidden="true"><input type="text" name="b_%s_%s" tabindex="-1" value=""></div>' % (u.group(1), i.group(1))
        tag_ids = MAILCHIMP_TAGS
        if extra:
            tag_ids = ",".join(t for t in [MAILCHIMP_TAGS, MAILCHIMP_EXTRA_TAGS[extra]] if t)
        tags = ('<input type="hidden" name="tags" value="%s">' % tag_ids) if tag_ids else ""
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
    "WELCOME": "/assets/img/welcome.jpg",      # Easter 2026, 417A6310 (Eden) - greeter at the welcome table
    "GREETER": "/assets/img/greeter.jpg",      # Easter 2026, 417A6374 (Eden)
    "CHECKIN": "/assets/img/kids-checkin.jpg", # Easter 2026, 417A6353 (Eden) - BuckCity Kids check-in
    "HALLWAY": "/assets/img/hallway.jpg",      # Easter 2026, 417A6389 (Eden)
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

# Google tag. Paste the IDs from Google Analytics (G-...) and Google Ads (AW-...).
# Leave blank and nothing is added to the pages.
GA4_ID = ""
ADS_ID = "AW-18553804873"   # Google Ads (Ad Grant account 775-246-8219)
# Google Ads conversions: page slug -> conversion label. The thank-you page each
# form lands on fires its conversion (counted once per ad click).
ADS_CONVERSIONS = {
    "visit-thanks":   "d_47CJmMzbEdEMmwko9F",   # Plan a Visit form
    "webinar-thanks": "bQGJCO7KzbEdEMmwko9F",   # Your Walk with Jesus Webinar registration
    "thanks":         "SsYGCOeizbEdEMmwko9F",   # Email signup (GCB Weekly)
    # "christmas-thanks": "",                   # Christmas Eve registration (create the conversion, paste its label)
}


def ads_conversion(slug):
    label = ADS_CONVERSIONS.get(slug)
    if not (ADS_ID and label):
        return ""
    # Enhanced conversions: the form stashes the visitor's contact info in sessionStorage
    # (key gcb-ec) right before redirecting here; gtag hashes it before sending to Google.
    return ("\n<script>(function(){var u=null;try{u=JSON.parse(sessionStorage.getItem('gcb-ec')||'null');sessionStorage.removeItem('gcb-ec');}catch(e){}"
            "if(u&&u.email){var d={email:String(u.email).trim().toLowerCase()};"
            "var p=String(u.phone||'').replace(/\\D/g,'');if(p.length===10)p='1'+p;if(p.length===11)d.phone_number='+'+p;"
            "if(u.first||u.last)d.address={first_name:String(u.first||'').trim().toLowerCase(),last_name:String(u.last||'').trim().toLowerCase()};"
            "gtag('set','user_data',d);}"
            "gtag('event','conversion',{send_to:'%s/%s',value:1.0,currency:'USD'});})();</script>"
            % (ADS_ID, label))

def gtag():
    ids = [i for i in (GA4_ID, ADS_ID) if i]
    if not ids:
        return ""
    cfg = "".join("gtag('config','%s');" % i for i in ids)
    return ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
            "gtag('js',new Date());%s</script>" % (ids[0], cfg))

SCHEMA = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"Church",
"name":"GateCity Buckhead","url":"https://gatecitybuckhead.com/","logo":"https://gatecitybuckhead.com/assets/img/logo.png",
"description":"A presence-centered church in Buckhead, Atlanta. Sundays at 11am at Atlanta International School.",
"address":{"@type":"PostalAddress","streetAddress":"2890 N Fulton Dr NE","addressLocality":"Atlanta","addressRegion":"GA","postalCode":"30305","addressCountry":"US"},
"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"11:00","closes":"12:30"},
"parentOrganization":{"@type":"Organization","name":"All Peoples Church, Inc."}}</script>"""

NOINDEX = ("404", "thanks", "visit-thanks", "webinar-thanks", "christmas-thanks")  # christmas-eve, cohort, assessment: public as of Nov 3 2026

# Vision (5-4-3-2-1) video on /our-mission. Paste the YouTube video ID
# (the part after watch?v=). Blank = the video section is hidden.
VISION_VIDEO_YT = "YmUsydgXMBE"  # 90 Second DNA Video (unlisted)

def vision_video():
    if not VISION_VIDEO_YT:
        return ""
    return ('<section><div class="wrap"><div class="n99-video">'
            '<iframe src="https://www.youtube-nocookie.com/embed/%s" title="GateCity Buckhead vision: 5-4-3-2-1" '
            'style="width:100%%;height:100%%;border:0" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe>'
            '</div></div></section>' % VISION_VIDEO_YT)

# page slug -> (output path, <title>, meta description, solid header?)
PAGES = {
    "index":             ("index.html",                    "GateCity Buckhead | Sundays at 11am in Buckhead, Atlanta", "A presence-centered church in Buckhead. We gather Sundays at 11am at Atlanta International School. Plan your first visit.", False),
    "new-here":          ("new-here/index.html",            "Church in Buckhead, Atlanta | Plan a Visit | GateCity Buckhead",        "Looking for a church near you in Buckhead? GateCity Buckhead is a non-denominational, Spirit-filled church. Sundays at 11am at 2890 N Fulton Dr NE, Atlanta. Kids welcome, free parking.", True),
    "our-mission":       ("our-mission.html",               "Our Mission | GateCity Buckhead",         "GateCity Buckhead helps you walk closely with Jesus today and for the rest of your life. Our vision map, 5-4-3-2-1: five behaviors, four spaces, three promises, two distinctives, one purpose.", True),
    "our-beliefs":       ("our-beliefs.html",               "Our Beliefs | GateCity Buckhead",         "What we believe: the fifteen statements of faith that shape GateCity Buckhead.", True),
    "our-team":          ("our-team.html",                  "Our Team | GateCity Buckhead",            "Meet the leadership team at GateCity Buckhead in Atlanta.", True),
    "buckcity-kids":     ("buckcity-kids.html",             "Kids & Youth | GateCity Buckhead",       "BuckCity Kids for age 3 through 5th grade every Sunday at 11am (check-in at 10:45am), plus middle and high school youth gatherings. Pre-register before your first visit.", True),
    "digital-community": ("digital-community.html",         "Digital Community | GateCity Buckhead",   "Virtual prayer, Sunday Forum, Formation Nights and the Discipleship Cohort — ways to belong between Sundays.", True),
    "resources":         ("resources/index.html",           "Resources | GateCity Buckhead",           "Podcast, books, YouVersion reading plans, music and more from GateCity Buckhead.", True),
    "location":          ("location.html",                  "Where We Meet | GateCity Buckhead",       "GateCity Buckhead meets at Atlanta International School, 2890 N Fulton Dr NE. Directions and parking.", True),
    "pledge":            ("pledge.html",                    "Give | GateCity Buckhead",                "Give to GateCity Buckhead — one-time or recurring, and become one of the 99 partners helping us reach the one.", False),
    "99-for-the-1":      ("99-for-the-1.html",              "99 for the 1 | GateCity Buckhead",        "Jesus left the 99 to go after the one. We're believing for 99 partners — 90 individuals and 9 churches — to sustain and expand GateCity Buckhead.", False),
    "privacy":           ("privacy.html",                   "Privacy Policy | GateCity Buckhead",      "How GateCity Buckhead handles information collected through this website and our tools.", True),
    "cohort":            ("cohort.html",                    "Digital Discipleship Cohort | GateCity Buckhead", "Walk with Jesus daily and grow closer to Him than ever before. An online discipleship cohort from GateCity Buckhead: community, prayer, and simple weekly rhythms. Next cohort starts January 10, 2027.", True),
    "assessment":        ("assessment/index.html",         "Your Walk with Jesus Assessment | GateCity Buckhead", "A free, private snapshot of where you are in your walk with Jesus, with personal growth recommendations.", True),
    "webinar-thanks":    ("cohort/thanks.html",             "You're Registered | GateCity Buckhead",  "Thanks for registering for Your Walk with Jesus Webinar.", True),
    "events":            ("events/index.html",              "Events | GateCity Buckhead", "Upcoming events at GateCity Buckhead in Buckhead, Atlanta, including our Christmas Eve candlelight service.", True),
    "fearless":          ("fearless/index.html",            "Struggling With Anxiety? Free Fearless Devotionals | GateCity Buckhead", "Struggling with anxiety? Three free 7-day Christian devotionals for anxiety and fear, 21 short video devotionals, and a message on fearless living from Pastor Hazen Stevens of GateCity Buckhead.", True),
    "christmas-eve":     ("christmas-eve/index.html",       "Christmas Eve Candlelight Service in Atlanta | GateCity Buckhead", "Christmas Eve candlelight service in Buckhead, Atlanta. Thursday, December 24 at 5pm at Atlanta International School, followed by Christmas cookies. Save your spot.", True),
    "christmas-thanks":  ("christmas-eve/thanks.html",      "You're All Set for Christmas Eve | GateCity Buckhead", "Thanks for saving your spot at the GateCity Buckhead Christmas Eve candlelight service.", True),
    "visit-thanks":      ("new-here/thanks.html",           "You're All Set | GateCity Buckhead",      "Thanks for planning your visit to GateCity Buckhead. See you Sunday at 11am.", True),
    "thanks":            ("thanks.html",                    "Thanks for Subscribing | GateCity Buckhead", "You're on the GCB Weekly list.", True),
    "404":               ("404.html",                       "Page Not Found | GateCity Buckhead",      "That page doesn't exist.", True),
}


def fill(text, extra=None):
    vals = {}
    vals.update(LINKS)
    vals.update(IMAGES)
    vals["YEAR"] = str(datetime.date.today().year)
    vals["GTAG"] = gtag()
    vals["SCHEMA"] = SCHEMA
    vals["VISION_VIDEO"] = vision_video()
    vals.setdefault("ROBOTS", "")
    vals["DONORS_99"] = str(DONORS_99)
    vals["DONORS_99_PCT"] = str(round(min(DONORS_99, 99) / 99 * 100, 1))
    # Cache-busting: short content hash of site.css / site.js so browsers
    # pick up new styles immediately after a deploy.
    for name in ("site.css", "site.js"):
        with open(os.path.join(ROOT, "assets", name), "rb") as f:
            vals[name.upper().replace(".", "_") + "_V"] = hashlib.md5(f.read()).hexdigest()[:8]
    if extra:
        vals.update(extra)
    text = re.sub(r"\{\{NL_FORM:([a-z0-9-]+)(?::([a-z]+))?\}\}", lambda m: newsletter_form(m.group(1), m.group(2)), text)
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
    hero = ""
    if posts:
        p = posts[0]
        desc = p.get("description", "")
        if len(desc) > 220:
            desc = desc[:220].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
        hero = (
            '<section class="blog-hero">\n  <div class="wrap split wide-left">\n'
            '    <a class="msg-thumb" href="/blog/%s"><img src="%s" alt="" loading="lazy"></a>\n'
            '    <div>\n      <div class="eyebrow">From the Blog &middot; %s</div>\n'
            '      <h2>%s</h2>\n      <p class="lede">%s</p>\n'
            '      <div class="btn-row"><a class="btn btn-primary" href="/blog/%s">Read the Post <span class="arrow">&rarr;</span></a>'
            '<a class="btn btn-outline" href="/blog/">All Posts</a></div>\n    </div>\n  </div>\n</section>'
            % (p["slug"], p["cover"], nice_date(p["date"]), _html.escape(p["title"]), _html.escape(desc), p["slug"])
        )
    return outs, latest, hero


# --- Bible plan landing pages (data in plans_data.py) ----------------------
CTA_DEEPER = """<section class="dark">
  <div class="wrap narrow" style="text-align:center">
    <div class="eyebrow on-dark">Your Next Step</div>
    <h2>Do you want to go deeper in your walk with Jesus?</h2>
    <p class="lede">Take Your Walk with Jesus Assessment, about 10 minutes, for a personal snapshot and growth steps. Or join Your Walk with Jesus Webinar, a free live hour on Zoom with Pastors Hazen and Hannah Stevens.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="/assessment/">Take the Assessment <span class="arrow">&rarr;</span></a><a class="btn btn-ghost" href="/cohort#masterclass">Join the Webinar</a></div>
  </div>
</section>
"""


def plan_pages():
    import html as H
    from plans_data import PLANS
    pages = {}
    cards = []
    for pl in PLANS:
        days = ("%d days" % pl["days"]) if pl.get("days") else "Reading plan"
        pts = "".join("<li>%s</li>" % H.escape(x) for x in pl["points"])
        body = f"""<div class="pagehead">
  <div class="wrap">
    <div class="eyebrow on-dark">Free Bible Plan &middot; {days}</div>
    <h1>{H.escape(pl['title'])}.</h1>
    <p class="lede">{H.escape(pl['subtitle'])}</p>
  </div>
</div>

<section>
  <div class="wrap split wide-left">
    <a class="msg-thumb" href="{pl['url']}" target="_blank" rel="noopener">
      <img src="/assets/img/plans/yv/{pl['id']}.jpg" alt="{H.escape(pl['title'])} Bible plan cover" style="opacity:1">
    </a>
    <div>
      <p class="lede">{H.escape(pl['lede'])}</p>
      <ul class="plan-points">{pts}</ul>
      <p style="color:var(--ink-soft)">{H.escape(pl['who'])}</p>
      <div class="btn-row"><a class="btn btn-primary" href="{pl['url']}" target="_blank" rel="noopener">Start the Plan in the Bible App <span class="arrow">&rarr;</span></a></div>
      <p style="color:var(--ink-soft);font-size:14px;margin-top:14px">Free in the Bible App by YouVersion, on your phone or computer.</p>
    </div>
  </div>
</section>

<!--EXTRA-->{{CTA_DEEPER}}"""
        se = pl.get("series")
        extra_html = ""
        from series_data import SERIES as _S
        _ss = next((x for x in _S if pl["slug"] in ([x["plan"]] if isinstance(x.get("plan"), str) else (x.get("plan") or []))), None)
        series_href = ("/series/%s/" % _ss["slug"]) if _ss else ("https://www.youtube.com/playlist?list=" + se["playlist"] if se else "")
        if not se and _ss:
            p1 = _ss["parts"][0]
            se = {"name": _ss["name"], "video": p1["video"], "part": "Part 1: " + p1["title"], "playlist": _ss["playlist"], "related": True}
        if se:
            if se.get("related"):
                lede = "Go deeper with %s, our message series on %s. Start with %s." % (H.escape(se['name']), H.escape(_ss['theme'].lower()), H.escape(se['part']))
                btn = "Watch the Full Series"
            elif se.get("single"):
                series_href = "https://www.youtube.com/playlist?list=" + se["playlist"]
                lede = "Watch %s, the %s message at GateCity Buckhead that goes with this plan." % (H.escape(se['part']), H.escape(se['name']))
                btn = "More from %s" % H.escape(se['name'])
            else:
                lede = "This plan grew out of our %s series at GateCity Buckhead. Start with %s, then watch the rest of the series." % (H.escape(se['name']), H.escape(se['part']))
                btn = "Watch the Full Series"
            series_html = f"""<section class="tight wwj-band">
  <div class="wrap split wide-left">
    <a class="msg-thumb" href="https://www.youtube.com/watch?v={se['video']}&list={se['playlist']}" data-yt-embed="{se['video']}" target="_blank" rel="noopener">
      <img src="https://i.ytimg.com/vi/{se['video']}/maxresdefault.jpg" alt="{H.escape(se['name'])} {H.escape(se['part'])}" loading="lazy">
      <span class="play" aria-hidden="true"></span>
    </a>
    <div>
      <div class="eyebrow">{'The Message' if se.get('single') else 'The Message Series'}</div>
      <h2>{H.escape(se['name'])}.</h2>
      <p class="lede">{lede}</p>
      <div class="btn-row"><a class="btn btn-primary" href="{series_href}"{' target="_blank" rel="noopener"' if series_href.startswith('http') else ''}>{btn} <span class="arrow">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""
            extra_html += series_html
        bk = pl.get("book")
        if bk:
            amz = LINKS[bk["link"]]
            wb = (' <a class="btn btn-outline" href="%s" target="_blank" rel="noopener">Free Companion Workbook (PDF)</a>' % bk["workbook"]) if bk.get("workbook") else ""
            extra_html += f"""<section class="tight wwj-band">
  <div class="wrap split">
    <a class="book-cover plan-book" href="{amz}" target="_blank" rel="noopener"><img src="/assets/img/books/{bk['cover']}.jpg" alt="{H.escape(bk['title'])} by {H.escape(bk['by'])}" loading="lazy"></a>
    <div>
      <div class="eyebrow">The Book</div>
      <h2>{H.escape(bk['title'])}.</h2>
      <div class="by" style="font-weight:600;color:var(--green-ink);margin-bottom:12px">{H.escape(bk['by'])}</div>
      <p class="lede">{H.escape(bk['desc'])} Go deeper than the plan with the full book.</p>
      <div class="btn-row"><a class="btn btn-primary" href="{amz}" target="_blank" rel="noopener">Get the Book on Amazon <span class="arrow">&rarr;</span></a>{wb}</div>
    </div>
  </div>
</section>
"""
        if pl.get("blogs"):
            bymap = {p["slug"]: p for p in load_posts()}
            bcards = "\n".join(post_card(bymap[b]) for b in pl["blogs"] if b in bymap)
            heading = "Read more from the series." if se and not se.get("single") else "Read more on this theme."
            extra_html += f"""<section class="tight">
  <div class="wrap">
    <div class="eyebrow">From the Blog</div>
    <h2>{heading}</h2>
    <div class="cards">
{bcards}
    </div>
  </div>
</section>
"""
        if extra_html:
            body = body.replace('<!--EXTRA-->', extra_html, 1)
        body = body.replace('<!--EXTRA-->', '').replace('{CTA_DEEPER}', CTA_DEEPER).replace('{{CTA_DEEPER}}', CTA_DEEPER)
        key = "plan:" + pl["slug"]
        desc = "%s: a free %s Bible plan from GateCity Buckhead. %s" % (pl["title"], days.lower() if pl.get("days") else "", pl["subtitle"] + ".")
        pages[key] = (("plans/%s/index.html" % pl["slug"]), "%s | Free Bible Plan | GateCity Buckhead" % pl["title"], desc.replace("  ", " "), True, body)
        cards.append(f"""      <div class="card">
        <div class="card-img"><img src="/assets/img/plans/yv/{pl['id']}.jpg" alt="{H.escape(pl['title'])}" loading="lazy"></div>
        <div class="card-body">
          <div class="card-when">{days}</div>
          <h3>{H.escape(pl['title'])}</h3>
          <p>{H.escape(pl['subtitle'])}</p>
          <div class="card-links"><a class="card-link" href="/plans/{pl['slug']}/">See the plan <span class="arrow">&rarr;</span></a></div>
        </div>
      </div>""")
    hub = """<div class="pagehead">
  <div class="wrap">
    <div class="eyebrow on-dark">Free Bible Plans</div>
    <h1>Read the Bible with us.</h1>
    <p class="lede">Free reading plans from GateCity Buckhead in the Bible App, from a few days on prayer and money to the whole Bible in 100 days.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="cards">
%s
      <div class="card">
        <div class="card-img"><img src="/assets/img/plans/songs-of-ascent.jpg?v=2" alt="Read the Songs of Ascent with us" loading="lazy"></div>
        <div class="card-body">
          <div class="card-when">Read along on our site</div>
          <h3>The Songs of Ascent</h3>
          <p>Psalms 120 to 134, with the passages built in.</p>
          <div class="card-links"><a class="card-link" href="/songs-of-ascent/">Open the reading plan <span class="arrow">&rarr;</span></a></div>
        </div>
      </div>
    </div>
  </div>
</section>

""" % "\n".join(cards)
    pages["plan:hub"] = ("plans/index.html", "Free Bible Plans | GateCity Buckhead", "Free Bible reading plans from GateCity Buckhead in the Bible App: prayer, money, holiness, Jesus, and the whole Bible in 100 days.", True, hub)
    return pages


def series_pages():
    import html as H
    from series_data import SERIES
    from plans_data import PLANS
    plans = {p["slug"]: p for p in PLANS}
    posts = {p["slug"]: p for p in load_posts()}
    pages, cards = {}, []
    for s in SERIES:
        n = len(s["parts"])
        p1 = s["parts"][0]
        yt_list = "https://www.youtube.com/playlist?list=" + s["playlist"]
        parts = "\n".join(f"""      <div class="card part-card">
        <a class="msg-thumb" href="https://www.youtube.com/watch?v={p['video']}&list={s['playlist']}" data-yt-embed="{p['video']}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{p['video']}/hqdefault.jpg" alt="{H.escape(s['name'])} Part {p['n']}: {H.escape(p['title'])}" loading="lazy"><span class="play" aria-hidden="true"></span></a>
        <div class="card-body"><div class="card-when">Part {p['n']}</div><h3>{H.escape(p['title'])}</h3></div>
      </div>""" for p in s["parts"])
        body = f"""<div class="pagehead">
  <div class="wrap">
    <div class="eyebrow on-dark">Message Series &middot; {n} Messages &middot; {H.escape(s['theme'])}</div>
    <h1>{H.escape(s['name'])}.</h1>
    <p class="lede">{H.escape(s['lede'])}</p>
  </div>
</div>

<section>
  <div class="wrap split wide-left">
    <a class="msg-thumb" href="https://www.youtube.com/watch?v={p1['video']}&list={s['playlist']}" data-yt-embed="{p1['video']}" target="_blank" rel="noopener">
      <img src="https://i.ytimg.com/vi/{p1['video']}/maxresdefault.jpg" alt="{H.escape(s['name'])} Part 1: {H.escape(p1['title'])}">
      <span class="play" aria-hidden="true"></span>
    </a>
    <div>
      <div class="eyebrow">Start Here</div>
      <h2>Part 1: {H.escape(p1['title'])}.</h2>
      <p class="lede">Press play to watch here, then keep going with the rest of the series below.</p>
      <div class="btn-row"><a class="btn btn-outline" href="{yt_list}" target="_blank" rel="noopener">Full Playlist on YouTube <span class="arrow">&rarr;</span></a></div>
    </div>
  </div>
</section>

<section class="tight wwj-band">
  <div class="wrap">
    <div class="eyebrow">Watch the Series</div>
    <h2>All {n} messages.</h2>
    <div class="cards">
{parts}
    </div>
  </div>
</section>
"""
        pl = s.get("plan")
        pl = [pl] if isinstance(pl, str) and pl else (pl or [])
        if pl:
            pcards = "\n".join(f"""      <a class="card" href="/plans/{plans[x]['slug']}/"><div class="card-img"><img src="/assets/img/plans/yv/{plans[x]['id']}.jpg" alt="{H.escape(plans[x]['title'])}" loading="lazy"></div><div class="card-body"><div class="card-when">{plans[x]['days']} days &middot; Free</div><h3>{H.escape(plans[x]['title'])}</h3><p>{H.escape(plans[x]['subtitle'])}</p><span class="card-link">See the plan <span class="arrow">&rarr;</span></span></div></a>""" for x in pl if x in plans)
            body += f"""
<section class="tight">
  <div class="wrap">
    <div class="eyebrow">Read Along</div>
    <h2>A free Bible plan to go with it.</h2>
    <p class="lede">Short daily readings in the Bible App by YouVersion, on your phone or computer.</p>
    <div class="cards">
{pcards}
    </div>
  </div>
</section>
"""
        bk = s.get("book")
        if bk:
            amz = LINKS[bk["link"]]
            wb = (' <a class="btn btn-outline" href="%s" target="_blank" rel="noopener">Free Companion Workbook (PDF)</a>' % bk["workbook"]) if bk.get("workbook") else ""
            chapters = ""
            if s.get("chapters"):
                chapters = '<ol class="plan-points">' + "".join("<li>%s</li>" % H.escape(c) for c in s["chapters"]) + "</ol>"
            body += f"""
<section class="tight wwj-band">
  <div class="wrap split">
    <a class="book-cover plan-book" href="{amz}" target="_blank" rel="noopener"><img src="/assets/img/books/{bk['cover']}.jpg" alt="{H.escape(s['name'])} by {H.escape(bk['by'])}" loading="lazy"></a>
    <div>
      <div class="eyebrow">The Book</div>
      <h2>{H.escape(s['name'])}.</h2>
      <div class="by" style="font-weight:600;color:var(--green-ink);margin-bottom:12px">{H.escape(bk['by'])}</div>
      <p class="lede">{H.escape(bk['desc'])}</p>
      {chapters}
      <div class="btn-row"><a class="btn btn-primary" href="{amz}" target="_blank" rel="noopener">Get the Book on Amazon <span class="arrow">&rarr;</span></a>{wb}</div>
    </div>
  </div>
</section>
"""
        bl = [posts[x] for x in s.get("blogs", []) if x in posts]
        if bl:
            body += f"""
<section class="tight">
  <div class="wrap">
    <div class="eyebrow">From the Blog</div>
    <h2>Read more from the series.</h2>
    <div class="cards">
{chr(10).join(post_card(p) for p in bl)}
    </div>
  </div>
</section>
"""
        body += "\n" + CTA_DEEPER
        desc = "Watch the %s message series from GateCity Buckhead: %d messages on %s, plus %s." % (s["name"], n, s["theme"].lower(), "the book, a free Bible plan, and blog posts" if bk else "a free Bible plan and blog posts")
        pages["series:" + s["slug"]] = ("series/%s/index.html" % s["slug"], "%s: Watch the Series | GateCity Buckhead" % s["name"], desc, True, body)
        cards.append(f"""      <a class="card" href="/series/{s['slug']}/"><div class="card-img wide"><img src="https://i.ytimg.com/vi/{p1['video']}/hqdefault.jpg" alt="{H.escape(s['name'])}" loading="lazy"></div><div class="card-body"><div class="card-when">{n} messages &middot; {H.escape(s['theme'])}</div><h3>{H.escape(s['name'])}</h3><span class="card-link">Watch the series <span class="arrow">&rarr;</span></span></div></a>""")
    cur = next((x for x in SERIES if x.get("current")), None)
    feat = ""
    if cur:
        feat = f"""
<section class="tight wwj-band">
  <div class="wrap split wide-right">
    <a class="msg-thumb" href="/series/{cur['slug']}/"><img src="/assets/img/series/{cur['slug']}.jpg" alt="{H.escape(cur['name'])}" loading="lazy" style="opacity:1"></a>
    <div>
      <div class="eyebrow">Current Series</div>
      <h2>{H.escape(cur['name'])}.</h2>
      <p class="lede">{H.escape(cur['lede'])}</p>
      <div class="btn-row"><a class="btn btn-primary" href="/series/{cur['slug']}/">Watch the Series <span class="arrow">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""
    hub = """<div class="pagehead">
  <div class="wrap">
    <div class="eyebrow on-dark">Watch</div>
    <h1>Message series.</h1>
    <p class="lede">Teaching from GateCity Buckhead in Atlanta on prayer, the Holy Spirit, perseverance, and walking with Jesus every day. Each series comes with a free Bible plan, blog posts, and often a book.</p>
  </div>
</div>
%s
<section>
  <div class="wrap">
    <div class="cards">
%s
    </div>
  </div>
</section>
""" % (feat, "\n".join(cards)) + CTA_DEEPER
    pages["series:hub"] = ("series/index.html", "Message Series | GateCity Buckhead", "Watch message series from GateCity Buckhead in Atlanta: the Holy Spirit, prayer, perseverance, forgiveness, and more, with free Bible plans and books.", True, hub)
    return pages


def questions_pages():
    """'Your Biggest Questions': /questions/ hub + one page per question (from questions_data.py)."""
    import html as H, json
    from questions_data import QUESTIONS
    from series_data import SERIES
    series = {s["slug"]: s for s in SERIES}
    pages, items = {}, []
    for q in QUESTIONS:
        body = f"""<div class="pagehead">
  <div class="wrap narrow">
    <div class="eyebrow on-dark"><a href="/questions/" style="color:inherit">Your Biggest Questions</a></div>
    <h1>{H.escape(q['q'])}</h1>
  </div>
</div>

<section class="tight">
  <div class="wrap narrow">
    <div class="q-answer">
      <div class="eyebrow">The short answer</div>
      <p class="lede">{H.escape(q['answer'])}</p>
    </div>
  </div>
</section>
"""
        if q.get("video"):
            body += f"""
<section class="tight">
  <div class="wrap narrow">
    <a class="msg-thumb" href="https://www.youtube.com/watch?v={q['video']}" data-yt-embed="{q['video']}" target="_blank" rel="noopener">
      <img src="https://i.ytimg.com/vi/{q['video']}/maxresdefault.jpg" alt="{H.escape(q.get('video_title', q['q']))}" loading="lazy">
      <span class="play" aria-hidden="true"></span>
    </a>
    <p style="margin-top:10px;font-size:15px;color:var(--muted, #5b6660)">{H.escape(q.get('video_title', ''))}</p>
  </div>
</section>
"""
        body += f"""
<section class="tight">
  <div class="wrap narrow post-body prose">
{q['body']}
    <h2>A prayer you can pray</h2>
    <p><em>{H.escape(q['prayer'])}</em></p>
  </div>
</section>
"""
        s = series.get(q.get("series"))
        bk = q.get("book")
        if bk:
            title, cover, link, desc = bk[:4]
            by = q.get('book_by', 'Hazen Stevens')
            amz = LINKS[link]
            watch = f'<a class="btn btn-outline" href="/series/{s["slug"]}/">Watch the {H.escape(s["name"])} Series <span class="arrow">&rarr;</span></a>' if s else ""
            body += f"""
<section class="tight wwj-band">
  <div class="wrap split">
    <a class="book-cover plan-book" href="{amz}" target="_blank" rel="noopener"><img src="/assets/img/books/{cover}.jpg" alt="{H.escape(title)} by {H.escape(by)}" loading="lazy"></a>
    <div>
      <div class="eyebrow">Go Deeper</div>
      <h2>{H.escape(title)}.</h2>
      <div class="by" style="font-weight:600;color:var(--green-ink);margin-bottom:12px">{H.escape(by)}</div>
      <p class="lede">{H.escape(desc)}</p>
      <div class="btn-row"><a class="btn btn-primary" href="{amz}" target="_blank" rel="noopener">Get the Book on Amazon <span class="arrow">&rarr;</span></a>{watch}</div>
    </div>
  </div>
</section>
"""
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}}]}
        body += '\n<script type="application/ld+json">%s</script>\n' % json.dumps(ld)
        body += "\n" + CTA_DEEPER
        pages["q:" + q["slug"]] = ("questions/%s/index.html" % q["slug"], "%s | GateCity Buckhead" % q["q"], q["desc"], True, body)
        items.append(f"""      <a class="card q-card" href="/questions/{q['slug']}/"><div class="card-body"><h3>{H.escape(q['q'])}</h3><p>{H.escape(q['answer'].split('. ')[0])}.</p><span class="card-link">Read the answer <span class="arrow">&rarr;</span></span></div></a>""")
    hub = """<div class="pagehead">
  <div class="wrap">
    <div class="eyebrow on-dark">Resources</div>
    <h1>Your biggest questions.</h1>
    <p class="lede">Honest answers to the questions people ask most about God, the Bible, and following Jesus, from the teaching at GateCity Buckhead in Atlanta.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="cards">
%s
    </div>
  </div>
</section>
""" % "\n".join(items) + CTA_DEEPER
    pages["q:hub"] = ("questions/index.html", "Your Biggest Questions | GateCity Buckhead", "Answers to the questions people ask most about God, the Holy Spirit, forgiveness, prayer, and the Bible, from GateCity Buckhead in Atlanta.", True, hub)
    return pages


def main():
    head = read("partials/head.html")
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    built = []
    blog_outs, blog_latest, blog_hero = render_blog(head, header, footer)
    GEN = plan_pages()
    GEN.update(series_pages())
    GEN.update(questions_pages())
    for k, v in GEN.items():
        PAGES[k] = v[:4]
    for slug, (out, title, desc, solid) in PAGES.items():
        body = GEN[slug][4] if slug in GEN else read("pages/%s.html" % slug)
        body = body.replace("{{BLOG_LATEST}}", blog_latest).replace("{{BLOG_HERO}}", blog_hero).replace("{{BLOG_LATEST_URL}}", "/blog/" + load_posts()[0]["slug"]).replace("{{BLOG_LATEST_TITLE}}", _html.escape(load_posts()[0]["title"])).replace("{{BLOG_LATEST_DESC}}", _html.escape(load_posts()[0].get("description", "")))
        body += ads_conversion(slug)
        path = "/" + out.replace("index.html", "").replace(".html", "")
        page_head = fill(head, {"TITLE": title, "DESC": desc, "PATH": path,
                                "ROBOTS": '<meta name="robots" content="noindex">' if slug in NOINDEX else ""})
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
        if slug in NOINDEX:
            continue
        urls.append(BASE + "/" + out.replace("index.html", "").replace(".html", ""))
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
