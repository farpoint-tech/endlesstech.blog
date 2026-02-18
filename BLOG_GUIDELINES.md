# EndlessTech Blog - Content Creation Guidelines

**IMPORTANT: READ THIS FILE BEFORE CREATING ANY BLOG CONTENT**

---

## 🌍 Language Requirements

### PRIMARY RULE: ALL BLOG CONTENT MUST BE 100% IN ENGLISH

- ✅ **Blog posts:** English only
- ✅ **Titles:** English only
- ✅ **Descriptions:** English only
- ✅ **Meta tags:** English only
- ✅ **Image alt text:** English only
- ✅ **Navigation:** English only
- ❌ **NO German content** in blog posts or UI

**Exception:** Only the author name "Philipp Schmidt" and company references may remain in their original form.

---

## 🎨 Branding Guidelines

### Logo
- **File:** `/assets/images/logo.png`
- **Usage:** Header, footer, social media cards
- **Alt text:** "Philipp Schmidt - Secure. Scalable. Simple M365."

### Main Hero Image
- **File:** `/assets/images/cloudknox-hero.png`
- **Character:** CloudKnox (Rottweiler with "CLOUDKNOX" collar)
- **Usage:** Homepage hero section, main branding image
- **Style:** Neon cyan/pink aesthetic, futuristic tech theme

### Characters
- **CloudKnox:** Rottweiler with "CLOUDKNOX" collar (Main brand mascot, Security guardian)
- **Hawk/Infinity:** Falcon (Monitoring and oversight)
- **Power Duo:** Knox & Hawk together (Combined strength)

**Character Files:**
- `/assets/images/cloudknox-hero.png` - **PRIMARY hero image**
- `/assets/images/knox-hawk-hero.png` - Power duo with cyber effects
- `/assets/images/knox-hawk.png` - General use
- `/assets/images/knox-infinity.png` - Alternative pairing

### Color Scheme
- **Primary:** Royal Blue `#3366FF`
- **Accent:** Orange/Gold `#FFB84D`
- **Neon Cyan:** `#00D9FF` (from CloudKnox image)
- **Neon Pink:** `#FF00FF` (from CloudKnox image)
- **Background:** Light Gray `#F5F5F5` or White `#FFFFFF`
- **Text:** Dark Gray `#333333`
- **Links:** Royal Blue `#3366FF`

### Typography
- **Headings:** Inter or Montserrat (Bold, modern)
- **Body text:** Inter or System-UI (Readable)
- **Code blocks:** Fira Code (Technical content)

---

## 📝 Content Guidelines

### Target Audience
- **Primary:** IT professionals, system administrators, security specialists
- **Secondary:** CXOs, IT decision-makers in SMEs
- **Focus:** Microsoft 365, Security, Zero Trust, Cloud Solutions

### Tone of Voice
- **Professional** but approachable
- **Technical** but not overwhelming
- **Solution-oriented** and practical
- **Educational** with actionable insights

### Content Structure
Each blog post should include:
1. **Engaging title** (SEO-optimized)
2. **Meta description** (150-160 characters)
3. **Hero image** (preferably CloudKnox or Knox & Hawk themed)
4. **Introduction** (Hook the reader)
5. **Main content** (Well-structured with headings)
6. **Key takeaways** (Bullet points or summary)
7. **Call-to-action** (Link to services or contact)
8. **Author bio** (Philipp Schmidt)

### SEO Requirements
- **Title:** 50-60 characters
- **Meta description:** 150-160 characters
- **URL slug:** Lowercase, hyphens, descriptive
- **Headings:** Proper H1, H2, H3 hierarchy
- **Images:** Alt text, compressed, WebP format preferred
- **Internal links:** Link to other blog posts
- **External links:** Open in new tab

---

## 🗂️ File Structure

### Blog Post Location
- **Path:** `/posts/YYYY-MM-DD-slug.md`
- **Example:** `/posts/2025-10-24-microsoft-365-security-best-practices.md`

### Post Frontmatter (YAML)
```yaml
---
title: "Your Blog Post Title"
date: 2025-10-24
author: "Philipp Schmidt"
categories: ["Security", "Microsoft 365", "Zero Trust"]
tags: ["M365", "Security", "Best Practices"]
excerpt: "A brief summary of the blog post (150-160 characters)"
image: "/assets/images/cloudknox-hero.png"
featured: true
---
```

### Categories (Use these consistently)
- **Security** - Security-related topics
- **Microsoft 365** - M365 features, tips, updates
- **Zero Trust** - Zero Trust architecture and implementation
- **Cloud Solutions** - Cloud strategy and migration
- **Compliance** - NIS2, GDPR, regulations
- **Automation** - PowerShell, automation tools
- **Best Practices** - How-to guides and recommendations

---

## 🧱 Formatting & Layout Standards

### Single Post Template (HTML)
- **Required layout:** `article.post-full` with:
  - `header.post-full-header` → `h1.post-full-title` and `div.post-full-meta` (`<time>` + author)
  - `figure.post-full-image` for the hero image (max-height enforced via CSS)
  - `section.post-full-content` containing `div.post-content` for all text and elements
  - `section.author-bio` with avatar and info
  - Site-wide footer using `footer.footer > .footer-container`

### Consistent Spacing & Width
- **Max content width:** Use site variable `--max-width-content` (currently 800px)
- **Left/right spacing:** Always use `.post-full` and `.container` wrappers; never override padding/margins inline
- **Headings:** H1 once per post, then H2/H3 hierarchy only

