# Living backlog governance mechanization proposal

Date: 2026-06-12
Status: proposal / not yet implemented
Scope: Terminal Velocity backlog governance and the profile-local `living-backlog-governance` skill.

Purpose: preserve the proposal to move enforceable backlog/runner rules out of prose-only skill guidance and into repo-local mechanical checks, while keeping the skill as the judgment layer for cases that require source/fidelity interpretation or coordination decisions.

This is a process artifact, not an EV Classic behavior source.

## Source context

- Skill under review: `/home/bh/.hermes/profiles/loki-game/skills/software-development/living-backlog-governance/SKILL.md`.
- Skill origin: created after the EV Classic fidelity backlog's live-execution role was too implicit; the durable rule became: a backlog that drives execution must say so inside the backlog itself.
- Current skill risk: it now mixes three layers:
  1. core backlog contract and anti-staleness guidance;
  2. worker-readiness / executability audit guidance;
  3. runner/index/validator policy for generated dispatch, verifier maps, and playable priority overlays.
- User question that triggered this artifact: whether portions can be made mechanical instead of incorporated into a skill.

## Decision recommendation

Do not keep adding prose to `living-backlog-governance` for rules that can be checked deterministically.

Make the skill a compact policy wrapper and move enforceable TV rules into repo-local tools plus machine-readable artifacts. Future runners should fail fast on checker output rather than relying on an agent to remember prose from the skill.

## Proposed mechanical surfaces

### 1. Backlog contract checker

Candidate tool: `tools/check_ev_fidelity_backlog.py`

Checks:

- the canonical backlog has a role/use contract;
- status vocabulary is declared;
- item requirements are declared;
- selection rule exists;
- compaction / anti-staleness rule exists.

Primary failure prevented: the live-backlog contract exists only in chat, prompts, or memory.

### 2. Active item schema checker

Candidate tool: extend `tools/check_ev_fidelity_backlog.py` or add a focused parser module used by it.

For each active/open backlog item, require explicit fields or project-equivalent values:

- `status`;
- `source_basis` / evidence;
- `next_action`;
- `verifier`;
- `blocked_reason` or explicit `none`;
- `risk_gate`;
- `touched_surfaces`;
- `promotion_status`.

Primary failure prevented: broad `candidate` or `needs evidence` entries being treated as runnable implementation tasks.

### 3. Generated dispatch index freshness

Candidate tool: `tools/build_ev_fidelity_backlog_index.py`

Candidate artifact: `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`

Rules:

- markdown backlog remains canonical;
- generated JSON/index says `do not edit by hand`;
- checker regenerates in memory and fails if the checked-in index is stale;
- index includes enough dispatch fields for runners:
  - `id`, `title`, `status`, `next_action`, `lane_class`, `oracle_class`, `source_basis`, `verifier`, `blocked_reason`, `promotion_status`, `risk_gate`, `touched_surfaces`, `markdown_anchor` or `line_range`, and an item-body hash.

Primary failure prevented: long-running runners repeatedly parse a huge markdown file or select stale/incomplete items.

### 4. Verifier impact map validation

Candidate artifact: `docs/checklists/tv-verifier-impact-map.json`

Checks:

- every known `touched_surfaces` key used by active dispatch items resolves to a map entry;
- every entry has a cheap verifier family;
- checkpoint/broader verifier is present where required by risk or checkpoint policy;
- actionable items with touched surfaces have non-empty verifier hints.

Primary failure prevented: verifier selection is scattered in prompts or chosen by agent taste instead of by touched surface and risk.

### 5. Playable milestone priority map validation

Candidate artifact: `docs/checklists/tv-playable-milestone-priority-map.json`

Checks:

- expected milestone IDs, order, and ranks are valid;
- `current_path` values are controlled vocabulary, such as `scaffold`, `needs evidence`, or `fidelity-promoted`;
- every referenced backlog item exists in the generated index or canonical backlog;
- every milestone has verifier hints;
- `fidelity-promoted` is rejected unless at least one referenced canonical backlog item has a supported promoted status.

