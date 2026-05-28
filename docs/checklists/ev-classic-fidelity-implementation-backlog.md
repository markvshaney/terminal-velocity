# EV Classic fidelity implementation backlog

Purpose: live checklist for recommendations and potential Terminal Velocity implementations that come out of original EV Classic observation, decoded resources, or comparison work.

Rationale/source record: `docs/decisions/2026-05-19-ev-classic-observation-to-implementation-workflow.md`.

Status vocabulary: `candidate`, `needs evidence`, `ready`, `implemented`, `verified`, `deferred`, `blocked`.

## Active / recurring workflow

- [x] Maintain observation-to-implementation split
  - Status: `verified`
  - Source: user request on 2026-05-19 plus workflow artifact above.
  - Rule: every durable recommendation from observation work should either be implemented immediately if small/source-backed, or captured here with a next action.
  - Storage rule: original-system observations that may inform future Terminal Velocity behavior, data, UI, economy, services, missions, combat, hazards, or progression must be recorded in `docs/research/original-ev-classic-runtime-observations.md` with evidence/provenance before implementation or deferral decisions are made.

- [x] Seed playable observations for later Terminal Velocity incorporation
  - Status: `verified`
  - Source: user clarification on 2026-05-20: as EV Classic is played, observations should be seeded into artifacts so they can later be incorporated into Terminal Velocity.
  - Rule: every play session should produce zero or more observation seeds in `docs/research/original-ev-classic-runtime-observations.md` using the seed format there. A seed is not automatically implementation authority; it is a durable handoff containing the observed behavior, learned player skill/use, evidence, likely Terminal Velocity surface, and missing evidence/status.
  - Next action during play: after each meaningful original-runtime observation, add or update a seed, then either link it to an existing backlog item or create a compact candidate/needs-evidence item here.

- [x] Reuse learned EV player skill sets in Terminal Velocity design
  - Status: `verified`
  - Source: user guidance on 2026-05-20: the skill set learned while playing EV Classic can later be utilized for Terminal Velocity.
  - Rule: treat learned player skills as reusable design material, not just operator notes. Capture mission-running, trading, route planning, fuel/risk management, combat avoidance/engagement, ship modification, outfitting, and system-provisioning judgment in observation seeds when they are learned from play. Mark whether each learned skill can transfer to other pilots/test profiles, and distinguish transferable player strategy from pilot-specific state, cargo, reputation, mission deadlines, equipment, or save-risk constraints.
  - Future incorporation surfaces: Terminal Velocity tutorials/onboarding, hints, mission/economy balance, AI/player guidance, progression design, regression scenarios, and test pilots.

- [x] Report mission completion and pirate/hostile avoidance during play
  - Status: `verified`
  - Source: user guidance on 2026-05-20 requesting reports about how missions are completed and how pirates or other threats are avoided.
  - Rule: mission/travel play reports should document the active mission, route selection, cargo/passenger constraints, fuel/credit changes, completion/failure state, encountered pirates/hostiles/asteroids, avoidance or engagement tactics, damage/risk outcome, and reusable lessons for other pilots.
  - Future incorporation surfaces: Terminal Velocity mission tutorials, route-risk hints, pirate/hostile threat modeling, defensive-readiness balance, AI guidance, and regression scenarios for safe travel.

## Source-backed implementations already integrated

- [x] EV Classic starting credits
  - Status: `verified`
  - Evidence: `original-runtime-observed`; first playable HUD shows `Credits: 10,000`.
  - Implementation: `godot_ev/scripts/main.gd` uses `credits := 10000`.
  - Verification: Python model tests and Godot selftest passed in the 2026-05-19 observation pass.

- [x] EV Classic start at Levo in space
  - Status: `verified`
  - Evidence: `original-runtime-observed` plus `decoded-resource-backed` Levo landing text.
  - Implementation: `native_ev/data/universe.json` starts with Levo; `godot_ev/scripts/main.gd` resolves `START_SYSTEM_NAME := "Levo"` by name.
  - Caveat: Levo routing/coordinates are minimal bridge scaffolding pending fuller topology work.

- [x] Levo landing panel visible services
  - Status: `verified`
  - Evidence: `original-runtime-observed`; Levo landed screen exposes `Spaceport Bar`, `Mission Computer`, `Commodity Exchange`, and `Leave`, with no visible outfitter button.
  - Implementation: Levo inventory/services omit outfitter/weapons listings; Godot landing panel only shows outfitter/shipyard when listings exist.

