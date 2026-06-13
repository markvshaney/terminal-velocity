# TV blocked-state recovery recommendation

Date: 2026-06-12
Status: canonical recommendation artifact
Source / evidence basis:
- Telegram Loki GameTV discussion about whether to approve the 11:01 p.m.–11:03 p.m. recommendation posts.
- Current implementation surfaces inspected before artifact creation:
  - `tools/tv_runner_recovery_preflight.py`
  - `tools/tv_integration_lane.py`
  - `native_ev/tests/test_tv_runner_recovery_preflight.py`
  - `native_ev/tests/test_tv_integration_lane.py`
  - `docs/research/2026-06-13-tv-runner-recovery-ledger-follow-up.md`
  - archived provenance copy outside repo: `/home/bh/.hermes/profiles/loki-game/home/terminal-velocity-archived-research/2026-06-12-tv-runner-integration-owner-review-gate.md`

## How this artifact should be used

This is the canonical summary of the recommendation from the 11:01 p.m.–11:03 p.m. discussion. It supersedes the intermediate chat fragments from that window.

Use it as the process/design artifact for implementing automated recovery of Terminal Velocity runner/integration fail-closed states. It is not an instruction to weaken fail-closed safety. It is a recommendation to replace vague human-review stops with deterministic recovery attempts and exact blocker classes.

## Bottom-line recommendation

Implement automated blocked-state recovery in the integration lane.

Preferred first command:

```bash
tools/tv_integration_lane.py --recover-dirty-handoff --push
```

Broader follow-on command:

```bash
tools/tv_integration_lane.py --recover-blocked-state
```

The system should evolve from:

```text
detect unsafe state -> label fail-closed -> wait
```

to:

```text
detect blocked state -> classify exact cause -> run safe deterministic recovery -> verify -> publish or stop at precise unresolved hazard
```

Default behavior should be dry-run JSON. Mutating behavior should require explicit flags such as `--push`, `--apply-gate-comments`, or `--repair-unsafe-debris`.

## Authority split

### `tv_runner_recovery_preflight.py`: classifier/checkpoint authority

This script should answer:

- Is the repo dirty?
- Which paths are dirty?
- Are the paths safe TV project paths?
- Are any paths sensitive, proprietary, or unrelated?
- Do dirty paths match exactly one handoff card?
- Does that handoff name the intended files?
- Is focused verifier evidence present and passed?
- If safe, can this dirty bundle become a local checkpoint commit?

It may create a local checkpoint commit when the bundle is proven attributable and verifier-passed.

It should not push, close cards, or perform integration-owner publication.

### `tv_integration_lane.py`: publish/recovery orchestration authority

This script should answer:

- Is there an active worker?
- Is the branch behind or divergent?
- Are local commits safe to publish?
- Do path, diff, and secret checks pass?
- Can a normal non-force push proceed?
- After push, does local `HEAD == origin/main`?
- Should Kanban comments/events be normalized?

The publish side belongs here. `tv_integration_lane.py` may call or import the recovery preflight classifier/checkpoint logic, but publication and closeout remain integration-lane responsibilities.

## Eleven-step tracked-handoff recovery guard sequence

The “right design” is an automated guard sequence, not a manual checklist:

1. Inspect tracked dirty paths.
2. Match them to exactly one blocked/running handoff card.
3. Require the handoff text to name the intended files.
4. Require focused verifier evidence, or run the focused verifier if the command is discoverable.
5. Stage only the matched paths.
6. Run `git diff --cached --check`.
7. Run existing integration-lane safety checks:
   - no active worker conflict;
   - no branch divergence;
   - no unsafe changed files;
   - no secret/proprietary path or diff hits;
   - no unrelated files.
8. Commit locally.
9. Push normally if this is Terminal Velocity and standing normal-push policy passes.
10. Fetch and verify local `HEAD == origin/main`.
11. Normalize/update the Kanban card or gate comments/events.

This fixes `unsafe_dirty_state` for attributable tracked handoffs without treating arbitrary tracked dirt as safe.

## Why tracked dirty recovery must differ from untracked debris repair

Automated tracked-handoff recovery is appropriate only when guarded.

