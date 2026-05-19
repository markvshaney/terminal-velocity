# EV Classic original-runtime observation setup checklist

Date: 2026-05-18

Purpose: live execution surface for getting from local Think-laptop materials to source-backed original Escape Velocity Classic runtime observations, without committing proprietary ROM/OS/game files or letting EV Classic-for-Nova stand in as original-runtime truth.

Related plan artifact: `docs/plans/2026-05-18-original-ev-classic-emulator-observation.md`

Related behavior baseline checklist: `docs/checklists/ev-classic-behavior-baseline-checklist.md`

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
  - Next action: user points Loki at likely folders or provides authorized ROM material outside the repo.

- [ ] Compatible Classic Mac OS install/media located.
  - Status: blocked/pending user-provided authorized material
  - Search result: no compatible Mac OS media was identified during the 2026-05-18 search.
  - Next action: user points Loki at likely folders or provides authorized OS material outside the repo.

- [ ] Emulator located or installed.
  - Status: pending
  - Search result: no obvious Basilisk II or SheepShaver install found under `/mnt/c/Users/bh` during the 2026-05-18 search.
  - Next action: prefer Windows GUI Basilisk II after ROM/OS availability is confirmed, unless WSL GUI forwarding is intentionally used.
  - Approval gate: installing emulator software or changing Windows host state requires user approval.

## Execution checklist

- [ ] Create local-only emulator workspace.
  - Status: pending
  - Path: `/home/bh/workspaces/loki/ev-classic-emulator/`
  - Suggested subdirs: `roms/`, `os-images/`, `disks/`, `captures/raw/`, `captures/notes/`, `shared/`
  - Done when: workspace exists, contains `README.local.md`, and `git -C /home/bh/workspaces/loki/ev-classic-emulator rev-parse --show-toplevel` confirms it is not inside the Terminal Velocity repo.

- [ ] Stage authorized ROM/OS/game inputs outside the repo.
  - Status: blocked until ROM and OS media are found/provided
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

Create the local-only emulator workspace, then locate/provide authorized Classic Mac ROM and compatible Mac OS install/media. Do not install emulator software or mutate Windows host state without explicit approval.
