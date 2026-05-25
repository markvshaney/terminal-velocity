# EV-family gameplay source deep dive

Date: 2026-05-21

Purpose: mine public EV Classic, Escape Velocity: Override, and Escape Velocity Nova sources for transferable gameplay lessons for Terminal Velocity. This is not a source-of-truth artifact for exact EV Classic runtime fidelity; use original runtime observation and decoded resources for that. External EV-family sources here are strategy/design-learning sources and hypothesis generators.

User guidance captured for this pass: basic gameplay is shared across EV Classic, EV Override, and EV Nova, so Override/Nova gameplay sources are relevant for learning the Terminal Velocity loop.

## Source quality labels

- `primary/manual-adjacent`: official or near-official manuals, keyboard overlays, data-derived walkthroughs, resource bibles.
- `community-guide`: player-authored FAQ/guide/walkthrough; useful but may contain opinion, version assumptions, or spoilers.
- `community-wiki/archive`: wiki/forum/archive material; useful for discovery and pain points, verify exact mechanics elsewhere.
- `implementation-reference`: open-source reimplementation or EV-inspired engine; useful for engineering patterns and semantic questions, not canon.

## High-value source map

### Manuals, overlays, and manual-adjacent docs

- EV Classic keyboard overlay: https://www.bobheffner.com/overlays/evv1xt.pdf
  - Quality: `primary/manual-adjacent`.
  - Use for: controls, map/mission/player info access, landing destination, secondary weapons, shift-click style route plotting.
  - Lesson: player-facing control discovery matters; navigation and mission status must be one-key accessible.

- EV Nova User Guide PDF: https://download.escape-velocity.games/extras/EV%20Nova%20User%20Guide.pdf
  - Quality: `primary/manual-adjacent`.
  - Use for: shared EV-family basics: controls, navigation, landing/takeoff, map, missions, trading, combat, outfitter/shipyard, escorts.
  - Lesson: because the basic gameplay loop is shared, Nova docs can inform Terminal Velocity tutorial/manual structure even where exact Classic fidelity still needs original-runtime verification.
  - Extraction note: the `+` URL form returned 404 during the 2026-05-21 pass; the `%20` URL form returned the PDF. Local PDF text extraction was noisy because the available environment lacked robust PDF text tooling, so do not quote it until re-extracted with `pdftotext`, `pypdf`, or equivalent.

- EV Nova walkthroughs index: https://escape-velocity.games/EVN_Walkthroughs/html/index.html
  - Quality: `primary/manual-adjacent` / data-derived community reference.
  - Use for: mission flow, legal/combat prerequisites, cargo/time/pay fields, storyline chains.
  - Lesson: mission systems need clear structured metadata: start location, prerequisites, deadline, cargo/passenger burden, pay, reputation/legal consequences, next mission.

- EV Nova Bible: https://andrews05.github.io/evstuff/guides/evnbible.html
  - Quality: `primary/manual-adjacent` technical reference.
  - Use for: resource/system semantics: ships, outfits, governments, legal status, mission bits/control bits.
  - Lesson: Terminal Velocity should keep gameplay data inspectable and modder-friendly; mission/faction state should be cleanly modeled.

- EVO political map: http://www.cytheraguides.com/archives/ambrosia_addons/evo/Guides/2381_EVOPoliticalMap04.pdf
  - Quality: `community-archive` but high-value for route/faction planning.
  - Use for: government territories, spatial route planning.
  - Lesson: map overlays for government, danger, services, commodity hints, shipyards/outfitters, and mission destinations are not extras; they are core strategy support.

- EVO Resource/Override Bible: http://www.cytheraguides.com/archives/ambrosia_addons/evo/Guides/2386_OverrideBible102.pdf
  - Quality: `primary/manual-adjacent` technical/modding reference.
  - Use for: mission bits, governments, disasters, resource concepts.
  - Lesson: expose enough state for tools and modding without forcing ordinary players into raw internals.

### Classic / Override / Nova guide sources

- EV Classic GameFAQs guide index: https://gamefaqs.gamespot.com/mac/575197-escape-velocity-1996/faqs
- EV Classic FAQ by AKishan: https://gamefaqs.gamespot.com/mac/575197-escape-velocity-1996/faqs/2600
  - Quality: `community-guide`.
  - Use for: ship stats, weapons, outfits/extras, progression advice.
  - Lesson: players need comparative ship/outfit info; in-game shipyard/outfitter UI should reduce spreadsheet dependence.

