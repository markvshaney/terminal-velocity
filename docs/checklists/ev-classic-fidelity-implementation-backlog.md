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

## Development method / process optimization

- [x] Source-aligned vertical-slice development method
  - Status: `verified`
  - Source/rationale: `docs/research/source-aligned-game-development-method.md`; uses project-local automation synthesis plus Godot best-practice docs and practitioner game-development sources on vertical slices, backlog granularity, agile/demonstrable iterations, and playtesting.
  - Rule: develop gameplay as small vertical slices with one player-visible or symbolic behavior, one named scenario/evaluator, one cheap verification command, one source/fidelity label, and a backlog/docs update when future behavior is affected.
  - Kanban rule: use direct TDD inside a tight single-slice loop; use Kanban only at feature/lane boundaries such as Godot UI, symbolic model, original EV observation, source/fidelity docs, and review.
  - Fidelity guardrail: general game-development and automation sources improve method only; they do not justify EV Classic behavior claims.

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

- [x] EV Classic map multi-stop Shift-click route planning
  - Status: `verified scaffold / screenshot-confirmed original route-path example; needs edge-case pass`
  - Source: user-observed original-runtime behavior in Basilisk II on 2026-05-28; user-provided screenshot-confirmed example on 2026-05-29; see `docs/research/original-ev-classic-runtime-observations.md#2026-05-28-map-multi-stop-route-planning-seed`.
  - Scope: holding Shift and clicking multiple available systems should extend a green multi-hop route path. Terminal Velocity now stores an ordered route queue/path, appends only systems linked from the current route tail, draws the full green polyline, and consumes/advances the first leg on jump.
  - Implementation: Godot map route selection uses `selected_route` with tail-linked append and full green route drawing; symbolic scenario `shift_click_multi_stop_route_queue` verifies Levo → Sol → Sirius queue construction and first-leg consumption.
  - Verification: `python3 -m unittest native_ev.tests.test_scenario_eval.ScenarioEvalHarnessTests.test_shift_click_multi_stop_route_queue_draws_green_path_and_consumes_first_leg -v`; `./run_godot.sh tv-map-route-log`; full native tests and `./run_godot.sh self-test` pass with `gameplayScenarios=11`.
  - Next action: capture an original-runtime step-by-step Basilisk pass when input/capture is reliable enough to verify exact edge cases such as route clearing, invalid clicks, and path truncation.

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
  - Implementation/instrumentation: `RunGodot.ps1 -LandedUiMatrix` emits each TV body’s visible landed buttons, services, item counts, mutating actions, and `observationGuard=before_after_capture_required`. Terminal Velocity now also exposes service availability in play: landed panels show `Refuel: F5 available` or `Refuel: unavailable`, the HUD shows current/max fuel, F5 refuels when local service exists, and blocked/success refuel attempts flow through the recent message surface.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_landing_panels_are_actionable native_ev.tests.test_model.NativeEvModelTests.test_godot_route_jump_land_refuel_autoresearch_log_contract -v`; `./run_godot.sh tv-route-land-refuel-log` emitted `refuelAvailable=true`, `refuelSucceeded=true`, and `travelLoopComplete=true`.
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
  - Status: `partially implemented scaffold / original mission-map auto-objective not observed`
  - Source: EV Nova Bible `Jump Distance`, fuel/nav interface fields, and mission map-arrow flags; local EV Classic hyperspace attempts remain `runtime-observed` but inconclusive. A 2026-05-28 original EV Classic/Basilisk capture with active missions visible in Mission Info found no visible automatic mission objective route/arrow/marker on the zoomed galaxy map; see `docs/research/original-ev-classic-runtime-observations.md` and local-only capture `C:\Games\BasiliskII\ev-mission-map-kathoon-active-missions-zoomout-20260528T235242Z.png`.
  - Scope: show mission travel/return/special-ship arrows, visible fuel/jump units, partial fuel state, route risk, and explicit feedback when jump conditions are not met.
  - Implementation: symbolic scenario `mission_destination_route_hint` accepts the intro courier mission and queues the active contract destination (`Centauri`) as the next route leg with `sourceLabel=terminal-velocity-design-scaffold` and `oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace`. Godot exposes the same route-hint surface through `./run_godot.sh tv-mission-route-hint-log` / `RunGodot.ps1 -MissionRouteHintLog`, emitting `TV_MISSION_ROUTE_HINT_EVENT`; in the player map, `G` queues the active mission route as a helper-labeled Terminal Velocity convenience.
  - Verification: `python3 -m unittest native_ev.tests.test_scenario_eval.ScenarioEvalHarnessTests.test_mission_destination_route_hint_sets_route_to_active_contract_destination -v`; `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_mission_destination_route_hint_log_contract -v`; full native discovery passed 90 tests; Godot self-test passed with `gameplayScenarios=12`; Godot route-hint log emitted `missionRouteQueued=true route=["Centauri"] routeHops=1`.
  - Next action: keep the Terminal Velocity mission route hint as an opt-in/helper scaffold or explicitly helper-labeled UI, not an EV Classic fidelity claim. To promote further, capture a stronger EV Classic pass that finds the mission destination on the map, tests multi-hop Shift-click routing through adjacent stops toward non-direct destinations such as Torgo Prime from Kathoon, and separately captures fuel/jump feedback.
  - Fidelity boundary: use EV-family docs for learning/UI structure; capture EV Classic runtime for exact jump timing/distance/sound/animation; do not claim original EV auto-draws active mission objective routes from the current capture.

- [ ] Per-government legal/reputation and AI behavior model
  - Status: `candidate`
  - Source: EV Nova Bible government definition/flags and legal-status scaling by crime tolerance, summarized in the deep dive.
  - Scope: track legal/reputation per government; drive landing rights, patrol aggression, bribes, mission eligibility, distress/greetings, roadside assistance, shipyard/outfitter access, and faction ally/enemy consequences.
  - Next action: draft a data schema proposal separating global pilot state from per-government standing.
  - Fidelity boundary: formulas and exact thresholds need EV Classic confirmation.

- [x] Cargo/trade coupling and mission-reserved capacity
  - Status: `implemented Terminal Velocity scaffold / source-family structured`
  - Source: EVN mission cargo fields, Nova Bible commodity purchase-location fields, and disaster/commodity-price references.
  - Scope: make cargo a shared constraint across missions and trade; expose mission-reserved cargo/passengers in trade screens; retain discovered buy/sell markets, route profit per jump/day, fuel/refuel risk, and event/disaster price effects.
  - Implementation: Godot Mission Info (`I`) summarizes active mission count, reserved mission tons, and free capacity; the HUD shows `Cargo: used/capacity (mission, free)`; Commodity Exchange displays `Cargo reserved for missions`, explicit `Buy B` and `Sell S` columns, buy/sell prices, and only marks sell action on held cargo. The selected commodity now shows a Terminal Velocity scaffold hint for the best linked-system sell price/profit per ton when local market data exists. Mission acceptance and commodity buys use the shared `_cargo_available_tons()` helper so mission cargo and trade cargo compete visibly for the same hold. A small HUD `Messages:` stack now preserves recent mission/trade success and blocked-reason feedback such as insufficient free cargo, full hold, unavailable commodity, no sell price, no cargo to sell, or insufficient credits.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_commodity_buy_sell_affordance_contract -v`; `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_commodity_route_hint_contract -v`; `./run_godot.sh tv-commodity-trade-log` emitted `buySucceeded=true sellSucceeded=true roundTripVisible=true`; full native discovery passed 96 tests; Godot self-test passed with `gameplayScenarios=12`.
  - Next action: defer exact Classic commodity prices/events until decoded resources or runtime confirmation; next safe playable slice is likely stronger ship/outfit purchase persistence.
  - Fidelity boundary: exact Classic commodity prices/events require decoded resources or runtime confirmation.

