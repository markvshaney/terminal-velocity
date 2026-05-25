# EV gameplay external-demo source survey and gameplay-autoresearch plan

Date: 2026-05-20

Purpose: reduce slow original-runtime discovery by using outside gameplay demos/guides as secondary learning sources, while preserving the project truth hierarchy: original EV Classic runtime observations and decoded resources remain primary; outside demos/guides are strategy hypotheses and comparison prompts unless later verified.

## Source hierarchy for this artifact

1. Original EV Classic runtime in local Basilisk II: primary source for Terminal Velocity fidelity.
2. Decoded EV Classic resources and original/manual documentation: primary/static source.
3. External gameplay demos, Let's Plays, community guides, and ports: secondary/tertiary learning sources for strategy, route planning, and questions to verify.
4. EV Nova/Override gameplay: transferable gameplay-pattern source only; not direct EV Classic fidelity proof.

## Sources found

### Effing Controller — Let's Play Escape Velocity playlist

- URL: `https://www.youtube.com/playlist?list=PL64Ji1ic63wF4RI58ywineBli7l5-g4r3`
- Type: 26-video YouTube Let's Play of original Escape Velocity.
- Source quality: secondary for strategy/play progression; not a primary fidelity source.
- Discovery evidence: YouTube playlist page exposed 26 video entries, including:
  - Episode 1: `https://www.youtube.com/watch?v=vxm2G0x5qxw`
  - Episode 2: `https://www.youtube.com/watch?v=cdDmL02ug-E`
  - Episode 3: `https://www.youtube.com/watch?v=q_oR1aL-xFE`
  - Episode 23: `https://www.youtube.com/watch?v=rOy-PRf5hfE`
  - Episode 26 finale: `https://www.youtube.com/watch?v=KKuNcGh_-70`
- Potential use:
  - Watch early episodes for starter route/mission/trade habits.
  - Watch mid/late episodes for ship upgrade ladder, combat risk, faction commitments, and finale conditions.
  - Extract route-choice and tactical patterns, then verify critical mechanics in local EV Classic before implementation.
- Caveat: captions were advertised in YouTube page metadata for some videos, but direct timedtext fetches returned empty in this environment. Use browser/manual viewing or a dedicated transcript tool if needed.

### BitChute / mirrored playlist — Let's Play Escape Velocity by Ambrosia Software

- URL: `https://www.youtube.com/playlist?list=PLH9XAe9eLGSj_fGBVB1rXIg5sy1Pt50cl`
- Type: 7-video Let's Play playlist found through YouTube search, with titles emphasizing early advancement and combat escalation.
- Source quality: secondary for strategy/play progression.
- Discovery evidence: playlist page exposed entries:
  - Episode 1: `A Brave New Universe` (`UUZXuGAH_io`)
  - Episode 2: `Exploration and Advancement` (`EpEX828AWpc`)
  - Episode 3: `Taking on my first Rebel Destroyer` (`uXpK1TllU-U`)
  - Episode 4: `Path to Power` (`gSOSf7Sep8s`)
  - Episode 5: `Building a Fleet` (`DV4aItGjVtg`)
  - Episode 6: `Becoming a Galactic Scourge` (`upEbpxvYg_8`)
  - Episode 7: `Becoming a Universal Terror` (`wcuJuue0DDM`)
- Potential use:
  - Learn progression arcs: exploration/advancement, first capital-ship combat, fleet building, and high-risk combat/piracy path.
- Caveat: likely less safe for the current reusable mission/trade pilot after episode 3 because it moves into combat/destructive play.

### CliveAtFive — Escape Velocity (Original), Let's Play Part 1

- URL: `https://www.youtube.com/watch?v=4VX6TZEfqf4`
- Type: YouTube Let's Play of original EV Classic.
- Source quality: secondary for strategy/play progression.
- Discovery evidence: YouTube oEmbed confirmed title `Escape Velocity (Original), Let's Play -- Part 1`, author `CliveAtFive`; search found additional parts such as Part 4 and Part 5.
- Potential use:
  - Alternative early-game demonstration source if Effing Controller pacing or route is not enough.