- EVO GameFAQs guide/walkthrough by Lord_Seth: https://gamefaqs.gamespot.com/mac/581097-escape-velocity-override/faqs/29907
- EVO FAQ by Capt_Falcon: https://gamefaqs.gamespot.com/mac/581097-escape-velocity-override/faqs/21023
  - Quality: `community-guide`.
  - Use for: faction mission chains, legal/combat requirements, early money-making, cargo mission stacking, route planning.
  - Lesson: early game should teach mission stacking, map use, cargo capacity as first progression lever, and where major factions begin.

- EV Nova GameFAQs ship guide: https://gamefaqs.gamespot.com/mac/578133-escape-velocity-nova/faqs/23469
- EV Nova Vell-os guide: https://gamefaqs.gamespot.com/pc/562562-escape-velocity-nova/faqs/51750
  - Quality: `community-guide`.
  - Use for: ship evaluation, outfitting strategy, faction/storyline example.
  - Lesson: ship progression should support role-specific sidegrades: courier, cargo hauler, armed merchant, interceptor, gunship, carrier, capital hunter.

- Hellfire McQueen EVO ship guide: https://docmaker.whpress.com/files/evo-ship-guide/ and https://archive.org/details/hellfire_EVO_ship_guide
  - Quality: `community-guide`.
  - Use for: ship stats and practical role analysis.
  - Lesson: surface ship role identity and tradeoffs: cargo, outfit space, armor/shields, speed, maneuverability, crew, cost, fuel/range.

### Wikis, archives, and community surfaces

- EVN Wiki home: https://evn.fandom.com/
- EV Classic overview: https://evn.fandom.com/wiki/Escape_Velocity
- EV Override overview: https://evn.fandom.com/wiki/Escape_Velocity_Override
- EV Nova overview: https://evn.fandom.com/wiki/Escape_Velocity_Nova
- Missions: https://evn.fandom.com/wiki/Missions_(EVN)
- Legal status: https://evn.fandom.com/wiki/Legal_status
- Combat rating: https://evn.fandom.com/wiki/Combat_Rating
- Trading: https://evn.fandom.com/wiki/Trading
- Trade routes: https://evn.fandom.com/wiki/Trade_Routes
- Ships: https://evn.fandom.com/wiki/Ships_(EVN)
- Outfits: https://evn.fandom.com/wiki/Outfits_(EVN)
- Tutorial: https://evn.fandom.com/wiki/Tutorial
- AgGro's New Pilot Guide: https://evn.fandom.com/wiki/AgGro%27s_New_Pilot_Guide
- Close Combat Guide: https://evn.fandom.com/wiki/Close_Combat_Guide
  - Quality: `community-wiki/archive`.
  - Use for: structured overview, player-facing terminology, ship/outfit/faction/legal concepts, new-player pain points.
  - Lessons:
    - Legal/reputation should be local to governments, not a single global morality score.
    - Combat rating is a non-money progression axis that can gate high-risk missions.
    - Regional shipyard/outfitter inventory and licenses make exploration meaningful.
    - New-pilot guidance should exist in-game, not only in external guides.

- Cythera Guides Ambrosia add-on archives:
  - EVO: http://www.cytheraguides.com/archives/ambrosia_addons/evo/
  - EV Nova: http://www.cytheraguides.com/archives/ambrosia_addons/evn/
  - Quality: `community-wiki/archive`.
  - Use for: preserved Ambrosia-era guides, maps, mission workbooks, plugins.
  - Lesson: old community docs are fragile; Terminal Velocity should ship durable static docs plus in-game reference surfaces.

- Ambrosia Garden / forum archives:
  - Resources: https://community.ambrosia.garden/d/5-resources
  - Trade route example: https://archive.ambrosia.garden/topic/12316/what-are-good-trading-routes-for-money-
  - Mission-start discovery: https://archive.ambrosia.garden/topic/13348/where-to-go
  - Citizen/legal rating: https://archive.ambrosia.garden/topic/13374/how-to-raise-my-citizen-rating-
  - Quality: `community-wiki/archive`.
  - Use for: player pain points and practical strategy questions.
  - Lessons:
    - Players ask “where do I go next?”, “how do I improve reputation?”, “what route makes money?”, and “which ship should I buy?”
    - Terminal Velocity should answer these in-world through rumors, mission boards, faction contacts, map overlays, ship comparison, and a progress log.

### Implementation and open-source comparison sources

- OpenNova: https://github.com/dmaulikr/OpenNova and https://opennovablog.wordpress.com/
  - Quality: `implementation-reference`.
  - Use for: EV Nova reimplementation architecture, movement/resource/pilot reverse-engineering questions.

