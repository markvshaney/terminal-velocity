# Terminal Velocity continuation prompt

Purpose: reusable prompt to restart Loki Game work on Terminal Velocity from the current source-backed state, using Basilisk II and gathered EV sources without losing source/fidelity discipline.

```text
Resume Terminal Velocity development in the Loki Game profile.

Project: /home/bh/workspaces/loki/terminal-velocity
Goal: drive Terminal Velocity toward a playable, source-aligned Escape Velocity Classic reimplementation, using the gathered EV Classic/Basilisk observations, decoded resources, manuals/Bibles, and existing docs/checklists as the working source base.

First load and follow these skills:
- source-and-fidelity
- ev-classic-basilisk-observation
- ev-terminal-velocity-play
- game-prototyping if building a gameplay slice
- systematic-debugging if blocked by tool/runtime failures

Stored-artifact regression checklist before implementation:
- exact artifact read with line numbers?
- every skill named by the artifact loaded?
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

4. Do not stop at recommendations or at a completed slice. Pick the strongest safe local next slice from the live backlog and repo state, implement it, verify it, update docs/checklists, then continue to the next safe slice until a real gate is reached **and no other safe local slice remains available**. A push/PR/publication gate on the just-finished commit is not a blocker to starting the next local slice; keep the unpushed commit local and continue from the backlog unless the worktree state itself prevents safe continuation.

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
   - use existing wrapper probes such as tv-map-route-log, tv-route-jump-log, tv-low-fuel-jump-log, tv-mission-route-hint-log, tv-combat-log, tv-legal-status-log, etc.
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
   Ask only for real gates: external actions, destructive original-EV tests, Strict Play/death tests, publication, credentials/accounts, live repo pushes/PRs, or risky host/system changes.

Current durable context to respect:
- The backlog is the live execution surface: docs/checklists/ev-classic-fidelity-implementation-backlog.md
- The source-aligned method is documented in docs/research/source-aligned-game-development-method.md
- Original runtime observations live in docs/research/original-ev-classic-runtime-observations.md
- Existing high-value pending areas include original-runtime comparison for movement/facing, hyperspace/land/takeoff timing, landed service matrices, combat fidelity, legal/reputation/runtime UI confirmation, economy spread/edge cases, topology/service provisioning, and continuing source-mined gameplay scaffolds.
- If the repo has uncommitted work, finish/cohere/verify that current slice before choosing a fresh one.

Post-slice gate template before using the closeout block:
- real gate? (Strict Play/destructive original-EV test/credentials/account/provider/gateway/external publication/push/PR/live-browser mutation/irreversible or social side effect)
- hard tool/time/budget cap?
- unsafe dirty worktree that must be stabilized first?
- no safe backlog/docs slice remains after inspection?
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
