#!/usr/bin/env python3
"""Shared helpers for generating the site index files of endlesstech.blog.

Used by:
  * tools/check-findability.py        (validation)
  * .github/scripts/release-scheduled.py (scheduled release automation)
  * one-off maintenance scripts

Standard library only. No build step, no dependencies.
"""

from __future__ import annotations

import datetime as _dt
import glob
import html as _html
import os
import re
import subprocess
import xml.sax.saxutils as _sax

SITE_URL = "https://endlesstech.blog"
POSTS_DIR = "posts"
GRID_OPEN = '<div class="posts-grid">'
GRID_CLOSE = "\n            </div>\n        </section>"
RELEASE_MARKER = "<!-- SERIES-RELEASE-SLOT -->"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
RFC822_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RFC822_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

_DATE_PREFIX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-")

# A redirect stub is a retired URL kept alive: it forwards to the article that
# replaced it and asks robots not to index it. Stubs are content-free, so they
# are never listed in index.html, sitemap.xml, feed.xml or llms.txt — but the
# URL they forward to has to exist.
_META_REFRESH = re.compile(
    r'<meta[^>]+http-equiv=["\']?refresh["\']?[^>]*content=["\'][^"\']*'
    r'url=\s*([^"\';\s]+)', re.I)
_ROBOTS_NOINDEX = re.compile(
    r'<meta[^>]+name=["\']?robots["\']?[^>]*content=["\'][^"\']*noindex', re.I)

# An article under review stays reachable by URL but is pulled from every
# listing (homepage, sitemap, feed, llms.txt) until its facts are settled.
# Mark it with <meta name="endlesstech-status" content="under-review"> and a
# robots noindex; remove both tags to relist it.
_UNDER_REVIEW = re.compile(
    r'<meta[^>]+name=["\']?endlesstech-status["\']?[^>]*content=["\']under-review', re.I)


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def _search(pattern: str, text: str):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else None


def plain(text: str | None) -> str:
    """HTML source fragment -> plain unicode text."""
    if not text:
        return ""
    text = re.sub(r"(?s)<[^>]+>", "", text)
    return re.sub(r"\s+", " ", _html.unescape(text)).strip()


def xml_escape(text: str) -> str:
    return _sax.escape(text)


def month_year(date_str: str | None) -> str:
    if not date_str:
        return ""
    y, m, _d = date_str.split("-")
    return "%s %s" % (MONTHS[int(m) - 1], y)


def rfc822(date_str: str) -> str:
    y, m, d = (int(x) for x in date_str.split("-"))
    day = _dt.date(y, m, d)
    return "%s, %02d %s %04d 00:00:00 +0000" % (
        RFC822_DAYS[day.weekday()], d, RFC822_MONTHS[m - 1], y)


def _git_added_date(root: str, relpath: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%ad", "--date=short",
             "-1", "--", relpath],
            cwd=root, capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    value = out.stdout.strip().splitlines()
    if out.returncode == 0 and value and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value[0]):
        return value[0]
    return None


# --------------------------------------------------------------------------
# post metadata
# --------------------------------------------------------------------------

def redirect_target(text: str) -> str | None:
    """The article a redirect stub forwards to, or None if it is a real post.

    A file counts as a stub only when it both meta-refreshes somewhere and
    carries a noindex robots directive — a real article never does both.
    """
    refresh = _META_REFRESH.search(text)
    if not refresh or not _ROBOTS_NOINDEX.search(text):
        return None
    return refresh.group(1).strip()


def stub_target_filename(target: str) -> str | None:
    """posts/<file>.html the stub points at, or None if it leaves the blog."""
    if target.startswith(("http://", "https://")):
        if not target.startswith(SITE_URL + "/"):
            return None
        target = target[len(SITE_URL) + 1:]
    target = target.split("#")[0].split("?")[0].lstrip("/")
    if target.startswith(POSTS_DIR + "/"):
        return target[len(POSTS_DIR) + 1:]
    return None


