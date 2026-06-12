# Living backlog governance mechanization proposal

Date: 2026-06-12
Status: implemented / protected by repo-local checks
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

Important implementation boundary: this is a mechanization/refactor of existing backlog infrastructure, not a greenfield checker suite. Prefer extending `tools/backlog_dispatch_index.py` and the existing checked-in JSON maps before adding parallel tools. Add a new tool only when the existing checker would become unclear or overloaded.

## Proposed mechanical surfaces

### 1. Backlog contract checker

Primary surface: extend `tools/backlog_dispatch_index.py check`.

Candidate split-out tool only if needed: `tools/check_ev_fidelity_backlog.py`

Checks:

- the canonical backlog has a role/use contract;
- status vocabulary is declared;
- item requirements are declared;
- selection rule exists;
- compaction / anti-staleness rule exists.

Current state: the canonical backlog already declares a live execution purpose, use contract, anti-staleness rule, generated dispatch index, playable priority overlay, and status vocabulary. The checker should protect that contract from regression rather than perform an initial repair.

Primary failure prevented: the live-backlog contract regresses into chat-, prompt-, or memory-only state.

### 2. Active item schema checker

Primary surface: extend `tools/backlog_dispatch_index.py` parsing/validation.

Candidate split-out parser module only if the parser needs to be reused by multiple commands.

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

Implementation boundary: conform active/open items incrementally. Do not rewrite completed or historical entries for schema purity unless they block dispatch or create current ambiguity.

### 3. Generated dispatch index freshness

Existing tool: `tools/backlog_dispatch_index.py`

Existing artifact: `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`

Rules:

- markdown backlog remains canonical;
- generated JSON/index says `do not edit by hand`;
- checker regenerates in memory and fails if the checked-in index is stale;
- index includes enough dispatch fields for runners:
  - `id`, `title`, `status`, `next_action`, `lane_class`, `oracle_class`, `source_basis`, `verifier`, `blocked_reason`, `promotion_status`, `risk_gate`, `touched_surfaces`, `markdown_anchor` or `line_range`, and an item-body hash.

Primary failure prevented: long-running runners repeatedly parse a huge markdown file or select stale/incomplete items.

Implementation boundary: keep the markdown backlog canonical and keep the existing index path stable unless there is a concrete migration reason.

### 4. Verifier impact map validation

Existing artifact: `docs/checklists/tv-verifier-impact-map.json`

Primary surface: extend `tools/backlog_dispatch_index.py check` to validate the map against active dispatch items.

Checks:

- every known `touched_surfaces` key used by active dispatch items resolves to a map entry;
- every entry has a cheap verifier family;
- checkpoint/broader verifier is present where required by risk or checkpoint policy;
- actionable items with touched surfaces have non-empty verifier hints.

Primary failure prevented: verifier selection is scattered in prompts or chosen by agent taste instead of by touched surface and risk.

### 5. Playable milestone priority map validation

Existing artifact: `docs/checklists/tv-playable-milestone-priority-map.json`

Primary surface: extend `tools/backlog_dispatch_index.py check` to validate the map against the generated dispatch index and canonical promotion metadata.

Checks:

- expected milestone IDs, order, and ranks are valid;
- `current_path` values are controlled vocabulary, such as `scaffold`, `needs evidence`, or `fidelity-promoted`;
- every referenced backlog item exists in the generated index or canonical backlog;
- every milestone has verifier hints;
- `fidelity-promoted` is rejected unless at least one referenced canonical backlog item has a supported promoted status.

Primary failure prevented: autonomous runners choose easy isolated static/resource fragments instead of the highest-ranked player-visible progress lane.

### 6. Pre-worker executability report

Implementation state: implemented as `python3 tools/backlog_dispatch_index.py audit-workers`.

Candidate command: `python3 tools/backlog_dispatch_index.py audit-workers`

Alternative only if the command becomes too broad: `python3 tools/check_ev_fidelity_backlog.py --audit-workers`

Read-only report should include:

- current branch/status summary;
- active dirty files relevant to TV workers;
- active Kanban/runners when available;
- active backlog items missing required fields;
- items safe for read-only scouting;
- items unsafe for mutation because gates, touched surfaces, or verifier contracts are incomplete.

Primary failure prevented: adding mutating workers while the shared checkout is dirty or while candidate work lacks gates and file ownership.

### 7. Runner preflight gate

Implementation state: implemented as `python3 tools/backlog_dispatch_index.py runner-preflight` and called by `tools/tv_runner_autostart.py` before dispatching or seeding continuation work. When no selected item ID is available yet, `runner-preflight` validates global backlog/index/map readiness without treating an arbitrary first backlog item as the selected item; selected-item gate checks apply when `--selected-item-id` is provided.

Candidate command: `python3 tools/backlog_dispatch_index.py runner-preflight`

Alternative only if runner state checks need a clearer separate boundary: `python3 tools/check_tv_runner_preflight.py`

Before dispatching or continuing an autonomous TV runner, require:

- clean checkout or explicitly owned dirty surfaces;
- fresh dispatch index;
- valid verifier impact map;
- valid playable priority map;
- selected item has `next_action`, `verifier`, `risk_gate`, and `touched_surfaces`;
- selected item's verifier map entry exists;
- selected item is compatible with current gate/dirty-state policy.

Primary failure prevented: prompt says the right thing but a worker ignores or forgets it.

This is the highest-value integration point. Static validation is useful only if runner selection and autonomous dispatch actually fail closed on it.

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

1. Extend `tools/backlog_dispatch_index.py check` with contract-regression and active-item field validation.
2. Add RED tests with small fixture backlogs/maps for missing live-backlog contract, missing active dispatch fields, stale generated index, unknown `touched_surfaces`, and invalid playable priority metadata.
3. Strengthen validation of existing `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json` rather than creating a second generated index path.
4. Strengthen validation of existing `docs/checklists/tv-verifier-impact-map.json`.
5. Strengthen validation of existing `docs/checklists/tv-playable-milestone-priority-map.json`.
6. Wire TV runner/autostart prompt/spec to call the checker before selecting work, or add a small runner-preflight command that composes the existing checks.
7. Shrink `living-backlog-governance` text to the judgment/policy wrapper and link this artifact plus the checker commands.

Implementation note: steps 1–7 are implemented in the repo-local checker/preflight/audit paths and the profile-local skill has been shrunk/cross-linked.

## Acceptance checks

A mechanized fix is done when:

- `tools/backlog_dispatch_index.py check` or its test fixture equivalent fails on at least one fixture missing the live-backlog contract;
- `tools/backlog_dispatch_index.py check` or its test fixture equivalent fails on at least one active item missing dispatch fields;
- a stale generated index is detected using the existing checked-in index path;
- an unknown `touched_surfaces` value is rejected against the existing verifier impact map;
- an invalid playable priority map is rejected against the existing playable priority map path;
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
- Refactors and extends `tools/backlog_dispatch_index.py`; do not add duplicate backlog/index checker commands unless the existing command boundary becomes unclear.
- Extends the existing generated index and maps: `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`, `docs/checklists/tv-verifier-impact-map.json`, and `docs/checklists/tv-playable-milestone-priority-map.json`.
- Complements `docs/research/terminal-velocity-coordination-topology.md` by making parts of its coordination advice enforceable before worker dispatch.
- Complements `docs/research/tv-spec.md` by protecting source/fidelity execution from prompt-only runner drift.
- Cross-linked from the profile-local `living-backlog-governance` skill; the repo-local mechanical surfaces are the authority for deterministic validation.