- [x] Levo commodity names, statuses, buy prices, and same-port sell prices
  - Status: `verified`
  - Evidence: `original-runtime-observed`; Levo Commodity Exchange visible rows and buy/sell-back captures.
  - Implementation: `native_ev/data/economy.json` uses Food `120`, Industrial `192`, Medical `600`, Metal `144`, Equipment `360` for both buy and sell at Levo, with EV Classic status labels where observed.
  - Caveat: this proves Levo same-port sell prices, not the global economy formula.

## Candidates / potential implementations

- [ ] Player strategy skills as distinct progression loops
  - Status: `candidate`
  - Source: user framing on 2026-05-20; partially supported by observed Mission Computer, Spaceport Bar, Commodity Exchange, cargo, credits, passenger-mission UI, and later user guidance to learn opportunistic trade-with-missions and ship modification as separate skills.
  - Scope: model separate-but-overlapping skills/strategies for mission running, commodity trading, piracy/privateering/looting, faction progression, and upgrade/ship-ladder planning instead of treating credits as a single undifferentiated grind.
  - Design direction: players should be able to develop skill/capability in various niches, with different pilots specializing in different loops rather than every pilot converging on the same optimal path. Mission runners should learn when spare cargo capacity, route alignment, capital, deadlines, and safety make it worth carrying trade goods alongside jobs; ship modification and ship trade-up should be learned as capability-planning loops, including cargo/storage capacity, hardening, instruments/equipment, and when weapons/outfits/escorts are needed for defensive survival versus when avoidance/speed/route choice is enough. Combat-adjacent learning should include system-level hazards such as asteroids, pirate/hostile traffic levels, when to avoid other ships, and when attacking is worthwhile or too risky, but destructive/legal-consequence tests stay on disposable non-strict pilots. As exploration reaches new systems or landable bodies, verify whether Terminal Velocity needs original-game planet graphics and stores/services provisioned there, including commodities, outfitters, weapon availability, shipyards, and absent services.
  - Plan: `docs/plans/2026-05-20-player-strategy-niches.md`.
  - Next action: gather original-runtime evidence for each loop using separate non-strict pilots where useful: mission/trade/navigation pilot first, commodity spread pilot second, outfitting/ship-stats pass third, combat/piracy/privateering on a disposable non-strict pilot only after controls and save safety are understood.
  - Pilot policy: creating multiple pilots for different strategy tracks is approved by the user; keep Strict Play off unless explicitly directed otherwise.
  - Do not implement piracy/legal/faction consequences from inference alone; require original runtime, decoded resources, or manual/source evidence.

- [ ] Fuller EV Classic galaxy topology and coordinates
  - Status: `needs evidence`
  - Source: current Levo bridge is intentionally minimal.
  - Next action: decode/source-integrate topology records or capture/runtime-verify map links before broad universe changes.
  - Do not implement from adaptation data alone.

- [ ] Exact starting primary weapons/outfits
  - Status: `needs evidence`
  - Source: first HUD proves `No Secondary Weapon`, `No Target`, full shield/fuel, and `Free: 20`; it does not prove full primary weapon/outfit inventory.
  - Next action: open a player/ship info screen or an outfitter/status screen at a port that exposes one, without changing inventory.

- [x] EV Classic commodity transaction granularity
  - Status: `implemented`
  - Source: Levo buy/sell observation showed `Buy` purchases 10 tons at a time from the starting shuttle state.
  - Implementation: `godot_ev/scripts/main.gd` now uses `EV_CLASSIC_COMMODITY_LOT_SIZE := 10` for commodity buy/sell actions, bounded by free cargo, credits, and held quantity.
  - Verification: `native_ev/tests/test_model.py` asserts the ten-ton lot implementation. Full partial-capacity original-runtime behavior remains an edge-case observation candidate if exact EV behavior matters.

- [ ] System-by-system original service/store provisioning
  - Status: `needs evidence`
  - Source: user guidance on 2026-05-20: as other systems are explored, determine whether they need to be provisioned with original-game planet graphics, stores, weapons, outfitters, shipyards, or absent-service behavior as originally implemented by EV Classic.
  - Next action: for each newly reached landable body, capture in-space/landed planet graphics plus landed services and all visible store/weapon/outfitter/shipyard/equipment surfaces before buying/selling; compare against Terminal Velocity active data; provision only bounded source-backed data and otherwise record `missing`, `scaffold`, `needs evidence`, or `not present in original`.