def read_stubs(root: str) -> dict:
    """{filename: redirect target} for every redirect stub in posts/."""
    stubs = {}
    for path in sorted(glob.glob(os.path.join(root, POSTS_DIR, "*.html"))):
        target = redirect_target(read(path))
        if target is not None:
            stubs[os.path.basename(path)] = target
    return stubs


def is_under_review(text: str) -> bool:
    return bool(_UNDER_REVIEW.search(text)) and redirect_target(text) is None


def read_under_review(root: str) -> set:
    """Filenames in posts/ that are marked under review (unlisted, noindex)."""
    out = set()
    for path in sorted(glob.glob(os.path.join(root, POSTS_DIR, "*.html"))):
        if is_under_review(read(path)):
            out.add(os.path.basename(path))
    return out


def read_post(root: str, filename: str) -> dict:
    relpath = "%s/%s" % (POSTS_DIR, filename)
    text = read(os.path.join(root, relpath))

    title = _search(r'<h1 class="post-full-title">(.*?)</h1>', text)
    if not title:
        title = _search(r'"headline"\s*:\s*"(.*?)"', text)
    if not title:
        title = _search(r"<title>(.*?)</title>", text) or filename
    title = re.sub(r"\s*\|\s*EndlessTech Blog\s*$", "", title.strip())

    description = _search(r'<meta\s+name="description"\s+content="(.*?)"', text) or ""

    date_published = _search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', text)
    date_modified = _search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', text)
    file_date = None
    m = _DATE_PREFIX.match(filename)
    if m:
        file_date = "%s-%s-%s" % m.groups()

    visible_time = _search(r"<time[^>]*>(.*?)</time>", text)

    published = date_published or file_date or _git_added_date(root, relpath)
    modified = date_modified or file_date or published

    return {
        "filename": filename,
        "relpath": relpath,
        "url": "%s/%s" % (SITE_URL, relpath),
        "title_html": title,
        "title": plain(title),
        "description_html": description,
        "description": plain(description),
        "published": published,
        "modified": modified,
        "file_date": file_date,
        "visible_date": plain(visible_time) if visible_time else "",
        "sort_key": published or "0000-00-00",
    }


def read_posts(root: str) -> list[dict]:
    """All listable posts/*.html, newest first.

    Redirect stubs and articles marked under review are skipped."""
    files = sorted(os.path.basename(p)
                   for p in glob.glob(os.path.join(root, POSTS_DIR, "*.html")))
    stubs = read_stubs(root)
    review = read_under_review(root)
    posts = [read_post(root, f) for f in files if f not in stubs and f not in review]
    posts.sort(key=lambda p: (p["sort_key"], p["filename"]), reverse=True)
    return posts


def posts_by_filename(posts: list[dict]) -> dict:
    return {p["filename"]: p for p in posts}


# --------------------------------------------------------------------------
# index.html card grid
# --------------------------------------------------------------------------

def split_grid(index_text: str) -> tuple[str, str, str]:
    """Return (before, grid_inner, after) for the main .posts-grid listing."""
    start = index_text.index(GRID_OPEN) + len(GRID_OPEN)
    end = index_text.index(GRID_CLOSE, start)
    return index_text[:start], index_text[start:end], index_text[end:]


def extract_cards(grid_inner: str) -> list[str]:
    return re.findall(r'<article class="post-card".*?</article>', grid_inner, re.S)


def card_target(card_html: str) -> str | None:
    m = re.search(r'href="posts/([^"#]+\.html)"', card_html)
    return m.group(1) if m else None


def render_grid(cards: list[str]) -> str:
    """Rebuild the inner part of .posts-grid, marker first, cards newest first."""
    body = "\n\n".join("                " + c.strip() for c in cards)
    return "\n                %s\n\n%s\n\n" % (RELEASE_MARKER, body)


