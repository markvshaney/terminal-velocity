# EV Classic original-runtime observation setup checklist

Date: 2026-05-18

Purpose: live execution surface for getting from local Think-laptop materials to source-backed original Escape Velocity Classic runtime observations, without committing proprietary ROM/OS/game files or letting EV Classic-for-Nova stand in as original-runtime truth.

Related plan artifact: `docs/plans/2026-05-18-original-ev-classic-emulator-observation.md`

Related behavior baseline checklist: `docs/checklists/ev-classic-behavior-baseline-checklist.md`

Related emulator route recommendation: `docs/research/2026-05-18-ev-classic-emulator-route-recommendation.md`

Related Mac OS requirements artifact: `docs/research/2026-05-18-classic-mac-os-requirements-for-basilisk-ev.md`

Related ROM acquisition options artifact: `docs/research/2026-05-18-basilisk-compatible-rom-acquisition-options.md`

## Source hierarchy for this checklist

1. Original EV Classic running under an authorized Classic Mac emulator environment: primary runtime truth.
2. Decoded EV Classic resources and original/manual documentation: primary static/source truth.
3. EV Classic-for-Nova on EV Nova: runnable comparison/adaptation only; useful for hypotheses and workflow, not original-runtime truth.

## Guardrails

- Do not download ROMs, Mac OS installers, or commercial game files from unauthorized sources.
- Do not commit ROMs, OS images, original game apps/installers, emulator disks, save files containing proprietary blobs, or raw proprietary captures.
- Keep emulator assets outside the repo at `/home/bh/workspaces/loki/ev-classic-emulator/` unless a future reviewed decision says otherwise.
- Record only paths, sizes, hashes, provenance notes, and derived observations in repo artifacts.
- Label EV Classic-for-Nova observations as `external-adaptation-observed` unless independently verified against original runtime or decoded/manual evidence.

## Local material inventory

- [x] Original EV Classic Mac installer located.
  - Status: completed 2026-05-18
  - Path: `/mnt/c/Users/bh/Downloads/EV_Installer_1.0.5.bin`
  - Type evidence: `file` reports `MacBinary II`, creator `VIS3`, type `application`, title `Escape Velocity Installer`.
  - Size: 5,401,984 bytes
  - SHA256: `5c6b8ed5ee1efb67f3f7cbe62b051f36d26753337f18a238febbdc023ef0a5a2`

- [x] EV Nova Windows runtime located.
  - Status: completed 2026-05-18
  - Path: `/mnt/c/Games/EV Nova/EV Nova.exe`
  - Size: 1,697,280 bytes
  - SHA256: `0465342781627fcdf23082c587710cee411e2ad3cc3c84c84c53864ce02f3a5e`
  - Use: runnable host for EV Classic-for-Nova only; not original EV Classic runtime truth.

- [x] EV Classic-for-Nova active plugin located.
  - Status: completed 2026-05-18
  - Launcher path: `/mnt/c/Games/EV Nova/Nova Plugins/Play Escape Velocity.nplay`
  - Launcher SHA256: `ff857b87452b253cfb4d267c4e784d00c98e27737b7f4f60a42aabc997d4cc7e`
  - Declared name/version: `EV Classic for Nova` `1.1.6`
  - Use: adaptation/reference workflow only; do not promote observations to original-runtime truth.

- [x] EV Classic-for-Nova download archive located.
  - Status: completed 2026-05-18
  - Path: `/mnt/c/Users/bh/Downloads/EV_Classic_for_Nova (1).zip`
  - Size: 7,599,355 bytes
  - SHA256: `e827e2a0a5d0fab0481e31b1e9078add0da4df46235706b89e1511fe0b0c7d3d`

- [x] EV Nova legacy download archive located.
  - Status: completed 2026-05-18
  - Path: `/mnt/c/Users/bh/Downloads/EV Nova (legacy).zip`
  - Size: 98,190,116 bytes
  - SHA256: `7d31041e2a056d8d6f4098f26cba3b7eda4b030b7e5ecf8f97e46e7d8b908583`

- [x] EV Game Expander for Nova archive located.
  - Status: completed 2026-05-18
  - Path: `/mnt/c/Users/bh/Downloads/EV Game Expander for Nova 1.1 (2).zip`
  - Size: 19,038,995 bytes
  - SHA256: `6798f5aa7531749bc85555aa37e14e4b321639227af83d3c01c13da4c2755e7d`