- [ ] Economy-wide buy/sell display and spread rules
  - Status: `candidate`
  - Source: Levo sell-back proves same-port sell equals visible buy price for Levo, but not a universal rule.
  - Next action: observe additional ports or decode commodity/economy resources before changing global formula assumptions.

- [ ] EV Classic prefs screen fidelity
  - Status: `implemented`
  - Source: original EV prefs screen visual observation and current Godot selftest output reports `prefScreen=original-ev-classic-observed`.
  - Strict Play caveat: observed Set Prefs does not include `Strict Play`; do not add it to this prefs modal without direct new-pilot UI evidence.
  - Next action: keep as regression surface in Godot selftest; add new items here if another prefs control needs exact behavior beyond visual layout.

- [x] EV Classic Strict Play / permadeath pilot option
  - Status: `implemented-default-off`
  - Source: original EV Classic New Pilot dialog capture at `C:\Games\BasiliskII\ev-new-pilot-strict-play-unchecked.png`, plus local EV manual/string evidence and pilot-file structure evidence. User notes correctly that Strict Play should not be used casually because ship destruction can force starting over.
  - Current evidence boundary: setting Strict Play off is directly observed as leaving `Strict Play` unselected in the New Pilot dialog, corresponding to `strictPlayFlag = 0`. The captured dialog text is `If you check this box, when you're dead, you're dead. No reincarnation allowed.`
  - Implementation: `godot_ev/scripts/main.gd` places `Strict Play` in the New Pilot name dialog, defaults it unchecked/off, saves it per pilot as `strict_play`, and restores it when opening a pilot file. `godot_ev/scripts/self_test.gd` emits `strictPlay=off-by-default`; `native_ev/tests/test_model.py` asserts the source-backed contract.
  - Remaining boundary: destructive strict-play death/permadeath semantics remain intentionally untested and unimplemented.

- [ ] Ship facing/frame-order runtime confirmation
  - Status: `needs evidence`
  - Source: decoded 36-facing sprite sheets are integrated, but runtime frame-order/facing behavior still needs observation.
  - Next action: capture deterministic original-runtime turning/facing sequence and compare against Terminal Velocity movement log.

- [ ] Movement tuning: turn rate, acceleration curve, max speed, inertial drift
  - Status: `instrumented / needs original comparison`
  - Source: behavior baseline checklist marks exact original acceleration/max-speed/drift integration as unknown; decoded EV Classic ship fields are wired and Terminal Velocity now emits deterministic movement scenarios.
  - Implementation/instrumentation: `RunGodot.ps1 -MovementLog` emits `right_turn`, `left_turn`, `thrust`, `coast`, and `thrust_right_turn` scenarios with tick count, facing index, angle, velocity, position, and selected ship physics fields.
  - Next action: capture original-runtime acceleration/max-speed/drift against the same scenario shape, then tune Terminal Velocity integration if the deterministic logs diverge.

- [ ] Land/takeoff and hyperspace timing/sound/animation fidelity
  - Status: `instrumented / needs original comparison`
  - Source: baseline checklist marks landing/hyperspace loop partial or unknown; 2026-05-20 recovery/continuation passes found post-movement key automation no longer delivered visible `J`/`I`/`M`/`A` effects from the `Hyperspace / Rigel` state, even though arrow acceleration and animation still worked. User correction: the player must be far enough from the planet/system center before hyperspace can start, so jump attempts must be iterated after sustained movement rather than abandoned after one try. Follow-up iteration used multiple longer acceleration segments plus `J` retries; no successful transit or distance-failure message was captured.
  - Implementation/instrumentation: `RunGodot.ps1 -TravelEventLog` emits deterministic start, land request, leave, hyper mode, hyper select, and jump events from current Terminal Velocity behavior.
  - Next action: use a fresh non-strict original EV session/pilot or alternate input route that first proves reliable letter-hotkey receipt (`I`, `M`, `L`, `H`, `J`, `A`) before and after movement, then capture successful hyperspace transit and compare to Godot event logs.

- [ ] Landed service/button matrix: bar, mission computer, commodities, outfitter, shipyard, gambling
  - Status: `instrumented / needs original click-through`
  - Source: user-requested EV mirroring pass for clicking available landed buttons/options; Levo original-runtime observation only proves `Spaceport Bar`, `Mission Computer`, `Commodity Exchange`, and `Leave` are visible there, with no outfitter button.
  - Implementation/instrumentation: `RunGodot.ps1 -LandedUiMatrix` emits each TV body’s visible landed buttons, services, item counts, mutating actions, and `observationGuard=before_after_capture_required`.
  - Next action: run bounded original EV click-through starting at Levo and then an outfitter/shipyard/gambling-capable early port, using disposable/non-strict state and before/after captures for every mutating option.

