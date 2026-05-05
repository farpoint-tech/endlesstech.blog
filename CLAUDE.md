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
4. Add the post to the listing on `index.html`
5. Commit, push to master

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