- [x] Ship/outfit comparison and upgrade consequence surfaces
  - Status: `implemented Terminal Velocity scaffold / source-backed manifest fields`
  - Source: local EV Classic ship-like records in `native_ev/data/ships.json`, local shipyard PICT assets, local outfitter effect manifest; EV Nova Bible outfit fields remain source-family guidance only.
  - Scope: expose purchase deltas for mass, cargo/outfit space, crew/capture effects, weapon roles, licenses/permits, resale restrictions, and persistence across hull changes.
  - Implementation: Shipyard listings now show immediate deltas against the current hull for cargo, hull, max speed, and turning; outfitter listings now show concise numeric effect summaries for cargo, hull, and fuel upgrades. Existing Source PICT shipyard art remains visible on the selected listing.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_landing_panels_are_actionable -v`; `./run_godot.sh self-test`.
  - Next action: add a safe in-game learning/help overlay that explains currently wired keys, route helper, mission cargo reservation, and ship/outfit comparison without making unverified Classic claims.
  - Fidelity boundary: exact EV Classic item stats and persistence behavior require Classic resource/manual/runtime confirmation; current comparison uses the local structured manifest as a Terminal Velocity scaffold.

- [x] In-game learning/documentation surfaces for EV-style strategy
  - Status: `implemented Terminal Velocity helper/scaffold`
  - Source: same EV-family deep dive plus recurring guide/player-pain signals from GameFAQs, EVN Wiki, Ambrosia/Cythera archives, and EV Nova manual/walkthroughs.
  - Scope: add or plan durable player learning aids: beginner guide, keyboard overlay, map/service reference, trading guide, combat guide, ship/outfit comparison help, faction/storyline hinting, and mission checklist/log.
  - Implementation: Godot now has an F10 help overlay that explains currently wired keys, map route planning, the `G` mission-route helper, mission/free cargo reservation, landing tabs, buy/accept controls, recent message feedback, player-info/inventory overlay, shipyard/outfitter comparison surfaces, refuel, and F6 pilot save/resume. The overlay explicitly labels itself `Terminal Velocity helper/scaffold — not an EV Classic fidelity claim`.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_landing_panels_are_actionable -v`; `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_player_inventory_overlay_contract -v`; `./run_godot.sh self-test`.
  - Next action: broad Classic strategy/tutorial detail should wait for stronger manual/runtime evidence; the next safe playable slice is likely refuel/service visibility or save/load pilot persistence.
  - Fidelity boundary: learning aids may explain Terminal Velocity behavior directly; do not present unverified EV Classic facts as canonical.

