# GateCity Buckhead — website

The site for [gatecitybuckhead.com](https://www.gatecitybuckhead.com). Plain HTML
and CSS. No frameworks, no npm, no database. Netlify serves the files in this
repo exactly as they are.

---

## How to change something

**The short version:** ask Claude. Say what you want changed, and it edits the
right file, rebuilds, and pushes. You don't have to learn any of what follows.

**If you want to do it yourself:**

1. Edit the file in `pages/` (page content) or `partials/` (header, footer, `<head>`).
2. Run `python3 build.py`
3. Commit and push. Netlify deploys in about 30 seconds.

### Important

Do **not** edit `index.html`, `our-team.html`, or any other `.html` file at the
top level. Those are generated. `build.py` overwrites them every time it runs.
Edit `pages/` and `partials/` instead.

---

## Where things live

```
pages/           <- the content of each page. Edit these.
partials/        <- header, footer, and <head>. Shared by every page.
assets/site.css  <- all styling
assets/site.js   <- nav dropdowns and the mobile menu
build.py         <- assembles pages/ + partials/ into the .html files
netlify.toml     <- hosting config and URL redirects
```

## Changing a link

Every outbound URL — Church Center forms, Zoom rooms, the giving page, YouTube —
lives in the `LINKS` dictionary at the top of `build.py`. Change it once there,
run `python3 build.py`, and it updates on every page that uses it.

Same for photos: the `IMAGES` dictionary right below it.

## Changing the navigation

`partials/header.html`. It contains both the desktop nav and the mobile menu, so
change it in both places in that one file, then rebuild.

---

## What stays in Planning Center

Events, giving, and every sign-up form still live in Planning Center / Church
Center. The website only links to them. Nobody needs to update the website when
an event changes — update it in Planning Center like always.

Sermons live on YouTube. Same idea.

---

## Deploying

Pushing to the `main` branch deploys automatically. Pull requests get their own
preview URL, so a change can be looked at before it goes live.

To undo a bad change: Netlify → Deploys → find the last good one → "Publish
deploy." Takes about ten seconds.