- [x] Classic Mac ROM located/staged for technical bootstrap.
  - Status: completed/staged locally 2026-05-19 with provenance caveat.
  - Earlier search result: no obvious user-owned `Basilisk`, `SheepShaver`, or `Mac*ROM*` file was found under `/mnt/c/Users/bh` during the 2026-05-18 search.
  - Clean route remains: dump from an owned/borrowed compatible color-capable 68k Mac if publishable/provenance-clean evidence is needed.
  - Bootstrap decision: archive-sourced Basilisk-compatible 68k Macintosh ROMs are acceptable for local runtime bootstrap when needed; observations using this route carry a ROM provenance caveat.
  - Local ROM manifest: `/home/bh/workspaces/loki/ev-classic-emulator/local/roms/ROM-MANIFEST.local.md`
  - Selected ROM path: `/home/bh/workspaces/loki/ev-classic-emulator/local/roms/F1ACAD13 - Quadra 610,650,maybe 800.ROM`
  - Selected ROM SHA256: `05ad753fb594e656cf078023ec189e09e2a7655a780de993b75b8c51ed6b09ca`

- [x] Compatible Classic Mac OS install/media located/staged.
  - Status: completed/staged locally 2026-05-18; bootable disk image selected 2026-05-19 with provenance caveat.
  - Search result: no compatible Mac OS media was identified during the 2026-05-18 search.
  - User update 2026-05-18: user does not have any Mac OS media.
  - Found 2026-05-18: Apple-hosted System 7.5.3 installer parts are directly reachable from `download.info.apple.com`; all 19 expected parts responded `200 OK` to HEAD checks.
  - Source artifact: `docs/research/2026-05-18-classic-mac-os-requirements-for-basilisk-ev.md`
  - Local staging path: `/home/bh/workspaces/loki/ev-classic-emulator/os-images/apple-system-7.5.3/`
  - Local-only manifest: `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/manifests/2026-05-18-apple-system-7.5.3-download.md`
  - Verification: 19 installer parts downloaded; total size 22,763,648 bytes; per-file SHA256 and source URLs recorded in the local-only manifest; emulator workspace is not a git repository.
  - Bootable disk image path: `/home/bh/workspaces/loki/ev-classic-emulator/local/disks/System7_5_3.img`
  - Bootable disk image manifest: `/home/bh/workspaces/loki/ev-classic-emulator/local/disks/DISK-MANIFEST.local.md`
  - Remaining clean-route issue: validate a clean Basilisk II bootstrap/install workflow for the 19-part Apple-hosted System 7.5.3 installer set if provenance-clean OS setup becomes necessary.
  - Hardware trigger: buy/borrow a USB CD/DVD drive only if we abandon the Apple-hosted installer route and choose a physical retail OS source that cannot otherwise be imaged.

- [x] Emulator located or installed.
  - Status: completed 2026-05-18 on Think laptop
  - Recommendation: use Basilisk II first, preferably native Windows GUI on Think/main gear.
  - Source: `docs/research/2026-05-18-ev-classic-emulator-route-recommendation.md`
  - Installed Windows path: `C:\Games\BasiliskII\`
  - GUI executable: `C:\Games\BasiliskII\BasiliskIIGUI.exe`
  - Desktop shortcut: `C:\Users\bh\Desktop\Basilisk II GUI.lnk`
  - Local-only install manifest: `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/manifests/2026-05-18-basiliskii-windows-install.md`
  - Verification: Windows Defender scan found no threats; GUI launch smoke stayed alive for 5 seconds; executables are unsigned.
  - Earlier blocker resolved for technical-bootstrap work on 2026-05-19; ROM/OS materials now exist locally with provenance caveats.

## Execution checklist

- [x] Create local-only emulator workspace.
  - Status: completed 2026-05-18
  - Path: `/home/bh/workspaces/loki/ev-classic-emulator/`
  - Subdirs: `roms/`, `os-images/`, `disks/`, `captures/raw/`, `captures/notes/`, `shared/`, `tools/`, `reference-archive/`
  - Verification: workspace exists and `git -C /home/bh/workspaces/loki/ev-classic-emulator rev-parse --show-toplevel` reports it is not a git repository.

- [x] Stage ROM/OS/game inputs outside the repo.
  - Status: completed for technical-bootstrap work; cleaner user-owned ROM/OS provenance remains optional if needed for publication or anomaly diagnosis.
  - Done when: local-only notes record paths, sizes, hashes, and source/provenance labels for ROM, OS media, and EV installer/app.

- [x] Configure emulator using local-only paths.
  - Status: completed 2026-05-19 for local technical-bootstrap observation.
  - Preferred route: Basilisk II for 68k Classic Mac OS; SheepShaver only if the authorized package/environment requires PPC.
  - Config path: `C:\Games\BasiliskII\BasiliskII_prefs`
  - Configured ROM/disk paths point at the local-only emulator workspace.

- [ ] Build clean baseline Mac disk.
  - Status: partially complete; Mac OS boots and EV Classic launches, but a pristine baseline snapshot/restore copy is not yet recorded here.
  - Evidence: EV Classic launch capture exists at local-only path `C:\Games\BasiliskII\basiliskii-ev-launched-check.png`.
  - Done when: Mac OS boots, EV Classic launches, and a pristine disk copy/snapshot exists outside the repo.

- [ ] Create first observation artifact before drawing behavior conclusions.
  - Status: partially satisfied for title prefs screen; broader observation artifact still pending.
  - Path: `docs/research/original-ev-classic-runtime-observations.md`
  - Done when: artifact includes observation protocol, emulator/version/config, source material hashes, capture references, evidence labels, confidence, and uncertainty notes.

- [x] Capture title preferences screen.
  - Status: completed 2026-05-19 for the visible Set Prefs screen.
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Local-only capture: `C:\Games\BasiliskII\ev-prefs-correct-coords-2.png`.
  - Derived visible controls: `Navigation Controls:`, `Escort Controls:`, `Weapon Controls:`, `Misc. Controls:`, `Sound Volume: Quiet`, `Intro Music`, `Game Speed...`, `Cancel`, `OK`.
  - Consumed by: `docs/checklists/ev-classic-behavior-baseline-checklist.md` and `godot_ev/scripts/main.gd` prefs modal.

- [x] Capture start/new-pilot baseline.
  - Status: completed/partial 2026-05-19 for start ship, credits, first playable state, starting system/location, and first-HUD equipment clues; detailed equipment inventory remains a follow-up.
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` start-state rows.
  - Observation artifact: `docs/research/original-ev-classic-runtime-observations.md`.
  - Local-only captures include `C:\Games\BasiliskII\ev-new-pilot-after-ship-name.png`, `C:\Games\BasiliskII\ev-new-pilot-enter-ship.png`, and `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`.

