# Original EV Classic runtime observations

Date: 2026-05-19

Purpose: source-backed observation log for original Escape Velocity Classic running locally in Basilisk II. Raw captures remain local-only; this file records derived observations with evidence labels and provenance caveats.

## Environment / provenance

- Runtime: original EV Classic launched inside Basilisk II on the Think/Windows host.
- Emulator: Windows Basilisk II at `C:\Games\BasiliskII\`.
- ROM/boot disk route: local technical-bootstrap route with archive-sourced ROM/boot-disk provenance caveat; see `docs/checklists/ev-classic-original-runtime-observation-checklist.md`.
- Local-only capture root used in this pass: `C:\Games\BasiliskII\`.
- Evidence label for observations below: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.

## Observation protocol

1. Start from EV Classic title screen.
2. Open Set Prefs only as a prior visual baseline; do not use it for gameplay behavior.
3. Create a new pilot with default generated pilot name.
4. Accept default ship name when prompted.
5. Enter ship and wait through the intro until first playable in-space state.
6. Record derived facts only; keep screenshots local-only.

## 2026-05-19 new-pilot/start-state observation

Local-only captures:

- `C:\Games\BasiliskII\ev-new-pilot-after-ship-name.png`
- `C:\Games\BasiliskII\ev-new-pilot-enter-ship.png`
- `C:\Games\BasiliskII\ev-new-pilot-enter-ship-5s.png`
- `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`
- `C:\Games\BasiliskII\ev-new-pilot-player-info.png`

Derived observations:

- New pilot name prompt defaulted to `Rick Hardslab`.
- Ship christening prompt text: `Now, please christen your brand-new Rendell StarDrive 805R cargo shuttle:`.
- Ship name default: `Starseeker`.
- Title status panel after new pilot creation:
  - `Pilot Name: Rick Hardslab`
  - `Ship Name: Starseeker`
  - `Ship Type: Shuttlecraft`
  - `Levo system: Clean`
  - `Combat Rating: Harmless`
  - `Current Date: May 19th, 2276`
- First playable state: in space, not landed.
- First playable local context: near Levo.
- First playable HUD:
  - message: `Welcome to Escape Velocity - it would be a good idea to start by landing on Levo and checking out the prices. Hit ‘L’ to request landing clearance, then hit it again to land.`
  - `Credits: 10,000`
  - `Free: 20`
  - `No Secondary Weapon`
  - `No Target`
  - Shield and Fuel bars appear full.

## Terminal Velocity comparison notes

- `godot_ev/scripts/main.gd` already selected `shuttlecraft`; this matches the observed starting ship type.
- `godot_ev/scripts/main.gd` used `credits := 5000`; corrected to `credits := 10000` after this observation.
- `native_ev/data/universe.json` still starts at `Sol`, while original EV Classic start-state evidence points to Levo. This remains a mismatch because Levo-backed universe integration is not yet complete.
- Starting equipment remains partial: the first HUD proves no secondary weapon and free cargo space 20, but a full inventory/status screen was not captured in this automation pass.

## Open verification items

- Open player/ship info or a landed status/outfitter screen without changing inventory, to record exact starting weapons/outfits.
- Source-integrate Levo/system data from decoded EV Classic resources before changing Terminal Velocity’s `current_system_index`/universe start system.
- Cross-check the `Rendell StarDrive 805R cargo shuttle` prompt against decoded static resources if exact ship variant/resource naming matters.