- [x] Visible mission log/status detail
  - Status: `implemented Terminal Velocity helper/scaffold`
  - Source: Terminal Velocity mission JSON and recurring EV-family player-guide pattern that active contracts need visible destination/cargo/reward status; exact EV Classic mission log window layout/text remains unverified.
  - Scope: make active mission state visible without relying on transient status text: title, active status, destination system/body, current progress, route hint, cargo reserved, reward, briefing when available, and recent completion history with cargo/reward settlement.
  - Implementation: `I` now toggles a Mission Log overlay and still updates the status line summary; the overlay is labeled `Terminal Velocity mission log helper/scaffold — not an EV Classic fidelity claim`; active contracts show whether to travel, land, or complete at the current port plus a `G` route-helper hint; completed missions now record recent title/port/cargo-released/reward-paid history and persist it in the TV pilot JSON.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_mission_completion_history_contract -v`; full native discovery passed 94 tests; Godot self-test passed with `gameplayScenarios=12`.
  - Next action: mission-log screenshots only after stronger UI evidence or a visual-review need appears; next safe non-gated slice is stronger commodity sell/transaction affordance.
  - Fidelity boundary: this is TV usability scaffolding, not a claim about the original Classic mission-log UI.

- [x] Pilot save/resume persistence affordance
  - Status: `implemented Terminal Velocity save scaffold / needs EV Classic pilot-file evidence`
  - Source: Terminal Velocity JSON pilot persistence path and existing title-screen New/Open Pilot flow; exact EV Classic pilot file layout and autosave/manual-save semantics remain unverified.
  - Scope: make longer sessions resumable by saving current system, position/velocity/facing, fuel, credits, cargo/cargo space, active/completed missions, story flags, commodity hold, owned outfits/weapons, ship identity, and Strict Play flag.
  - Implementation: in-flight `F6` now saves the currently loaded pilot through the same `user://pilots/*.tvpilot.json` path used by New/Open Pilot; the HUD and F10 help expose `F6 save`; the title-screen Open Pilot list shows pilot/ship, saved system, credits, and Strict Play status before resume; `./run_godot.sh tv-pilot-save-resume-log` / `RunGodot.ps1 -PilotSaveResumeLog` creates/overwrites a deterministic non-strict test pilot, accepts a courier mission, buys a ship plus outfit/weapon inventory, saves, mutates state including inventory/ship/cargo-space and the Strict Play flag, reopens the pilot, and checks round-trip system/fuel/credits/active-mission/Strict-Play/outfit/weapon/ship/cargo-space fields.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_pilot_save_resume_log_contract -v`; `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_open_pilot_list_shows_resume_context_contract -v`; `./run_godot.sh tv-pilot-save-resume-log` emitted `saveSucceeded=true`, `resumeSucceeded=true`, `systemRoundTrip=true`, `fuelRoundTrip=true`, `creditsRoundTrip=true`, `missionRoundTrip=true`, `strictPlayRoundTrip=true`, `outfitRoundTrip=true`, `weaponRoundTrip=true`, `shipRoundTrip=true`, and `cargoSpaceRoundTrip=true`; full native discovery passed 96 tests; Godot self-test passed with `gameplayScenarios=12`.
  - Next action: if this verifies, consider a visible mission-log/status detail slice; defer exact Classic pilot-file fidelity until original pilot-file/resource evidence exists.
  - Fidelity boundary: this is Terminal Velocity save/persistence implementation, not an EV Classic pilot-file fidelity claim.

