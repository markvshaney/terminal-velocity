# EV gameplay state-probe and autoresearch expansion gate

Date: 2026-05-28

## Problem

Loki's live EV Classic gameplay is slow because too much play time is spent in per-action screenshot/vision loops and coordinate/input debugging. The current bottleneck is not strategy knowledge alone; it is missing cheap, repeatable game-state feedback.

## Immediate local probe

Created local-only helper:

- `C:\Games\BasiliskII\ev-state-probe.ps1`
- `C:\Games\BasiliskII\ev-trace.ps1`

Purpose:

- capture Basilisk once;
- classify coarse screen state (`map`, `space_or_modal`, `landed_or_dialog`);
- infer current map system from known local early-region map coordinates;
- estimate shield/fuel bar ratios from HUD pixels;
- detect known-system route-line candidates on the map;
- distinguish landed/dialog screens from maps when large planet art overlaps the map coordinate region;
- emit compact JSON so routine play can checkpoint without full vision review.
- append before/action/after JSONL traces for batched actions via `ev-trace.ps1`.

Verification command:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Games\BasiliskII\ev-state-probe.ps1'
```

Observed verification result after opening the map:

```json
{
  "screen": "map",
  "currentSystemGuess": "Kathoon",
  "routeLineDetected": false,
  "systemGreenScores": {"Kathoon": 34},
  "shieldBarRatio": 0.592,
  "fuelBarRatio": 0.148
}
```

Additional smoke checks performed:

- Known landed screenshot `C:\Games\BasiliskII\ev-continue-landed-tabletop-20260521.png` now classifies as `landed_or_dialog` instead of `map`.
- `ev-trace.ps1 -Label 'noop-probe-smoke-after-detector-fix' -Actions 'release'` appended a before/action/after JSONL trace to `C:\Games\BasiliskII\ev-action-traces.jsonl`.

Limits:

- This is **not** a RAM probe. It is a fast screenshot/state probe.
- `currentSystemGuess` is local-coordinate based and only reliable for known early-region map positions.
- `routeLineDetected` is a pixel detector for known-system map routes; no-route negative detection and landed-vs-map disambiguation are smoke-tested, but route-positive cases still need visual/live calibration before navigation depends on them.
- It does not OCR mission text, credits, destination text, or modal messages.
- Trace entries include full compact probe JSON and may contain failed/smoke attempts; treat the JSONL as an engineering trace, not a cleaned gameplay fact log.

## Operating change

Use the state probe for routine checkpoints before falling back to vision. Vision should be reserved for:

- unknown modal/dialog text;
- mission computer/bar text;
- route-line confirmation when the probe is ambiguous;
- death/damage/landing/jump anomalies;
- new systems outside the coordinate table.

## Autoresearch expansion decision

Do **not** expand into broad autonomous gameplay yet. First expand the local state/action interface until the loop has cheap measurements.

Recommended staged expansion:

1. **State probe hardening** — add known system coordinates as discovered; add route-line and landed-screen detectors; optionally add OCR/template recognition later.
2. **Action-labeled traces** — log batches from `ev-fast.ps1` plus probe output before/after each batch.
3. **Bounded gameplay evals** — score route/jump/land/refuel/mission attempts using the existing 10-point gameplay-autoresearch rubric.
4. **Facet expansion** after state feedback is reliable:
   - navigation and route planning;
   - landing/refuel/service availability;
   - mission acceptance/completion;
   - commodity trading;
   - combat/escape only on disposable non-strict pilots.

Approval gates remain unchanged: no unattended long-running gameplay, no recurring cron/background job, no Strict Play, no destructive/combat-risk tests on the reusable pilot, and no external publication without approval.
