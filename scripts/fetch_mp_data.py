#!/usr/bin/env python3
"""
Fetches current MP data from the Riigikogu open-data API
and saves to data/mp_data_fetched.json.
Run by GitHub Actions monthly workflow.
"""

import requests
import json
import sys
from datetime import datetime

API_URL = "https://api.riigikogu.ee/api/plenary-members?lang=en"
PROFILE_BASE = "https://www.riigikogu.ee/en/parliament-of-estonia/composition/members-riigikogu/saadik"

session = requests.Session()
session.headers.update({"User-Agent": "RiigikoguMonitor/1.0"})


def fetch_mps():
    print("Fetching MP list from API...")
    resp = session.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    mps = []
    for member in data:
        uuid = member.get("uuid", "")
        full_name = member.get("fullName", "")
        if not full_name:
            continue

        # Photo download URL
        photo = member.get("photo")
        photo_url = ""
        if photo:
            photo_url = photo.get("_links", {}).get("download", {}).get("href", "")

        # Profile URL on riigikogu.ee website
        name_slug = full_name.replace(" ", "-")
        profile_url = f"{PROFILE_BASE}/{uuid}/{name_slug}"

        # Current faction (first active one)
        factions = member.get("factions", [])
        faction = "Unknown"
        for f in factions:
            if f.get("active"):
                faction = f.get("name", "Unknown")
                break

        mps.append({
            "name": full_name,
            "photoUrl": photo_url,
            "profileUrl": profile_url,
            "faction": faction,
            "fetched_at": datetime.utcnow().isoformat()
        })

    print(f"Found {len(mps)} MPs")
    return mps


mps = fetch_mps()
if len(mps) < 90:
    print(f"ERROR: Only {len(mps)} MPs found — likely an API failure. Aborting.")
    sys.exit(1)

with open("data/mp_data_fetched.json", "w", encoding="utf-8") as f:
    json.dump(mps, f, ensure_ascii=False, indent=2)

print(f"Saved to data/mp_data_fetched.json")
print(f"\nSample (first 3 entries):")
for entry in mps[:3]:
    print(f"  {entry['name']} | {entry['faction']}")
    print(f"    photo: {entry['photoUrl'][:80]}...")
    print(f"    profile: {entry['profileUrl'][:80]}...")