### EpicStuffForYou — Escape Velocity (Nova Port) gameplay, no commentary

- URL: `https://m.youtube.com/watch?v=gu7ywaTGp4c`
- Type: no-commentary gameplay of EV Classic content in Nova port.
- Source quality: external adaptation observed; hypothesis source only.
- Potential use:
  - UI/route/combat comparison prompts, not direct original-runtime behavior.
- Caveat: Nova port can differ from original EV Classic; never promote directly to fidelity implementation.

### GameFAQs — Escape Velocity (1996) FAQ by AKishan

- URL: `https://gamefaqs.gamespot.com/mac/575197-escape-velocity-1996/faqs/2600`
- Type: text FAQ/data guide for original EV Classic.
- Source quality: secondary/community guide.
- Search snippets relevant to strategy:
  - Player starts on neutral Levo piloting a small shuttlecraft.
  - Guide mentions cargo pod details and broad Confed/Rebel/Alien mission pathways.
- Potential use:
  - Route/mission/ship/outfit data questions to verify against runtime or decoded resources.
  - Searchable mission-name clues when local play reaches mission arcs.
- Caveat: direct page fetch returned HTTP 403 from this environment; use browser or cached/search snippets, and verify facts before promotion.

### Tea Leaves — Playable Classics: Escape Velocity

- URL: `http://tleaves.com/2005/06/27/playable-classics-escape-velocity/index.html`
- Type: retrospective with a short beginning-game walkthrough.
- Source quality: secondary interpretive source.
- Extracted strategy points:
  - Start with a small shuttlecraft with hyperdrive, cargo space, and a weak gun.
  - Early money comes from commodity trading, ferrying passengers, and timed cargo deliveries.
  - Heavily patrolled lanes are safer for merchant play; police may help against attackers.
  - Reputation and combat capability unlock more interesting bar/faction work.
  - Upgrades/ship progression are funded by early trade/mission loops.
- Potential use:
  - Confirms the current safe learning focus: mission/trade/navigation before piracy/destructive tests.

### Let's Play Archive — Escape Velocity: Nova

- URL: `https://lparchive.org/Escape-Velocity-Nova/`
- Type: long-form LP archive for EV Nova.
- Source quality: EV Nova only; transferable strategy framework, not EV Classic fidelity.
- Extracted strategy points:
  - Open-ended roles: fight, bribe, trade, pirate, conquer, courier, mine, explore.
  - Ship choice should reflect playstyle: trade ships for hauling, gunboats/capital ships for combat, not one universal optimal path.
  - Separate storyline paths can justify separate pilot profiles.
- Potential use:
  - Strategy taxonomy and tutorial/AI-hint design for Terminal Velocity.

## Immediate learning recommendations

1. Use Effing Controller episode 1–3 as the main outside demo sequence for near-term learning.
   - Reason: original EV, 26-episode complete run, starts from early game.
   - Extract: first accepted missions, first profitable trade/cargo choices, route selection, first upgrade target, first combat avoidance/fighting threshold.

2. Use Tea Leaves as the current concise strategy prior.
   - Early loop: combine commodity trading + passenger/cargo missions while staying on safer/patrolled lanes.
   - Treat combat as a later threshold once reputation/ship capability improves.

3. Use the 7-video `A Brave New Universe` playlist only after safe mission/trade basics.
   - Reason: titles indicate rapid escalation into combat/fleet/piracy; useful, but not for the reusable non-strict mission/trade pilot until a separate risk/combat pilot exists.

4. Use GameFAQs as a lookup index, not proof.
   - Search snippets and guide metadata are useful, but every specific mission/outfit/route claim needs local runtime or decoded-resource verification before implementation.

## Gameplay-autoresearch loop design

### Goal

