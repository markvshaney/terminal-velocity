# EV Classic emulator route recommendation

Date: 2026-05-18

Purpose: decide the best practical emulator route for source-backed original Escape Velocity Classic observation on the Think laptop and, by extension, the main gear if it is also a modern Windows/x64 machine.

## Recommendation

Use **Basilisk II as the first emulator target**, preferably as a **native Windows GUI app** on both the Think laptop and main gear.

Do **not** buy a USB CD-ROM drive yet. Based on the local material we found, the EV payload is a MacBinary downloadable installer (`EV_Installer_1.0.5.bin`), not evidence of a CD-only install path. Basilisk II can use hardfile/disk images and a host directory tree for file exchange; the official Basilisk II page also lists a CD-ROM driver, but CD-ROM hardware is not the blocker for this workflow.

## Why Basilisk II first

Source-backed reasons:

- Basilisk II describes itself as an "Open Source 68k Macintosh emulator" and says it runs 68k MacOS software on other operating systems, while still requiring a copy of MacOS and a Macintosh ROM image.
- Basilisk II can emulate a Mac Classic or Mac II series machine depending on ROM. The Mac II route supports color video and Mac OS 7.x / 8.0 / 8.1, which fits the needs of a color 1996 Mac game better than a black-and-white compact Mac setup.
- Basilisk II lists useful workflow features: HFS hardfiles, color video, sound, CD-ROM driver, and easy host file exchange via a "Host Directory Tree" icon on the Mac desktop.
- The local EV installer is verified as MacBinary II application data, title `Escape Velocity Installer`, so it should be imported into a Classic Mac environment rather than treated as a raw Windows/Linux executable.

Local Think laptop fit:

- Host inspected: `THINK`, Lenovo `21QLCTO1WW`, Windows 10 Pro x64, WSL2 Linux `think`.
- CPU inspected: AMD Ryzen AI 7 PRO 350, 16 logical CPUs, ~27 GiB WSL-visible memory.
- This is far more than enough for 68k Mac emulation.
- No Basilisk II, SheepShaver, QEMU m68k/PPC command was found in the current WSL path during inspection.

Main gear fit:

- I could not inspect main gear from this session.
- If main gear is also modern Windows x64, the same recommendation applies: run Basilisk II natively on Windows for easier display, keyboard/mouse, and screen capture.
- If main gear is Linux-only with a reliable desktop session, Linux Basilisk II is also plausible. Avoid WSL GUI unless we specifically want to debug WSL display/audio.

## Alternatives considered

### Mini vMac

Verdict: not first choice.

Mini vMac is a good early-Mac emulator, but its standard path starts around Macintosh Plus / System 6 workflows. The public Mini vMac getting-started page says it needs a ROM and a bootable disk image, and points to System 6.0.8 install disks. That is likely too constrained for EV Classic fidelity work because we need color, sound, and a Mac II-class environment.

Use Mini vMac only if we later prove the target EV build runs correctly in an available supported color-capable Mini vMac variation and we want a simpler reproducible setup.

### SheepShaver

Verdict: backup only.

SheepShaver is a PowerMac emulator and its official page says it needs MacOS and a PowerMac ROM image. It runs MacOS 7.5.2 through 9.0.4 and has color/sound/host-directory features. That is useful, but original EV Classic is a 68k-era target and Basilisk II is a closer fit. Use SheepShaver only if the available authorized environment is PPC-oriented or Basilisk II fails with the EV installer/runtime.

### QEMU / MAME

Verdict: not first choice for this project step.

QEMU/MAME may be more automatable or hardware-faithful in some contexts, but they are not the shortest path to a GUI Classic Mac environment with easy file exchange and capture for EV behavior observation. Keep them as later options if Basilisk II cannot produce stable observations.

## CD-ROM question

Current answer: **do not buy a CD-ROM drive now.**

Reasons:

- The EV file we have is a MacBinary downloadable installer, not a CD image.
- The required blockers are ROM and Mac OS media, not optical hardware.
- A compatible Mac OS can often be installed from disk images/hardfiles in emulator workflows; physical optical media is only needed if the only authorized OS media you possess is on a physical CD and cannot otherwise be imaged.

Purchase trigger:

- Buy/borrow a USB CD-ROM drive only if we confirm your only authorized Mac OS install media is a physical CD and we cannot make/use a disk image from another machine.

## Required materials still missing

- Authorized 68k Macintosh ROM compatible with Basilisk II / Mac II-class emulation.
- Authorized Classic Mac OS install media/image, preferably System 7.5.x through Mac OS 8.1-era.

User update 2026-05-18: the user does not have Mac OS media. Follow-up research found the Apple-hosted System 7.5.3 installer parts still directly reachable from `download.info.apple.com`; see `docs/research/2026-05-18-classic-mac-os-requirements-for-basilisk-ev.md`. Treat Classic Mac OS staging as approval-gated local acquisition/provenance work, not a search-only blocker. Avoid using random abandonware images as project truth.

No longer missing:

- Basilisk II Windows GUI app is installed on Think at `C:\Games\BasiliskII\`; install details and verification are tracked in the live checklist and local-only install manifest.

## Proposed next steps

1. Keep the EV installer in the local reference archive:
   - `/home/bh/workspaces/loki/ev-classic-emulator/reference-archive/downloads/EV_Installer_1.0.5.bin`
2. Acquire/provide an authorized compatible 68k Mac ROM.
3. With approval, download/stage Apple-hosted System 7.5.3 installer parts under `/home/bh/workspaces/loki/ev-classic-emulator/os-images/apple-system-7.5.3/` and record per-file hashes/provenance.
   - Hardware trigger: buy/borrow a USB CD/DVD drive only if we abandon the Apple-hosted System 7.5.3 route and select a physical retail OS source that cannot otherwise be imaged.
4. Validate the cleanest bootstrap workflow for installing the 19-part System 7.5.3 set into a Basilisk II hardfile without relying on provenance-weak prebuilt abandonware images.
5. Stage ROM/OS inputs outside the repo and record paths, sizes, hashes, and provenance in local-only notes.
6. Create a Basilisk II hardfile/disk under:
   - `/home/bh/workspaces/loki/ev-classic-emulator/disks/`
7. Configure Basilisk II host-directory sharing to expose:
   - `/home/bh/workspaces/loki/ev-classic-emulator/shared/`
8. Import the MacBinary EV installer through the shared folder or disk-image workflow.
9. Only after EV launches, create `docs/research/original-ev-classic-runtime-observations.md` and start the evidence protocol.

## Sources inspected

- Local Think host inspection: `uname`, `lscpu`, `free`, Windows `Get-ComputerInfo`, emulator command checks.
- Local EV installer inspection: `file` and `sha256sum` on `EV_Installer_1.0.5.bin`.
- Basilisk II official page: https://basilisk.cebix.net/
- SheepShaver official page: https://sheepshaver.cebix.net/
- Mini vMac official/getting-started pages: https://www.gryphel.com/c/minivmac/ and https://www.gryphel.com/c/minivmac/start.html
