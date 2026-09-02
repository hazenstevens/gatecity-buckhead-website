# Go-live checklist

Work top to bottom. Nothing here touches the live site until Step 5.

---

## ⚠️ Read this first: the photos

Every photo on the new site is still being loaded **from Squarespace's servers**.
The pages point at URLs like `images.squarespace-cdn.com/...`.

**If you cancel Squarespace before fixing this, every image on the site breaks.**

Fixing it is Step 4. Do not skip it, and do not cancel Squarespace until Step 8.

---

## Step 1 — Create the GitHub repo

1. Go to <https://github.com/new>
2. Owner: the church organization if you have one, otherwise your account
3. Repository name: `gatecity-buckhead-website`
4. Set it to **Private**
5. Do **not** add a README, .gitignore, or license — this repo already has them
6. Click **Create repository**

Then, in the folder containing these files:

```bash
git init
git add .
git commit -m "New GateCity Buckhead website"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/gatecity-buckhead-website.git
git push -u origin main
```

If `git push` asks for a password, use a personal access token, not your GitHub
password. GitHub → Settings → Developer settings → Personal access tokens.

## Step 2 — Connect Netlify

1. Sign up at <https://netlify.com> with your GitHub account
2. **Add new site → Import an existing project → GitHub**
3. Pick `gatecity-buckhead-website`
4. Leave the build settings alone — `netlify.toml` already sets them
   (build command: empty, publish directory: `.`)
5. Click **Deploy**

You'll get a URL like `random-name-12345.netlify.app`. **The real site is still
untouched.** Open the Netlify URL and click through every page.

## Step 3 — Add the team

Netlify → Site settings → Members. Invite anyone who needs to publish.
GitHub → repo → Settings → Collaborators for anyone who needs to edit code.

## Step 4 — Move the photos off Squarespace

While Squarespace is still running:

1. Open each URL in the `IMAGES` dictionary at the top of `build.py`
2. Right-click → Save Image As → into a new `assets/img/` folder
3. In `build.py`, change each entry from the long squarespace-cdn URL to
   `/assets/img/hero.jpg` (and so on)
4. `python3 build.py`, then commit and push
5. Reload the Netlify URL and confirm every image still appears

Ask Claude to do this if you'd rather — but the *downloading* has to happen on
your computer, since the files are behind Squarespace.

## Step 5 — Point the domain at Netlify

This is the moment the public site changes.

1. Netlify → Domain settings → **Add custom domain** → `gatecitybuckhead.com`
2. Netlify will show you the DNS records it needs
3. Go to wherever your domain is registered (possibly Squarespace, possibly
   GoDaddy or Google Domains) and update the records to match
4. Wait. DNS usually moves within an hour but can take up to 48

Netlify issues an SSL certificate automatically once DNS resolves. Don't panic
if the site shows a security warning for the first few minutes.

## Step 6 — Check the old URLs still work

After DNS moves, load each of these and confirm none 404:

- `/` `/new-here/` `/our-beliefs` `/our-team` `/buckcity-kids`
- `/digital-community` `/resources/`
- `/home/` → should redirect to `/location`
- `/pledge` → should redirect to Church Center giving

## Step 7 — Tell Google

1. <https://search.google.com/search-console> → add the property
2. Submit `https://www.gatecitybuckhead.com/sitemap.xml`

The old site had `robots.txt` blocking AI crawlers. The new one doesn't, so
assistants can find you when someone asks about churches in Buckhead.

## Step 8 — Only now, cancel Squarespace

Confirm first:

- [ ] Every page loads on the real domain
- [ ] Every image loads (Step 4 is done — check on your phone too)
- [ ] Forms and Zoom links open correctly
- [ ] Anything you had on Squarespace that isn't in this repo has been saved

Then cancel.

---

## If something goes wrong

**A change broke the site:** Netlify → Deploys → last good deploy → "Publish
deploy." Ten seconds.

**The whole thing is wrong and you want the old site back:** change the DNS
records back to Squarespace. As long as you haven't cancelled (Step 8), the old
site is still sitting there and comes back when DNS propagates.

That's why Step 8 is last.
