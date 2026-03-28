# Riigikogu Desktop Dashboard — Claude Code Instructions

## Repository Purpose
Interactive dashboard for the XV Riigikogu (101 MPs).
Hosted as a static site on GitHub Pages at https://igorljapin.github.io/riigikogu-desktop/

## File Map
- `index.html` — All MP data is hardcoded here as JavaScript objects. This is
  the primary file requiring edits when composition changes.
- `data/mp_data_current.json` — Committed baseline of MP data used for diff 
  comparison by the monthly workflow.
- `mp-data-scraped.json` — Legacy photo/link lookup used by the popup window.
  Keep in sync with mp_data_current.json after any update.
- `data/mp_data_fetched.json` — Temporary file created by workflow, never 
  committed directly.
- `data/change_report.json` — Output of comparison script; read this first 
  before making any changes.

## Monthly Update Procedure

1. READ `data/change_report.json` completely before touching anything.

2. For PARTY SWITCHES (politically significant — flag these in the PR):
   - Find the MP by name in index.html
   - Update their party/faction field
   - Update seating position if the switch crosses coalition/opposition line
   - Recalculate coalition and opposition seat totals in the header
   - Update mp_data_current.json and mp-data-scraped.json

3. For NEW MEMBERS (typically replacements after resignation):
   - Add MP object to index.html with correct seating position
   - Add entry to mp-data-scraped.json with photoUrl and profileUrl
   - Update mp_data_current.json
   - Note in PR body that seating position requires manual verification

4. For REMOVED MEMBERS:
   - Remove from index.html active roster
   - Remove from mp-data-scraped.json
   - Update mp_data_current.json
   - DO NOT remove from any vote history data

5. For PHOTO CHANGES only:
   - Update photoUrl in mp-data-scraped.json and mp_data_current.json only
   - No changes to index.html needed

6. VALIDATION before committing:
   - Total MP count in index.html must equal 101
   - Coalition + Opposition totals must equal 101
   - All bracket pairs must match

7. CREATE a pull request:
   - Title: "MP Data Update — [Month YYYY]"
   - Flag party switches as requiring human review before merge
   - Target branch: main

## Critical Rules
- Never change UI layout or CSS
- Never modify vote calculator logic
- Never alter the seating grid structure — only data values within it
- Always create a feature branch, never commit directly to main
