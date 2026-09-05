#!/usr/bin/env python3
"""Findability check for endlesstech.blog.

Verifies that every article in posts/ is reachable:

  * exactly once as a card in the main listing of index.html
  * exactly once in sitemap.xml, feed.xml and llms.txt
  * every posts/... reference in those four files points at a real file
  * index.html no longer advertises "Coming Soon"
  * sitemap.xml and feed.xml are well-formed XML

Exit code 0 when everything is green, 1 with a readable list of problems.

    python3 tools/check-findability.py [--root .] [--strict]

--strict additionally rejects inline style="" attributes in posts/.

Standard library only.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_index  # noqa: E402

POST_REF = re.compile(r"posts/([A-Za-z0-9._-]+\.html)")


def _collect(text: str) -> list[str]:
    return POST_REF.findall(text)


def check(root: str, strict: bool = False) -> list[str]:
    errors: list[str] = []

    posts = sorted(os.path.basename(p)
                   for p in glob.glob(os.path.join(root, site_index.POSTS_DIR, "*.html")))
    if not posts:
        return ["posts/: no article found"]
    known = set(posts)

    # ---------------------------------------------------------------- index
    index_path = os.path.join(root, "index.html")
    index_text = site_index.read(index_path)

    if site_index.RELEASE_MARKER not in index_text:
        errors.append("index.html: release marker %s is missing"
                      % site_index.RELEASE_MARKER)

    if "Coming Soon" in index_text:
        errors.append('index.html: still contains "Coming Soon" placeholders')

    try:
        _before, grid_inner, _after = site_index.split_grid(index_text)
    except ValueError:
        errors.append("index.html: main listing (.posts-grid) not found")
        grid_inner = ""

    listing: dict[str, int] = {}
    for card in site_index.extract_cards(grid_inner):
        target = site_index.card_target(card)
        if target is None:
            title = site_index._search(r"<h3[^>]*>(.*?)</h3>", card) or "?"
            errors.append("index.html: card without a posts/ link (%s)"
                          % site_index.plain(title)[:60])
            continue
        listing[target] = listing.get(target, 0) + 1

    for filename in posts:
        count = listing.get(filename, 0)
        if count == 0:
            errors.append("index.html: no card in the main listing for %s" % filename)
        elif count > 1:
            errors.append("index.html: %d cards in the main listing for %s"
                          % (count, filename))
    for filename in sorted(set(listing) - known):
        errors.append("index.html: card links to missing file posts/%s" % filename)

    # every posts/... reference anywhere in index.html (cards, hero, cornerstone
    # cards, JSON-LD) has to resolve to a real file
    for filename in sorted(set(_collect(index_text)) - known):
        errors.append("index.html: reference to missing file posts/%s" % filename)

    # ------------------------------------------------------- the three feeds
    files = {
        "sitemap.xml": os.path.join(root, "sitemap.xml"),
        "feed.xml": os.path.join(root, "feed.xml"),
        "llms.txt": os.path.join(root, "llms.txt"),
    }
    contents: dict[str, str] = {}
    for name, path in files.items():
        if not os.path.exists(path):
            errors.append("%s: file is missing" % name)
            continue
        contents[name] = site_index.read(path)

    for name in ("sitemap.xml", "feed.xml", "llms.txt"):
        text = contents.get(name)
        if text is None:
            continue
        seen: dict[str, int] = {}
        for filename in _collect(text):
            seen[filename] = seen.get(filename, 0) + 1
        # sitemap/feed repeat the URL in <loc>/<guid>; count unique entries
        if name == "sitemap.xml":
            seen = _count_xml(text, ".//{*}loc", errors, name)
        elif name == "feed.xml":
            seen = _count_xml(text, ".//{*}item/{*}link", errors, name)
        for filename in posts:
            count = seen.get(filename, 0)
            if count == 0:
                errors.append("%s: %s is missing" % (name, filename))
            elif count > 1:
                errors.append("%s: %s listed %d times" % (name, filename, count))
        for filename in sorted(set(seen) - known):
            errors.append("%s: reference to missing file posts/%s" % (name, filename))
        for filename in sorted(set(_collect(text)) - known):
            errors.append("%s: reference to missing file posts/%s" % (name, filename))

    # ------------------------------------------------------------- XML sanity
    for name in ("sitemap.xml", "feed.xml"):
        text = contents.get(name)
        if text is None:
            continue
        try:
            ET.fromstring(text)
        except ET.ParseError as exc:
            errors.append("%s: not well-formed XML (%s)" % (name, exc))

    # ------------------------------------------------------------- --strict
    if strict:
        for path in sorted(glob.glob(os.path.join(root, site_index.POSTS_DIR, "*.html"))):
            body = site_index.read(path)
            hits = re.findall(r"<[^>]+\sstyle\s*=\s*\"[^\"]*\"", body)
            if hits:
                errors.append("posts/%s: %d inline style=\"\" attribute(s)"
                              % (os.path.basename(path), len(hits)))

    return sorted(set(errors))


def _count_xml(text: str, path: str, errors: list[str], name: str) -> dict[str, int]:
    """Count posts/<file>.html occurrences in one XML element type."""
    counts: dict[str, int] = {}
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return counts  # reported separately
    for node in root.findall(path):
        for filename in _collect(node.text or ""):
            counts[filename] = counts.get(filename, 0) + 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repository root (default: the repo this script lives in)")
    parser.add_argument("--strict", action="store_true",
                        help="also reject inline style=\"\" attributes in posts/")
    args = parser.parse_args()

    errors = check(args.root, args.strict)
    if errors:
        print("check-findability: %d problem(s)\n" % len(errors))
        for line in errors:
            print("  - %s" % line)
        return 1

    count = len(glob.glob(os.path.join(args.root, site_index.POSTS_DIR, "*.html")))
    print("check-findability: OK — %d articles listed in index.html, "
          "sitemap.xml, feed.xml and llms.txt" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