- [ ] Basic combat fidelity: fire rate, projectile speed/lifetime/damage, target selection, explosions
  - Status: `needs evidence`
  - Source: current data may be scaffold unless separately decoded/source-backed.
  - Next action: decode weapon/resource fields and/or capture original runtime combat behavior.

- [ ] EV-family gameplay learning source integration
  - Status: `candidate`
  - Source: `docs/research/ev-family-gameplay-source-deep-dive.md`; user guidance on 2026-05-21 that EV Classic, Escape Velocity: Override, and EV Nova share basic gameplay, so Override/Nova sources should be mined for transferable learning. Deeper source pass used locally extracted EVN walkthrough index/faction pages and EV Nova Bible text under `/tmp/ev-source-deep-dive-20260521/text/`.
  - Scope: use EV-family manuals, overlays, data-derived walkthroughs, community guides, wikis, archives, and implementation references to shape Terminal Velocity gameplay learning surfaces without treating non-Classic sources as exact EV Classic runtime truth.
  - Design direction: preserve the EV-family core loop of landing, missions/trade, map route planning, fuel/risk management, combat survival, ship/outfit upgrades, faction/reputation progression, and harder route/story unlocks. Prioritize player-facing learning surfaces: keyboard overlay/manual, new-pilot tutorial, mission log details, map overlays, ship/outfit comparisons, spoiler-light faction hints, trade-route notes, and reputation/legal feedback.
  - Next action: convert the source-grounded model in `docs/research/ev-family-gameplay-source-deep-dive.md` into small implementation plans or UI/data tickets, starting with mission state/log, map arrows/fuel feedback, per-government legal state, cargo reservation, and ship/outfit comparison.
  - Fidelity boundary: exact Classic behavior still requires original runtime observation, decoded EV Classic resources, manuals/docs, or Terminal Velocity instrumentation; EV Override/Nova/community/open-source sources are hypothesis/design-learning inputs unless independently verified.

- [ ] Mission state/log and mission-surface model
  - Status: `candidate`
  - Source: EVN walkthrough index mission key and EV Nova Bible mission fields, recorded in `docs/research/ev-family-gameplay-source-deep-dive.md`.
  - Scope: model mission availability, offer surface, accept/success/failure/abort state, travel destination, return destination, special ship goals, deadline, cargo/passenger reservation, pay, combat/legal/ship gates, and faction/legal consequences. Preserve distinct surfaces such as Mission Computer, Bar, Trading Center, Shipyard, and Outfitter instead of flattening all jobs into one list.
  - Next action: draft a mission data/UI ticket with visible blocked reasons and next-step mission log text.
  - Fidelity boundary: EVN fields inform structure; exact EV Classic field names/limits require Classic confirmation.

- [ ] Map objective arrows, fuel/range, and hyperspace feedback
  - Status: `candidate`
  - Source: EV Nova Bible `Jump Distance`, fuel/nav interface fields, and mission map-arrow flags; local EV Classic hyperspace attempts remain `runtime-observed` but inconclusive.
  - Scope: show mission travel/return/special-ship arrows, visible fuel/jump units, partial fuel state, route risk, and explicit feedback when jump conditions are not met.
  - Next action: create a small UI/data plan for map overlays and hyperspace failure/success messages before more runtime travel attempts.
  - Fidelity boundary: use EV-family docs for learning/UI structure; capture EV Classic runtime for exact jump timing/distance/sound/animation.

- [ ] Per-government legal/reputation and AI behavior model
  - Status: `candidate`
  - Source: EV Nova Bible government definition/flags and legal-status scaling by crime tolerance, summarized in the deep dive.
  - Scope: track legal/reputation per government; drive landing rights, patrol aggression, bribes, mission eligibility, distress/greetings, roadside assistance, shipyard/outfitter access, and faction ally/enemy consequences.
  - Next action: draft a data schema proposal separating global pilot state from per-government standing.
  - Fidelity boundary: formulas and exact thresholds need EV Classic confirmation.