def sort_cards(cards: list[str], posts: list[dict]) -> list[str]:
    index = posts_by_filename(posts)

    def key(card):
        target = card_target(card)
        post = index.get(target)
        return (post["sort_key"] if post else "0000-00-00", target or "")

    return sorted(cards, key=key, reverse=True)


def set_grid(index_text: str, cards: list[str], posts: list[dict]) -> str:
    before, _old, after = split_grid(index_text)
    return before + render_grid(sort_cards(cards, posts)) + after


def insert_card(index_text: str, card_html: str, posts: list[dict]) -> str:
    """Add one card to the main listing and re-sort newest first."""
    before, grid_inner, after = split_grid(index_text)
    if RELEASE_MARKER not in index_text:
        raise ValueError("release marker %s missing from index.html" % RELEASE_MARKER)
    cards = extract_cards(grid_inner)
    target = card_target(card_html)
    cards = [c for c in cards if card_target(c) != target]
    cards.append(card_html.strip())
    return before + render_grid(sort_cards(cards, posts)) + after


# --------------------------------------------------------------------------
# sitemap.xml
# --------------------------------------------------------------------------

def build_sitemap(posts: list[dict]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             "  <url>",
             "    <loc>%s/</loc>" % SITE_URL,
             "    <changefreq>weekly</changefreq>",
             "    <priority>1.0</priority>",
             "  </url>",
             "  <url>",
             "    <loc>%s/about.html</loc>" % SITE_URL,
             "    <changefreq>monthly</changefreq>",
             "    <priority>0.6</priority>",
             "  </url>"]
    for post in posts:
        lines.append("  <url>")
        lines.append("    <loc>%s</loc>" % xml_escape(post["url"]))
        if post["modified"]:
            lines.append("    <lastmod>%s</lastmod>" % post["modified"])
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# feed.xml
# --------------------------------------------------------------------------

def build_feed(posts: list[dict], old_feed: str) -> str:
    """Regenerate the item list, keep the existing channel header verbatim."""
    head_end = old_feed.index("    <item>")
    head = old_feed[:head_end]
    newest = next((p["published"] for p in posts if p["published"]), None)
    if newest:
        head = re.sub(r"<lastBuildDate>.*?</lastBuildDate>",
                      "<lastBuildDate>%s</lastBuildDate>" % rfc822(newest), head)

    items = []
    for post in posts:
        pub = post["published"] or post["modified"]
        item = ["    <item>",
                "      <title>%s</title>" % xml_escape(post["title"]),
                "      <link>%s</link>" % xml_escape(post["url"]),
                "      <guid>%s</guid>" % xml_escape(post["url"]),
                ]
        if pub:
            item.append("      <pubDate>%s</pubDate>" % rfc822(pub))
        item.append("      <description>%s</description>" % xml_escape(post["description"]))
        item.append("    </item>")
        items.append("\n".join(item))

    return head + "\n\n".join(items) + "\n  </channel>\n</rss>\n"


# --------------------------------------------------------------------------
# llms.txt
# --------------------------------------------------------------------------

ALL_ARTICLES_HEADING = "## All articles"


def one_liner(post: dict, limit: int = 155) -> str:
    text = post["description"] or post["title"]
    # first sentence, but never cut mid-word
    match = re.match(r"(.+?[.!?])(?:\s|$)", text)
    if match and len(match.group(1)) >= 40:
        text = match.group(1)
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    return text


def llms_entry(post: dict) -> str:
    return "- [%s](%s) — %s" % (post["title"], post["url"], one_liner(post))


