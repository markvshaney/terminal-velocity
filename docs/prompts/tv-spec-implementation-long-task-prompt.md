# TV spec implementation long-running task prompt

Purpose: durable prompt for a recurring Loki Game task that implements `docs/research/tv-spec.md` as the active Terminal Velocity development workflow.

```text
You are running under the `loki-game` Hermes profile for Terminal Velocity.

Objective: implement `docs/research/tv-spec.md` as an executable long-running development workflow for `/home/bh/workspaces/loki/terminal-velocity`, not merely as a documented policy. Each run should perform one safe, source-labeled, verified increment that advances the live backlog under the tv-spec contracts.

Required first actions every run:
1. Load/follow these skills when available: `long-running-task-harness`, `source-and-fidelity`, `artifact-governance`, `living-backlog-governance`, `ev-terminal-velocity-play`.
2. Inspect live repo state: `git status --short --branch`, current branch, `HEAD`, and `origin/main`.
3. Read with line numbers:
   - `.hermes/long-running/tv-spec-implementation/task-ledger.json`
   - the latest tail of `.hermes/long-running/tv-spec-implementation/events.jsonl`
   - `docs/research/tv-spec.md`
   - relevant section(s) of `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
4. If the worktree is dirty, understand and stabilize the existing slice before starting a new one. Do not overwrite or abandon unknown dirty work.

Task loop:
- Prefer current actionable backlog items that already expose `next_action`, `lane_class`, `oracle_class`, `source_basis`, `verifier`, `blocked_reason`, and `promotion_status`.
- Default initial lane, if the repo is clean and no stronger live blocker exists: Lane A static galaxy topology semantics from the backlog item “Fuller EV Classic galaxy topology and coordinates,” continuing one field family at a time after the current `syst` coordinate/link-slot static promotions.
- Use the tv-spec routing decision tree:
  - static-resource/manual-backed items: decoded resources, Resource Bible/manuals, extractor/model tests;
  - runtime-ui/timing/combat items: bounded Basilisk/original-runtime evidence only when safe and explicitly needed;
  - tv-scaffold/evaluator items: Godot/Python deterministic probes with clear scaffold labels.
- Build one vertical increment per run unless a small adjacent verifier/doc update is needed to stabilize the slice.
- Each increment packet must record: behavior/claim, `oracle_class`, `source_basis`, lane class, source/fidelity label, verifier command and actual result, files/captures/logs touched, backlog/provenance update or explicit reason, promotion status, uncertainty/gates.
- Update `.hermes/long-running/tv-spec-implementation/task-ledger.json` and append JSONL events for every slice start, artifact read, edit, verification, checkpoint, gate, and completion.
- Normal coherent non-force pushes to `markvshaney/terminal-velocity` are preapproved after the established TV checks: inspect status/remotes/branch, stage intended files only, run relevant verification, check no secrets/proprietary/unrelated files, push, fetch, verify local `HEAD == origin/main`, and report concise bundle summary. Do not force-push/rewrite history.

Verification defaults:
- Static/model slices: targeted unittest(s), relevant extractor command, JSON parse/idempotence check, and `git diff --check`.
- Native gameplay scenario slices: targeted unittest(s), targeted `tools/run_gameplay_scenarios.py <scenario> --pretty`, broader native scenario suite when practical.
- Godot slices: target `./run_godot.sh <mode>`, and `./run_godot.sh self-test` when practical.
- Always verify the ledger JSON parses and events JSONL parses before closing a run.

Gates:
- Stop and record `waiting_gate` only for: destructive/risky original-EV tests, Strict Play, hard-to-restore/save-corrupting original pilot mutation, raw proprietary asset publication, external/account/config/provider/gateway changes, changing other scheduled jobs, force-push/history rewrite, deletion/merge/release/settings changes, non-TV repo/public/social side effects, missing evidence required for a fidelity claim, or unsafe dirty state that cannot be separated.
- A completed safe slice is a checkpoint, not task completion. Continue on the next recurrence unless the ledger `done_condition` is met or a real gate/blocker/no-safe-slice state is recorded.

Closeout for each run:
- Final response should be local-only concise: status (`productive slice`, `checkpoint`, `waiting_gate`, `blocked`, or `no-op with reason`), files touched, verification output, source/fidelity labels, next resume action, and any gate.
```
