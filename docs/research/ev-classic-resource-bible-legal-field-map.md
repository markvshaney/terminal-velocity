# EV Classic Resource Bible legal/government field map

Source: `docs/references/ev-family/ev-classic-resource-bible.pdf` and extracted text `docs/references/ev-family/ev-classic-resource-bible.txt`.

Purpose: promote legal/faction pieces from generic inference to **Classic Resource Bible-backed resource-semantics claims** where the manual explicitly describes the data model. This does not by itself prove exact runtime timing, UI wording, stock data values, or combat-resolution tuning.

## Applied resource decode slice

A follow-up source-backed slice derives stock Classic `gövt` semantics from the local primitive resource decode:

- extractor: `tools/extract_ev_government_semantics.py`
- mission extractor: `tools/extract_ev_mission_semantics.py`
- outputs: `native_ev/data/sourced_ev_governments.json`, `native_ev/data/sourced_ev_missions.json`
- input: `native_ev/data/sourced_ev_structures.json`
- methods: `ev-classic-resource-bible-govt-field-map-v1`, `ev-classic-resource-bible-misn-field-map-v1`

Representative decoded stock values now under test:

- resource 128 / Confederation: `CrimeTol=50`, `SmugPenalty=3`, `KillPenalty=25`
- resource 129 / Rebellion: `CrimeTol=75`
- resource 130 / Pirates: `CrimeTol=-20`, xenophobic flag set
- resource 133 / Militia: `SmugPenalty=5`, `KillPenalty=20`
- 116 Classic `mïsn` records decoded through the manual-backed availability/travel/cargo/scan/pay/special-ship/completion fields, including `AvailStel`, `AvailBitSet`, `AvailLoc`, `AvailRecord`, `TravelStel`, `ReturnStel`, `CargoType`, `CargoQty`, `ScanGovt`, `FailIfScanned`, `PayVal`, `ShipCount`, `ShipSyst`, `ShipDude`, `ShipGoal`, `ShipBehav`, `CompBitSet`, `CompGovt`, `CompReward`, and `FailBitSet`.

These values can drive TV legal scaffolds as decoded Classic resource evidence, but TV-specific government names and systems still need a full stock-resource join before they become exact Classic faction placement.

## Strong Classic Resource Bible claims

### Government records are collective reputation/legal entities

Evidence, lines 179-183:

> A govt resource defines the parameters for a government, which is in turn defined as "any collection of ships and planets that react collectively to the actions of the player and other ships." Governments keep track of how they feel toward you, and they can also have set enemies and allies.

Terminal Velocity claim allowed:

- Tracking legal/reputation state per government is Classic resource-semantics faithful.
- Surfacing government-specific legal state in logs/UI is a faithful scaffold, though exact original UI wording remains unconfirmed.

### Crime tolerance gates hostile warship behavior

Evidence, lines 188-190:

> CrimeTol The maximum amount of evilness the player can accumulate before warships of this govt start to beat on him.

Terminal Velocity claim allowed:

- A government-specific `CrimeTol`-style threshold driving hostile patrol/warship posture is Classic resource-semantics faithful.
- Current TV numeric threshold is tuning data until stock Classic resources are decoded/mapped.

### Government penalties cover smuggling, disabling, boarding, killing, and shooting

Evidence, lines 191-198:

> SmugPenalty The amount of evilness a player gains for being detected smuggling illegal cargo (defined in a misn resource) past this government's ships.
>
> DisabPenalty The amount of evilness for disabling one of this govt's ships.
>
> BoardPenalty Evilness from pirating one of this govt's ships
>
> KillPenalty Evilness from killing this govt's ships
>
> ShootPenalty Evilness from shooting one of this govt's ships (currently ignored)

Terminal Velocity claim allowed:

- Legal/reputation consequences for smuggling and hostile action against government ships are Classic resource-semantics faithful.
- Current TV `destroy_patrol`, `contraband_fine`, and reputation deltas are scaffolding/tuning until exact stock field values and event mapping are decoded.
- Do not claim that shooting alone should alter EV Classic legal record, because the Classic Bible says `ShootPenalty` is currently ignored.

### Interceptors scan illegal cargo and enforce piracy-police behavior

Evidence, lines 120-125:

> 4 - Interceptor Seeks out his enemies, or parks in orbit around a planet if he can't find any. Buzzes incoming ships to scan them for illegal cargo. Also acts as "piracy police" by attacking any ship that fires on or attempts to board another, non-enemy ship while the interceptor is watching.

Terminal Velocity claim allowed:

- A scanner/patrol/interceptor legal surface that warns, scans cargo, and reacts to player attacks is Classic resource-semantics faithful.
- TV's current scan-on-landing shortcut is a playable scaffold; exact Classic scan trigger, range, cadence, and nearby-ship witness conditions need runtime/resource confirmation.

### Government flags include attack/bribe behavior