- [x] Capture Strict Play New Pilot dialog default state.
  - Status: completed 2026-05-20.
  - Local-only capture: `C:\Games\BasiliskII\ev-new-pilot-strict-play-unchecked.png`.
  - Observed original EV Classic behavior: `Strict Play` appears in the `Enter your name, pilot:` New Pilot dialog and defaults unchecked/off; the dialog was cancelled after capture and Strict Play was not selected.

- [ ] Capture movement/facing baseline.
  - Status: unblocked; original runtime launches, but measured movement/facing captures are not yet recorded.
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` ship-facing and movement rows.
  - Done when: turn/thrust/no-input captures distinguish measured values from qualitative impressions.

- [ ] Capture landing/hyperspace/basic-combat smoke baseline.
  - Status: partial; landing/takeoff, Hyper Mode, Hyper Select, near-center jump failure, mission info, and movement away from Levo were observed in the 2026-05-20 non-strict gameplay learning pass. Automation hit intermittent Basilisk keyboard-input reliability after movement, but human takeover later demonstrated successful hyperspace to Kathoon and landing; the post-landing state is screenshot-confirmed while the exact route/jump input sequence still needs step-by-step capture. Basic combat remains intentionally unrecorded/unfinished.
  - Local-only blocker capture: `C:\Games\BasiliskII\ev-gameplay-learning-rigel-input-recovery-failed-20260520.png`.
  - Local-only successful travel/landing capture: `C:\Games\BasiliskII\ev-kathoon-landed-user-demonstrated-2026-05-20.png`.
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` landing/hyperspace/basic-combat rows.
  - Done when: each observation has capture reference, evidence label, confidence, and Terminal Velocity comparison target.

## Current next action

Use the four live Basilisk II `TV4-*` lanes for scout-only, non-timing runtime-UI setup/capture work when original-runtime evidence is needed. The 2026-06-11 capacity pass verified four responding, independently disked, capture-ready, host-focusable lanes and recorded them in `docs/research/basilisk-speed-qualification.json`; it did not re-qualify guest EV command input, route/travel behavior, timing/feel, or combat cadence. Next safe Basilisk step for gameplay evidence is to choose one lane, restore/launch a known EV app/pilot state, verify a reversible guest input, and record that lane-local restore/reset procedure before using it for route/map/mission claims. Keep screenshots/captures local-only unless explicitly reviewed for commit/publication; record derived observations and evidence labels in repo docs. Treat observations from the current archive-sourced ROM/boot disk route as original-runtime observations with provenance caveats, and revisit cleaner ROM/OS provenance only if emulator-specific anomalies appear or publishable evidence is needed.