- [x] Automated gameplay learning harness and skill curriculum
  - Status: `implemented-extended`
  - Source: `docs/research/ev-automated-gameplay-learning-synthesis.md`; `docs/research/ev-gameplay-autoresearch-results.jsonl`; source-grounded EV-family mission data from `/tmp/ev-source-deep-dive-20260521/text/`; Tea Leaves early EV merchant-loop guide; LP Archive EV Nova role/playstyle framing; prior Basilisk stabilization notes.
  - Scope: build a symbolic/LLM-controller gameplay loop for Terminal Velocity before attempting long unattended Basilisk play. Minimum pieces: structured game-state observer, bounded action API, reusable skill library, scenario/evaluator ladder, action/evidence trace logging, and separate non-strict pilot/scenario profiles for merchant, route-planner, mission-runner, outfitter, and disposable combat.
  - Initial curriculum: screen classifier; Levo commodity 10-ton lot; safe passenger/cargo mission; route to known neighbor and land/refuel; mission completion; opportunistic trade with mission-reserved cargo; mission-surface archive; map objective arrows; pirate avoidance; blocked-reason recognition for combat/cargo/legal/ship gates.
  - Implementation: `native_ev/scenario_eval.py` now provides a structured state/action/evaluator harness and the scenario curriculum `levo_merchant_first_hop`, `mission_runner_first_delivery`, `scan_intro_mission_offers`, `intro_courier_mission_delivery`, `chapter_one_courier_chain`, `alignment_choice_guardrail`, `mission_destination_route_hint`, `shift_click_multi_stop_route_queue`, `route_planner_refuel_loop`, `low_fuel_jump_recovery`, `blocked_reason_curriculum`, and `disposable_combat_placeholder`; `tools/run_gameplay_scenarios.py --all` runs the full curriculum. `native_ev/data/gameplay_curriculum.json` exposes the curriculum to Godot self-test, which reports `gameplayScenarios=12`.
  - Verification: `python3 -m unittest native_ev.tests.test_scenario_eval -v`; `python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`; `python3 tools/run_gameplay_scenarios.py --all --pretty`; Godot `./run_godot.sh self-test` passed with `gameplayScenarios=12`.
  - Next action: promote `mission_destination_route_hint` into Godot map overlay/arrow UI, add pirate-avoidance and outfitter/ship-ladder scenarios, then decide which scenario outcomes should become in-game tutorial/hint surfaces.
  - Fidelity boundary: use this as an automation/design scaffold. Original EV Classic fidelity claims still require original runtime, decoded Classic resources, or manual/docs confirmation; long unattended Basilisk play, Strict Play, and piracy/combat on reusable pilots remain gated.

## Deferred / guardrail items

- [ ] External adaptation comparisons
  - Status: `deferred`
  - Source: external engines/adaptations may provide hypotheses only.
  - Rule: do not implement behavior from external adaptations unless original runtime, decoded resources, manual/docs, or Terminal Velocity instrumentation confirms it.
