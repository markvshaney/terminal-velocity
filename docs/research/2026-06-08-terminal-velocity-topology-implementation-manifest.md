# Terminal Velocity topology implementation manifest

Date: 2026-06-08T01:06:08-04:00
Status: safe-local topology implemented for the next acceleration burst; no workers, cron jobs, emulator sessions, or external mutations were launched by this manifest.

Purpose: turn `docs/research/terminal-velocity-coordination-topology.md` from process doctrine into an executable, current-state coordination packet. This is process evidence only. It does not justify EV Classic gameplay/fidelity claims.

## 1. Live-state preflight

Observed before writing this manifest:

- Branch/status: `main`, clean, `## main...origin/main`.
- Worktrees: one active checkout at `/home/bh/workspaces/loki/terminal-velocity`, `HEAD 13ebd77961dc52434bdeb13e24dc3b41b9220d00`, branch `refs/heads/main`.
- Active Terminal Velocity workers/processes: none found beyond the live `loki-game` Hermes gateway and other unrelated Hermes profile gateways.
- Kanban/cron/watchdog state: three Terminal Velocity jobs exist and are paused:
  - `72e736287129` Terminal Velocity Kanban watchdog/coordinator (quiet local), paused.
  - `58592dca0042` Terminal Velocity autonomous blocked-run repair loop, paused.
  - `4e9cc82d1a99` Terminal Velocity slice completion reporter, paused.
- Hermes profiles discovered: `default`, `campaign`, `loki-game`, `loki-shop`, `loki-trade`, `loki-youtube`, `terminal-velocity`, `travel-agent`. Use `loki-game` for this channel unless the user explicitly chooses another TV profile.
- Basilisk lane filesystem exists at `/mnt/c/Games/BasiliskII/multi4-trial/instance-{1..4}` with per-instance prefs, System 7.5.3 images, and EV transfer HFVs.
- Source/data surfaces checked as present:
  - `native_ev/data/sourced_ev_structures.json`
  - `native_ev/data/sourced_ev_names.json`
  - `native_ev/data/sourced_ev_junk.json`
  - `native_ev/data/sourced_ev_weapons.json`
  - `native_ev/data/sourced_ev_missions.json`
  - `native_ev/data/universe.json`
  - `tools/run_gameplay_scenarios.py`
  - `run_godot.sh`

## 2. Non-blocking operating mode

Topology setup is now implemented enough to start a worker burst, but it is still not a precondition for a single safe-local acceleration slice.

Use this manifest when the next action is one of:

- multi-worker coding;
- durable Kanban/dependency tracking;
- parallel Basilisk/original-runtime evidence;
- scheduled/watchdog mutation;
- cross-lane fan-in.

- Do not use this manifest as a reason to stop a single source/static semantic promotion, labeled scaffold, or cheap verifier improvement.
- For automatic-gameplay worker launch details, also read `docs/research/2026-06-08-automatic-gameplay-worker-application.md`; it supplies the lane types, failure packet schema, and semantic-Godot vs capture-driven-Basilisk split for applying external automation sources to workers.

## 3. Resource claim levels

Claim levels:

- `read`: may be inspected by any lane.
- `review-only`: may be summarized or linked but not edited by worker lanes.
- `write-exclusive`: only the named lane may write during a burst.
- `external-effect`: requires explicit user approval before activation.

Current shared read surfaces:

- `docs/research/terminal-velocity-development-compendium.md`
- `docs/research/source-aligned-game-development-method.md`
- `docs/research/terminal-velocity-coordination-topology.md`
- `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md`
- `docs/research/2026-06-07-static-source-fidelity-learning-pass-1.md`
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- `native_ev/data/sourced_ev_structures.json`
- `native_ev/data/sourced_ev_names.json`
- `native_ev/data/sourced_ev_governments.json`
- `native_ev/data/sourced_ev_junk.json`
- `native_ev/data/sourced_ev_missions.json`
- `native_ev/data/sourced_ev_weapons.json`
- `native_ev/data/sourced_ev_graphics.json`
- `native_ev/data/sourced_ev_sounds.json`

Current review-only surfaces during a burst unless specifically claimed by the integration owner:

