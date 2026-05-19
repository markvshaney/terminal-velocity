# Classic Mac OS requirements for Basilisk II EV Classic observation

Date: 2026-05-18

Purpose: identify the Mac OS material required to run original Escape Velocity Classic under Basilisk II for Terminal Velocity behavior observation, now that the user has confirmed they do not already have Mac OS media.

## Recommendation

Use **Apple-hosted System 7.5.3 installer parts** as the first Mac OS target, paired with a **compatible 68k Mac II / Quadra / LC-class ROM** for Basilisk II.

This is a better first path than buying random retail media because the Apple-hosted System 7.5.3 files are still directly reachable, Basilisk II’s own page links to Apple’s Mac OS 7.5.3 software area, and EV Classic community compatibility data points to System 7.x as sufficient.

Do **not** buy a USB CD/DVD drive for Mac OS yet. A CD drive only becomes relevant if we intentionally choose a physical retail Mac OS CD instead of the Apple-hosted System 7.5.3 installer workflow.

## Required pieces

### 1. Basilisk-compatible Macintosh ROM

Status: still blocked.

Basilisk II’s official page says it still needs both a copy of MacOS and a Macintosh ROM image. It also says Basilisk II emulates either:

- a Mac Classic, running MacOS 0.x through 7.5; or
- a Mac II series machine, running MacOS 7.x, 8.0, and 8.1;

with the choice depending on the ROM used.

For EV observation, prefer a **Mac II / LC / Quadra / Centris-class 68k ROM** over a compact black-and-white Mac Classic ROM because we want color video, sound, and a closer 1996 game environment.

### 2. Classic Mac OS installer source

Status: staged locally 2026-05-18.

The first target should be **System 7.5.3** from Apple’s legacy download host:

- Base URL: `https://download.info.apple.com/Apple_Support_Area/Apple_Software_Updates/English-North_American/Macintosh/System/Older_System/System_7.5_Version_7.5.3/`

Direct file availability was checked with HTTP HEAD on 2026-05-18. All 19 installer parts responded `200 OK`:

- `System_7.5.3_01of19.smi.bin` — 1,425,664 bytes
- `System_7.5.3_02of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_03of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_04of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_05of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_06of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_07of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_08of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_09of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_10of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_11of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_12of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_13of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_14of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_15of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_16of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_17of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_18of19.part.bin` — 1,206,656 bytes
- `System_7.5.3_19of19.part.bin` — 824,832 bytes

Staging target:

- `/home/bh/workspaces/loki/ev-classic-emulator/os-images/apple-system-7.5.3/`

Local-only manifest with source URL, size, and SHA256 for every part:

- `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/manifests/2026-05-18-apple-system-7.5.3-download.md`

Verification: 19 files downloaded, total size 22,763,648 bytes; the emulator workspace is outside git.

### 3. Boot/install workflow material

Status: unresolved implementation detail.

System 7.5.3 is distributed as MacBinary/BinHex-era self-mounting image parts, so it is not simply an ISO to attach. A Basilisk II setup usually also needs a bootable starter disk/hardfile or a host-side HFS tooling workflow to get the installer parts onto an emulated disk.

Next investigation step after downloading/staging the Apple installer parts:

- determine the cleanest Windows/WSL workflow to create a Basilisk II hardfile, boot System 7.5.3, and run the 19-part installer set without relying on provenance-weak prebuilt abandonware images.

Possible approaches to evaluate:

- use a minimal boot disk image only as a bootstrap, with provenance labelled separately;
- create/populate an HFS hardfile using host-side tooling if available;
- use Basilisk II host-directory exchange after a basic OS boot exists.

## EV Classic OS compatibility evidence

Primary runtime truth is still the actual original EV runtime once launched.

Current compatibility evidence is secondary/community evidence:

- Macintosh Garden lists `EV_Installer_1.0.5.bin` for “System 7.0 - 7.6 - Mac OS X”.
- Macintosh Repository lists Escape Velocity as 68K + PPC FAT and says “From Mac OS 7.0 up to Mac OS 9.2”, with at least 7 MB free RAM.
- The local installer matches the Macintosh Garden MD5 for `EV_Installer_1.0.5.bin`:
  - MD5: `2a357d43a41f4cfc2a0d6288110d73e9`
  - SHA256: `5c6b8ed5ee1efb67f3f7cbe62b051f36d26753337f18a238febbdc023ef0a5a2`
  - `file`: MacBinary II application, title `Escape Velocity Installer`

Interpretation: System 7.5.3 should be sufficient for first-run EV Classic observation if paired with a suitable color-capable 68k ROM/environment.

## Non-goals / avoided paths

- Do not use random prebuilt “Mac OS for Basilisk” abandonware images as project truth.
- Do not buy physical optical hardware unless we choose a physical retail Mac OS source.
- Do not switch to SheepShaver/PPC unless the available ROM/OS material makes Basilisk II impractical.
- Do not mark Terminal Velocity behavior as `original-runtime-observed` until EV Classic is actually running and captured.

## Current next actions

1. Continue looking for or acquiring a compatible authorized 68k Mac ROM source.
2. Research/validate the cleanest bootstrap workflow for installing System 7.5.3 into a Basilisk II hardfile.
3. Once ROM + OS boot path are available, configure Basilisk II and build the clean baseline disk.

## Sources inspected

- Basilisk II official page: `https://basilisk.cebix.net/`
- Apple legacy download host direct HEAD checks for System 7.5.3 installer parts.
- Scruss Basilisk II / Mac OS 7.5.3 setup article: `https://scruss.com/enterprise.net/basilisk_OS753.html`
- Macintosh Garden Escape Velocity page: `https://macintoshgarden.org/games/escape-velocity`
- Macintosh Repository Escape Velocity page: `https://www.macintoshrepository.org/6700-escape-velocity`
- Local EV installer inspection: `md5sum`, `sha256sum`, and `file` on `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/downloads/EV_Installer_1.0.5.bin`