- [ ] Cargo reservation, trade-route learning, and event-sensitive economy
  - Status: `candidate`
  - Source: EVN mission cargo fields, Nova Bible commodity purchase-location fields, and disaster/commodity-price references.
  - Scope: make cargo a shared constraint across missions and trade; expose mission-reserved cargo/passengers in trade screens; retain discovered buy/sell markets, route profit per jump/day, fuel/refuel risk, and event/disaster price effects.
  - Next action: draft a cargo/trade UI ticket that prevents mission cargo from feeling invisible or arbitrary.
  - Fidelity boundary: exact Classic commodity prices/events require decoded resources or runtime confirmation.

- [ ] Ship/outfit comparison and upgrade consequence surfaces
  - Status: `candidate`
  - Source: EV Nova Bible outfit fields for mass, weapons, marines/capture, permits/intangible items, unsellable/persistent outfits, and ship-change consequences.
  - Scope: expose purchase deltas for mass, cargo/outfit space, crew/capture effects, weapon roles, licenses/permits, resale restrictions, and persistence across hull changes.
  - Next action: draft shipyard/outfitter comparison UI fields and role tags.
  - Fidelity boundary: exact EV Classic item stats and persistence behavior require Classic resource/manual/runtime confirmation.

- [ ] In-game learning/documentation surfaces for EV-style strategy
  - Status: `candidate`
  - Source: same EV-family deep dive plus recurring guide/player-pain signals from GameFAQs, EVN Wiki, Ambrosia/Cythera archives, and EV Nova manual/walkthroughs.
  - Scope: add or plan durable player learning aids: beginner guide, keyboard overlay, map/service reference, trading guide, combat guide, ship/outfit comparison help, faction/storyline hinting, and mission checklist/log.
  - Next action: draft a Terminal Velocity player-learning surface plan that separates in-game UI, static docs, and future modder/reference docs.
  - Fidelity boundary: learning aids may explain Terminal Velocity behavior directly; do not present unverified EV Classic facts as canonical.

- [x] Automated gameplay learning harness and skill curriculum
  - Status: `implemented-extended`
  - Source: `docs/research/ev-automated-gameplay-learning-synthesis.md`; `docs/research/ev-gameplay-autoresearch-results.jsonl`; source-grounded EV-family mission data from `/tmp/ev-source-deep-dive-20260521/text/`; Tea Leaves early EV merchant-loop guide; LP Archive EV Nova role/playstyle framing; prior Basilisk stabilization notes.
  - Scope: build a symbolic/LLM-controller gameplay loop for Terminal Velocity before attempting long unattended Basilisk play. Minimum pieces: structured game-state observer, bounded action API, reusable skill library, scenario/evaluator ladder, action/evidence trace logging, and separate non-strict pilot/scenario profiles for merchant, route-planner, mission-runner, outfitter, and disposable combat.
  - Initial curriculum: screen classifier; Levo commodity 10-ton lot; safe passenger/cargo mission; route to known neighbor and land/refuel; mission completion; opportunistic trade with mission-reserved cargo; mission-surface archive; map objective arrows; pirate avoidance; blocked-reason recognition for combat/cargo/legal/ship gates.
  - Implementation: `native_ev/scenario_eval.py` now provides a structured state/action/evaluator harness and the scenario curriculum `levo_merchant_first_hop`, `mission_runner_first_delivery`, `route_planner_refuel_loop`, `low_fuel_jump_recovery`, `blocked_reason_curriculum`, and `disposable_combat_placeholder`; `tools/run_gameplay_scenarios.py --all` runs the full curriculum. `native_ev/data/gameplay_curriculum.json` exposes the curriculum to Godot self-test, which reports `gameplayScenarios=6`.
  - Verification: `python3 -m unittest native_ev.tests.test_scenario_eval -v`; `python3 -m unittest discover -s native_ev/tests -v`; `python3 tools/run_gameplay_scenarios.py --all --pretty`; Windows Godot `RunGodot.ps1 -SelfTest` passed with `gameplayScenarios=6`.
  - Next action: add richer mission-surface/archive, map objective-arrow, pirate-avoidance, and outfitter/ship-ladder scenarios; then decide which scenario outcomes should become in-game tutorial/hint surfaces.
  - Fidelity boundary: use this as an automation/design scaffold. Original EV Classic fidelity claims still require original runtime, decoded Classic resources, or manual/docs confirmation; long unattended Basilisk play, Strict Play, and piracy/combat on reusable pilots remain gated.

## Deferred / guardrail items

- [ ] External adaptation comparisons
  - Status: `deferred`
  - Source: external engines/adaptations may provide hypotheses only.
  - Rule: do not implement behavior from external adaptations unless original runtime, decoded resources, manual/docs, or Terminal Velocity instrumentation confirms it.