- this manifest;
- `docs/research/original-ev-classic-runtime-observations.md`;
- `docs/research/ev-classic-quirk-review-ledger.md`;
- always-injected Hermes memories and skills.

External-effect surfaces:

- GitHub publication beyond normal coherent TV non-force push;
- cron/watchdog resume or mutation;
- Telegram/group reporting beyond ordinary final status;
- Basilisk input that mutates original EV pilot/save/disk state;
- raw proprietary asset publication.

## 4. Accelerated lane-contract audit

Selected lanes for the next safe acceleration burst. These lanes are independent enough to scout in parallel. Mutating implementation should still use actual worktrees and one fan-in owner.

### Lane A: static galaxy topology semantics

- Track: `fidelity-gate / static-source-mined`.
- Backlog anchor: `Fuller EV Classic galaxy topology and coordinates`.
- Owner/card: `TV-TOP-A-static-galaxy-topology`.
- Current status: IDs/name seeds and candidate hyperspace-link field family promoted; remaining coordinate/exact topology mapping has no Basilisk dependency until ambiguity spot checks.
- Writable surfaces if activated:
  - `tools/extract_ev_system_topology.py` or focused existing extractor extension;
  - `native_ev/data/sourced_ev_systems.json`;
  - `native_ev/tests/test_model.py` or focused sourced-data tests;
  - backlog/docs addendum for the promoted field family.
- Read/review surfaces: source manifests and compendium docs.
- Source-label policy: `decoded-resource-backed` for raw field mapping, `manual/docs-backed` only where Resource Bible field definitions are used, `terminal-velocity-observed` only after runtime verifier output.
- Verifier: JSON parse; extractor deterministic output; focused native tests; `python3 tools/run_gameplay_scenarios.py --all --pretty` if runtime-facing data changes.
- Merge contract: promote one field family at a time: IDs/names -> candidate links -> coordinates/exact record-to-name runtime topology -> ports/hazards/government. Do not replace the 10-system runtime subset in one broad edit.
- Gate: no exact Classic routing behavior claim from static fields alone.
- Rollback/cleanup: revert generated manifest plus extractor/test/docs commit chunk together.

### Lane B: system service/store provisioning manifest

- Track: `mixed build / static-source-mined fidelity-gate`.
- Backlog anchor: `System-by-system original service/store provisioning`.
- Owner/card: `TV-TOP-B-service-store-provisioning`.
- Current status: ready for static/source scout; Basilisk spot checks only for ambiguous UI-sensitive surfaces.
- Writable surfaces if activated:
  - `tools/extract_ev_service_matrix.py` or focused extractor extension;
  - `native_ev/data/sourced_ev_services.json`;
  - service matrix tests under `native_ev/tests/`;
  - `docs/checklists/ev-classic-fidelity-implementation-backlog.md` compact addendum.
- Source-label policy: `decoded-resource-backed` for landing/body/service fields; `original-runtime-observed` only for captured click-throughs such as Levo.
- Verifier: JSON parse; unit/model tests for service matrix; `./run_godot.sh tv-gameplay-curriculum-help-log` if visible help/scout guidance changes.
- Merge contract: begin with absent/present service matrix, then store inventories, then graphics/text cross-links.
- Gate: before/after captures required for any original EV mutating service click-through.
- Rollback/cleanup: revert service manifest/extractor/tests/docs as one slice.

### Lane C: economy and commodity semantic expansion

- Track: `mixed build / static-source-mined fidelity-gate`.
- Backlog anchor: `Economy-wide buy/sell display and spread rules` plus specialized `jünk` runtime availability.
- Owner/card: `TV-TOP-C-economy-commodity-semantics`.
- Current status: static `jünk` semantics exist; regular market formula/spread remains partial.
- Writable surfaces if activated:
  - economy extractor/import script under `tools/`;
  - `native_ev/data/sourced_ev_economy.json` or focused extension of existing sourced commodity manifest;
  - economy/scenario tests;
  - backlog/docs addendum.
