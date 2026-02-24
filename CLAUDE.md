# EndlessTech Blog

## Overview

A GitHub Pages-hosted technology blog by Philipp Schmidt focused on Microsoft 365, Security, Zero Trust, and Cloud Solutions. The blog features a custom mascot character "CloudKnox" (a Rottweiler) and companion "Hawk" (a Falcon).

**Live site:** https://farpoint-tech.github.io/endlesstech.blog
**Author:** Philipp Schmidt
**Tagline:** "Secure. Scalable. Simple M365."

## Critical Rules

- **ALL content must be 100% in English** (no German content in posts or UI)
- Exception: author name "Philipp Schmidt" and company references keep original form
- No inline `style=""` attributes in posts - use CSS classes only
- Always follow the HTML template structure in BLOG_GUIDELINES.md
- Read BLOG_GUIDELINES.md before creating any blog content

## Tech Stack

- **Hosting:** GitHub Pages (free, HTTPS enabled)
- **Format:** Static HTML + CSS + JS (no Jekyll processing, `.nojekyll` present)
- **Domain:** Custom domain configured via CNAME file
- **Deployment:** Push to master, GitHub Pages auto-deploys

## File Structure

```
/
  index.html          - Homepage with post listings
  about.html          - About page
  CNAME               - Custom domain config
  .nojekyll           - Disables Jekyll processing
  BLOG_GUIDELINES.md  - Comprehensive content creation guide
  /posts/             - Blog posts (HTML and MD files)
    YYYY-MM-DD-slug.html   - Published post (HTML)
    YYYY-MM-DD-slug.md     - Source markdown (some posts)
  /assets/
    /css/             - Stylesheets (style.css, blog-post.css)
    /images/          - All images (hero, logos, post images)
    /js/              - JavaScript files
```

## Blog Post HTML Template

Posts must use this structure:
- `article.post-full` wrapper
  - `header.post-full-header` with `h1.post-full-title` and `div.post-full-meta`
  - `figure.post-full-image` for hero image
  - `section.post-full-content > div.post-content` for body text
  - `section.author-bio` with avatar and info
  - Site-wide footer using `footer.footer > .footer-container`

## Branding

- **Primary color:** Royal Blue `#3366FF`
- **Accent:** Orange/Gold `#FFB84D`
- **Neon Cyan:** `#00D9FF` (CloudKnox aesthetic)
- **Neon Pink:** `#FF00FF` (CloudKnox aesthetic)
- **Background:** Light Gray `#F5F5F5` or White `#FFFFFF`
- **Text:** Dark Gray `#333333`
- **Logo:** `/assets/images/logo.png`
- **Hero image:** `/assets/images/cloudknox-hero.png`

## Content Categories

Security, Microsoft 365, Zero Trust, Cloud Solutions, Compliance, Automation, Best Practices

## Target Audience

IT professionals, system administrators, security specialists, CXOs, IT decision-makers in SMEs

## Publishing Workflow

1. Write content following BLOG_GUIDELINES.md
2. Create HTML file in /posts/ with proper naming: `YYYY-MM-DD-slug.html`
3. Commit and push to master
4. Verify deployment on live site after 2-3 minutes
5. Prepare LinkedIn announcement text

## SEO Requirements

- Title: 50-60 characters
- Meta description: 150-160 characters
- URL slugs: lowercase, hyphens, descriptive
- Proper heading hierarchy (H1 once, then H2/H3)
- All images need descriptive alt text in English
- Images should be optimized, WebP preferred
