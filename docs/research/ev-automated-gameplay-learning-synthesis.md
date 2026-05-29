# EV-family automated gameplay learning synthesis

Date: 2026-05-24

Purpose: convert the already-searched EV Classic / Escape Velocity: Override / EV Nova gameplay sources into a concrete learning plan for automated or semi-automated Terminal Velocity gameplay. This is not exact EV Classic fidelity proof. It is a source-labeled strategy and automation design artifact.

Primary source artifacts used:

- `docs/research/ev-gameplay-external-demo-and-autoresearch-plan.md`
- `docs/research/ev-family-gameplay-source-deep-dive.md`
- `docs/research/2026-05-20-basilisk-freeze-input-debug.md`
- local extracted text under `/tmp/ev-source-deep-dive-20260521/text/`
  - `evn_walkthrough_index.txt`
  - `evn_federation.txt`
  - `evn_polaris.txt`
  - `evn_sidemissions.txt`
  - `evn_bible.txt`
- Tea Leaves, *Playable Classics: Escape Velocity*, fetched live on 2026-05-24 from `http://tleaves.com/2005/06/27/playable-classics-escape-velocity/index.html`.
- LP Archive, *Escape Velocity: Nova*, fetched live on 2026-05-24 from `https://lparchive.org/Escape-Velocity-Nova/`.
- `docs/research/automated-gameplay-learning-reference-sources.md`
  - Voyager / MineDojo (`arXiv:2305.16291`): `https://arxiv.org/abs/2305.16291`, `https://voyager.minedojo.org/`
  - Go-Explore (`arXiv:1901.10995`): `https://arxiv.org/abs/1901.10995`
  - GVGAI (`arXiv:1802.10363`): `https://arxiv.org/abs/1802.10363`
  - Google Research, *Quickly Training Game-Playing Agents with Machine Learning*: `https://research.google/blog/quickly-training-game-playing-agents-with-machine-learning/`
  - OpenAI VPT paper: `https://cdn.openai.com/vpt/Paper.pdf`
  - BrowserGym: `https://github.com/ServiceNow/BrowserGym`
  - WebArena (`arXiv:2307.13854`): `https://arxiv.org/abs/2307.13854`, `https://webarena.dev/`
  - OSWorld (`arXiv:2404.07972`): `https://arxiv.org/abs/2404.07972`, `https://os-world.github.io/`

Source labels:

- `runtime-observed`: local EV Classic/Basilisk evidence.
- `community-guide`: player-authored or retrospective guide evidence.
- `source-grounded EV-family`: EV Nova data-derived walkthrough/Bible evidence; transferable structure, not exact Classic proof.
- `demo-hypothesis`: YouTube/LP examples identified but not yet transcript-mined.
- `automation-design`: inference for Terminal Velocity agent/eval design based on the above.
- `automation-design reference`: general game-agent/autonomous-task research source used for automation architecture only; not EV Classic behavior evidence.

## Executive learning model

The strongest path is not raw pixel-RL. Use a symbolic/LLM-controller gameplay loop:

1. Observe structured game state: location, landed/in-space/modal, credits, cargo/free tons, fuel, active missions, deadlines, known route graph, legal/faction status, ship/outfit state, hazards, current UI surface.
2. Choose a bounded player tactic from a skill library.
3. Execute through a small action API: click/keypress/UI command, or Godot-native scripted action in Terminal Velocity.
4. Verify with cheap checks: mission state changed, credits/cargo/fuel changed, location changed, ship survived, deadline still viable, no destructive/legal gate crossed.
5. Score the attempt and either keep, revise, or discard the tactic.

This matches the earlier external game-agent technique stack: Voyager-style skill library, GVGAI-style scenario/evaluator separation, Go-Explore-style state archive, MineRL/VPT-style action-labeled traces, and Procgen-style varied scenario seeds.

## Specific EV gameplay examples already found

### 1. EV Classic early merchant loop

Source: `community-guide`, Tea Leaves live fetch.