### Images
- **Hero image:** Place inside `figure.post-full-image`; CSS limits height and ensures cover fit
- **Inline images:** Use `figure.post-content-image` with `<img>` and `<figcaption>`
- **Do not** use inline styles for sizing or margins; rely on CSS classes
- **Alt text:** Descriptive, in English

### Blockquotes, Lists, Tables, Code
- **Blockquotes:** Use plain `<blockquote>`; styling comes from CSS (border, spacing, italics)
- **Lists:** Standard `<ul>/<ol>`; no custom inline margins
- **Tables:** Use `.post-table` (headers, rows, hover states standardized)
- **Code:** `<pre><code>` only; no inline style attributes

### No Inline Styles
- Avoid inline `style=""` in posts (images, figures, quotes, headings)
- All visual adjustments must be done via shared CSS:
  - `assets/css/style.css`
  - `assets/css/blog-post.css` (post-specific refinements)

### HTML Skeleton Example
```html
<article class="post-full">
  <header class="post-full-header">
    <h1 class="post-full-title">Post Title</h1>
    <div class="post-full-meta">
      <time datetime="YYYY-MM-DD">Month D, YYYY</time> • By Philipp Schmidt
    </div>
  </header>

  <figure class="post-full-image">
    <img src="../assets/images/hero.png" alt="Hero Alt">
  </figure>

  <section class="post-full-content">
    <div class="post-content">
      <h2>Section</h2>
      <p>Paragraph text…</p>

      <figure class="post-content-image">
        <img src="../assets/images/example.png" alt="Example">
        <figcaption>Concise caption</figcaption>
      </figure>

      <blockquote>Key callout.</blockquote>
    </div>
  </section>

  <section class="author-bio">
    <img src="../assets/images/cloudknox-author.png" alt="CloudKnox - Philipp Schmidt" class="author-avatar">
    <div class="author-info">
      <h3>Philipp Schmidt</h3>
      <p>IT consultant specializing in Microsoft 365, Security, and Zero Trust.</p>
    </div>
  </section>
</article>
```

### Validation Checklist (Formatting)
- [ ] Uses `.post-full` and `.post-full-content` containers
- [ ] Meta section includes `<time>` and author
- [ ] Hero image inside `.post-full-image`
- [ ] Inline figures use `.post-content-image` + caption
- [ ] No inline `style=""` anywhere
- [ ] Footer uses `.footer-container`
- [ ] Author bio section present

---

## 🎯 LinkedIn Announcement Guidelines

### When creating LinkedIn posts:
1. **Language:** English (matching blog content)
2. **Length:** 150-300 characters (short and engaging)
3. **Include:**
   - Hook (first line must grab attention)
   - Key benefit or insight
   - Link to blog post
   - Call-to-action
   - Relevant hashtags (3-5)

### Example LinkedIn Post Template:
```
🔒 [Attention-grabbing statement or question]

[One-sentence key insight from the blog]

[Brief explanation or benefit - 1-2 sentences]

Read the full guide: [Blog URL]

#Microsoft365 #CyberSecurity #ZeroTrust #CloudSecurity
```

---

## ✅ Pre-Publication Checklist

Before pushing any blog post, verify:

- [ ] **Content is 100% in English**
- [ ] Title is SEO-optimized (50-60 characters)
- [ ] Meta description is present (150-160 characters)
- [ ] Frontmatter is complete and correct
- [ ] Images are optimized and have alt text
- [ ] Internal links are working
- [ ] External links open in new tab
- [ ] Code blocks have proper syntax highlighting
- [ ] Headings follow proper hierarchy (H1 → H2 → H3)
- [ ] Author bio is included
- [ ] Call-to-action is present
- [ ] Categories and tags are assigned
- [ ] LinkedIn announcement text is prepared
- [ ] Giscus comments are enabled (if applicable)

---

## 🚀 Publishing Workflow

### Step 1: Create Blog Post
1. Write content in Markdown
2. Add frontmatter
3. Optimize images
4. Add internal/external links
5. Review checklist

### Step 2: Push to GitHub
```bash
cd /home/ubuntu/endlesstech.blog
git add posts/YYYY-MM-DD-slug.md
git add assets/images/ (if new images)
git commit -m "Add blog post: [Title]"
git push origin master
```

### Step 3: Verify Deployment
1. Wait 2-3 minutes for GitHub Pages to build
2. Visit blog URL
3. Check formatting, images, links
4. Test on mobile devices

### Step 4: LinkedIn Announcement
1. Use prepared LinkedIn post text
2. User posts manually (or via browser automation)
3. Include blog link
4. Engage with comments

---

## 📊 Analytics & Tracking

### Monitor:
- Page views (GitHub Pages stats)
- LinkedIn engagement (likes, comments, shares)
- Giscus comments
- Referral sources

### Optimize:
- Update popular posts with new information
- Create follow-up posts for high-engagement topics
- Improve SEO for underperforming posts

---

## 🔄 Maintenance

### Regular Tasks:
- **Weekly:** Check for broken links
- **Monthly:** Update outdated content
- **Quarterly:** Review analytics and adjust strategy

### Content Updates:
- Microsoft 365 feature updates
- Security patches and vulnerabilities
- Industry news and trends
- User feedback and questions

---

## 📞 Contact & Support

**Author:** Philipp Schmidt  
**Website:** https://easym365.de  
**Tagline:** "Secure. Scalable. Simple M365."

---

**Last Updated:** 2025-10-24  
**Version:** 1.1
