# Terminal Velocity acceleration plan

Date: 2026-06-07
Source: Loki Game Telegram assistant post at 2026-06-07 09:20:26 EDT, message stored in profile session `20260607_084853_b72a9a`, message id `42847`.

Purpose: preserve the long acceleration/process recommendation as a durable Terminal Velocity process artifact so it is not lost in chat. This is a process artifact, not an EV Classic behavior source.

Canonical summary: this page is part of the Terminal Velocity development compendium. Read `docs/research/terminal-velocity-development-compendium.md` first for current doctrine; keep this page as the acceleration synthesis and deficiency/improvement rationale.

## Decision

The strongest acceleration plan is now **parallel executable lanes + fast evaluators + batched integration + fidelity gates**, with aggressive try-first/test-after acceleration rather than conservative waiting.

Non-blocking acceleration rule: the lane-contract audit, Kanban, extra worktrees, and Basilisk lane records are setup steps for worker bursts and parallel original-runtime evidence, not prerequisites for every improvement. A single safe-local acceleration slice should proceed immediately with source/fidelity labels and a cheap verifier.

Current implementation packet: `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md` converts this plan into live lane contracts, resource claims, Basilisk records, and worktree activation commands for the next burst.

Current automatic-gameplay worker application: `docs/research/2026-06-08-automatic-gameplay-worker-application.md` deepens the external automation/game-testing source stack and applies it to worker lane types, failure packets, and Lane E semantic-Godot vs capture-driven-Basilisk splitting. The first combined Lane A/E safe evaluator packet is `static_topology_source_readiness_scout`, which confirms static topology source readiness without importing the full galaxy: 67 decoded `syst-like` records, 88-byte record size, 9 heuristic system-name seeds, 72 landing-name seeds, and an unchanged 10-system runtime subset.

This artifact carries only the current acceleration doctrine. Superseded compendium-doc versions are retained outside the repo at `/home/bh/workspaces/loki/terminal-velocity-doc-archives/2026-06-08-superseded-compendium-docs/`.

Operationally:

1. keep one integration owner for fan-in, final verification, commit, and normal non-force push;
2. run 3-5 mutating worker lanes in isolated worktrees once lane contracts exist, while continuing single safe-local slices without waiting for the burst setup;
3. give each lane an owner, writable surface, verifier, source/fidelity label policy, merge contract, and rollback path;
4. use deterministic TV scenario/evaluator coverage as the velocity lane;
5. use the **4 Basilisk emulator lanes** for bounded original-runtime evidence, with lane records for disk/prefs/window/input/capture/restore state when Basilisk evidence is the lane; Basilisk K speeds EV by at least **2x**, so original-runtime evidence lanes should start there, try speeds significantly higher when the lane has restore/capture/input checks and the run is not breaking, and test afterward rather than holding back preemptively;
6. let build-track scaffolds proceed with explicit labels when original-runtime evidence is missing;
7. run static/source-mined **semantic-promotion and integration** lanes in parallel for map topology, planets/systems, stations, landing services, commodities, ships, outfits, weapons, descriptions/text resources, and decoded mission/resource data; these lanes are source/data limited, not Basilisk-speed limited. Primitive/resource inventory is already learned for many of these surfaces; the remaining work is field-family semantics, cross-links, runtime-facing import, and tests. Current promoted semantic manifests cover system ID/name-seed readiness, candidate hyperspace-link field-family readiness, service-matrix scaffold/source seeds, government, mission, weapon, and specialized `jünk` commodity records;
8. use Basilisk aggressively for behavioral confirmation, ambiguity resolution, UI/state-transition checks, and timing/feel exploration; slow down only after capture/input drift, contradictory evidence, failed post-run checks, or canonical promotion proves slower/1x evidence is required;
9. reserve strict source gates for fidelity promotion, exact claims, constants, and Classic quirk/intentional-divergence decisions, not for permission to try faster safe-local routes;
10. integrate in coherent batches rather than one tiny serial slice at a time.

Reasonable planning target: **6-10 months to meaningfully playable TV** under this accelerated topology.

## First safe step

The first **accelerated lane-contract audit** is now implemented in `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md`. Refresh its live-state preflight before starting a later worker burst. Do not use this audit as a reason to stop ordinary single-writer acceleration work.

Audit each candidate lane for:

- track: `build`, `fidelity-gate`, or `mixed`;
- owner/card;
- source/evidence label policy;
- concrete next action;
- verifier or scenario/evaluator;
- expected touched files/resources;
- worktree/branch;
- merge contract;
- rollback/cleanup path;
- gates/blockers.

Then start a bounded batch when the goal is a worker burst:

- 1 integration owner;
- start from the implemented lanes in `2026-06-08-terminal-velocity-topology-implementation-manifest.md`: static galaxy topology, service/store provisioning, economy/commodity semantics, mission-family semantics, and evaluator/playtest packets;
- 3 initial mutating worker lanes, selected from that packet or a refreshed equivalent;
- 1 static/source-mined fidelity lane for map/planet/station/commerce/ship/outfit/resource data; current promoted semantic manifests cover system ID/name-seed readiness, candidate hyperspace-link field-family readiness, service-matrix scaffold/source seeds, government, mission, weapon, and specialized `jünk` commodity records;
- 1 read-only reviewer/scenario scout if useful;
- 4 Basilisk emulator lanes available for evidence tasks with lane records.

Scale to 5 mutating workers only after clean integration flow is proven.

## Relationship to existing process artifacts

- Extends `docs/research/terminal-velocity-coordination-topology.md` with lane-contract parallelism and one integration owner.
- Implemented by `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md` for the current safe next-burst packet.
- Reinforces `docs/research/source-aligned-game-development-method.md`, especially build-track scaffolds versus fidelity-track promotion.
- Uses `docs/checklists/ev-classic-fidelity-implementation-backlog.md` as the execution surface for lane contracts and fidelity gates.
- Aligns with `docs/research/terminal-velocity-development-compendium.md`, the canonical short doctrine.
- Keeps `docs/research/2026-05-20-basilisk-freeze-input-debug.md` relevant for per-lane Basilisk recovery, while recognizing the fixed 4-emulator topology.