- NovaJS: https://github.com/mattsoulanille/NovaJS and https://novajs.net
  - Quality: `implementation-reference`.
  - Use for: browser implementation of EV Nova-like runtime and plugin assumptions.

- KestrelEngine: https://github.com/Evocation-Games/KestrelEngine
  - Quality: `implementation-reference`.
  - Use for: modern EV-family remaster engine patterns, resource packs, Lua logic, plugin/resource replacement semantics.

- evnova-utils: https://github.com/vasi/evnova-utils
  - Quality: `implementation-reference` / technical community tooling.
  - Use for: examining EV/EVO/EVN internals, pilot/resource docs, mission workbook artifacts.

- Endless Sky: https://endless-sky.github.io/ and https://github.com/endless-sky/endless-sky/wiki/PlayersManual
  - Quality: `implementation-reference` for EV-inspired open source, not EV canon.
  - Use for: mission system, outfitter/shipyard, cargo/passengers, fleet, route planning, plugin docs.

- Naev: https://naev.org/
  - Quality: `implementation-reference` for EV-inspired open source.
  - Use for: alternative mission/faction/trading/combat design comparison.

## Source-grounded deeper model from extracted references

This section records the stronger pass requested after the initial source list. Evidence came from locally extracted text under `/tmp/ev-source-deep-dive-20260521/text/`, primarily the EV Nova data-derived walkthrough index and the EV Nova Bible. Treat this as `source-grounded EV-family model`, not exact EV Classic behavior.

### Mission availability and state

Evidence:

- The EVN walkthrough index says its walkthroughs are based on data extracted from Ambrosia Software's EV Nova 1.0.3 and organized mission-by-mission.
- Its mission key documents acquisition surfaces and gates: `Available from`, `Travel to`, `Return to`, `Ship Location`, `Ship Goal`, `Location`, `Random`, `Legal Record`, `Combat Rating`, `Ship Type`, `Cargo`, `Time Limit`, `Pay Type`, and control-bit expressions such as `AvailBits`, `OnAccept`, `OnSuccess`, `OnFailure`, `OnAbort`, and `OnShipDone`.
- It defines `Random` as the percentage chance a mission is available, calculated separately for each eligible planet/station whenever the pilot enters a system.
- The Nova Bible similarly says `AvailRandom` prevents missions from always being available and that mission randomizing values are recalculated each time the player warps into a system.
- The Nova Bible lists `Max Simultaneous Missions 16`.

Terminal Velocity implications:

- Model missions as structured state machines, not just text cards. Minimum state fields should include offer surface, acceptance state, travel-destination state, return-destination state, special-ship-goal state, deadline/failure/abort state, cargo/passenger reservation, pay, and faction/legal effects.
- Mission availability should be explainable where appropriate: blocked by cargo, legal status, combat rating, ship class, prior mission state, location/service, random refresh, or faction/story lockout.
- The mission log should show the next actionable step: travel, return, kill/disable/board/escort/observe/rescue, wait, or complete.
- If Terminal Velocity adopts random postings, make refresh rules legible so players learn to travel/revisit rather than thinking a board is broken.

### Mission surfaces and player habit formation

Evidence:

- The EVN walkthrough key lists possible mission locations as Mission Computer/BBS, Bar, Person Ship, Main Spaceport, Trading Center, Shipyard, and Outfitter.
- Extracted side/faction examples show missions appearing in Bar, Outfitter, and faction/government locations, with different legal/combat/cargo gates.

Terminal Velocity implications:

- Preserve distinct mission surfaces. The Mission Computer teaches public jobs, the Bar teaches rumors/contacts, the Trading Center teaches commerce-linked work, and Shipyard/Outfitter surfaces teach equipment- or license-linked progression.
- Do not flatten every job into one universal board unless a deliberate modern accessibility layer preserves the original surface identity.

### Navigation, map arrows, fuel, and jump constraints

Evidence:

- The Nova Bible lists `Jump Distance 1000 pixels`.
- It describes HUD/interface fields for `FuelArea`, `FuelFull`, `FuelPartial`, and `NavArea`.
- Mission flags can `Show green arrow on map in initial briefing` and `Show an additional arrow on the map for the ShipSyst`.
- Some mission flags can take away 100 fuel on auto-abort and prevent mission offer if the player has less than 100 fuel.

Terminal Velocity implications:

- Hyperspace/fuel should be taught as concrete route planning, not hidden button magic. The game needs visible fuel/jump units, partial-fuel handling, and feedback when jump conditions are not met.
- Map arrows are first-class mission UI. Support separate arrows for travel/return destinations and special-ship systems.
- Mission acceptance should preview fuel/cargo/deadline risk. A mission that consumes or requires fuel should say so.

### Government, legal status, and faction behavior

Evidence:

- The Nova Bible defines a government as a collection of ships and planets that react collectively to actions by the player and other ships.
- It states governments track how they feel toward the player and may have enemies/allies.
- The walkthrough index and Nova Bible describe legal status as based on the crime tolerance of the system's government.
- Government flags affect behavior such as attacking criminals, never attacking the player, accepting bribes, demanding larger bribes, suppressing distress/greetings, roadside assistance/free repair/refuel, and hypergate/wormhole/jump preferences.

Terminal Velocity implications:

- Use per-government legal/reputation state. A single global morality score is too weak for EV-style play.
- Government state should drive landing rights, patrol aggression, bribe availability/cost, mission eligibility, shipyard/outfitter access, distress calls, and AI route behavior.
- Mission success/failure should be able to adjust the primary government, allies, and enemies separately.

### Combat rating and combat-gated progression

Evidence:

- The EVN walkthrough index says combat rating is based on kills, specifically the sum of destroyed ships' strengths times an internal multiplier.
- Mission examples extracted from Federation/Polaris pages show combat rating gates such as `Combat Rating: 150` or `Combat Rating: 200`.

Terminal Velocity implications:

- Combat reputation should be a separate progression axis from credits and faction standing.
- Higher-risk missions should be gated by combat credibility, and the UI should explain that the player lacks sufficient combat rating rather than hiding the mission silently when that is better for learning.

### Trade, cargo, and economy events

Evidence:

- Mission fields include required free `Cargo`; examples include cargo burdens from 1 to 20 tons.
- The Nova Bible lists cargo/commodity limits and commodity purchase-location fields such as `BoughtAt1-8`.
- It also includes disaster records that can affect commodity prices.

Terminal Velocity implications:

- Cargo is a shared strategic constraint across trade and missions. Mission cargo/passenger reservations must be visible in both mission and trade screens.
- Trade should be place-based and event-sensitive: known buy/sell markets, route profit per jump/day, fuel/refuel risk, and disaster/news effects.
- Commodity discovery should be retained as player knowledge, not require memorizing external guides.

### Ships, outfits, and upgrade consequences

Evidence:

- The Nova Bible says outfit resources store items bought via `Outfit Ship`.
- Outfit fields include `Mass`; outfit types can add weapons, modify effective crew/marines for capture odds, represent permits/intangible purchases, be unsellable, or persist across ship changes.
- Ship-changing script commands can preserve or reset outfits differently.

Terminal Velocity implications:

- Ship/outfit progression needs explicit consequences: mass, cargo/outfit space, crew/capture effects, weapon roles, license/permit gates, resale restrictions, and persistence across hull changes.
- Shipyard and outfitter comparison screens should show deltas before purchase. EV-family players rely on external ship/outfit guides when this is opaque.

### Source boundary

- `source-grounded`: EVN walkthrough index, extracted faction/side mission pages, EV Nova Bible.
- `runtime-observed`: local Basilisk captures from 2026-05-21 showed EV Classic landing, Mission Computer, Mission Info, map zoom, and some hyperspace-control confusion; do not use those as exact mechanics until recaptured cleanly.
- `blocked/low-confidence`: EVN Fandom, GameFAQs, and Neoseeker pages were blocked by Cloudflare/403 during this pass; search snippets and prior guide links are discovery aids only.
- `needs Classic confirmation`: exact EV Classic keybindings, jump-distance behavior, mission field names/limits, combat-rating scaling, government/legal formulas, trade/disaster mechanics, and ship/outfit persistence.

## Transferable gameplay pillars for Terminal Velocity

### 1. Shared EV-family core loop

The common loop across EV Classic, Override, and Nova:

1. Start weak in a small ship.
2. Land on worlds to find missions, trade goods, rumors, outfits, ships, and faction contacts.
3. Take cargo/passenger/combat/story jobs.
4. Use the map to plan fuel-safe and politically safe routes.
5. Survive travel, pirates, hazards, and hostile governments.
6. Convert money/reputation/combat rating into better ships, outfits, escorts, and faction access.
7. Unlock harder routes and storylines.

Terminal Velocity should preserve this loop before adding complexity.

