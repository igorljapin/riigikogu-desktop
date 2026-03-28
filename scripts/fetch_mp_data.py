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
    # Each MP is in a card/list element — adjust selector if site structure changes
    for card in soup.select(".mp-list-item, .member-item, article"):
        name_tag = card.find("a")
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name:
            continue

        profile_url = urljoin(BASE, name_tag.get("href", ""))
        
        img = card.find("img")
        photo_url = img.get("src", "") if img else ""
        if photo_url and not photo_url.startswith("http"):
            photo_url = urljoin(BASE, photo_url)

        faction_tag = card.find(class_=lambda c: c and "faction" in c.lower()) \
                      or card.find("strong")
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