- Source-label policy: Levo same-port sellback is `original-runtime-observed`; broad spreads stay `decoded-resource-backed` or `terminal-velocity-scaffold` until behavior evidence exists.
- Verifier: extractor deterministic output; targeted scenario(s); full scenario suite if runtime market data changes.
- Merge contract: specialized commodity metadata first, regular commodity formula second, runtime import last.
- Gate: do not infer universal buy/sell behavior from Levo sellback.
- Rollback/cleanup: revert data/import/tests/docs together.

### Lane D: mission-family semantic promotion

- Track: `fidelity-gate / static-source-mined` with build scaffolds allowed.
- Backlog anchor: mission families and offer/completion/deadline behavior from static pass.
- Owner/card: `TV-TOP-D-mission-family-semantics`.
- Current status: mission fields through flags are sourced; exact generation/UI/deadline behavior remains pending.
- Writable surfaces if activated:
  - mission extractor/import code;
  - `native_ev/data/sourced_ev_mission_families.json` or extension of `sourced_ev_missions.json`;
  - mission model/scenario tests;
  - backlog/docs addendum.
- Source-label policy: `decoded-resource-backed / manual/docs-backed` for field semantics; `terminal-velocity-scaffold` for playable approximations; no exact offer/deadline claim without runtime or stronger field-family evidence.
- Verifier: mission manifest parse; targeted scenario tests; help log if player guidance changes.
- Merge contract: one mission family or field group per slice.
- Gate: avoid broad story/economy changes from low-confidence fields.
- Rollback/cleanup: revert generated mission manifest/import/tests/docs together.

### Lane E: deterministic evaluator and playtest evidence packets

- Track: `build / verifier-lane`.
- Backlog anchor: active gameplay curriculum, playtesting-as-evidence, scenario/evaluator harness.
- Owner/card: `TV-TOP-E-fast-evaluator-playtest-packets`.
- Current status: safe immediate lane; no Basilisk dependency.
- Writable surfaces if activated:
  - `tools/run_gameplay_scenarios.py` only if evaluator UX changes;
  - `native_ev/tests/test_scenario_eval.py`;
  - `native_ev/tests/test_model.py`;
  - `docs/research/playtest-runs/`;
  - backlog/docs addendum.
- Source-label policy: `terminal-velocity-observed` for Godot/scenario output; `help_surface_pending_playtest` for F10/help copy until human or structured playtest evidence exists.
- Verifier: `python3 tools/run_gameplay_scenarios.py --all --pretty`; focused `./run_godot.sh tv-*-log`; `./run_godot.sh tv-gameplay-curriculum-help-log`.
- Merge contract: evaluator-only changes may fan in after focused plus all-scenario verification; do not mix with semantic data import in the same worker branch unless the manifest is updated.
- Gate: no EV Classic behavior claims from evaluator feel/playtest alone.
- Rollback/cleanup: revert tests/log docs and any evaluator code together.

## 5. Worktree and branch registry

No mutating workers were launched in this safe setup pass, so no extra worktrees were created. When activating the burst, use these actual local paths and branches:

- Lane A branch/path: `tv/topology-static-galaxy` at `/home/bh/workspaces/loki/tv-lanes/topology-static-galaxy`.
- Lane B branch/path: `tv/topology-service-store` at `/home/bh/workspaces/loki/tv-lanes/topology-service-store`.
- Lane C branch/path: `tv/topology-economy-commodity` at `/home/bh/workspaces/loki/tv-lanes/topology-economy-commodity`.
- Lane D branch/path: `tv/topology-mission-family` at `/home/bh/workspaces/loki/tv-lanes/topology-mission-family`.
- Lane E branch/path: `tv/topology-evaluator-playtest` at `/home/bh/workspaces/loki/tv-lanes/topology-evaluator-playtest`.

Activation command pattern, run by the integration owner only after checking `git status --short --branch` and `git worktree list --porcelain`:

