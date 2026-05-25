# Player Strategy Niches Implementation Plan

> **For Hermes:** Use source-backed EV Classic observation and bite-sized local implementation passes. Do not implement broad inferred mechanics without original-runtime, decoded-resource, manual, or project-instrumentation evidence.

**Goal:** Make Terminal Velocity support multiple viable player skill/progression niches rather than a single generic credit grind.

**Architecture:** Treat each strategy niche as an observable gameplay loop with its own evidence, pilot profile, implementation surface, and verification path. Start with low-risk mission/trade/navigation loops, then add outfitting/ship-ladder surfaces, and only later explore combat/piracy/privateering on disposable non-strict pilots.

**Tech Stack:** Original EV Classic in Basilisk II for runtime observation; Terminal Velocity Godot frontend under `godot_ev/`; Python/data model under `native_ev/`; durable tracking in `docs/research/` and `docs/checklists/`.

---

## Strategy niches

- **Mission runner / courier**: Mission Computer and Spaceport Bar jobs, passenger/cargo delivery, deadlines, route planning, mission cargo constraints, reputation hooks.
- **Commodity trader / merchant**: buy/sell goods across ports, price spreads, cargo-capacity planning, fuel/route safety, market discovery.
- **Pirate / privateer / looter**: prey on ships, disable/destroy targets, loot cargo/spoils, absorb legal/faction consequences. Use only disposable non-strict pilots for observation.
- **Faction/storyline operative**: build alignment and unlock faction-specific opportunities/consequences.
- **Outfitter / ship-ladder optimizer**: convert credits into weapons, outfits, escorts, ship upgrades, and better ships.
- **Mission-trader hybrid**: decide when a mission route should also carry commodities based on spare cargo, route alignment, capital tied up, deadlines, fuel/safety, and expected destination prices.
- **Ship trade-up planner**: decide when to buy a new ship versus keep or modify the current ship; learn opportunity cost, cargo/mission fit, combat survivability, hardening, storage capacity, speed/range, cash reserve requirements, and useful instruments/equipment.
- **Defensive readiness planner**: decide when weapons/outfits/escorts, ship hardening, or support instruments are needed for protection versus when speed, route choice, avoidance, or deliberate attack is the right move.
- **Explorer / route mapper**: discover topology, system properties, hazards, asteroid presence/density, hostile/pirate traffic, safe/profitable paths, and which original-game port services each system/body provides.
- **System provisioning verifier**: as new systems are explored, determine whether Terminal Velocity needs original-game stores, commodity exchanges, outfitters, weapon shops, shipyards, planet graphics, or other services provisioned to match EV Classic.

## Pilot policy

- Create multiple non-strict pilots for separate strategy tracks when useful.
- Keep Strict Play off unless explicitly directed otherwise.
- Do not use the reusable mission/trade pilot for destructive piracy/combat-risk experiments.
- Keep raw screenshots and emulator assets local-only unless explicitly reviewed for publication.

## Evidence order

1. Mission/trade/navigation on the current safe non-strict pilot.
2. Commodity spread observations across additional ports.
3. Opportunistic mission+trade observations after route/hyperspace is reliable.
4. Outfitting, ship stats, ship modification, cargo-capacity/storage expansion, hardening, support instruments, and ship purchase/trade-up UI/status observations.
5. Defensive readiness observations: whether weapons/outfits/escorts, hardening, or support instruments are needed for safe travel, whether systems contain asteroids or higher pirate/hostile traffic, when to avoid other ships, and when attacking is worthwhile or too risky.
6. Combat controls and defensive observations.
7. Per-system provisioning observations: for every newly reached system/body, capture and record original-game planet graphics and stores/services, including commodity exchange, outfitters, weapon availability, shipyards, bar/mission services, and absent services.
8. Piracy/privateering/legal/faction consequences on a disposable non-strict pilot.

## Tasks

### Task 1: Complete current passenger mission route learning