Observed source content:

- The player begins with little money and a shuttlecraft.
- The shuttle has hyperdrive, cargo space, and a weak gun.
- Early money comes from commodity trading, ferrying passengers, and timed cargo deliveries.
- Heavily patrolled lanes are safer for merchant play; local police may rescue a weak player from attackers.
- After building a reputation by defending yourself, bar contacts offer more interesting faction work.
- EV Classic, EV Override, and EV Nova are described as having nearly identical mechanics but different stories.

Automation implications:

- First autonomous curriculum should be merchant/survival, not combat.
- Initial skills:
  - `read_landed_services`
  - `inspect_mission_computer`
  - `accept_safe_passenger_or_cargo_job`
  - `buy_commodity_with_spare_capacity`
  - `plot_patrolled_or_known_safe_route`
  - `jump_and_refuel`
  - `land_and_complete_delivery`
  - `avoid_or_wait_out_pirates`
- Evaluation should reward survival, completed delivery, retained cargo/fuel margin, and evidence quality more than raw credits.

### 2. User-demonstrated EV Classic hyperspace progress to Kathoon

Source: `runtime-observed` / user-demo plus screenshot-confirmed landed state recorded in `ev-gameplay-autoresearch-results.jsonl`.

Observed/source-backed facts:

- User demonstrated successful route progress to Kathoon.
- Screenshot confirmed a landed state at Maxwell's Purchase with `Refuel Ship`, `Commodity Exchange`, `Spaceport Bar`, `Mission Computer`, and `Leave`.
- Exact step-by-step route-selection/jump input sequence remains uncaptured.

Automation implications:

- Treat `reach_known_neighbor_and_land` as verified partially but incomplete.
- Build a trace recorder before more live play: log every key/click, pre/post capture path, modal state, HUD text, and interpreted command.
- A valid travel skill is not only `press J`; it is:
  1. confirm in-space state;
  2. choose hyperspace destination;
  3. move far enough from the system center/planet;
  4. retry jump after movement if the distance gate blocks;
  5. wait for transition;
  6. land/refuel at destination.

### 3. EV Nova mission state examples: Federation chain

Source: `source-grounded EV-family`, local `evn_federation.txt` extracted from data-derived EVN walkthroughs.

Concrete examples found:

- First Federation example appears from random Federation stellar objects, at `Outfitter`, with `Random: 50%`, `Legal Record: 2`, `Combat Rating: 150`, `Cargo: 20 tons`, and `Pay Value: 30,000`.
- Follow-up examples use fixed locations such as Spacedock III / Earth / Spacedock II, `Random: 100%` or other percentages, `Cargo: 20 tons`, `Pay Value: 30,000`, and mission-bit transitions such as `OnSuccess: b51`, `OnSuccess: b52`, etc.

Automation implications:

- Mission agents need blocked-reason awareness. A shuttle with only 20 free tons cannot take a 20-ton mission if it is already carrying trade goods/passengers.
- Mission acceptance policy must reserve cargo before buying commodities.
- Mission availability should be refreshed by system entry and evaluated against legal record, combat rating, cargo, ship type, location surface, random chance, and bit state.
- `Outfitter` can be a mission surface, so an automated player must inspect more than Mission Computer/Bar.

### 4. EV Nova mission state examples: Polaris chain

Source: `source-grounded EV-family`, local `evn_polaris.txt`.

Concrete examples found:

- Early Polaris examples appear in the `Bar`, often with `Cargo: 1 ton`, `Pay Value: 20000`, and route-style returns such as New Ireland, Earth, Goliath, or Port Kane.
- One opening branch requires `Combat Rating: 200`; another branch has `Combat Rating: 0` when a control bit is already set.
- Mission bits and faction/story branch state strongly govern availability.

Automation implications:

- Separate `story_chain_state` from generic mission board state.
- Automated play should keep separate pilots/profiles for separate major storylines and faction commitments.
- A beginner policy should not chase combat-rating-gated openings until the ship, weapons, and legal/faction risks are suitable.