Improve Loki's EV Classic play skill and Terminal Velocity strategy/fidelity notes by converting each gameplay/demo observation into a scored decision-policy update, while keeping destructive gameplay and live automation gated.

### Metric

Use a mixed local rubric, scored per short run or watched-demo segment:

- `objective_progress` (0–3): mission completed, route advanced, new port reached, or useful source-backed fact found.
- `risk_control` (0–3): avoided death/destructive changes, monitored shields/fuel, used non-strict/disposable pilots appropriately.
- `resource_efficiency` (0–2): credits/fuel/cargo improved or conserved; no avoidable stranded state.
- `observation_quality` (0–2): screenshot/source evidence captured, user-observed vs screenshot-confirmed separated, docs updated.

Total: 10 points. Keep policy updates only if they improve the rolling average or add a new verified tactic without reducing safety/observation quality.

### Mutable surface

Allowed local/documentary surfaces:

- `docs/research/original-ev-classic-runtime-observations.md`
- `docs/checklists/ev-classic-behavior-baseline-checklist.md`
- `docs/checklists/ev-classic-original-runtime-observation-checklist.md`
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- new local gameplay/autoresearch artifacts under `docs/research/` or `.hermes/artifacts/`
- local-only capture files under `C:\Games\BasiliskII\`

Do not mutate shared Hermes config, cron, gateway, memory, platform routing, or public/external surfaces without explicit approval.

### Trusted/read-only surfaces

- Original EV Classic runtime captures and current pilot state.
- Decoded EV Classic resources and original/manual documentation.
- External demo URLs listed above, labeled as secondary/adaptation where appropriate.
- User corrections and direct demonstrations, labeled separately from screenshot proof.

### Candidate loop

For each session segment:

1. Observe current state or external demo segment.
2. Extract one candidate tactic, e.g. `pair passenger mission with cargo route`, `refuel before multi-hop route`, `avoid combat in shuttle`, `wait until far from system center before jump`.
3. Before acting in EV Classic, check safety gate:
   - safe on reusable non-strict mission/trade pilot?
   - requires disposable combat/piracy pilot?
   - requires user manual takeover?
4. Run one bounded gameplay attempt or mark as external-demo-only hypothesis.
5. Score the result with the 10-point rubric.
6. Keep, discard, or defer the tactic:
   - `keep_verified`: original runtime or decoded source confirms it and score improves.
   - `keep_hypothesis`: external demo suggests it, but original verification pending.
   - `discard`: unsafe, false, low value, or contradicted.
   - `needs_disposable_pilot`: combat/piracy/destructive track.
7. Append result to a JSONL log.

### Suggested log path

`docs/research/ev-gameplay-autoresearch-results.jsonl`

Suggested JSONL fields:

```json
{
  "timestamp": "2026-05-20T00:00:00Z",
  "source": "original_runtime | user_demo | youtube | guide | nova_lp",
  "source_url_or_capture": "...",
  "tactic": "...",
  "status": "keep_verified | keep_hypothesis | discard | needs_disposable_pilot",
  "score": {"objective_progress": 0, "risk_control": 0, "resource_efficiency": 0, "observation_quality": 0, "total": 0},
  "evidence_notes": "...",
  "next_verification": "..."
}
```

### Approval gates

Need explicit approval before:

- creating recurring cron/background autoresearch jobs;
- letting Loki operate EV unattended for long periods;
- enabling Strict Play or intentionally death-testing;
- piracy/privateering/combat-risk testing on the reusable mission/trade pilot;
- changing Hermes config/gateway/supervision/provider/memory/routing;
- publishing or sending raw captures externally.

Local one-shot artifact/log creation and source search are safe and were performed in this pass.

## General autonomous game-learning sources added 2026-05-21

These sources are not EV Classic fidelity evidence. They are technique references for improving the gameplay-autoresearch loop above: curriculum design, replayable scenarios, demonstration capture, exploration archives, and skill-library learning.

### Recommended Terminal Velocity technique stack

Use a hybrid loop rather than pure reinforcement learning from pixels:

1. Build a source/manual + runtime-observation task taxonomy.
2. Create replayable scenarios with cheap verification.
3. Prompt/train through a skill curriculum: landing, trading, route planning, mission acceptance, hyperspace, combat.
4. Seed with human or scripted demonstrations where possible.
5. Use exploration methods for sparse-reward problems: hidden mission chains, route discovery, unlock conditions.
6. Use an LLM/controller layer over symbolic or OCR-derived game state before attempting raw motor learning.

### High-value source candidates

- **Voyager** — https://arxiv.org/abs/2305.16291 and https://github.com/MineDojo/Voyager
  - Technique: LLM agent with automatic curriculum, executable skill library, iterative prompting, and environment feedback.
  - Transferable lesson: store reusable gameplay procedures such as accept ferry mission, land safely, buy low/sell high, plot route, and escape hostile system.
- **General Video Game AI / GVGAI** — https://arxiv.org/abs/1802.10363 and https://gaigresearch.github.io/gvgaibook/
  - Technique: agents play unseen games through separated game descriptions, forward models, agent interfaces, and evaluators.
  - Transferable lesson: separate Terminal Velocity task manifests, observations, action interfaces, and evaluators.
- **Go-Explore** — https://arxiv.org/abs/1901.10995
  - Technique: archive interesting states/cells, return to promising cells, explore outward, then robustify.
  - Transferable lesson: archive reached systems, ports, mission surfaces, accepted mission states, completion states, and profitable routes.
- **MineRL** — https://arxiv.org/abs/1907.13440
  - Technique: large-scale Minecraft demonstrations paired with simulator action data.
  - Transferable lesson: collect action-labeled traces, not just screenshots, for landing, takeoff, map, jump, and mission-flow routines.
- **OpenAI Video PreTraining / VPT** — https://cdn.openai.com/vpt/Paper.pdf and https://github.com/openai/Video-Pre-Training
  - Technique: learn from human gameplay video, then fine-tune with RL.
  - Transferable lesson: recorded play can seed autonomous exploration, but local work should start with small action-labeled traces.
- **Procgen Benchmark** — https://arxiv.org/abs/1912.01588
  - Technique: procedurally generated game-like environments measuring sample efficiency and generalization.
  - Transferable lesson: do not evaluate agents on one fixed pilot/save/seed; use varied scenario starts and holdouts.
- **Agent57** — https://arxiv.org/abs/2003.13350
  - Technique: exploration/exploitation policy family and long-vs-short horizon control across Atari57.
  - Transferable lesson: robust play needs explicit exploration modes and long-horizon behavior, not just immediate score maximization.
- **Never Give Up** — https://arxiv.org/abs/2002.06038
  - Technique: episodic memory and intrinsic novelty rewards.
  - Transferable lesson: distinguish episode-local novelty from globally useful progress in map/system exploration.
- **Random Network Distillation** — https://arxiv.org/abs/1810.12894
  - Technique: intrinsic reward from prediction error against a random target network.
  - Transferable lesson: novelty rewards can guide sparse-reward exploration, but must be constrained to avoid irrelevant novelty loops.
- **Open-Ended Learning / XLand** — https://arxiv.org/abs/2107.12808
  - Technique: procedural universe of tasks and automatic curriculum.
  - Transferable lesson: generate a ladder of EV-like tasks: land, trade, refuel, route, avoid pirate, complete courier job, escape combat, recover from low fuel.
- **SIMA** — https://arxiv.org/pdf/2404.10179
  - Technique: instruction-following agent across many virtual 3D environments and commercial games.
  - Transferable lesson: language-conditioned goals plus a common action interface can generalize across games; adapt to 2D/top-down play with explicit state logs.
- **Awesome LLM Game Agent Papers** — https://github.com/git-disl/awesome-LLM-game-agent-papers
  - Type: secondary discovery index.
  - Use: find more LLM/game-agent sources, then verify against primary papers/repos.

### Immediate design implications

- Treat each gameplay lesson as a bounded eval, not an open-ended play session.
- Keep source labels distinct: `source-grounded`, `runtime-observed`, `demonstration-derived`, `hypothesis`, `needs EV Classic confirmation`.
- Prefer reversible local artifacts: logs, screenshots, save-state copies, action traces.
- Save reusable procedures as skills only after verified success across more than one scenario or after a tricky failure has been understood.
- Highest-value near-term adaptations: Voyager-style skill library, Go-Explore-style state archive, MineRL/VPT-style action-labeled traces, GVGAI-style scenario/evaluator separation, and Procgen-style varied scenario seeds.

## Recommended next safe action

Create the JSONL log and begin with two non-destructive entries:

1. `keep_verified`: user-demonstrated hyperspace to Kathoon; landed state screenshot-confirmed; exact input sequence pending.
2. `keep_hypothesis`: Tea Leaves early-game strategy: combine commodity trading, passenger/cargo missions, and safer patrolled lanes before combat.

Then watch or inspect Effing Controller Episode 1 for early route and first-upgrade strategy, preserving it as `keep_hypothesis` until local verification.

## Telegram checkpoint summary saved 2026-05-20

This section preserves the user-facing post so it can be referred to after chat/context compaction.

- Verdict: it is time to start learning EV Classic play skills, but first through a bounded safe workflow: external demo mining -> hypothesis log -> local original-runtime verification.
- Best near-term demo source: Effing Controller's 26-part *Let's Play Escape Velocity* playlist, `https://www.youtube.com/playlist?list=PL64Ji1ic63wF4RI58ywineBli7l5-g4r3`.
  - Use episodes 1-3 for early missions, route selection, first money loops, and first upgrade choices.