```bash
mkdir -p /home/bh/workspaces/loki/tv-lanes
git worktree add -b tv/topology-static-galaxy /home/bh/workspaces/loki/tv-lanes/topology-static-galaxy main
git worktree add -b tv/topology-service-store /home/bh/workspaces/loki/tv-lanes/topology-service-store main
git worktree add -b tv/topology-economy-commodity /home/bh/workspaces/loki/tv-lanes/topology-economy-commodity main
git worktree add -b tv/topology-mission-family /home/bh/workspaces/loki/tv-lanes/topology-mission-family main
git worktree add -b tv/topology-evaluator-playtest /home/bh/workspaces/loki/tv-lanes/topology-evaluator-playtest main
```

Fan-in rule: merge or cherry-pick one branch at a time into `main`; run the lane verifier before fan-in and integrated verification after fan-in. Remove linked worktrees with `git worktree remove <path>` only after their branch state is safely integrated or intentionally abandoned.

## 6. Basilisk four-lane register

These records implement the topology's four-lane shape without starting or mutating any emulator. Use a lane only after confirming the pilot/save/restore state and capture path for the specific evidence question.

### BAS-1

- Emulator/lane ID: `BAS-1`.
- Instance directory: `/mnt/c/Games/BasiliskII/multi4-trial/instance-1`.
- Guest disk image: `/mnt/c/Games/BasiliskII/multi4-trial/instance-1/System7_5_3_tv4_1.img`.
- Transfer/disk copy: `/mnt/c/Games/BasiliskII/multi4-trial/instance-1/EV_Installer_Transfer_tv4_1.hfv`.
- Prefs file: `/mnt/c/Games/BasiliskII/multi4-trial/instance-1/BasiliskII_prefs_tv4_1`.
- Pilot/save/restore state: not verified in this pass; must be named before use.
- Window/input target: not verified in this pass; must be probed before use.
- Capture directory: `/mnt/c/Games/BasiliskII/` or a per-question subdirectory under it.
- Assigned evidence question: unassigned.
- Allowed mutations: none until a question-specific record is written.
- Status: `ready-filesystem / needs pilot-window-restore verification`.

### BAS-2

- Emulator/lane ID: `BAS-2`.
- Instance directory: `/mnt/c/Games/BasiliskII/multi4-trial/instance-2`.
- Guest disk image: `/mnt/c/Games/BasiliskII/multi4-trial/instance-2/System7_5_3_tv4_2.img`.
- Transfer/disk copy: `/mnt/c/Games/BasiliskII/multi4-trial/instance-2/EV_Installer_Transfer_tv4_2.hfv`.
- Prefs file: `/mnt/c/Games/BasiliskII/multi4-trial/instance-2/BasiliskII_prefs_tv4_2`.
- Pilot/save/restore state: not verified in this pass; must be named before use.
- Window/input target: not verified in this pass; must be probed before use.
- Capture directory: `/mnt/c/Games/BasiliskII/` or a per-question subdirectory under it.
- Assigned evidence question: unassigned.
- Allowed mutations: none until a question-specific record is written.
- Status: `ready-filesystem / needs pilot-window-restore verification`.

### BAS-3

- Emulator/lane ID: `BAS-3`.
- Instance directory: `/mnt/c/Games/BasiliskII/multi4-trial/instance-3`.
- Guest disk image: `/mnt/c/Games/BasiliskII/multi4-trial/instance-3/System7_5_3_tv4_3.img`.
- Transfer/disk copy: `/mnt/c/Games/BasiliskII/multi4-trial/instance-3/EV_Installer_Transfer_tv4_3.hfv`.
- Prefs file: `/mnt/c/Games/BasiliskII/multi4-trial/instance-3/BasiliskII_prefs_tv4_3`.
- Pilot/save/restore state: not verified in this pass; must be named before use.
- Window/input target: not verified in this pass; must be probed before use.
- Capture directory: `/mnt/c/Games/BasiliskII/` or a per-question subdirectory under it.
- Assigned evidence question: unassigned.
- Allowed mutations: none until a question-specific record is written.
- Status: `ready-filesystem / needs pilot-window-restore verification`.

### BAS-4

