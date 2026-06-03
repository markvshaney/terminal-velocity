# EV Classic observation-to-implementation workflow

Date: 2026-05-19

Purpose: keep original EV Classic runtime observations from turning into either untracked chat notes or unreviewed implementation drift. Raw captures remain local-only; this artifact records the decision workflow. The live execution surface is `docs/checklists/ev-classic-fidelity-implementation-backlog.md`.

## Decision

Use both surfaces:

- `docs/research/original-ev-classic-runtime-observations.md` records derived original-system observations, evidence labels, capture paths, caveats, and provenance for future Terminal Velocity implementation.
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md` tracks recommendations, candidate implementations, status, next action, and verification.

Observation alone is not implementation authority. Each observation gets classified before code/data changes.

Original-system observations should not remain only in chat or ephemeral screenshots. If an observation may shape future Terminal Velocity behavior, data, UI, economy, services, missions, combat, hazards, progression, or fidelity tests, store the derived observation in the research log first, then classify it for immediate implementation, backlog tracking, or observation-only retention.

Use observation seeds as the bridge between play and implementation. A seed is a compact, evidence-labeled record of a played/observed behavior plus the likely Terminal Velocity surface it may affect. Seeds let gameplay observations accumulate safely until they are ready to be incorporated into Terminal Velocity data, code, tests, or backlog items. A seed may be incomplete, but it must preserve the evidence boundary and name what remains missing before implementation.

Player skill sets learned while operating original EV are also implementation inputs. Record reusable skills such as mission-running judgment, trade-route selection, mission+trade pairing, fuel/risk management, combat avoidance/engagement, ship modification, outfitting, and system-provisioning judgment as part of the seed when they are learned from play. These learned skills can later inform Terminal Velocity tutorials, hints, progression design, balance, AI/player guidance, and regression scenarios. Learned skills may be reused by other pilots/test profiles; preserve that transferability explicitly while keeping pilot-specific state, cargo, reputation, deadlines, equipment, and save-risk constraints separate.

When a play session involves missions or travel risk, include a play report. The report should explain how the mission was completed or why it failed, which route was chosen, what constraints mattered, whether pirates/hostiles/asteroids appeared, how threats were avoided or handled, and what reusable lessons should transfer to future pilots and Terminal Velocity design.

## Classification rules

### Incorporate immediately

Use for small, low-risk, source-backed corrections where the target surface is obvious and bounded.

Examples:

- starting credits
- visible button labels
- commodity names/prices for a specific observed port
- start location/state corrections
- UI wording directly visible in original runtime

Required slice evidence before the run can close (close out only when a real gate, cap, unsafe dirty state, or no-safe-local-slice condition has been reached):

1. Update data/code/docs/tests in a small patch.
2. Add or update a test when practical.
3. Run Python tests and Godot selftest/check-only.
4. Mark the backlog item `implemented` or `verified`.

### Record as candidate

Use when the observation suggests an implementation but needs more evidence, a design choice, or broader scope control.

Examples:

- physics tuning
- combat behavior
- economy-wide rules inferred from one port
- galaxy topology beyond decoded evidence
- save/load or resource-format changes

Required candidate record before the run can close (close out only when a real gate, cap, unsafe dirty state, or no-safe-local-slice condition has been reached):

1. Record the observation in the research artifact.
2. Add a backlog item with `status: candidate` or `status: needs evidence`.
3. Name the next evidence/action needed.
4. Do not silently implement broad behavior.

### Keep observation-only

Use when the observation is useful context but not currently actionable.

Examples:

- one-off UI state with no planned Terminal Velocity surface
- ambiguous visual read
- proprietary/raw evidence that should not be integrated directly

Required observation-only record before the run can close (close out only when a real gate, cap, unsafe dirty state, or no-safe-local-slice condition has been reached):

1. Record derived fact and caveat.
2. Mark backlog only if it implies future work.

## Evidence labels

Use existing evidence labels consistently:

- `original-runtime-observed`: observed in EV Classic running locally through Basilisk II.
- `decoded-resource-backed`: derived from decoded EV Classic resources/manifests.
- `terminal-velocity-observed`: observed in the Terminal Velocity implementation.
- `external-adaptation-observed`: observed in a community engine/adaptation; hypothesis only unless confirmed by primary evidence.
- `unknown`: not yet source-backed.

## Status vocabulary for the backlog

- `candidate`: plausible implementation, not yet ready.
- `needs evidence`: blocked on runtime/resource observation.
- `ready`: sufficiently source-backed and bounded; safe to implement.
- `implemented`: code/data/docs changed; verification may still be pending.
- `verified`: implementation and tests/selftests passed.
- `deferred`: intentionally not doing now; reason recorded.
- `blocked`: cannot proceed until named blocker clears.

## Guardrails

- Do not use external adaptations as source of truth.
- Do not put raw proprietary captures or assets in the repo without explicit review/approval.
- Do not infer global rules from one runtime observation unless the artifact says it is an inference and the backlog keeps it as a candidate.
- For repository changes, report files modified and verification run.
- If a recommendation list has multiple future actions, update the backlog in the same turn instead of leaving it only in chat.

## Execution cadence preference

The preferred Terminal Velocity workflow is proactive and implementation-forward, not timid or ritual-heavy. Safe local changes should move fast enough that playable progress does not take eternity.

Checklist for safe local implementation slices:

1. Batch related changes into one coherent player-visible slice instead of splitting adjacent polish into many micro-slices.
2. Prefer direct implementation once scope is bounded; do not over-plan or repeatedly ask when the next safe action is clear.
3. Use targeted tests while developing, then run full native/Godot verification once at the commit boundary.
4. Use proportional verification: heavier tests for persistence, data migration, source/fidelity claims, or cross-system behavior; lighter tests for local text/layout polish.
5. Update docs/checklists when the player-visible surface, verifier, source/fidelity boundary, or future decision changes; avoid doc churn for every tiny implementation detail.
6. Preserve real gates for real risk: Strict Play, destructive original-EV tests, credentials/account/provider/gateway changes, external messages, publishing, pushes, or other irreversible/socially consequential actions.
7. If the user explicitly approves inferred Terminal Velocity scaffolds, continue implementing bounded local scaffolds with clear `inferred`/`Classic unconfirmed` labels instead of stopping at a source-evidence gate; stop only before claiming EV Classic fidelity or taking a real side-effect gate.
8. If repeated input/tooling produces no state change, treat it as a tooling/input failure and change strategy instead of continuing cautiously.
9. Process failure recorded 2026-05-29: do not end source/fidelity turns with baby-step recommendations when the obvious safe local follow-through is to mine saved references, promote supported claims, implement the adjacent resource-backed slice, and run proportional verification. Batch that work before reporting; only stop for real gates.
10. Process bug recorded 2026-05-29: "proactive by default" was present in memory/SOUL-style instructions but not enforced as a task-level invariant, so after context pressure the agent reverted to conservative tomorrow-baseline recommendations and one-off apologies. Future corrections of this class must be logged in this artifact/backlog, not only chat, and the current safe local slice must continue to verification in the same turn.
11. Bug/meeting logging expectation: when user explicitly identifies recurring workflow defects or meeting-like decision moments, update the project decision/backlog surface immediately before or while continuing the implementation work; do not claim the issue is tracked unless this file or the live backlog was actually patched.
12. Approval asks are friction too. Do not ask approval for routine safe local work: source mining, generated manifests, tests, docs/backlog edits, scaffolds, reversible hygiene, or player-visible local slices. Gate only real risk: Strict Play, destructive original-EV tests, credentials/account/provider/gateway changes, external messages, publishing, pushes, live-browser mutations, or other irreversible/socially consequential actions.
13. Process bug recorded 2026-05-29: acknowledging a workflow bug, patching memory/docs, and stopping is still defective if safe local implementation work remains. Durable correction must be paired with actual repo progress and verification in the same turn whenever tools can do it.
14. Process bug recorded 2026-05-30: completing one verified/committed slice is a checkpoint, not a stopping condition. If another safe local slice remains, continue selecting from the backlog in the same autonomous run. Do not treat an unpushed local commit as a blocker; push/publication is gated, but safe local work can continue on top of the unpushed branch.
15. Recurrence analysis recorded 2026-05-30: if the agent stops after one verified safe slice, classify the origin as a mechanism-application failure, not a missing preference. Known contributing triggers are: failing to load all skills named by the continuation prompt; treating source-aligned "slice done" criteria, observation-workflow "required closeout" language, or generic inspected/changed/verified reporting habits as higher priority than the autonomous continuation rule; and failing to run a post-slice gate check (`is there a real gate, tool/time cap, dirty-worktree safety issue, or truly no safe local backlog slice?`). Required prevention: after every verified slice in this mode, inspect repo/backlog state and either start the next safe local slice or name the concrete gate/cap/no-safe-alternative evidence.
16. Remediation checklist recorded 2026-05-30: the 6:19 p.m. and 6:23 p.m. process-failure posts describe a combined failure class: stored-artifact lookup was skipped, required skills were not fully loaded, memory substituted for the exact artifact, and the completed-slice closeout reflex overrode continuation. Track step-by-step remediation in `docs/checklists/agent-continuation-process-failure-remediation.md` before resuming ordinary TV implementation work.
17. Tool-cap handoff rule recorded 2026-05-30: a hard tool-call cap is a legitimate stop only when the handoff names the dirty state, unfinished verification, exact resume commands, and whether commit/push remains gated. The next continuation run must resume by finishing verification/backlog cleanup/commit for the in-progress slice before selecting new work.

This preference does not remove evidence boundaries: original EV Classic remains truth for fidelity claims, while Terminal Velocity scaffolds must stay labeled as scaffolds until source-backed.