### 5. EV Nova side mission examples

Source: `source-grounded EV-family`, local `evn_sidemissions.txt`.

Concrete examples found:

- Side missions can start from random Federation stellar objects in the `Bar` with low random availability such as `25%` or `5%`.
- Follow-up missions can move to `Main Spaceport` with `Random: 100%`.
- Cargo requirements in sampled examples include `2 tons` and `15 tons`, with pay values such as `75,000` and `50,000`.

Automation implications:

- Rechecking ports after travel is a gameplay mechanic, not noise.
- Low-random bar missions require an exploration/archive strategy: record where a lead was seen, what bit/state it likely set, and what follow-up surface changed.
- The agent should not overfit to one board scan; it needs a state archive of visited systems/ports/surfaces and observed offers.

### 6. Mission special-ship goals

Source: `source-grounded EV-family`, `evn_walkthrough_index.txt` lines describing mission `Ship Goal`.

Relevant goal types:

- Destroy all target ships.
- Disable without destroying.
- Board disabled ships.
- Escort and keep ships intact.
- Observe ships/system presence.
- Rescue disabled ships.
- Chase off targets by destruction or forcing them to flee.

Automation implications:

- Mission execution should branch by objective class:
  - delivery/courier: route and land;
  - cargo/passenger: route, preserve reserved cargo, land by deadline;
  - escort: path planning plus ally survival checks;
  - disable/board/rescue: precision combat, boarding action, and non-destruction constraint;
  - observe: enter/approach target system, possibly visual range;
  - chase-off/destroy: combat-capable pilot only.
- Combat mission tests belong on disposable non-strict pilots until survival and save safety are understood.

### 7. Mission cargo, illegal cargo, deadlines, and pay semantics

Source: `source-grounded EV-family`, `evn_walkthrough_index.txt` and `evn_bible.txt`.

Relevant mechanics found:

- Cargo requirement uses the pilot ship's free space, not escorts.
- Time limit is measured in days; exceeding it fails the mission.
- Mission cargo can be picked up at start, at travel destination, or by boarding a special ship.
- Cargo can be dropped at travel destination or at mission end.
- Mission cargo can be illegal for governments whose scan masks match.
- Pay can be credits, legal-record cleanup, cash loss, or other non-credit effects.

Automation implications:

- State needs `reserved_cargo`, `mission_cargo_type`, `mission_cargo_qty`, `deadline_date`, `illegal_cargo_by_govt`, and `non_credit_reward` fields.
- Before accepting a mission, evaluate route duration, fuel, cargo free space, scan/legal risk, and whether trade cargo should be sold first.
- Trade agent must not spend cargo space needed for accepted missions.

### 8. Map arrows, fuel, and route constraints

Source: `source-grounded EV-family`, `evn_bible.txt`; plus `runtime-observed` EV Classic distance-gate confusion.

Relevant mechanics found:

- EVN Bible lists `Jump Distance 1000 pixels`.
- Interface fields include full-jump and partial-fuel display concepts.
- Mission flags can show a green map arrow in the initial briefing and a separate arrow for special ship systems.
- Some missions can auto-abort with fuel penalties and be unavailable if the player has less than 100 fuel.

Automation implications:

- Route planning must be fuel-aware and state-aware.
- Mission arrows are an automation affordance: use them as objective hints in Terminal Velocity, and log whether they correspond to travel, return, or special-ship target.
- `jump_to_destination` must handle failure feedback: too close to system center, no fuel, no destination selected, modal open, or input not delivered.

### 9. Government, bribes, police, and faction relations

Source: `source-grounded EV-family`, `evn_bible.txt`; `community-guide`, Tea Leaves.

Relevant mechanics found:

- Governments are collections of ships and planets reacting collectively to the player and other ships.
- Governments track their feeling toward the player and have enemies/allies.
- Government flags include warship/freighter/planet bribe behavior, larger bribe demands, inability to hail, plundering before destruction, and other AI behaviors.
- Tea Leaves emphasizes political systems/law enforcement and police assistance on heavily patrolled lanes.

