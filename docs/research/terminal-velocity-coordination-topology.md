# Terminal Velocity coordination topology

Date: 2026-06-06
Source: Loki Game Telegram post at 2026-06-06 15:27:45 EDT, message stored in profile session `bg_152708_d421b5`, message id `37710`.

Purpose: preserve the coordination/worker-efficiency recommendation as a durable Terminal Velocity process artifact. This is a process artifact, not an EV Classic behavior source.

Canonical summary: this page is part of the Terminal Velocity development compendium. Read `docs/research/terminal-velocity-development-compendium.md` first for current doctrine; keep this page as the detailed coordination topology, manifest, and worker-resource rationale.

## Decision

Use **accelerated parallel lanes with one integration owner** as the default coordination topology once lane contracts exist.

1. Keep one integration owner for fan-in, final diff review, integrated verification, commit, and normal non-force push.
2. Use multiple mutating worker lanes in isolated worktrees when each lane has an owner, writable surface, verifier, source/fidelity label policy, merge contract, and rollback path.
3. Use Kanban for durable multi-lane work and context survival, not for line-level patches.
4. Use a coordination manifest before any multi-worker coding slice.
5. Keep one writer per file/resource surface by assigning lane ownership; do not enforce global serial development merely to avoid collisions.
6. Treat the local runtime setup as **4 Basilisk emulator lanes** with per-lane disk/prefs/window/input/capture/restore records.

## Coordination topology

### Default mode: accelerated parallel lanes with one integration owner

Use this for most Terminal Velocity development once a lane contract exists:

- **Integration owner:** owns final fan-in, diff review, integrated verification, commit, and normal non-force push.
- **Mutating worker lanes:** may write in isolated worktrees within assigned surfaces.
- **Evidence lanes:** source/resource/manual/Basilisk observations produce labeled evidence packets. Static/source-mined fidelity lanes should not wait on emulator speed when decoded resources or manuals can answer the question.
- **Verifier lanes:** scenario/test/probe workers produce executable checks and failure packets.
- **Reviewer lanes:** inspect fidelity/spec/test risks and consolidation opportunities.

One-writer discipline applies at integration and per-resource ownership boundaries, not as a blanket ban on parallel writing.

### Build-track lane classes

Valid mutating or semi-mutating lanes include:

- static/source-mined fidelity: semantic-promotion and integration lanes for map topology, planets/systems, stations, landing services, commodities, ships, outfits, weapons, descriptions/text resources, and decoded mission/resource data. Much of the primitive/resource inventory is already learned; remaining work is field-family semantics, cross-links, runtime-facing import, and tests. Current promoted semantic manifests cover government, mission, weapon, and specialized `jünk` commodity records;
- missions/story chains;
- economy/commodity trade;
- map/routing/hyperspace;
- landed UI/services;
- combat/AI;
- ships/outfits/weapons/data import;
- tutorial/help/player guidance;
- scenario/evaluator harness;
- source/resource mining and provenance docs;
- Basilisk original-runtime observation lanes.

Each lane must name owner/card, worktree if mutating, writable surfaces, source/fidelity label policy, verifier, merge contract, and cleanup/rollback plan.

### Fidelity gate lanes

Fidelity promotion remains strict. Use fidelity gate lanes for:

- original-runtime claims;
- decoded-resource constants;
- exact UI text;
- mission/economy behavior;
- movement/physics tuning;
- Classic quirks vs intentional TV divergences;
- canonical checklist/backlog/source-doc promotion.

Build-track scaffolds may proceed with `scaffold`, `terminal-velocity-observed`, `source-grounded EV-family`, or `needs original confirmation` labels. They do not become EV Classic fidelity claims until a fidelity gate accepts the evidence.

### Basilisk emulator topology

The local runtime setup has **4 Basilisk emulator lanes**. Do not describe this as “up to 4” or “probably four.”

Basilisk is not the universal fidelity bottleneck. Use it for behavioral confirmation, ambiguity resolution, UI/state-transition observations, and timing/feel checks. Use decoded-resource/manual/local-source lanes first for static data such as maps, planets, stations, commodities, ships, outfits, weapons, descriptions/text, and decoded mission/resource data.

Each Basilisk lane record must include:

- emulator/lane ID;
- owning worker/card;
- guest disk image or disk copy;
- prefs file;
- pilot/save/restore state;
- window title/process/input target;
- capture directory;
- assigned evidence question;
- allowed mutations;
- status: `ready`, `blocked`, `dirty`, or `needs reset`.

A worker may own one emulator lane. If a specific lane lacks isolation records, that lane setup is incomplete; the emulator count remains 4.

### Worktree and merge rule

For parallel coding:

