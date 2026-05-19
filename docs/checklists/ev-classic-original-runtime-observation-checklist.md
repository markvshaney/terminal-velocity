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

- [ ] Classic Mac ROM located.
  - Status: blocked/pending user-provided authorized material
  - Search result: no obvious `Basilisk`, `SheepShaver`, or `Mac*ROM*` file found under `/mnt/c/Users/bh` during the 2026-05-18 search.
  - User update 2026-05-18: no Mac OS media is currently available from the user; ROM availability is also unresolved.
  - Research update 2026-05-18: source-backed clean route is to dump from an owned/borrowed compatible physical 68k Mac; strong target families are LC 475 / Performa 475 / Quadra 605 / Quadra 650 / Centris 650 class. Scruss reports LC475 and Classic II worked for Basilisk II ROM extraction/use and IIvx did not.
  - Source artifact: `docs/research/2026-05-18-basilisk-compatible-rom-acquisition-options.md`
  - Next action: acquire/borrow/buy access to a compatible color-capable 68k Mac and dump its ROM, then stage it outside the repo under `/home/bh/workspaces/loki/ev-classic-emulator/roms/` for hashing/provenance capture.
  - Last-resort technical option: Internet ROM archive candidates exist, but they are provenance/legal-risky; do not use as project truth without explicit user authorization and a `technical-bootstrap-only` label.

- [ ] Compatible Classic Mac OS install/media located.
  - Status: completed/staged locally 2026-05-18
  - Search result: no compatible Mac OS media was identified during the 2026-05-18 search.
  - User update 2026-05-18: user does not have any Mac OS media.
  - Found 2026-05-18: Apple-hosted System 7.5.3 installer parts are directly reachable from `download.info.apple.com`; all 19 expected parts responded `200 OK` to HEAD checks.
  - Source artifact: `docs/research/2026-05-18-classic-mac-os-requirements-for-basilisk-ev.md`
  - Local staging path: `/home/bh/workspaces/loki/ev-classic-emulator/os-images/apple-system-7.5.3/`
  - Local-only manifest: `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/manifests/2026-05-18-apple-system-7.5.3-download.md`
  - Verification: 19 installer parts downloaded; total size 22,763,648 bytes; per-file SHA256 and source URLs recorded in the local-only manifest; emulator workspace is not a git repository.
  - Remaining OS workflow issue: validate a clean Basilisk II bootstrap/install workflow for the 19-part System 7.5.3 installer set without relying on provenance-weak prebuilt abandonware images.
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
  - Remaining blocker: ROM/OS material is still needed before useful emulator configuration.

## Execution checklist

- [x] Create local-only emulator workspace.
  - Status: completed 2026-05-18
  - Path: `/home/bh/workspaces/loki/ev-classic-emulator/`
  - Subdirs: `roms/`, `os-images/`, `disks/`, `captures/raw/`, `captures/notes/`, `shared/`, `tools/`, `reference-archive/`
  - Verification: workspace exists and `git -C /home/bh/workspaces/loki/ev-classic-emulator rev-parse --show-toplevel` reports it is not a git repository.

- [ ] Stage authorized ROM/OS/game inputs outside the repo.
  - Status: partially complete; OS and EV installer staged, blocked on ROM
  - Done when: local-only notes record paths, sizes, hashes, and source/provenance labels for ROM, OS media, and EV installer/app.

- [ ] Configure emulator using local-only paths.
  - Status: blocked until emulator, ROM, and OS media are available
  - Preferred route: Basilisk II for 68k Classic Mac OS; SheepShaver only if the authorized package/environment requires PPC.
  - Done when: emulator path/version/config are recorded in local-only notes.

- [ ] Build clean baseline Mac disk.
  - Status: blocked until emulator, ROM, OS media, and EV Classic installer are available
  - Done when: Mac OS boots, EV Classic launches, and a pristine disk copy/snapshot exists outside the repo.

- [ ] Create first observation artifact before drawing behavior conclusions.
  - Status: pending after launch
  - Path: `docs/research/original-ev-classic-runtime-observations.md`
  - Done when: artifact includes observation protocol, emulator/version/config, source material hashes, capture references, evidence labels, confidence, and uncertainty notes.

- [ ] Capture start/new-pilot baseline.
  - Status: blocked until original runtime launches
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` start-state rows.
  - Done when: starting ship, credits, location, landed/space state, and initial equipment are recorded with `original-runtime-observed` evidence or explicit uncertainty.

- [ ] Capture movement/facing baseline.
  - Status: blocked until original runtime launches
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` ship-facing and movement rows.
  - Done when: turn/thrust/no-input captures distinguish measured values from qualitative impressions.

- [ ] Capture landing/hyperspace/basic-combat smoke baseline.
  - Status: blocked until original runtime launches
  - Feeds: `docs/checklists/ev-classic-behavior-baseline-checklist.md` landing/hyperspace/basic-combat rows.
  - Done when: each observation has capture reference, evidence label, confidence, and Terminal Velocity comparison target.

## Current next action

Acquire/provide a compatible 68k Mac ROM, preferably by dumping an owned/borrowed LC 475 / Performa 475 / Quadra 605 / Quadra 650 / Centris 650-class machine. Apple-hosted System 7.5.3 installer files were staged locally on 2026-05-18 with hashes/provenance recorded in a local-only manifest. Basilisk II Windows GUI and the local-only workspace are already installed/created on Think; do not buy a CD-ROM drive unless we abandon the Apple-hosted installer route and select physical optical media that cannot otherwise be imaged. After ROM acquisition, validate the clean bootstrap/install workflow for the 19-part System 7.5.3 set, then configure Basilisk II.
