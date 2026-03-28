#!/usr/bin/env python3
"""
Compares current committed MP data against freshly fetched data.
Outputs change report and sets GitHub Actions output variable.
"""

import json
import sys
import os

def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Support both list and dict formats
    if isinstance(data, list):
        return {m["name"]: m for m in data}
    return data  # already a name-keyed dict

current = load("data/mp_data_current.json")
fetched = load("data/mp_data_fetched.json")

report = {
    "new_members": [],
    "removed_members": [],
    "party_switches": [],
    "photo_changes": [],
    "total_current": len(current),
    "total_fetched": len(fetched)
}

for name in set(fetched) - set(current):
    report["new_members"].append(fetched[name])

for name in set(current) - set(fetched):
    report["removed_members"].append(current[name])

for name in set(current) & set(fetched):
    c, f = current[name], fetched[name]
    if c.get("faction") != f.get("faction"):
        report["party_switches"].append({
            "name": name,
            "from": c.get("faction"),
            "to": f.get("faction")
        })
    if c.get("photoUrl") != f.get("photoUrl") and f.get("photoUrl"):
        report["photo_changes"].append(name)

with open("data/change_report.json", "w") as f:
    json.dump(report, f, indent=2)

changes = any(len(v) > 0 for v in report.values() if isinstance(v, list))

# Write to GitHub Actions output
output_file = os.environ.get("GITHUB_OUTPUT", "")
if output_file:
    with open(output_file, "a") as f:
        f.write(f"changes_detected={'true' if changes else 'false'}\n")

print(f"Changes detected: {changes}")
if changes:
    for k, v in report.items():
        if isinstance(v, list) and v:
            print(f"  {k}: {len(v)}")
sys.exit(0)