- each coding worker gets an isolated branch/worktree;
- each worker has explicit file/resource claims;
- each worker runs its lane verifier before handoff;
- coordinator/integration owner merges one branch at a time or in an explicit batch;
- coordinator runs final integrated tests and resolves conflicts;
- no worker pushes independently unless the coordinator explicitly assigns that publication role.

### Coordination manifest template

Before any bigger/multi-worker slice, write a short manifest with:

- Objective:
- Track: `build`, `fidelity-gate`, or `mixed`:
- Source/fidelity boundary:
- Live-state preflight:
  - branch/status checked:
  - active TV workers/processes checked:
  - Kanban/cron/watchdog state checked:
  - available Hermes profiles checked:
  - WSL/host capacity assumptions checked when relevant:
- Worker lanes:
  - owner/card:
  - lane class:
  - worktree/branch:
  - writable surfaces:
  - read/review-only surfaces:
  - source/fidelity label policy:
  - verifier command:
  - merge contract:
  - cleanup/rollback plan:
- Basilisk lane record, if any:
  - emulator ID:
  - disk/prefs/pilot/save:
  - window/input target:
  - capture path:
  - restore method:
  - allowed mutations:
- Required verification:
- Human gates:
- Fan-in/integration owner:
- Done condition:
- Do-not-redo notes:

## Source cross-check: deficiencies and improvements

This artifact is source-backed process guidance, not an EV Classic behavior source. A 2026-06-06 source pass checked these coordination references:

- Anthropic Claude Code common workflows: plan-before-editing, subagent research, and parallel worktree sessions. Source: `https://docs.anthropic.com/en/docs/claude-code/common-workflows.md`.
- Git worktree documentation: multiple working trees can check out more than one branch at a time; linked worktrees have separate `HEAD`/`index` metadata and should be removed with `git worktree remove`. Source: `https://raw.githubusercontent.com/git/git/master/Documentation/git-worktree.adoc`.
- Karpathy `autoresearch`: one mutable training file, fixed 5-minute eval budget, trusted `val_bpb` metric, TSV logging, and keep/reset rule. Sources: `https://raw.githubusercontent.com/karpathy/autoresearch/master/README.md` and `https://raw.githubusercontent.com/karpathy/autoresearch/master/program.md`.
- Hermes/local coordination guidance: `subagent-driven-development` / `references/multi-agent-resource-coordination.md`, `kanban-orchestrator`, `bounded-autoresearch`, and the live `delegate_task`/`cronjob` tool contracts.

Deficiencies found in the first draft and corrective rules:

1. **Missing live-state preflight.** Before any topology decision, inspect the live repo state, current branch, dirty files, active long-running TV workers, existing Kanban/cron/watchdog state, and available Hermes profiles. Do not assign Kanban profiles by invented names.
2. **Manifest too prose-heavy for collisions.** Add explicit resource claims for files, directories, generated data, local captures, cron jobs, Kanban cards, skills/memory, and external side effects. Use `read`, `review-only`, `write-exclusive`, or `external-effect` claim levels.
3. **Parallel coding needs workspace verification, not just intent.** For true parallel coding, record the actual branch/worktree path for each writer, verify it exists, and require merge-one-at-a-time fan-in. Clean up linked worktrees deliberately after use.
4. **Subagent output is evidence, not proof.** Read-only scouts/reviewers may summarize, but the coordinator must verify returned paths/claims against live files, `git diff`, and real tests before reporting success.
5. **Kanban needs profile discovery and dependency links.** Use Kanban only after `hermes profile list` or equivalent profile discovery. Independent lanes may fan out; dependent lanes must be created with parent links so implementation/review cannot start before evidence exists.
6. **Cron/watchdogs are approval-gated runtime topology.** Keep proposed watchdogs report-only, quiet-on-no-change, and preferably script-only/no-agent. Do not let scheduled LLM runners mutate the same repo surface as a live serial implementer unless a manifest and gate explicitly say so.
7. **Autoresearch is not just “more agents.”** If a TV workflow becomes iterative optimization, define goal, metric, baseline, mutable surface, trusted surface, fixed budget, experiment log, and keep/revert rule before running it. Otherwise treat it as normal source-aligned development or read-only discovery.
8. **Source separation must stay visible.** External agent/workflow sources may improve process only. They do not justify EV Classic behavior claims; EV behavior still requires original runtime, decoded resources, manuals/Bibles, or explicitly labeled EV-family/community evidence.

## Automatic-gameplay source pass: topology implications

A 2026-06-06 automatic-gameplay source pass expanded `docs/research/automated-gameplay-learning-reference-sources.md` with implementation-oriented automation/game-testing sources. These sources reinforce the topology above, but they do **not** move Terminal Velocity to broad autonomous gameplay yet.

Sources checked for this pass:

