#!/usr/bin/env python3
"""Move a staged post card onto the homepage.

Cards live in .scheduled/<YYYY-MM-DD>.html and are dropped into index.html at
the SERIES-RELEASE-SLOT marker on their release day, newest first. Exits 0 with
no changes when there is nothing scheduled for the day, so a quiet run is not a
failed run.
"""
import pathlib
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[2]
MARKER = "<!-- SERIES-RELEASE-SLOT -->"
TZ = ZoneInfo("Europe/Berlin")

day = sys.argv[1] if len(sys.argv) > 1 else datetime.now(TZ).strftime("%Y-%m-%d")
card_path = ROOT / ".scheduled" / f"{day}.html"

if not card_path.exists():
    print(f"nothing scheduled for {day}")
    sys.exit(0)

index_path = ROOT / "index.html"
html = index_path.read_text(encoding="utf-8")

if MARKER not in html:
    print(f"ERROR: {MARKER} missing from index.html", file=sys.stderr)
    sys.exit(1)

card = card_path.read_text(encoding="utf-8").rstrip("\n")
if card.strip() in html:
    print(f"card for {day} already on the homepage, nothing to do")
    card_path.unlink()
    sys.exit(0)

html = html.replace(MARKER, f"{MARKER}\n{card}\n", 1)
index_path.write_text(html, encoding="utf-8")
card_path.unlink()
print(f"published {day}")