It would be wrong to use the same logic for tracked dirty files that is used for untracked debris.

### Untracked debris repair is reversible housekeeping

It can safely do things like:

- move unknown scratch files out of the repo;
- preserve them in quarantine;
- re-run status;
- make no claim about project semantics.

This is appropriate only for narrow cases like:

```text
untracked + non-sensitive + non-project path
```

### Tracked dirty recovery is publication/integration

Tracked dirty files may be real project work. Committing them creates project history. Pushing them mutates the public repo. Marking the card resolved changes Kanban truth.

Therefore tracked recovery needs stronger evidence:

- exact handoff match;
- intended file list;
- focused verifier evidence;
- staged-only-path discipline;
- integration-lane checks;
- normal push verification.

## Recommended handling by fail-closed state

### Unmatched dirty state

Current behavior: classify as `unsafe_dirty_state`.

Recommended behavior:

- If unmatched dirt is only untracked, non-sensitive, non-project debris:
  - quarantine it;
  - re-run classifier;
  - continue if clean or now attributable.
- If unmatched dirt includes tracked/project files:
  - do not commit or push;
  - emit a concrete blocker with exact paths;
  - create or update a repair card/comment.

Do not use generic “review required.”

### Mixed dirty state

Current behavior: fail closed.

Recommended behavior: split deterministically where possible:

- matched tracked handoff bundle;
- untracked non-sensitive debris;
- sensitive/unrelated/tracked remainder.

Then:

- quarantine only safe debris;
- checkpoint/publish only the matched handoff bundle;
- stop if any sensitive or unmatched tracked remainder remains.

Mixed state should not automatically block forever, but only the safe separable subset should advance.

### Sensitive paths

Current behavior: fail closed.

Recommended behavior: keep this fail-closed.

Automation may:

- identify sensitive/proprietary-looking paths;
- redact reports;
- preserve evidence;
- create a concrete blocked card.

Automation should not:

- push sensitive paths;
- commit secrets;
- casually move possible secrets;
- normalize the gate as resolved.

Sensitive state is a true human/repair gate unless there is a very narrow deterministic false-positive rule.

### Verifier missing or verifier failed

Current behavior: `rerun_focused_verifier` classification exists, but there is not yet a full recovery loop.

Recommended behavior:

- If the handoff names a focused verifier command, run it.
- If it passes, continue checkpoint/publish recovery.
- If it fails, create or dispatch a repair card with exact command/output.
- If no command is discoverable, fail with a concrete `rerun_focused_verifier` blocker.

The system should not ask for human review when the next safe action is simply to run the named verifier.

### Branch behind or divergent

Current behavior: integration lane blocks on `branch_behind_origin`.

Recommended behavior:

- Fetch first.
- If local commits are linear and a clean rebase/fast-forward is possible:
  - update safely;
  - rerun relevant checks;
  - continue publish.
- If conflict/divergence occurs:
  - stop;
  - create a conflict-repair card;
  - never force push.

This replaces “branch behind means human review” with “branch behind means attempt safe update; gate only on conflict or unsafe divergence.”

### Active worker

Current behavior: integration lane blocks on `active_worker`.

Recommended behavior: keep active worker as a publish blocker.

Automation should:

- wait/poll;
- observe worker completion;
- rerun integration after completion;
- detect stale claims separately.

Automation should not publish over a live worker.

If the claim is stale, a separate stale-worker cleanup path may clear or repair it after proof.

## Canonical gate classes

Avoid vague gate states such as `review required` for normal TV recovery. Use canonical classes with exact next actions:

- `push_ready`
- `unsafe_dirty_state`
- `unmatched_dirty_state`
- `mixed_dirty_state`
- `sensitive_path_blocked`
- `verifier_missing`
- `verifier_failed`
- `rerun_focused_verifier`
- `branch_behind_origin`
- `branch_divergent`
- `active_worker`
- `explicit_human_gate`

Each class should map to a deterministic remediation or a precise stop condition.

## Relationship to prior autostart/start-restart recommendation

The prior recommendation to automate Terminal Velocity continuous-runner start/restart with a script-only autostart watchdog remains valid, but this artifact qualifies its ordering.