Automation implications:

- Navigation policy needs `system_government`, `player_legal_record_by_government`, `enemy/allied_govts`, `patrol_density`, and `bribe_possible` concepts.
- Safe beginner route policy should prefer known lawful/patrolled systems over high-profit but hostile routes.
- Combat/autonomy policy should distinguish `evade`, `bribe`, `wait_for_police`, `fight`, and `abort_route`.

### 10. Ship/outfit progression and role-specific play

Source: `source-grounded EV-family`, EVN Bible and LP Archive EV Nova intro; `community-guide`, Tea Leaves.

Relevant mechanics found:

- Outfit items can have mass, add weapons, affect crew/marines/capture odds, represent permits/intangibles, be unsellable, or persist across ship changes.
- Ship-change commands can preserve or discard outfits differently.
- LP Archive EV Nova frames playstyles as trade, gunboat/capital, pirate, courier, mine, fight, explore; ship selection should reflect playstyle.
- Tea Leaves frames the starter shuttle as limited by cargo, weapons, and damage tolerance.

Automation implications:

- Agents should have role profiles rather than one generic credit-maximizer:
  - merchant/courier: cargo, fuel, safety, deadlines;
  - explorer/scout: range, speed, map completion;
  - armed merchant: survivability without seeking combat;
  - combat/pirate/privateer: weapons, legal risk, disposable pilot requirement;
  - storyline runner: faction locks and mission bits.
- Upgrade policy needs explicit goals: more cargo, more speed, more fuel/range, more defensive survival, enough combat rating, or license/story access.

## Automated gameplay state model

Minimum state fields for Terminal Velocity agent/eval work:

```text
mode: in_space | landed | map | mission_dialog | commodity_exchange | bar | outfitter | shipyard | modal_unknown
location: system, stellar/body, government, known services
ship: class, shields, armor, fuel_full_jumps, fuel_partial, free_cargo, mission_reserved_cargo, commodity_hold, weapons, outfits, escorts
pilot: credits, date, combat_rating, legal_record_by_government, faction_bits/storyline_state, strict_play=false
missions: active list with surface, travel target, return target, ship goal, cargo/passenger burden, deadline, pay, legal/faction effects, next action
map: known systems, route links, refuel points, mission arrows, danger/patrol notes, commodity notes
risk: hostile ships visible, pirate/warship/police presence, illegal cargo scan risk, low fuel, deadline slack
trace: last action, last observation, evidence path, confidence
```

## Initial skill library for autonomous play

Safe/reusable first:

1. `establish_state_from_ui`: classify modal/screen/HUD and capture evidence.
2. `land_or_takeoff_safely`: use landing clearance/takeoff loop with screenshot verification.
3. `scan_services`: record visible landed services before changing state.
4. `scan_mission_surfaces`: inspect Mission Computer, Bar, and later Trading Center/Shipyard/Outfitter where present.
5. `score_mission_offer`: evaluate cargo, deadline, destination, pay, risk, legal/combat gates.
6. `accept_safe_delivery`: accept only noncombat missions with enough cargo/fuel/time and no destructive/legal risk.
7. `reserve_mission_cargo`: mark cargo/passengers unavailable for commodity trading.
8. `trade_spare_capacity`: buy only with remaining cargo/credits after mission reservations.
9. `plot_known_safe_route`: prefer known/patrolled/refuel-safe paths; avoid hostile/unknown when fragile.
10. `depart_move_jump_land`: travel with distance-gate retries, fuel checks, and landing/refuel verification.
11. `complete_mission_and_log_delta`: record credits, cargo/free space, date, legal/faction changes, and next mission availability.
12. `abort_or_pause_on_uncertainty`: stop if modal/input/freeze ambiguity appears; capture and classify before more action.

Disposable/non-strict later:

13. `controlled_combat_escape`: learn fleeing, police assistance, shields/fuel margin.
14. `disable_board_rescue`: precision combat/boarding missions.
15. `piracy_or_privateering`: only on explicitly disposable pilot due to legal/destructive consequences.
16. `ship_upgrade_experiment`: compare ship/outfit deltas and buy only with rollback/save safety.

## Scenario/evaluator ladder

Each scenario should have a cheap, deterministic done condition in Terminal Velocity before trying it in original EV Classic.

1. **Screen classifier:** from start/landed/map/commodity/mission screenshots or UI state, choose legal actions.
   - Done: no destructive action selected from unknown modal.
2. **Levo commodity lot test:** buy/sell one 10-ton lot with free capacity and credits.
   - Done: credits/free/hold deltas match expected lot behavior.
3. **Safe passenger/cargo mission:** accept a noncombat job fitting free cargo.
   - Done: mission appears active; cargo/free space reservation visible.
4. **Route to known neighbor and land:** select destination, move far enough, jump, land/refuel.
   - Done: location changes, fuel/date update logged, no death/destructive state.
5. **Mission completion:** complete one delivery and record pay/date/cargo/free changes.
   - Done: mission removed/complete; next active step clear.
6. **Opportunistic trade with mission:** fill only spare cargo along mission route.
   - Done: mission still completable and trade improves credits without blocking cargo.
7. **Mission surface archive:** revisit a port after travel and compare mission random/bit changes.
   - Done: state archive logs offers by surface and system-entry refresh.
8. **Map objective arrows:** verify travel/return/special target arrows.
   - Done: route planner can explain objective marker source.
9. **Avoid pirate on safe lane:** choose evade/wait/land/jump rather than fight in shuttle.
   - Done: survival with shields/fuel threshold maintained.
10. **Combat-gated mission refusal:** identify a mission as blocked by combat rating/ship/cargo rather than attempting it.
    - Done: blocked reason recorded.

## Tactics to append to gameplay-autoresearch log

The following tactics should be logged as hypotheses/design rules now and verified in future bounded runs:

- `keep_hypothesis`: Beginner merchant policy: passenger/cargo missions plus commodity trades on safer/patrolled lanes before combat.
- `keep_hypothesis`: Mission cargo reservation must take priority over commodity trading.
- `keep_hypothesis`: Scan every visible mission surface, not only Mission Computer; EV-family missions can appear in Bar, Main Spaceport, Trading Center, Shipyard, and Outfitter.
- `keep_hypothesis`: Re-entering systems can refresh random mission availability; preserve a state archive of offers by system/port/surface.
- `keep_hypothesis`: Route policy should choose refuel-safe, politically safer lanes for fragile ships even if profit is lower.
- `needs_disposable_pilot`: Destroy/disable/board/rescue/chase-off missions require combat-capable or disposable pilots.
- `keep_hypothesis`: Upgrade planning should be role-specific, not a generic largest-ship heuristic.

## 2026-05-28 general gameplay-learning source sweep additions

Sources checked:

- Voyager (`arXiv:2305.16291`): LLM game agent for Minecraft using automatic curriculum, an ever-growing executable skill library, environment feedback, execution errors, and self-verification.
- Go-Explore (`arXiv:1901.10995`): hard-exploration method built around remembering visited states, returning to promising states first, then exploring from them, with later robustification.
- GVGAI (`arXiv:1802.10363`): general video-game AI framework emphasizing multi-game/task benchmarking, game descriptions, and multiple evaluation tracks.
- Google Research, “Quickly Training Game-Playing Agents with Machine Learning” (2021): recommends not one end-to-end agent, but ensembles of short gameplay-loop agents, semantic state/action APIs, and long tests made by remixing core loops with simple scripting.
- OpenAI VPT paper/source page found via `cdn.openai.com/vpt/Paper.pdf` and OpenAI VPT index: supports using small action-labeled human data plus large unlabeled gameplay video for behavior pretraining. For Terminal Velocity, use the lightweight analogue: capture user/operator action traces and reuse them as macro demonstrations, not large-scale video ML.
- Existing primary harness source notes: BrowserGym/WebArena/OSWorld patterns separate task/scenario manifests, setup, validation, result getters, expected rules, run events, and artifacts.

