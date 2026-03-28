#!/usr/bin/env python3
"""
Fetches current MP data from riigikogu.ee and saves to data/mp_data_fetched.json
Run by GitHub Actions monthly workflow.
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime
from urllib.parse import urljoin

BASE = "https://www.riigikogu.ee"
LIST_URL = f"{BASE}/en/parliament-of-estonia/composition/members-riigikogu/"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; RiigikoguMonitor/1.0)"})

def scrape_mps():
    print("Fetching MP list...")
    resp = session.get(LIST_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    mps = []
    # Each MP is in a li.item element on the riigikogu.ee member list page
    for card in soup.select("li.item"):
        # Name and profile URL from the h3 > a inside div.content
        content = card.select_one("div.content")
        if not content:
            continue
        name_tag = content.select_one("h3 a")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name:
            continue

        profile_url = urljoin(BASE, name_tag.get("href", ""))

        # Photo URL from lazy-loaded img (data-original attribute)
        img = card.select_one("img.lazy")
        photo_url = ""
        if img:
            photo_url = img.get("data-original", "") or img.get("src", "")
        if photo_url and not photo_url.startswith("http"):
            photo_url = urljoin(BASE, photo_url)

        # Faction from the <strong> tag inside content
        faction_tag = content.find("strong")
        faction = faction_tag.get_text(strip=True) if faction_tag else "Unknown"

        mps.append({
            "name": name,
            "photoUrl": photo_url,
            "profileUrl": profile_url,
            "faction": faction,
            "fetched_at": datetime.utcnow().isoformat()
        })

    print(f"Found {len(mps)} MPs")
    return mps

mps = scrape_mps()
if len(mps) < 90:
    print(f"ERROR: Only {len(mps)} MPs found — likely a scraping failure. Aborting.")
    sys.exit(1)

with open("data/mp_data_fetched.json", "w", encoding="utf-8") as f:
    json.dump(mps, f, ensure_ascii=False, indent=2)

print("Saved to data/mp_data_fetched.json")
