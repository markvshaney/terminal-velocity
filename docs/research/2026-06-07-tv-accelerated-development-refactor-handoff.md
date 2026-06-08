# Terminal Velocity accelerated development refactor handoff

Date: 2026-06-07

Purpose: review handoff for another LLM after refactoring Terminal Velocity process docs away from the overly conservative serial-development model.

## Review objective

Confirm that the process docs now consistently express:

- **parallel executable lanes + fast evaluators + batched integration + fidelity gates**;
- one **integration owner** instead of one global writer;
- multiple mutating workers in isolated worktrees when lane contracts exist;
- static/source-mined fidelity lanes for map, planet, station, commerce, ship, outfit, text, and decoded resource data that are source/data limited rather than Basilisk-speed limited;
- Basilisk as a behavioral confirmation, ambiguity-resolution, UI/state-transition, and timing/feel oracle rather than the universal fidelity bottleneck;
- strict source discipline only at fidelity-promotion/canonical-claim boundaries;
- build-track scaffolds can proceed with explicit labels while evidence remains pending;
- the local runtime setup has exactly **4 Basilisk emulator lanes**, not “up to 4.”

## Docs to review

1. Canonical compendium  
   Path: `docs/research/terminal-velocity-development-compendium.md`  
   Review focus: short doctrine, Definition of Done split, worker rules, WIP limits, Basilisk lane policy, acceleration metrics.

2. Gameplay/source method doc  
   Path: `docs/research/source-aligned-game-development-method.md`  
   Review focus: source hierarchy preserved; build track vs fidelity promotion; vertical increments as quality unit, not serial throttle.

3. Topology doc  
   Path: `docs/research/terminal-velocity-coordination-topology.md`  
   Review focus: lane-contract topology, worktree rules, 4 Basilisk lane records, manifest template, first safe step.

4. Acceleration doc  
   Path: `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md`  
   Review focus: new Decision supersedes preserved conservative source post; 6-10 month playable-TV target; bounded worker batch recommendation.

5. Static source fidelity learning pass 1  
   Path: `docs/research/2026-06-07-static-source-fidelity-learning-pass-1.md`  
   Review focus: first completed static/source-mined learning pass; verified local EV Data/Graphics/Sounds source assets and hashes; separates learned static facts from remaining semantic promotion work.

## Important historical context

The acceleration doc intentionally preserves the original Telegram post under `## Source post preserved`; the topology doc also preserves its older source post. Those quote blocks still contain conservative language such as serial implementer/read-only scouts. Treat preserved quote blocks as historical source context, not current doctrine. The current doctrine is the rewritten `## Decision` sections plus the compendium.

## Review questions

- Is any remaining non-quoted text still implying one global serial writer as the default?
- Is any non-quoted text still saying Basilisk capacity is “up to 4,” “probably 4,” or “1 unless isolation is proven”?
- Do the docs clearly separate build-track scaffolding from fidelity-track promotion?
- Do the docs clearly say static/source-mined fidelity is source/data limited, not emulator-speed limited?
- Do the docs avoid treating Basilisk as the universal fidelity bottleneck?
- Are lane contracts concrete enough for another worker to execute without handwaving?
- Are the safety gates still explicit for public/external/destructive/history-rewrite/credential/config actions?

## Current known caveat

This handoff covers a process-doc refactor plus static/source-mined learning pass 1. It does not create Kanban cards, spawn workers, change cron jobs, change `.wslconfig`, verify actual Basilisk lane isolation, or semantically promote the remaining static records into new runtime data. Those are follow-on actions after review.