Primary failure prevented: autonomous runners choose easy isolated static/resource fragments instead of the highest-ranked player-visible progress lane.

### 6. Pre-worker executability report

Candidate command: `python3 tools/check_ev_fidelity_backlog.py --audit-workers`

Read-only report should include:

- current branch/status summary;
- active dirty files relevant to TV workers;
- active Kanban/runners when available;
- active backlog items missing required fields;
- items safe for read-only scouting;
- items unsafe for mutation because gates, touched surfaces, or verifier contracts are incomplete.

Primary failure prevented: adding mutating workers while the shared checkout is dirty or while candidate work lacks gates and file ownership.

### 7. Runner preflight gate

Candidate command: `python3 tools/check_tv_runner_preflight.py`

Before dispatching or continuing an autonomous TV runner, require:

- clean checkout or explicitly owned dirty surfaces;
- fresh dispatch index;
- valid verifier impact map;
- valid playable priority map;
- selected item has `next_action`, `verifier`, `risk_gate`, and `touched_surfaces`;
- selected item's verifier map entry exists;
- selected item is compatible with current gate/dirty-state policy.

Primary failure prevented: prompt says the right thing but a worker ignores or forgets it.

## What should remain in the skill

Keep `living-backlog-governance` responsible for judgment that is not safely reducible to static checks:

- deciding whether a backlog/checklist is the correct durable surface;
- deciding when to compact history vs preserve it in a linked research/decision artifact;
- interpreting EV Classic source/fidelity boundaries;
- deciding whether a missing field blocks work or can be filled as scaffold/evidence-needed metadata;
- deciding whether worker parallelism is worth the coordination cost;
- handling dirty-state exceptions and human gates;
- updating the mechanical checker policy when a new failure pattern is discovered.

## Proposed implementation order

1. Add minimal parser/checker for the current backlog header contract and active item field presence.
2. Add RED tests with a small fixture backlog missing required fields.
3. Add generated dispatch index builder and stale-index check.
4. Add verifier impact map JSON and validation.
5. Add playable milestone priority map JSON and validation.
6. Wire TV runner/autostart prompt/spec to call the checker before selecting work.
7. Shrink `living-backlog-governance` text to the judgment/policy wrapper and link this artifact plus the checker commands.

## Acceptance checks

A mechanized fix is done when:

- a checker command fails on at least one fixture missing the live-backlog contract;
- a checker command fails on at least one active item missing dispatch fields;
- a stale generated index is detected;
- an unknown `touched_surfaces` value is rejected;
- an invalid playable priority map is rejected;
- the TV runner preflight uses these checks before selecting work;
- `living-backlog-governance` no longer needs to carry long mechanical rule lists inline, only links and judgment boundaries.

## Non-goals and gates

Non-goals:

- changing EV Classic fidelity behavior;
- adding new autonomous workers;
- mutating original EV/Basilisk state;
- broad artifact cleanup unrelated to this backlog governance fix.

Gates:

- profile/Hermes skill edits are profile-local and safe only inside the active `loki-game` profile unless the user explicitly asks for cross-profile changes;
- external/account/provider/gateway/supervision changes remain gated;
- normal TV repo code/docs changes can be implemented as safe-local slices with targeted tests and normal non-force push policy.

## Relationship to existing artifacts

- Complements `docs/checklists/ev-classic-fidelity-implementation-backlog.md` as the canonical backlog surface.
- Complements `docs/research/terminal-velocity-coordination-topology.md` by making parts of its coordination advice enforceable before worker dispatch.
- Complements `docs/research/tv-spec.md` by protecting source/fidelity execution from prompt-only runner drift.
- Should be cross-linked from the `living-backlog-governance` skill if/when implementation begins.