### 2. Mission-running lessons

- Mission systems need both generic jobs and authored story chains.
- Important mission fields:
  - start location/service
  - destination(s)
  - deadline/date
  - cargo/passenger burden
  - pay and consequences
  - combat rating requirement
  - legal/faction standing requirement
  - required prior mission bits
  - mutual-exclusion/lockout risks
- Player support:
  - mission log with destination, deadline, cargo/passenger burden, and route preview
  - spoiler-light hints for faction openers
  - visible reason when a known contact/job is unavailable, where appropriate
  - completion/failure history for durable learning

### 3. Trade and economy lessons

- Trading must be viable, not filler.
- Good route evaluation combines:
  - buy/sell spread
  - cargo capacity
  - profit per jump / profit per day
  - fuel cost and refuel stops
  - pirate/hostile-system risk
  - legal/contraband risk
  - escort/freighter strategy
- UI affordances:
  - map commodity overlays
  - local price history after discovery
  - known best buy/sell markets for discovered systems
  - risk warnings before committing a route
  - player notes/bookmarks for profitable loops

### 4. Navigation/map lessons

- The map is a strategic screen, not just a list of destinations.
- Useful overlays:
  - government/political control
  - known services: trading, outfitter, shipyard, bar, mission computer
  - hazard/danger/pirate activity
  - commodity hints and price history
  - mission destinations/deadlines
  - fuel/range/refuel stops
- Route planning should warn about insufficient fuel, hostile territory, dangerous routes, or illegal cargo.

### 5. Combat lessons

- EV combat works because arcade handling and RPG outfitting interact.
- Combat depth sources:
  - inertia and turn rate
  - thrust/speed/escape ability
  - primary vs secondary weapon roles
  - range control and reload timing
  - armor/shields vs maneuverability
  - escorts/fighters/carrier escalation
  - combat rating gates
- Teach combat through safe missions or simulator-style challenges before punishing story combat.

### 6. Ship and outfit progression lessons

- Avoid a single “bigger is better” ladder.
- Role archetypes to support:
  - shuttle/courier
  - scout/explorer
  - cargo hauler
  - armed merchant
  - raider/privateer
  - interceptor
  - heavy gunship
  - carrier/frigate/capital command ship
- Shipyard/outfitter UI should expose comparisons:
  - price
  - cargo
  - outfit space / mass constraints
  - armor/shields
  - speed/acceleration/turn
  - fuel/range
  - crew
  - weapons/secondary/fighter capacity
  - legal/faction/license requirements
- Regional/faction equipment and licenses make exploration strategically meaningful.

### 7. Faction/legal/reputation lessons

- Reputation should be government/faction-specific.
- Factions should affect:
  - hostility and patrol behavior
  - landing rights
  - mission availability
  - legal/crime tolerance
  - shipyard/outfitter inventory
  - licenses and special tech
  - tribute/domination consequences where applicable
- Faction exclusivity/lockouts should be telegraphed before irreversible choices.

### 8. Documentation and in-game learning

The existence of many long-lived external guides shows what players need:

- beginner guide
- keyboard overlay
- ship guide
- combat guide
- trading guide
- faction/storyline hints
- mission checklist/log
- map/service reference
- troubleshooting/preservation docs

Terminal Velocity should ship these as both static docs and in-game surfaces. Avoid making Discord/forum search the only way to learn.

## Concrete Terminal Velocity backlog candidates

- Add a player-facing keyboard overlay/manual page matching the EV-style control family.
- Add map overlays for government, services, mission destinations, hazards, and known trade data.
- Add mission log fields for deadline, cargo/passenger burden, pay, legal/faction effects, and route preview.
- Add shipyard/outfitter comparison panels with role tags and mass/capacity constraints.
- Add spoiler-light faction-contact hints and clear lockout warnings.
- Add a new-pilot/tutorial sequence that teaches landing, map, mission computer, commodity exchange, outfitter, and first hyperspace route.
- Add persistent player notes/bookmarks for trade routes and systems.
- Keep an implementation/reference lane for OpenNova/NovaJS/Kestrel/Endless Sky/Naev, but never promote their behavior as original EV Classic truth without primary verification.

## Verification and caveats

- This pass used web search and known URLs. Some extraction/browser tooling was unavailable in subagents, so not every page was fully extracted.
- Treat sources as learning/reference material. Exact Classic runtime behavior still requires Basilisk observation or decoded EV Classic resources.
- Do not copy raw proprietary mission strings, assets, or game data into public repo artifacts without review.
