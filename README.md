# Terminal Velocity

Native Windows 11 desktop space game prototype aiming at faithful Escape Velocity Nova-style play.

## Target runtime

This project no longer targets Chrome/browser/Vite. The browser prototype was archived at:

```text
archived-browser-prototype-2026-05-15/
```

The active game is a native Windows PowerShell/WPF desktop app:

```text
native_ev/windows/TerminalVelocity.ps1
```

It uses locally extracted, authorized EV sprite frames from:

```text
native_ev/assets/ships/shuttle/frame_00.png ... frame_35.png
```

Do not redistribute original or extracted EV assets outside the permitted local project context.

## Run

From WSL:

```bash
./run_game.sh
```

From Windows PowerShell:

```powershell
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File C:\Users\bh\Games\TerminalVelocity\TerminalVelocity.ps1
```

No-human smoke test:

```powershell
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File C:\Users\bh\Games\TerminalVelocity\TerminalVelocity.ps1 -SelfTest
```

## Controls

- `W` / `Up`: thrust
- `A` / `Left`: turn counter-clockwise
- `D` / `Right`: turn clockwise
- `S` / `Down`: brake/reverse
- `E`: land/dock when close and slow
- `Space`: fire primary weapon
- `T`: target nearest scanner contact
- `Y`: cycle scanner targets
- `L`: launch from landing screen
- `1`-`5`: accept listed cargo job while landed
- `F1`-`F5`: accept listed mission while landed
- `F6`: save game to `savegame.json`
- `F7`: load game from `savegame.json`
- `6`: repair hull while landed
- `7`-`9`: buy listed outfitter upgrades while landed
- `C` / `V`: select commodity while landed
- `X`: buy one ton of selected commodity while landed
- `Z`: sell one ton of selected commodity while landed
- `G`: cycle shipyard selection while landed
- `B`: buy selected shipyard ship while landed
- `H`: hyperspace to selected linked system
- `M`: open/close galaxy map
- `N` / `P`: select next/previous hyperspace destination
- `R`: reset ship in current system
- `Esc`: quit

## Current slice

- Native Windows desktop window, no browser.
- File-backed universe data loaded from `native_ev/data/universe.json`: 9 systems with connected jump routes, mapped coordinates, and multiple ports.
- First original-name fidelity slice: `tools/extract_ev_data_names.py` reads local `source-assets/ev-classic/Nova Files/EV Data.rez` BRGR chunks and writes provenance-preserving seeds to `native_ev/data/sourced_ev_names.json`; the active 9-system map now uses a seed set of sourced EV Classic system/landing names while topology/coordinates remain local remake scaffolding.
- First structured-resource fidelity slice: `tools/extract_ev_structured_records.py` decodes fixed-size BRGR record runs from local `EV Data.rez` into `native_ev/data/sourced_ev_structures.json`, including candidate `syst-like` 88-byte records, `spob-like` 400-byte records, ship-like, weapon-like, outfit-like, commodity-like, and mission-like runs with byte offsets and provisional confidence labels. Field semantics are not overclaimed yet; this is the source-backed base for replacing local topology/port scaffolding next.
- File-backed ship/NPC traffic data loaded from `native_ev/data/ships.json`.
- File-backed weapons data loaded from `native_ev/data/weapons.json`.
- File-backed outfit/shipyard/repair data loaded from `native_ev/data/outfits.json`.
- File-backed commodity markets loaded from `native_ev/data/economy.json`.
- File-backed governments, contraband, scan ranges, and fines loaded from `native_ev/data/governments.json`.
- Original 36-frame shuttle and light-freighter facings extracted from local EV resources.
- Inertial flight.
- EV-style ports, landing screen, jobs board, credits, deliveries.
- Cargo jobs now use route distance and destination risk to calculate payouts; far or hostile/low-law routes pay more.
- File-backed mission computer with accepted story missions, cargo reservation, completion, and rewards.
- Story flags gate mission-chain progression: accepting/completing missions can set flags, follow-up missions unlock only when prerequisites are met, and `excludesFlags` / `choiceGroup` support mutually exclusive branch choices.
- Current story branch: after the Luna → Sirius Station sample transfer, the captain can choose a Federation report path or a Sirius quiet-pact path; accepting one hides the other.
- Persistent save/load stores credits, system, ship, hull/fuel, cargo, outfits, commodities, active/completed missions, story flags, and legal status in local `savegame.json`.
- Outfitter upgrades, repair shop, and shipyard purchase loop while landed.
- Commodity exchange with per-system buy/sell prices and realized profit tracking.
- Government/law system with patrol scans, contraband seizure, fines, and legal-status HUD/landing readout.
- Laser/pulse projectile combat, hull damage, hostile NPC fire, and bounties.
- EV-style scanner target lock, target reticle, target cycling, and target hull/range readout.
- Ambient NPC traffic using file-backed ship definitions across core, border, and rim systems.
- Multi-system hyperspace loop with galaxy-map destination selection and file-backed jump links.
- Self-test/autopilot mode for no-human launch verification.
- Source assets and extraction tooling retained under `source-assets/` and `tools/`.

Next fidelity step: map the decoded `syst-like` and `spob-like` word offsets to concrete fields — coordinates, links, governments, landing flags, and port metadata — with per-field provenance before replacing the local universe scaffold.
