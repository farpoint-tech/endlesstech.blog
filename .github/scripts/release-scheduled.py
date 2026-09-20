#!/usr/bin/env python3
"""Publish the articles that are due today, from the scheduled-posts branch.

The release calendar lives in .scheduled/releases.json. Article HTML never
sits on master before its release date; it is fetched from the
``scheduled-posts`` branch on the day, together with any assets it needs
that master does not have yet.

For every entry that is due today *or earlier and not yet on master* (so a
missed run catches up by itself) this script:

  1. checks the article out of origin/<source_branch> into posts/
  2. checks out every assets/... file the article references and that
     master is missing
  3. drops the prepared card from .scheduled/cards/<slug>.html into the
     main listing of index.html at the SERIES-RELEASE-SLOT marker and
     re-sorts the listing newest first
  4. removes the consumed card
  5. regenerates sitemap.xml, feed.xml and llms.txt
  6. runs tools/check-findability.py

Nothing due   -> exit 0, "nothing to release", working tree untouched.
Check fails   -> exit 1, so the calling workflow never commits.

    python3 .github/scripts/release-scheduled.py [YYYY-MM-DD]

The date defaults to today in the calendar's timezone. Standard library
plus the git CLI only.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import site_index as si  # noqa: E402

CALENDAR = os.path.join(ROOT, ".scheduled", "releases.json")
CHECKER = os.path.join(ROOT, "tools", "check-findability.py")
ASSET_REF = re.compile(r'(?:src|href)="\.\./(assets/[^"?#]+)"')
SRCSET_REF = re.compile(r'srcset="([^"]+)"')


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise SystemExit("git %s failed:\n%s" % (" ".join(args), proc.stderr.strip()))
    return proc


def load_calendar() -> dict:
    with open(CALENDAR, encoding="utf-8") as fh:
        return json.load(fh)


def referenced_assets(article_path: str) -> list[str]:
    """assets/... paths the article links to, relative to the repo root."""
    text = si.read(article_path)
    found = set(ASSET_REF.findall(text))
    for srcset in SRCSET_REF.findall(text):
        for candidate in srcset.split(","):
            url = candidate.strip().split(" ")[0]
            if url.startswith("../assets/"):
                found.add(url[3:])
            elif url.startswith("assets/"):
                found.add(url)
    return sorted(found)


def due_entries(calendar: dict, today: str) -> list[dict]:
    out = []
    for entry in calendar["releases"]:
        if entry["date"] > today:
            continue
        if os.path.exists(os.path.join(ROOT, "posts", entry["slug"] + ".html")):
            continue  # already released
        out.append(entry)
    return sorted(out, key=lambda e: (e["date"], e["slug"]))


def release(entry: dict, source_ref: str) -> None:
    slug = entry["slug"]
    article = "posts/%s.html" % slug
    card_path = os.path.join(ROOT, entry["card"])

    if not os.path.exists(card_path):
        raise SystemExit("ERROR: card %s is missing — prepare it before the "
                         "release date" % entry["card"])

    print("releasing %s (due %s)" % (slug, entry["date"]))
    git("checkout", source_ref, "--", article)

    missing = [a for a in referenced_assets(os.path.join(ROOT, article))
               if not os.path.exists(os.path.join(ROOT, a))]
    for asset in missing:
        proc = git("checkout", source_ref, "--", asset, check=False)
        if proc.returncode != 0:
            raise SystemExit("ERROR: %s references %s, which exists neither on "
                             "master nor on %s" % (article, asset, source_ref))
        print("  + asset %s" % asset)

    index_path = os.path.join(ROOT, "index.html")
    card = si.read(card_path).strip()
    target = si.card_target(card)
    if target != os.path.basename(article):
        raise SystemExit("ERROR: %s links to posts/%s, expected %s"
                         % (entry["card"], target, os.path.basename(article)))

    posts = si.read_posts(ROOT)
    si.write(index_path, si.insert_card(si.read(index_path), card, posts))
    os.remove(card_path)
    print("  + card on the homepage")


def main() -> int:
    calendar = load_calendar()
    tz = ZoneInfo(calendar.get("timezone", "Europe/Berlin"))
    today = sys.argv[1] if len(sys.argv) > 1 else datetime.now(tz).strftime("%Y-%m-%d")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", today):
        raise SystemExit("ERROR: date must be YYYY-MM-DD, got %r" % today)

    entries = due_entries(calendar, today)
    if not entries:
        print("nothing to release for %s" % today)
        return 0

    source_branch = calendar.get("source_branch", "scheduled-posts")
    source_ref = "origin/%s" % source_branch
    git("fetch", "origin",
        "+refs/heads/%s:refs/remotes/%s" % (source_branch, source_ref))

    for entry in entries:
        release(entry, source_ref)

    si.regenerate_indexes(ROOT)
    print("regenerated sitemap.xml, feed.xml and llms.txt")

    check = subprocess.run([sys.executable, CHECKER, "--root", ROOT])
    if check.returncode != 0:
        print("ERROR: findability check failed — not committing", file=sys.stderr)
        return 1

    slugs = [e["slug"] for e in entries]
    print("released: %s" % ", ".join(slugs))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as fh:
            fh.write("slugs=%s\n" % " ".join(slugs))
            fh.write("message=release: %s\n" % ", ".join(slugs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