Additional process upgrades for Terminal Velocity:

1. **Curriculum queue, not ad-hoc next steps**
   - Maintain a queue of gameplay skills ordered by prerequisite state: state classification → map route append → jump/land/refuel → scan services → mission accept → mission complete → trade-with-mission → upgrade planning → escape/combat.
   - Each skill has a success metric, required observations, failure gates, and promotion criteria.

2. **State archive / waypoint library**
   - Keep reusable snapshots/checkpoints for known useful states: landed at Levo, map open, route selected, landed at first neighbor, mission accepted, commodity screen open, etc.
   - Apply Go-Explore’s principle: return to a known promising state cheaply, then explore one new branch, instead of replaying the full journey from scratch.

3. **Short loop agents / macros**
   - Follow Google’s gameplay-loop framing: create separate small controllers/macros for 1–3 minute loops rather than one broad play agent.
   - Compose loops with simple scripts for longer tasks: `scan_mission_surfaces` + `score_offer` + `reserve_cargo` + `append_route` + `jump_land_refuel` + `complete_mission`.

4. **Executable skill library**
   - Store successful routines as scripts/macros with preconditions, postconditions, and known failure modes.
   - Promote only routines that have passed deterministic Terminal Velocity scenarios and, where fidelity matters, a bounded Basilisk sample.

5. **Action-trace learning from human/operator demos**
   - When the user demonstrates something in Basilisk, record timestamped action traces plus before/after probes and screenshots.
   - Convert traces into reusable macros and test cases. This is the small-scale practical version of VPT/imitation-learning: action-labeled demonstrations are more valuable than prose recollection.

6. **Scenario manifests and validators**
   - Borrow browser/computer-agent harness structure: each gameplay eval should have a manifest with setup state, allowed actions, forbidden actions, expected result getters, validation rules, evidence artifacts, and teardown/reset policy.
   - This avoids losing time interpreting screenshots after every action.

7. **Generalization checks**
   - Borrow GVGAI/Procgen-style thinking: a skill is not learned if it works only for Levo→Sol. Test route/trade/mission routines across multiple systems, cargo loads, fuel levels, and service availability states.

8. **Basilisk as calibrator, not trainer**
   - Original EV Classic remains source truth, but use it like a calibration oracle: sample exact UI/edge cases, then run broad learning in Terminal Velocity.
   - Avoid long Basilisk sessions unless a captureable source-truth question cannot be answered by decoded resources or a short trace.

## Near-term implementation guidance for Terminal Velocity

Do first:

1. Build a small Terminal Velocity scenario/eval harness around structured game state and scripted action choices.
2. Add mission cargo reservation visibility to the mission/trade model before encouraging trade-with-missions.
3. Add mission-log next-action fields: travel target, return target, deadline, cargo burden, pay, and objective class.
4. Add map/objective route hints for mission destination and refuel/fuel risk.
5. Create separate test pilots/scenarios: merchant, route-planner, mission-runner, outfitter, disposable combat.

Do not do yet:

- Do not automate long unattended Basilisk play.
- Do not enable Strict Play.
- Do not treat EV Nova/Override fields as exact EV Classic formulas.
- Do not implement piracy/legal consequences from guides alone.
- Do not let an agent fight in the reusable merchant pilot.

## Verification targets for future sessions

- Original EV Classic: recapture exact hyperspace route/jump sequence now that Basilisk is stabilized.
- Original EV Classic: observe a complete mission acceptance -> travel -> completion loop with action trace.
- Decoded EV Classic resources: verify mission/cargo/faction field equivalents before making fidelity claims.
- Terminal Velocity: implement symbolic state/action/evaluator harness and run it on the Levo start + commodity + safe mission scenarios.