**Objective:** Learn enough departure/hyperspace/navigation behavior to complete `Ferry Passengers to New Istanbul` or record the exact blocker.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-behavior-baseline-checklist.md`
- Modify: `docs/checklists/ev-classic-original-runtime-observation-checklist.md`

**Steps:**
1. Capture current Basilisk state.
2. If in space near Levo, select hyperspace mode/destination and attempt controlled movement away from system center.
3. Record the successful hyperspace sequence or exact failure text/state.
4. Save named local-only captures under `C:\Games\BasiliskII\`.
5. Update docs/checklists with evidence label and remaining gap.

**Verification:** Capture path exists locally; docs contain exact visible text or explicit blocker.

### Task 2: Build a commodity spread observation pass

**Objective:** Establish that trading is a distinct skill loop by observing prices and cargo behavior at more than Levo.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- Potentially modify: `native_ev/data/economy.json`
- Potentially modify: `native_ev/tests/test_model.py`

**Steps:**
1. Start from a safe landed state.
2. Capture Levo baseline commodity screen if needed.
3. Travel to one reachable destination.
4. Capture destination Commodity Exchange.
5. Compare visible prices/status labels and hold/free-cargo values.
6. Only implement data changes if the observation is source-backed and bounded.
7. Run Python model tests if data/model changes are made.

**Verification:** At least one additional port has source-backed commodity evidence or an explicit blocker.

### Task 2a: Learn opportunistic trade-with-missions decisions

**Objective:** Learn when to buy goods while already taking a mission route, rather than treating missions and trading as separate loops.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- Potentially modify: `native_ev/data/economy.json`

**Steps:**
1. Start from a safe landed state with a known accepted mission and visible cargo/free-space status.
2. Record mission constraints: destination, deadline if visible, special/passenger/cargo slot usage, current credits, and free cargo.
3. Buy a bounded commodity lot only if it does not block the mission cargo/passenger requirement.
4. Travel the mission route and compare destination sell prices, remaining free cargo, fuel, and mission completion state.
5. Derive decision guidance from observed deltas: profitable carry-along, bad capital lockup, insufficient cargo, route mismatch, or deadline/safety risk.

**Verification:** One mission route has before/after cargo+credit+price evidence, or the blocker is named.

### Task 2b: Verify original system provisioning while exploring

**Objective:** As new systems or landable bodies are reached, determine whether Terminal Velocity needs original-game planet graphics and stores/services provisioned there.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- Potentially modify: `native_ev/data/universe.json`
- Potentially modify: `native_ev/data/economy.json`
- Potentially modify: ship/outfit/weapon data files if active data surfaces exist

**Steps:**
1. On first arrival at each new system/body, capture the in-space planet appearance if visible, then the landed main panel and every visible service screen before buying/selling.
2. Record exact original-game planet graphic evidence: visible planet art/thumbnail/background, color/shape features, landing-screen artwork if present, and any local capture/resource IDs if decoded later.
3. Record exact original-game service presence and absence: bar, mission computer, commodity exchange, outfitter, weapons, shipyard, escorts, and other store/instrument/equipment surfaces.
4. For commodity/stores/weapons, capture visible item names, prices/status labels, availability, and any requirements or absence messages.
5. Compare against Terminal Velocity active data and mark each surface as `matched`, `missing`, `scaffold`, `needs evidence`, or `not present in original`.
6. Only provision Terminal Velocity data when the original-game evidence is bounded and source-backed; otherwise record the gap without guessing from adaptation data.

**Verification:** Each newly explored system/body has a planet-graphics + provisioning note with evidence paths and an implementation/backlog decision.

### Task 3: Create separate non-strict pilot tracks

**Objective:** Preserve clean observation contexts for different strategy niches.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`

**Steps:**
1. Create or document pilot names for mission/trade, commodity-spread, outfitting/ship, and disposable combat/piracy tracks.
2. Confirm Strict Play is off for each pilot creation flow.
3. Capture the pilot creation/default-state evidence locally.
4. Record which pilot is used for which niche.

**Verification:** Docs list pilot track names, purpose, strict-play state, and local evidence paths.

### Task 4: Observe outfitting and ship-ladder surfaces

**Objective:** Learn where and how EV exposes ship stats, outfits, weapons, escorts, and purchases.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-behavior-baseline-checklist.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`

**Steps:**
1. Use a non-strict pilot with no risky commitments.
2. Locate a port with outfitter or shipyard services.
3. Capture visible stats/prices without buying/selling.
4. Record exact labels and evidence boundaries.
5. Add implementation candidates only where source-backed.

**Verification:** Starting equipment/ship-ladder checklist rows move from unknown to partial/source-backed, or the blocker is named.

### Task 4a: Learn ship trade-up, modification, and defensive-readiness decisions

**Objective:** Develop the player skill of deciding when to buy a new ship, when to modify the current ship, and when weapons/outfits/escorts are needed for survival.

**Files:**
- Modify: `docs/research/original-ev-classic-runtime-observations.md`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`

**Steps:**
1. Capture available shipyard/outfitter options without purchasing.
2. Record source-backed visible stats/prices: cargo, storage/capacity upgrades if shown, speed/acceleration if shown, armor/shields/hardening if shown, weapon/outfit slots, weapon availability, instrument/equipment availability, trade-in/cost if shown.
3. Compare each candidate against current mission/trade needs: cargo capacity, storage/capacity expansion, range/fuel, route risk, defensive survivability, instrument utility, and remaining cash after purchase.
4. Observe or decode threat/risk surfaces before claiming weapons are required; distinguish “needed to survive a route” from “useful for combat/piracy.” Track whether specific systems appear to have asteroids, more pirates, or hostile ships, and treat traffic/density as source-backed only when observed repeatedly or decoded from resources.
5. Treat purchase/trade-up decisions as reversible only if EV confirms that; otherwise do not mutate the reusable pilot without explicit scope.

**Verification:** At least one port exposes ship/outfit economics with captured stats/prices, or the blocker is named.

### Task 5: Plan disposable combat/piracy observation

**Objective:** Prepare but do not yet execute destructive or legally consequential tests.

**Files:**
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- Modify: `docs/checklists/ev-classic-original-runtime-observation-checklist.md`

**Steps:**
1. Define a disposable non-strict pilot for combat/piracy.
2. Identify safe first observations: targeting, firing, being shot at, escape, cargo drops, police/government response.
3. List stop conditions: low hull/shields, mission-pilot contamination, Strict Play accidentally enabled, unclear save state.
4. Do not execute piracy/death-risk tests until the checklist is ready.

**Verification:** Combat/piracy has a bounded checklist and explicit stop conditions before any destructive run.

### Task 6: Implement source-backed niche scaffolding in Terminal Velocity

**Objective:** Reflect observed strategy niches in Terminal Velocity without overbuilding unverified mechanics.

**Files:**
- Potentially modify: `native_ev/data/*.json`
- Potentially modify: `native_ev/tests/test_model.py`
- Potentially modify: `godot_ev/scripts/main.gd`
- Potentially modify: `godot_ev/scripts/self_test.gd`
- Modify: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`

**Steps:**
1. Pick one source-backed niche feature from the backlog.
2. Write/extend a test first for the smallest observable behavior.
3. Implement the minimal data/UI/model change.
4. Run Python tests and Godot selftest where applicable.
5. Mark backlog status with evidence and verification.

**Verification:** Tests pass and backlog status is updated to `implemented` or `verified` with evidence path.
