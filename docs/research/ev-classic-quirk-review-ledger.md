# EV Classic quirk / bug review ledger

Purpose: hold every discovered EV Classic behavior that might be a quirk, bug, later-EV fix candidate, or intentional Terminal Velocity divergence so mulvray can review the exact classification before it becomes durable game behavior.

This ledger is not an implementation backlog by itself. It is a review surface for fidelity judgment.

## Status vocabulary

- `needs-review`: behavior discovered; classification not yet accepted by mulvray.
- `preserve-quirk`: implement Classic-like behavior intentionally.
- `fix-bug`: do not recreate the Classic defect; implement fixed behavior.
- `adopt-later-ev-fix`: later EV-family behavior clarifies a defect or intended behavior; adopt the fix unless rejected.
- `intentional-divergence`: Terminal Velocity deliberately differs for usability, safety, accessibility, determinism, or design reasons.
- `needs-evidence`: behavior is suspected but evidence is insufficient.

## Required entry format

```md
- [ ] Short behavior title
  - Status: `needs-review`
  - Surface: controls | navigation | economy | missions | combat | UI | persistence | services | data | other
  - Evidence: `original-runtime-observed` | `decoded-original-variable` | `manual-or-bible-guided` | `later-ev-family` | `terminal-velocity-observed`; include file/log/capture/doc paths.
  - Observed Classic behavior: exact derived fact, with no guessing beyond evidence.
  - Later EV-family behavior/fix: if known; otherwise `unknown`.
  - Candidate classification: `quirk` | `bug` | `later-fix` | `divergence` | `unknown`.
  - Why it might be a quirk: player-legible/stable/integrated/fair aspects.
  - Why it might be a bug: inconsistency/destructive/unrecoverable/misleading/later-fixed/platform-artifact aspects.
  - Recommended Terminal Velocity handling: preserve | fix | adopt later fix | defer; include rationale.
  - User decision: `pending` until mulvray reviews.
  - Implementation/backlog link: path or `not linked yet`.
```

## Review rules

1. Any newly discovered Classic behavior that is odd, surprising, exploitable, inconsistent, or later fixed must be added here before it is treated as an intentional Terminal Velocity behavior.
2. The runner may implement safe scaffolding or tests around an entry, but must keep the entry `needs-review` unless the behavior is already clearly non-controversial or mulvray has classified it.
3. Preserve quirks intentionally; do not preserve bugs by default.
4. Later EV-family fixes are evidence of intended design, not automatic authority. Record them for review.
5. Platform/emulator artifacts should usually be `fix-bug` or `intentional-divergence`, not fidelity targets.

## Default handling policy

- Harmful, invisible, crashy, save-corrupting, misleading, implementation-artifact-only, or platform/emulator-specific Classic defects are not default fidelity targets. Prefer clean Terminal Velocity behavior, with the entry classified as `fix-bug` or `intentional-divergence` after review.
- If a suspected Classic defect affects old plug-in/data compatibility, model the compatibility need explicitly. Prefer an optional compatibility path or migration shim over making the defect the main Terminal Velocity behavior, unless Classic runtime/resource evidence and user review classify it as part of the player-visible compatibility contract.
- EV Override/Nova preserving or fixing a Classic behavior increases review confidence but does not by itself prove Classic intent. Record the later-family evidence and keep the Classic claim labeled until original runtime, decoded original resources, or Classic manuals/Bibles support it.

## Pending review

No entries yet. Add new candidate quirks/bugs here as they are discovered.
