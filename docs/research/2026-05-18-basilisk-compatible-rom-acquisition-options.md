# Basilisk II compatible Macintosh ROM acquisition options

Date: 2026-05-18

Purpose: identify practical ways to overcome the remaining Basilisk II hard blocker: a compatible 68k Macintosh ROM image for source-backed original Escape Velocity Classic observation.

## Recommendation

The cleanest route is to **obtain access to a compatible physical 68k Mac and dump its ROM**, rather than treating an Internet ROM archive as project truth.

Preferred machine families for this project:

- Macintosh LC 475 / Performa 475 / Quadra 605 class
- Quadra / Centris / Mac II-series color-capable 68k machines known to work with Basilisk II

Avoid making a compact black-and-white Classic ROM the first target unless it is the only legitimate ROM source available. It may boot a Classic environment, but EV observation wants color video and a closer 1996 game setup.

## Why this is the blocker

Basilisk II’s official page says it needs both:

- a copy of MacOS; and
- a Macintosh ROM image.

The Apple-hosted System 7.5.3 installer parts are now staged locally, so Mac OS is no longer the hard blocker. ROM provenance is.

## Options

### Option A — Best provenance: dump ROM from an owned/borrowed compatible 68k Mac

Status: recommended.

Method:

1. Acquire/borrow a compatible 68k Mac.
2. Boot it.
3. Run a ROM-dumping utility such as SaveROM from the ShapeShifter-era workflow.
4. Move the resulting ROM image into the local-only emulator workspace:
   - `/home/bh/workspaces/loki/ev-classic-emulator/roms/`
5. Record source machine, ownership/provenance, size, SHA256, and transfer method in local-only notes before use.

Source-backed compatibility note:

- The Scruss Basilisk/System 7.5.3 setup article says a Mac LC475 and Classic II worked for ROM extraction/use and that a IIvx did not.
- It reports expected ROM image sizes of 1,048,576 bytes for a 1 MB ROM and 524,288 bytes for a Classic ROM.

Project preference:

- LC 475 / Performa 475 / Quadra 605 is a strong target: color-capable, 68k, close to the Basilisk II Mac II-class path.

### Option B — Buy a low-cost compatible donor Mac specifically for ROM extraction

Status: practical if no owned/borrowed machine exists.

Recommended search targets:

- `Macintosh LC 475`
- `Performa 475`
- `Quadra 605`
- `Quadra 650`
- `Centris 650`

Selection criteria:

- Must power on well enough to run a ROM dumper or expose a dumpable ROM module.
- Prefer included keyboard/mouse/video path or a seller-confirmed boot state.
- Avoid PowerPC-only machines for Basilisk II’s 68k ROM requirement.
- Avoid IIvx as a first choice; at least one Basilisk II setup source says it did not work for that workflow.

### Option C — Ask another owner/community member to dump a compatible ROM

Status: acceptable if provenance is recorded.

Use if a trusted vintage Mac owner can dump from their own compatible machine and provide:

- exact source model;
- dump utility/process;
- file size;
- SHA256;
- permission/provenance note.

### Option D — Internet ROM archives / GitHub ROM collections

Status: technically easy, provenance/legal risk; do not use as project truth without explicit user authorization.

Search results expose multiple ROM archive sources, including Macintosh Garden/Repository/Internet Archive/GitHub-style collections. These may contain usable Quadra/Performa ROM images, but ROM copyright/provenance is weak. For Terminal Velocity’s source-fidelity work, treat these only as:

- last-resort technical bootstrap candidates; or
- checksum/filename references for comparing against a legitimately dumped ROM;

not as clean primary project truth.

I did not download a ROM from these archives during this pass.

## Operational staging rule

When a ROM candidate is available, stage it outside the repo:

- `/home/bh/workspaces/loki/ev-classic-emulator/roms/`

Then create a local-only manifest containing:

- source model / source URL / owner note;
- acquisition/dump method;
- local path;
- size;
- SHA256;
- confidence/provenance label;
- Basilisk II smoke result.

Do not commit ROM files or local-only ROM manifests into the Terminal Velocity repo.

## Current next action

Choose one:

1. Preferred: source/borrow/buy a compatible 68k Mac, especially LC 475 / Performa 475 / Quadra 605 / Quadra 650 class, and dump the ROM.
2. If the user explicitly accepts provenance/legal risk, use an Internet ROM archive candidate as a technical bootstrap only, label it accordingly, and keep it outside git.

## Sources inspected

- Basilisk II official page: `https://basilisk.cebix.net/`
- Scruss Basilisk/System 7.5.3 setup article: `https://scruss.com/enterprise.net/basilisk_OS753.html`
- OldOS Basilisk II setup how-to: `https://oldos.org/howtos/mac68kemulator/`
- Search results for E-Maculation, Macintosh Garden/Repository, Internet Archive, GitHub ROM collections, and Basilisk II ROM compatibility discussions.
