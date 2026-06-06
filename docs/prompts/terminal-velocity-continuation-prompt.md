# Terminal Velocity continuation prompt

Purpose: reusable prompt to restart Loki Game work on Terminal Velocity from the current source-backed state, using Basilisk II and gathered EV sources without losing source/fidelity discipline.

```text
Resume Terminal Velocity development in the Loki Game profile.

Project: /home/bh/workspaces/loki/terminal-velocity
Goal: drive Terminal Velocity toward a playable, source-aligned Escape Velocity Classic reimplementation, using the gathered EV Classic/Basilisk observations, decoded resources, manuals/Bibles, and existing docs/checklists as the working source base.

First load and follow these skills when available in the active profile (do not fail startup solely because a profile lacks one; fall back to repo docs/checklists and source/fidelity rules):
- source-and-fidelity
- ev-classic-basilisk-observation
- ev-terminal-velocity-play
- game-prototyping if building a gameplay slice
- systematic-debugging if blocked by tool/runtime failures

Mandatory long-task ledger preflight before implementation:
- read `.hermes/long-running/terminal-velocity/task-ledger.json` with line numbers;
- read the latest tail of `.hermes/long-running/terminal-velocity/events.jsonl`;
- apply `mandatory_resume_first_actions`, `stopping_state_contract`, `source_artifact_policy`, and `do_not_redo` from the ledger;
- verify live Kanban/cron-watchdog state only when the task involves runner ownership, cadence, dispatch, or silent-stop concerns; Kanban owns implementation work and script-only cron may only watch/dispatch.

Stored-artifact regression checklist before implementation:
- exact artifact read with line numbers?
- project-local long-task ledger and latest event tail read?
- every skill named by the artifact/ledger loaded?
- repo state inspected after artifact rules are active?
- live backlog/docs inspected for the current slice?
- post-slice gate check ready to run before any final report?

Hard requirements:
1. Inspect live repo state first:
   - git status --short
   - relevant docs/checklists/research files
   - current tests/probes/wrappers
   Do not overwrite or casually rebase existing uncommitted work. If the worktree is dirty, understand the current slice before starting a new one.

2. Use Terminal Velocity’s established source hierarchy:
   - EV Classic original runtime in Basilisk II = strongest behavior oracle.
   - Decoded EV Classic resources = strongest data/field oracle.
   - EV Classic manuals/Bibles/docs = strong semantics support.
   - EV Override/Nova/community/adaptations = hypothesis or transferable design only, not Classic truth.
   - Terminal Velocity/Godot logs = implementation/eval evidence only, not Classic truth.

3. Work in source-aligned vertical slices. Each completed slice must have:
   - one player-visible or symbolic gameplay behavior,
   - one named scenario/evaluator or deterministic probe,
   - one cheap verification command,
   - explicit source/fidelity labels,
   - docs/backlog update when future behavior is affected.

4. Do not stop at recommendations or at a completed slice. Pick the strongest safe local next slice from the live backlog and repo state, implement it, verify it, update docs/checklists, then continue to the next safe slice until a real gate is reached **and no other safe local slice remains available**. A normal coherent non-force push to `markvshaney/terminal-velocity` is preapproved after status/remotes/branch inspection, intended-only staging, relevant verification, a no-secrets/proprietary/unrelated-file check, push, fetch, and `HEAD == origin/main` verification; report the concise bundle summary after remote verification. Bundle pushes at natural boundaries: one or a few related gameplay/help/docs/ledger commits, or a tool-cap/handoff checkpoint that genuinely needs a remote anchor. Do **not** default to a separate remote push for every tiny feature commit and every follow-up process/finalization commit; if a ledger/process checkpoint is only bookkeeping, include it in the same coherent push as the slice or carry it to the next meaningful bundle when safe. Commit count alone is not a stop condition. If a train is noisy, misleading, unsafe, or entangled, audit and consolidate locally before publication; gate only history rewrite/force-push, deletion, merge/release/settings/public-state changes beyond normal push, credentials/accounts, non-TV repos, destructive/social actions, missing source evidence needed for a fidelity claim, or unsafe dirty state that cannot be separated.

5. Use Basilisk II only for bounded original-runtime questions:
   - local root: C:\Games\BasiliskII\
   - WSL path: /mnt/c/Games/BasiliskII/
   - repo: /home/bh/workspaces/loki/terminal-velocity/
   - observation log: docs/research/original-ev-classic-runtime-observations.md
   - implementation backlog: docs/checklists/ev-classic-fidelity-implementation-backlog.md
   - original-runtime checklist: docs/checklists/ev-classic-original-runtime-observation-checklist.md
   - behavior baseline checklist: docs/checklists/ev-classic-behavior-baseline-checklist.md

6. For Basilisk:
   - keep Strict Play off reusable pilots;
   - do not run destructive death/permadeath tests without explicit approval;
   - keep raw screenshots/assets local-only unless explicitly approved;
   - record derived observations in repo docs with evidence labels and local-only capture paths;
   - if controls/focus freeze or input wedges, diagnose foreground/session/input state before inferring game behavior.

7. Prefer the fast Terminal Velocity lane for implementation/eval:
   - Python tests: python3 -m unittest discover -s native_ev/tests -p 'test_*.py'
   - scenario harness: python3 tools/run_gameplay_scenarios.py --all --pretty
   - Godot wrapper: ./run_godot.sh self-test
   - use existing wrapper probes such as tv-map-route-log, tv-route-jump-log, tv-low-fuel-jump-log, tv-mission-route-hint-log, tv-service-provisioning-log, tv-combat-log, tv-legal-status-log, etc.
   - when adding a new Godot probe, expose it through run_godot.sh and godot_ev/windows/RunGodot.ps1.

8. Keep fidelity labels explicit:
   - original-runtime-observed
   - decoded-resource-backed
   - manual/docs-backed
   - source-grounded EV-family
   - terminal-velocity-observed
   - Terminal Velocity helper/scaffold
   - needs original confirmation

9. Do not fabricate Classic claims. If a behavior is useful but not source-confirmed, implement it only as a clearly labeled Terminal Velocity scaffold with oracleStatus/sourceLabel fields and backlog follow-up.

10. Continue aggressively through safe local work:
   - inspect,
   - write the smallest useful failing/contract test when practical,
   - implement,
   - run targeted verification,
   - run broader cheap verification,
   - update docs/checklists,
   - repeat.
   Ask only for real gates: history rewrite/force-push, deletion, merge/release/settings/public-state changes beyond a normal coherent push, credentials/accounts, non-Terminal-Velocity repos, destructive original-EV tests, Strict Play/death tests, publication/social side effects, risky host/system changes, unsafe dirty state that cannot be separated, or missing source evidence needed for a fidelity claim. Normal non-force pushes to `markvshaney/terminal-velocity` are preapproved after git/remotes/branch/status inspection, intended-file staging, verification, no-secrets/unrelated-file check, push, fetch, and remote HEAD verification. Reasonable bundling is part of the push policy: avoid push spam from one-commit micro-slices or separate finalizer-only pushes unless a checkpoint/handoff/tool-cap risk makes the remote anchor valuable.

11. Treat tool caps as per-run budgets, not task completion or task failure. Batch file inspection, edits, and verification where safe; prefer one compound terminal verification command over many separate probe calls; avoid rereading large unchanged files; and reserve the final few tool calls before cap for docs/backlog completion, git status/diff inspection, and a commit-shaped checkpoint. If the cap is approaching while a slice is only target-verified, stop starting new behavior and stabilize the current slice first. For work that may outlive the current turn or cap, use the durable long-task/checkpoint surface when available: record tool caps, current state, remaining verification, next wakeup/resume action, and continue in a fresh run instead of sending a vague out-of-budget status.

Current durable context to respect:
- The backlog is the live execution surface: docs/checklists/ev-classic-fidelity-implementation-backlog.md
- The source-aligned method is documented in docs/research/source-aligned-game-development-method.md
- Original runtime observations live in docs/research/original-ev-classic-runtime-observations.md
- Existing high-value pending areas include original-runtime comparison for movement/facing, hyperspace/land/takeoff timing, landed service matrices, combat fidelity, legal/reputation/runtime UI confirmation, economy spread/edge cases, topology/service provisioning, and continuing source-mined gameplay scaffolds.
- If the repo has uncommitted work, finish/cohere/verify that current slice before choosing a fresh one.

Post-slice gate template before using the closeout block:
- real gate? (Strict Play/destructive original-EV test/history rewrite/force-push/deletion/merge/release/settings/public-state change beyond normal push/credentials/account/provider/gateway/non-TV repo/live-browser mutation/irreversible or social side effect, missing source evidence needed for a fidelity claim, or unsafe dirty state that cannot be separated)
- hard tool/time/budget cap?
- unsafe dirty worktree that must be stabilized first?
- no safe backlog/docs slice remains after inspection?
- push/PR/publication gate on the just-finished commit is not a blocker if another safe local slice can proceed without crossing that gate; checkpoint it, leave publication gated, and continue safe local work.
If all answers are no, do not close out; start the next safe local slice.

Closeout format only when the autonomous run is genuinely ending because a real gate/tool cap/time cap/no-safe-alternative has been reached. Do **not** emit this closeout after every completed slice if another safe local slice is available; treat the completed slice as a checkpoint and keep working. A local branch being ahead/push-gated is not itself a reason to stop local work.
- inspected:
- changed:
- verified:
- source/fidelity labels:
- remaining gate/blocker, if any:
- next safe local action:
```

Recommended one-line mode prefix when the worktree is dirty:

```text
Mode for this run: continue from the dirty worktree and finish the current partially implemented slice before starting anything new.
```