- Voyager README: automatic curriculum, executable skill library, environment feedback, execution-error repair, and self-verification.
- Airtest README: image-recognition UI automation for games/apps, simulated input/assertions, command-line/Python API runs, HTML reports, and screen recording.
- Poco README.rst: SDK-integrated cross-engine UI hierarchy/action access for Unity3D/cocos/native apps.
- Stable-Retro README: emulator-backed Gymnasium environments for classic games, with ROM/state/emulator integration constraints.
- Wuji README: automatic online combat-game testing with MOEA/DRL to explore state and discover bugs.
- Tencent GAutomator README: SDK-integrated mobile-game test automation through engine elements/GameObjects.
- SerpentAI README: older Python game-agent framework lead; useful as architecture history, lower priority due to age/status.

Topology updates from those sources:

1. **Two automation lanes, not one.** Keep `symbolic/semantic Godot probes` separate from `screen/capture-driven Basilisk or UI automation`. Semantic hooks can write stable JSON event logs and scenario results; capture-driven automation must attach screenshots, OCR/vision notes, and uncertainty labels.
2. **Curriculum requires an execution surface.** Before automatic gameplay loops, define a scenario registry, objective queue, skill/macro library location, environment-feedback schema, and promotion rule from discovered macro → regression/test/backlog entry.
3. **State archive before exploration.** Go-Explore/Stable-Retro-style patterns only apply when a state can be named and returned to. For Terminal Velocity, record save/pilot/scenario seed, system/location, fuel/cargo/mission state, route, and expected restore command before branching exploration.
4. **Failure artifacts are first-class.** Automation runs should produce durable failure packets: command/macro, starting state, observed state, expected predicate, screenshot/log path when available, and whether the failure is `automation-flake`, `TV-bug`, `source-gap`, or `fidelity-pending`.
5. **Engine-integrated APIs are preferred in Godot, unavailable in Basilisk.** Poco/GAutomator-style hierarchy access supports adding Godot semantic probes/UI contracts; original EV Classic/Basilisk should remain capture/input based unless a real emulator/object-state bridge is built.
6. **RL/evolutionary exploration stays gated.** Wuji/Stable-Retro-style mutation-heavy exploration needs a bounded mutable surface, restoreable states, metric, run budget, and keep/revert rule. Until those exist, use read-only scouting and deterministic Godot scenario probes.
7. **Lane ownership still wins.** Gameplay agents may generate candidate macros, traces, bug reports, or code/data changes inside assigned worktrees. Repo mutation funnels through lane ownership and the integration owner: workers may write only their claimed surfaces, and fan-in requires manifest-backed merge/review/verification.
8. **Source labels must travel with automation output.** Every automatic gameplay finding should say whether it is `terminal-velocity-observed`, `automation-design`, `original-runtime-observed`, `decoded-resource`, `manual-backed`, or `external-adaptation-observed`.

### Automatic-gameplay manifest additions

For any gameplay-agent or automated-play slice, add these fields to the coordination manifest:

- Automation lane: `semantic-godot-probe`, `screen-capture-ui`, `emulator-state-wrapper`, `read-only-source-scout`, or `mutation-gated-experiment`.
- Objective/curriculum item:
- Starting state and restore method:
- Action/macro source: human demo, generated macro, existing regression, or source-derived scenario.
- Observation schema: JSON event, screenshot/vision packet, OCR text, trace log, or mixed.
- Success predicate / metric:
- Failure packet path:
- Skill/macro promotion rule:
- Exploration budget and stop condition:
- Keep/revert rule for any generated code/data:

## First safe step

Run an **accelerated lane-contract audit** before starting the next worker burst.

Scope:

- Inspect the live fidelity backlog and current continuation ledger.
- Select 3-5 candidate build-track lanes that can proceed in isolated worktrees.
- For each lane, fill in owner/card, writable surfaces, verifier, source-label policy, merge contract, and gate.
- Assign Basilisk work to the **4 emulator lanes** only with disk/prefs/window/input/capture/restore records.
- Keep one integration owner for final fan-in, verification, commit, and normal non-force push.
- Do not mutate a file/resource surface already owned by another active worker.

Why this first:

- It turns acceleration into executable lane contracts instead of vague “more workers.”
- It uses parallel writers where ownership is clear.
- It preserves fidelity gates without blocking scaffolded build-track progress.
- It gives another LLM or worker enough structure to review, continue, or reject the topology.

## Relationship to existing process artifacts

- Extends `docs/research/source-aligned-game-development-method.md`, especially its split between build-track scaffolds and fidelity-track promotion.
- Paired acceleration synthesis: `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md` carries the current accelerated doctrine only; superseded compendium-doc versions are retained outside the repo at `/home/bh/workspaces/loki/terminal-velocity-doc-archives/2026-06-08-superseded-compendium-docs/`.
- Uses `docs/checklists/ev-classic-fidelity-implementation-backlog.md` as the execution surface, not this artifact.
- Summarized by `docs/research/terminal-velocity-development-compendium.md` as the canonical entry point.
