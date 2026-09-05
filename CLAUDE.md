# EndlessTech Blog

Static blog hosted on GitHub Pages at **endlesstech.blog**. Author: Philipp Schmidt / farpoint.tech.

## Quick Reference

```bash
# No build step — push to master, GitHub Pages deploys in ~2 min
git push origin master
```

No Jekyll. Plain HTML + CSS. No static site generator.

## Content Rules

- **All content must be in English.** No German in posts, titles, meta, or UI.
- See `BLOG_GUIDELINES.md` for detailed branding, formatting, SEO, and publishing rules.

## Structure

```
index.html                 # Homepage with post listing
about.html                 # About page
CNAME                      # Custom domain: endlesstech.blog
assets/
├── css/
│   ├── style.css          # Site-wide styles
│   └── blog-post.css      # Post-specific styles
├── js/main.js             # Site JavaScript
└── images/                # All images (logo, heroes, post images)
posts/
├── YYYY-MM-DD-slug.html   # Published posts (HTML)
└── YYYY-MM-DD-slug.md     # Source drafts (some posts have both)
```

## Creating a Post

1. Create `posts/YYYY-MM-DD-slug.html` following the HTML skeleton in `BLOG_GUIDELINES.md`
2. Use CSS classes only — no inline `style=""` attributes
3. Required structure: `.post-full` > `.post-full-header` + `.post-full-image` + `.post-full-content` > `.post-content` + `.author-bio`
4. On the release day, add the post to `index.html`, `sitemap.xml`, `feed.xml`, and `llms.txt` in the same change — or let the scheduled release do it (see below)
5. Run `python3 tools/check-findability.py` — it must be green
6. Commit and push to `master`

### Renaming a post

Never just delete the old file — that turns every existing inbound link into a
404. Leave a **redirect stub** at the old path: a minimal page with a
`<meta http-equiv="refresh">` to the new URL, a `<link rel="canonical">`, and
`<meta name="robots" content="noindex, follow">`. See
`posts/2026-07-19-zero-trust-m365-*.html`.

A file with both a meta refresh and a `noindex` robots directive is treated as a
stub: it is deliberately kept out of `index.html`, `sitemap.xml`, `feed.xml` and
`llms.txt`, and `tools/check-findability.py` does not report it as missing — but
it does fail if the stub's target no longer exists or if a stub gets listed.

## Scheduled posts

**Never commit article HTML to `master` before its release date.** GitHub Pages
serves every file on that branch, so a post on `master` is public the moment it
lands there — a `noindex` tag is a crawl-control fallback, not a confidentiality
boundary.

Preparing a post:

1. Commit the article to the **`scheduled-posts`** branch (`posts/YYYY-MM-DD-slug.html`),
   together with any images it needs that `master` does not already have.
2. Add its release date to **`.scheduled/releases.json`**:
   `{"date": "2026-09-10", "slug": "2026-09-03-entra-pim-authentication-context",
   "card": ".scheduled/cards/2026-09-03-entra-pim-authentication-context.html"}`.
   The slug is the filename without `.html`; the release date and the date in the
   filename are independent of each other.
3. Commit the homepage card to **`.scheduled/cards/<slug>.html`** on `master`
   (a card only, no article text) — copy the markup of an existing `.post-card`.
   Visible dates use *Month YYYY* of the release, not the day.

On the release day the workflow `.github/workflows/release-series.yml` runs
`.github/scripts/release-scheduled.py` at 07:50 Europe/Berlin. It picks up every
entry due today or earlier that is not on `master` yet, so a missed run catches
up by itself, and it:

- fetches `posts/<slug>.html` and any missing `assets/` files from `scheduled-posts`
- inserts the card into the main listing of `index.html` at the
  `<!-- SERIES-RELEASE-SLOT -->` marker and re-sorts it newest first
- deletes the consumed card
- regenerates `sitemap.xml`, `feed.xml` and `llms.txt`
- runs `tools/check-findability.py` and refuses to commit if it fails

Nothing due is a green, empty run. Do not remove the `SERIES-RELEASE-SLOT`
marker from `index.html` — without it the release fails.

Manual run: the workflow has a `workflow_dispatch` input `date` (YYYY-MM-DD).
Locally, `python3 .github/scripts/release-scheduled.py 2026-09-10` does the same
thing without committing.

## Design

- Primary: `#3366FF` (Royal Blue), Accent: `#FFB84D` (Gold)
- Neon theme from CloudKnox mascot: Cyan `#00D9FF`, Pink `#FF00FF`
- Font: Inter / system-ui, Code: Fira Code
- Max content width: `--max-width-content` (800px)

## Branding

- **CloudKnox**: Rottweiler mascot (main hero: `assets/images/cloudknox-hero.png`)
- **Hawk/Infinity**: Falcon companion
- Logo: `assets/images/logo.png`

## Topics

Microsoft 365, Security, Zero Trust, Cloud Solutions, Compliance (NIS2/GDPR), Intune, Automation.

## Articles under review

An article whose facts are in doubt stays reachable by URL but is pulled from
every listing. Add to its `<head>`:

```html
<meta name="robots" content="noindex, follow">
<meta name="endlesstech-status" content="under-review">
```

then run `python3 tools/site_index.py` — it parks the homepage card in
`.scheduled/unlisted-cards/` and regenerates sitemap, feed and llms.txt.
Remove both tags and run the same command to relist. `check-findability.py`
fails if an article under review is still listed anywhere.