- Second original-EV demo source: 7-video *Let's Play Escape Velocity by Ambrosia Software* playlist, `https://www.youtube.com/playlist?list=PLH9XAe9eLGSj_fGBVB1rXIg5sy1Pt50cl`.
  - Keep for a separate combat/risk pilot because later titles escalate into destroyer combat, fleet building, and piracy/scourge play.
- Alternate original-EV source: CliveAtFive, *Escape Velocity (Original), Let's Play -- Part 1*, `https://www.youtube.com/watch?v=4VX6TZEfqf4`.
- Guide source: GameFAQs AKishan FAQ, `https://gamefaqs.gamespot.com/mac/575197-escape-velocity-1996/faqs/2600`.
  - Treat as secondary; direct fetch was blocked with HTTP 403 in the local environment; verify specifics locally.
- Concise strategy source: Tea Leaves, *Playable Classics: Escape Velocity*, `http://tleaves.com/2005/06/27/playable-classics-escape-velocity/index.html`.
  - Extracted early strategy: combine commodity trading, ferry/passenger/cargo missions, safer patrolled lanes, then upgrade before serious combat.
- Transferable but not fidelity-proof: LP Archive EV Nova and EV Nova port gameplay.
  - Useful for strategy taxonomy only; not original EV Classic proof.
- Artifacts created/updated:
  - `docs/research/ev-gameplay-external-demo-and-autoresearch-plan.md`
  - `docs/research/ev-gameplay-autoresearch-results.jsonl`
- JSONL initialization verified: two entries parsed successfully.
  1. `keep_verified_partial`: user-demonstrated hyperspace to Kathoon, with screenshot-confirmed landed state at Maxwell's Purchase.
  2. `keep_hypothesis`: Tea Leaves early-game strategy: safe mission/trade loops before combat.
- Autoresearch status:
  - local artifact and JSONL scoring log are set up;
  - no recurring cron/background loop has been created;
  - recurring automation requires explicit approval because it is durable runtime automation.
- Recommended next step: mine Effing Controller episodes 1-3 for early-game route/trade/mission tactics, record them as hypotheses, then verify locally in EV Classic without risking the reusable pilot.
