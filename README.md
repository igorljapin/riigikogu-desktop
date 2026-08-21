# riigikogu-desktop has moved

This repository is retired. The desktop dashboard for the XV Riigikogu now
lives as a second view layer inside **riigikogu-mobile**, reading the same
live parliamentary data as the mobile app so the two can never disagree
with each other again:

**https://igorljapin.github.io/riigikogu-mobile/desktop/**

Source: https://github.com/igorljapin/riigikogu-mobile
(`desktop/`, `src/views-desktop/`, `desktop.css`, `data/seating.json`)

## Why

This app's own bundle carried stale, pre-2026-08-09 parliamentary
composition data with no way to refresh it short of hand-editing a minified
build — while `riigikogu-mobile` maintained a live, tested data pipeline for
the same 101 MPs. `docs/desktop-2026/DESIGN_AND_MERGE_PLAN.md` in the mobile
repository has the full history of the merge.

`index.html` here is now only a redirect stub, and `service-worker.js` only
exists to clear any previously cached copy of the old app and send installed
PWAs to the new home. `BEHAVIOR_SNAPSHOT.md`, `snapshot/` and
`DESIGN_AND_MERGE_PLAN.md` remain as the historical record of what this app
did before the merge.