def build_llms(posts: list[dict], old_llms: str) -> str:
    """Keep the existing section structure; every post appears exactly once.

    Posts already curated in a hand-written section (``Start here``, the series
    section, ...) keep their place and get a one-liner; everything else is
    regenerated under ``## All articles``, newest first.
    """
    index = posts_by_filename(posts)
    lines = old_llms.splitlines()

    # locate section boundaries
    heads = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    try:
        all_i = next(i for i in heads if lines[i].strip() == ALL_ARTICLES_HEADING)
    except StopIteration:
        raise ValueError("llms.txt: '%s' section not found" % ALL_ARTICLES_HEADING)
    after = [i for i in heads if i > all_i]
    all_end = after[0] if after else len(lines)

    curated: set[str] = set()
    out: list[str] = []
    for i, line in enumerate(lines[:all_i]):
        m = re.match(r"^- \[.*?\]\((%s/posts/([^)]+\.html))\)" % re.escape(SITE_URL), line)
        if not m:
            out.append(line)
            continue
        filename = m.group(2)
        post = index.get(filename)
        if post is None:          # points at a file that no longer exists
            continue
        curated.add(filename)
        out.append(llms_entry(post))

    out.append(ALL_ARTICLES_HEADING)
    out.append("")
    for post in posts:
        if post["filename"] in curated:
            continue
        out.append(llms_entry(post))
    out.append("")

    out.extend(lines[all_end:])
    return "\n".join(out).rstrip("\n") + "\n"


# --------------------------------------------------------------------------
# full regeneration of the three index files
# --------------------------------------------------------------------------

def regenerate_indexes(root: str, posts: list[dict] | None = None) -> list[dict]:
    posts = posts if posts is not None else read_posts(root)
    write(os.path.join(root, "sitemap.xml"), build_sitemap(posts))
    feed_path = os.path.join(root, "feed.xml")
    write(feed_path, build_feed(posts, read(feed_path)))
    llms_path = os.path.join(root, "llms.txt")
    write(llms_path, build_llms(posts, read(llms_path)))
    return posts


def prune_unlisted_cards(root: str) -> list[str]:
    """Drop homepage cards whose article is a redirect stub or under review.

    Returns the filenames whose cards were removed. Cards for listable posts
    are left exactly as they are."""
    index_path = os.path.join(root, "index.html")
    text = read(index_path)
    _before, grid_inner, _after = split_grid(text)
    unlisted = set(read_stubs(root)) | read_under_review(root)
    cards = extract_cards(grid_inner)
    keep, dropped = [], []
    for card in cards:
        target = card_target(card)
        if target in unlisted:
            dropped.append(target)
            # park the card so relisting is a one-liner later
            write(os.path.join(root, ".scheduled", "unlisted-cards",
                               target.replace(".html", "") + ".html"), card.strip() + "\n")
        else:
            keep.append(card)
    if dropped:
        write(index_path, set_grid(text, keep, read_posts(root)))
    return dropped


def relist_cards(root: str) -> list[str]:
    """Put parked cards back for articles that are listable again."""
    folder = os.path.join(root, ".scheduled", "unlisted-cards")
    if not os.path.isdir(folder):
        return []
    posts = read_posts(root)
    listable = {p["filename"] for p in posts}
    index_path = os.path.join(root, "index.html")
    text = read(index_path)
    restored = []
    for path in sorted(glob.glob(os.path.join(folder, "*.html"))):
        filename = os.path.basename(path)
        if filename in listable:
            text = insert_card(text, read(path).strip(), posts)
            os.remove(path)
            restored.append(filename)
    if restored:
        write(index_path, text)
    return restored


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Regenerate sitemap.xml, feed.xml, llms.txt from posts/ and "
                    "prune homepage cards of unlisted articles.")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = parser.parse_args()
    restored = relist_cards(args.root)
    dropped = prune_unlisted_cards(args.root)
    posts = regenerate_indexes(args.root)
    print("regenerated sitemap.xml, feed.xml, llms.txt for %d articles" % len(posts))
    for f in restored:
        print("restored homepage card: posts/%s" % f)
    for f in dropped:
        print("removed homepage card: posts/%s (parked in .scheduled/unlisted-cards/)" % f)