Autostart is a liveness mechanism, not an integration-owner substitute. It may dispatch or seed a successor only after blocked-state recovery and integration-owner preflight determine that there is no unresolved completed handoff, dirty bundle, verifier gap, branch update, active worker, or explicit hazard to resolve first.

Correct ordering:

```text
start/resume tick -> blocked-state recovery preflight -> integration-owner recovery/publish if needed -> seed/dispatch successor only after no real gate remains
```

Autostart must not seed over these states:

- `push_ready`;
- attributable dirty handoff;
- verifier-missing or verifier-failed handoff;
- branch-behind/divergent publication state;
- active worker;
- sensitive, unrelated, or unmatched tracked dirty state.

### Why autostart must not seed over `push_ready`

`push_ready` means the previous worker finished a coherent local slice and handed it to the integration owner for publication/review. It is not an idle lane.

Seeding over `push_ready` is unsafe because it can:

- bury completed but unpublished work behind a new running card;
- create overlapping ownership between the integration owner and a new worker;
- mix old and new file changes, making attribution and staging unsafe;
- invalidate verifier evidence that applied to the earlier bundle;
- increase local/remote divergence before the completed checkpoint is normalized;
- hide the required publication action behind a false progress signal;
- blur the worker/autostart/integration-owner authority boundary.

The safe handling is:

1. detect `push_ready`;
2. prevent autostart successor seeding;
3. have the integration owner inspect intended files, verifier output, secrets/proprietary risk, and remote state;
4. checkpoint/push/fetch/verify when safe under the standing normal non-force TV policy;
5. normalize/complete the handoff card;
6. only then allow autostart to dispatch or seed the next successor.

## Recommended command behavior

### First slice: `--recover-dirty-handoff`

```bash
tools/tv_integration_lane.py --recover-dirty-handoff
```

Dry run should emit JSON:

- repo state;
- dirty paths;
- matched handoff;
- verifier status;
- planned checkpoint;
- active worker status;
- branch divergence status;
- path/secret/diff checks;
- whether push would be allowed.

With push:

```bash
tools/tv_integration_lane.py --recover-dirty-handoff --push
```

It should:

1. call recovery classifier;
2. require `checkpoint_and_push_ready`;
3. create local checkpoint commit;
4. rerun integration classification;
5. push only if existing integration guards pass;
6. fetch and verify remote;
7. write Kanban normalization comments/events.

### Second slice: `--recover-blocked-state`

```bash
tools/tv_integration_lane.py --recover-blocked-state
```

This should dispatch over broader fail-closed classes:

- debris repair;
- tracked handoff recovery;
- verifier rerun;
- safe branch update;
- active-worker wait/stale detection;
- concrete blocked-card creation for sensitive/unmatched states.

## Recommended safety defaults

1. Dry-run JSON by default.
2. Explicit flags for every mutation.
3. Stage only matched paths.
4. Never commit sensitive/unrelated files.
5. Never publish over active workers.
6. Never force push.
7. Always fetch and verify remote after push.
8. Always emit exact blocker names.
9. Normalize stale “review required” into actionable classes.
10. Create repair cards/comments instead of vague human-review gates.

## Implementation order

1. Add `tv_integration_lane.py --recover-dirty-handoff` dry-run JSON.
2. Wire it to `tv_runner_recovery_preflight.py` classification.
3. In mutating mode, let it create a local checkpoint only after `checkpoint_and_push_ready`.
4. Reuse existing integration-lane guards before push.
5. Push only under the standing normal non-force TV policy.
6. Fetch and verify local `HEAD == origin/main`.
7. Write idempotent Kanban normalization comments/events.
8. Add `--recover-blocked-state` as the broader dispatcher after the dirty-handoff slice is verified.

## Non-goals and gates

This recommendation does not authorize:

- force pushes or history rewrites;
- publication of sensitive/proprietary/raw-capture material;
- credential, account, provider, gateway, or config changes;
- destructive original-EV actions;
- publishing over a live active worker;
- treating arbitrary tracked dirt as safe.

Those remain explicit gates.