Evidence, lines 202-224:

> 0x0002 Ships of this govt will attack the player in non-allied systems if he's a criminal there ...
>
> 0x0004 Always attacks player
>
> 0x0008 Never attacks player
>
> 0x0200 Warships will take bribes.
>
> 0x2000 Freighters will take bribes.
>
> 0x4000 Planets of this govt will take bribes
>
> 0x8000 Ships of this govt taking bribes will demand a larger percentage of your cash supply, and their planets will always take bribes

Terminal Velocity claim allowed:

- Government-specific bribe/attack policy is Classic resource-semantics faithful.
- TV's current landed `C` clemency is only a stand-in for government/planet bribe semantics until the actual UI and data mapping are confirmed.

### Allied/enemy governments propagate reputation consequences

Evidence, lines 227-229:

> Doing evil deeds to one government will improve your rating with its enemies, and vice versa. Allied governments also communicate your actions, so attacking one government will make its allies hate you too.

Terminal Velocity claim allowed:

- Cross-government reputation deltas are Classic resource-semantics faithful.
- Exact ally/enemy graph and propagation magnitudes need decoded Classic data and/or runtime checks.

### Mission availability is explicitly gated by legal record

Evidence, lines 249-291, especially lines 273-277:

> AvailRecord What your legal record in this system must be for this mission to become available
>
> 0 ignored
>
> positive value record must be at least this high
>
> negative value record must be at least this low

Terminal Velocity claim allowed:

- Mission availability gates based on legal record are Classic resource-semantics faithful.
- TV's visible blocked-reason UI is a modern scaffold; original EV Classic mission-list wording/visibility of blocked missions needs runtime UI confirmation.

### Mission smuggling cargo can be illegal to a government and can fail when scanned

Evidence, lines 350-361:

> ScanGovt Which government considers your cargo illegal
>
> ... If you're scanned by a ship of this government, or any government that's not its enemy (important!) you'll get that government's SmugglePenalty added to your record.
>
> FailIfScanned Sets whether the mission fails if you're detected carrying the cargo
>
> 0 Mission doesn't fail if scanned
>
> Nonzero Mission fails if you're scanned

Terminal Velocity claim allowed:

- Mission cargo legality and scan-failure mechanics are Classic resource-semantics faithful.
- TV's commodity contraband scan is an adjacent playable scaffold; exact Classic commodity-vs-mission cargo distinction needs separate implementation.

### Mission completion/failure can alter government record

Evidence, lines 423-434:

> CompGovt Which government to use in determining how your record changes on completing this mission
>
> CompReward How much to increase your record with CompGovt ... if you fail the mission, that govt will take it personally and decrease your record by 1/2 the amount specified in CompReward.

Terminal Velocity claim allowed:

- Mission success/failure reputation/legal changes are Classic resource-semantics faithful.
- Current TV mission reward deltas can be promoted when tied to these fields.

### Mission PayVal can clean legal record

Evidence, lines 362-370:

> PayVal What you get if you're successful and you return to ReturnStel
>
> -10128 to -10255 Clean legal record with the govt with this ID

Terminal Velocity claim allowed:

- A mission reward that cleans legal record with a government is Classic resource-semantics faithful.
- This is a better Classic-backed route for legal-clearing than the current landed `C` clemency placeholder.

## Recommended implementation label changes

Use these labels for current deterministic logs:

- legal status: `sourceLabel=terminal-velocity-classic-resource-legal-semantics`, `oracleStatus=classic_runtime_thresholds_pending`
- patrol warning/hostility: `sourceLabel=terminal-velocity-classic-resource-patrol-semantics`, `oracleStatus=classic_runtime_combat_timing_pending`
- hostile action consequence: `sourceLabel=terminal-velocity-classic-resource-govt-penalty-semantics`, `oracleStatus=classic_runtime_combat_resolution_pending`
- mission legal availability: `sourceLabel=terminal-velocity-classic-resource-mission-availability`, `oracleStatus=classic_runtime_ui_wording_pending`
- contraband/smuggling scan: `sourceLabel=terminal-velocity-classic-resource-smuggling-scan-semantics`, `oracleStatus=classic_runtime_scan_frequency_and_fine_tuning_pending`
- landed `C` clemency: keep as `inferred` or rename to government/planet bribe scaffold until actual Classic UI/data mapping is implemented.

## Remaining promotion work

1. Decode stock Classic `gövt`, `düde`, and `mïsn` resources to replace TV-tuned placeholder values with resource-derived values.
2. Add a proper mission-cargo `ScanGovt` / `FailIfScanned` slice separate from general commodity contraband.
3. Add government ally/enemy propagation from decoded resource data.
4. Replace landed `C` clemency with Classic-backed planet/warship/freighter bribe semantics or mission `PayVal` legal-record cleaning.
5. Capture runtime UI for exact wording, encounter timing, scan cadence, and combat behavior.