- Emulator/lane ID: `BAS-4`.
- Instance directory: `/mnt/c/Games/BasiliskII/multi4-trial/instance-4`.
- Guest disk image: `/mnt/c/Games/BasiliskII/multi4-trial/instance-4/System7_5_3_tv4_4.img`.
- Transfer/disk copy: `/mnt/c/Games/BasiliskII/multi4-trial/instance-4/EV_Installer_Transfer_tv4_4.hfv`.
- Prefs file: `/mnt/c/Games/BasiliskII/multi4-trial/instance-4/BasiliskII_prefs_tv4_4`.
- Pilot/save/restore state: not verified in this pass; must be named before use.
- Window/input target: not verified in this pass; must be probed before use.
- Capture directory: `/mnt/c/Games/BasiliskII/` or a per-question subdirectory under it.
- Assigned evidence question: unassigned.
- Allowed mutations: none until a question-specific record is written.
- Status: `ready-filesystem / needs pilot-window-restore verification`.

Basilisk use gate: these records make the four lanes concrete, but they do not authorize destructive original-EV tests, Strict Play, save-corrupting experiments, or raw asset publication.

## 7. Coordination manifest for the next acceleration burst

- Objective: accelerate source-aligned Terminal Velocity progress by promoting static/source-mined semantics and verifier/playtest evidence in parallel while preserving one integration owner and explicit source labels.
- Track: `mixed`.
- Source/fidelity boundary: static resources and manuals can support field/data semantics; Godot/scenario probes can support Terminal Velocity observed behavior; original EV Classic UI/timing/behavior claims require Basilisk/runtime observation or decoded field evidence appropriate to the claim.
- Live-state preflight: use section 1, then refresh before launching workers.
- Worker lanes: use lanes A-E above.
- Fan-in/integration owner: current Loki Game integration owner unless delegated explicitly.
- Required verification before each lane handoff: lane-specific verifier plus visible `git status --short --branch` from the lane worktree.
- Required verification after fan-in: `git diff --check`; targeted lane verifier(s); `python3 tools/run_gameplay_scenarios.py --all --pretty` if native model/scenario/runtime-facing data changed; relevant `./run_godot.sh tv-*-log` if Godot behavior/help changed.
- Human gates: external/account/config changes, cron/watchdog resume, destructive or risky original-EV tests, Strict Play, raw proprietary asset publication, force-push/history rewrite, deletion, release/settings changes.
- Done condition: each lane produces either a committed implementation slice, an evidence packet, or a compact blocker with exact next action and verifier.
- Do-not-redo notes: do not repeat the live-state discovery in this manifest as if it were still current after context resets; refresh it. Do not wait on Basilisk for static source work. Do not use Kanban for one-off single-writer slices.

## 8. Automatic gameplay manifest additions

For Lane E or any automated-play extension, add these fields before execution:

- Automation lane: `semantic-godot-probe` unless a screen/capture or emulator-state wrapper is explicitly chosen.
- Objective/curriculum item: name one scenario/help/playtest question.
- Starting state and restore method: scenario name, pilot fixture, save path, or deterministic setup command.
- Action/macro source: existing regression, human demo, generated macro, or source-derived scenario.
- Observation schema: JSON event/log output first; screenshot/vision packet only when engine-side state is insufficient.
- Success predicate / metric: exact boolean/log field or scenario assertion.
- Failure packet path: `docs/research/playtest-runs/` for playtest evidence; use a per-run filename.
- Skill/macro promotion rule: only promote a macro to reusable workflow after it has a named verifier and a failure mode record.
- Exploration budget and stop condition: fixed command count/time; stop on first failing predicate that needs diagnosis.
- Keep/revert rule: generated code/data must be reverted unless it improves the metric and passes the agreed verifier.

## 9. Kanban and cron state

Kanban is implemented here as a manifest-level dependency map, not as live cards, because no durable multi-agent run was launched. If the next step launches multiple persistent workers, create Kanban cards from lanes A-E only after refreshing profile/board state and confirming the active board tool/profile.

Cron/watchdogs remain paused. Resuming them is an external/runtime topology change and stays explicitly gated.

## 10. Immediate safe acceleration recommendation

Start with Lane A or Lane E:

- Lane A if the goal is highest-fidelity static acceleration without Basilisk bottlenecks.
- Lane E if the goal is fastest player-visible/playtest evidence improvement.

Both can proceed single-writer immediately from this checkout without additional topology setup.
