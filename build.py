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
    return ("\n<script>gtag('event','conversion',{send_to:'%s/%s',value:1.0,currency:'USD'});</script>"
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
    "new-here":          ("new-here/index.html",            "Plan a Visit | GateCity Buckhead",        "Everything you need for your first Sunday at GateCity Buckhead — what to expect, parking, kids, and how to get connected.", True),
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

<section>
  <div class="wrap narrow">
    <div class="eyebrow">Want to go deeper?</div>
    <h2>Walk with Jesus, together.</h2>
    <p class="lede">Take the free Your Walk with Jesus Assessment, about 10 minutes, for a personal snapshot and growth steps, or join us on a Sunday in Buckhead, Atlanta.</p>
    <div class="btn-row"><a class="btn btn-primary" href="/assessment/">Take the Free Assessment <span class="arrow">&rarr;</span></a><a class="btn btn-outline" href="/plans/">More Bible Plans</a></div>
  </div>
</section>
"""
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


def main():
    head = read("partials/head.html")
    header = read("partials/header.html")
    footer = read("partials/footer.html")

    built = []
    blog_outs, blog_latest, blog_hero = render_blog(head, header, footer)
    GEN = plan_pages()
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
