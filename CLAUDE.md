# Riigikogu Desktop Dashboard — retired

This repository is retired behind a redirect. The app it describes no longer
runs here — do not follow the procedures below, and do not restore
`index.html`, `manifest.json`, `data/`, `scripts/`, or the monthly workflow;
they were deleted on purpose when this repo became a redirect stub (see
`README.md`).

The desktop dashboard lives on as a view layer inside **riigikogu-mobile**:

- Live app: https://igorljapin.github.io/riigikogu-mobile/desktop/
- Source: https://github.com/igorljapin/riigikogu-mobile
  (`desktop/`, `src/views-desktop/`, `desktop.css`, `data/seating.json`)
- Its own `CLAUDE.md` governs all future work on the merged app.

If you were sent here to update MP data, seating, or party affiliations, go
to `riigikogu-mobile` instead — this repo's data pipeline no longer exists.

`index.html` is a redirect stub (meta-refresh + `location.replace` to the
URL above) and `service-worker.js` is self-destructing: it clears every
cache it can find, unregisters itself, and navigates any open window
(including an already-installed PWA) to the new home. Both exist only to
stop this repo from serving its old, stale bundle to anyone who already has
it cached or installed — do not "fix" them into a working app again.

`BEHAVIOR_SNAPSHOT.md`, `snapshot/`, and `DESIGN_AND_MERGE_PLAN.md` are the
historical record of what this app did before the merge; they are kept for
reference and should not be treated as current documentation.
