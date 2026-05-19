# Original EV Classic Emulator Observation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task if/when the user approves execution. Do not download ROMs, OS installers, or proprietary game files; use only user-provided/authorized local materials.

**Goal:** Establish a local, evidence-preserving way to run original Escape Velocity Classic in an emulator and observe gameplay behavior for Terminal Velocity fidelity work.

**Architecture:** Keep original-game execution separate from Terminal Velocity code. Use an emulator workspace outside the repo for licensed ROM/OS/game files and write only observation artifacts, hashes, screenshots, videos, and derived notes into repo docs/artifacts. Treat original runtime observations as primary evidence; treat external adaptations as sources of ideas, not necessarily sources of truth.

**Tech Stack:** WSL/Linux planning and file inventory; Windows host GUI for emulator if needed; Basilisk II as the likely first emulator target for 68k Classic Mac OS; optional SheepShaver only if EV Classic copy or OS requirements make PowerPC easier; ffmpeg/OBS/Windows screen recording for captures; repo markdown checklists for evidence.

---

## Current local facts

- Repo: `/home/bh/workspaces/loki/terminal-velocity`
- Existing local EV Classic resource files found under `source-assets/ev-classic/Nova Files/`:
  - `EV Data.rez`
  - `EV Fixes.rez`
  - `EV Graphics.rez`
  - `EV Sounds.rez`
  - `EV Titles.rez`
- Existing plug-ins found under `source-assets/ev-classic/Plug-Ins/`:
  - `EV AI Rocket Hack.rez`
  - `EV Manual Flares.rez`
- No local disk image/application/installer was found in `source-assets/ev-classic/` during planning; only `.rez` resource files and extracted assets were found.

## Non-goals and legal/safety guardrails

- Do not obtain or download Macintosh ROMs, Mac OS installers, or commercial game files from unauthorized sources.
- Do not commit ROMs, OS images, original game apps, save files containing proprietary blobs, or source `.rez` files.
- Do not copy code/behavior from external adaptations into Terminal Velocity as fidelity truth.
- Do not mutate Terminal Velocity gameplay based on emulator observations until each observation is recorded with evidence and reviewed against the behavior checklist.

## Recommended emulator route

Start with **Basilisk II** because original EV Classic is a classic Mac-era 68k title and Basilisk II is usually the appropriate emulator class for System 7 / Mac OS 8-era 68k software.

Use **SheepShaver** only if:

- the available authorized game package is PowerPC-only;
- the user already has a PowerPC-era Mac OS environment prepared;
- Basilisk II cannot run the provided original EV copy.

## Workspace layout

Keep emulator assets outside the repo, for example:

```text
/home/bh/workspaces/loki/ev-classic-emulator/
  README.local.md                  # local-only notes, not committed unless scrubbed
  roms/                            # user-provided ROM; never commit
  os-images/                       # user-provided OS install media/images; never commit
  disks/
    ev-classic-baseline.hfv        # emulator disk image; never commit
  captures/
    raw/                           # screenshots/videos; commit only selected non-proprietary evidence if approved
    notes/                         # local observation notes
  shared/                          # file exchange with emulator if configured
```

Repo-side durable artifacts:

```text
docs/checklists/ev-classic-behavior-baseline-checklist.md
docs/research/original-ev-classic-runtime-observations.md   # create after first observation pass
```

## Task 1: Confirm authorized runtime materials

**Objective:** Determine whether we have enough authorized material to run original EV Classic, without acquiring anything externally.

**Files:**
- Inspect only: `/home/bh/workspaces/loki/terminal-velocity/source-assets/ev-classic/`
- Create local-only if needed: `/home/bh/workspaces/loki/ev-classic-emulator/README.local.md`

**Steps:**

1. Search for candidate runnable/install media locally:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   roots = [
       Path('/home/bh/workspaces/loki/terminal-velocity/source-assets/ev-classic'),
       Path('/mnt/c/Users'),
   ]
   suffixes = {'.sit', '.hqx', '.dsk', '.img', '.toast', '.iso', '.app', '.sea', '.bin'}
   names = ['escape velocity', 'ev classic', 'ev1', 'ev '] 
   for root in roots:
       if not root.exists():
           continue
       print(f'== {root} ==')
       count = 0
       for p in root.rglob('*'):
           if not p.is_file():
               continue
           low = p.name.lower()
           if p.suffix.lower() in suffixes or any(n in low for n in names):
               print(p)
               count += 1
               if count >= 200:
                   print('...truncated...')
                   break
   PY
   ```

2. Record only existence, path, size, and hash for candidate materials. Do not copy proprietary files into the repo.

3. Gate:
   - If an authorized runnable EV Classic app/installer and compatible Mac OS/ROM are available, proceed to Task 2.
   - If only `.rez` files are available, emulator runtime observation is blocked; continue with decoded-resource baselines and ask the user where the authorized game/OS/ROM materials live.

**Verification:** A local note states whether runtime materials are available and where they are stored.

## Task 2: Prepare emulator workspace

**Objective:** Create a local-only workspace and ensure it will not accidentally enter git.

**Files:**
- Create: `/home/bh/workspaces/loki/ev-classic-emulator/`
- Optionally modify repo `.gitignore` only if a repo-local emulator cache is ever created; preferred approach is outside repo.

**Steps:**

1. Create workspace directories:

   ```bash
   mkdir -p /home/bh/workspaces/loki/ev-classic-emulator/{roms,os-images,disks,captures/raw,captures/notes,shared}
   ```

2. Write local-only README:

   ```bash
   cat > /home/bh/workspaces/loki/ev-classic-emulator/README.local.md <<'EOF'
   # EV Classic emulator local workspace

   Local-only workspace for authorized ROM/OS/game runtime observation.
   Do not commit ROMs, OS images, disk images, original game apps, or proprietary captures without review.
   EOF
   ```

3. Verify workspace is outside the Terminal Velocity git repo:

   ```bash
   git -C /home/bh/workspaces/loki/terminal-velocity rev-parse --show-toplevel
   git -C /home/bh/workspaces/loki/ev-classic-emulator rev-parse --show-toplevel || true
   ```

**Verification:** Workspace exists and is not under Terminal Velocity git control.

## Task 3: Install or locate emulator

**Objective:** Identify a runnable emulator path without forcing a specific host route.

**Files:**
- Local-only emulator config under `/home/bh/workspaces/loki/ev-classic-emulator/` if supported.

**Steps:**

1. Check for existing emulators:

   ```bash
   command -v BasiliskII || true
   command -v basiliskII || true
   command -v SheepShaver || true
   command -v sheepshaver || true
   ```

2. On Windows host, also check manually for installed emulator GUI apps if CLI tools are absent.

3. If no emulator is installed, choose installation path:
   - Windows GUI Basilisk II if easiest for display/capture.
   - Linux/WSL Basilisk II only if X/Wayland GUI forwarding is confirmed.

4. Do not install via package manager without user approval if it requires sudo, external downloads, or Windows host mutation.

**Verification:** Document emulator binary/app path and version in local notes.

## Task 4: Build a clean baseline Mac disk

**Objective:** Create a reproducible baseline emulator disk from authorized user-provided OS/game materials.

**Files:**
- Local-only: `/home/bh/workspaces/loki/ev-classic-emulator/disks/ev-classic-baseline.hfv`
- Local-only: emulator config file if applicable.

**Steps:**

1. Create or select a blank HFS/HFV disk image.
2. Install compatible Classic Mac OS from authorized media.
3. Install/copy original Escape Velocity Classic app and required files.
4. Copy local `.rez` files only if they are part of the authorized game layout being reconstructed and the user confirms that is the intended source.
5. Make a pristine snapshot/copy:

   ```bash
   cp ev-classic-baseline.hfv ev-classic-baseline-pristine.hfv
   ```

**Verification:** Emulator boots to Mac OS and EV Classic launches from the baseline disk.

## Task 5: Define observation protocol before playing

**Objective:** Prevent vague play impressions from becoming unreviewed fidelity claims.

**Files:**
- Create after first run: `docs/research/original-ev-classic-runtime-observations.md`
- Update: `docs/checklists/ev-classic-behavior-baseline-checklist.md`

**Observation protocol:**

For every observed behavior, record:

```text
Observation ID:
Date:
Observer/tool:
Emulator/version/config:
Original game version/source:
ROM/OS version label, if known:
Capture file:
Behavior:
Observed original EV Classic behavior:
Evidence label: original-runtime-observed
Terminal Velocity comparison target:
Confidence:
Notes:
```

**Verification:** The protocol exists before any behavior conclusions are written.

## Task 6: First observation pass — start/new pilot state

**Objective:** Capture only the start-state baseline first.

**Steps:**

1. Start emulator from pristine disk copy.
2. Launch EV Classic.
3. Capture title/start/new-pilot flow screenshots or video.
4. Record:
   - first visible screen;
   - new pilot/default start flow;
   - starting ship;
   - starting credits;
   - starting location;
   - landed vs in-space state;
   - initial equipment visible in UI.
5. Do not adjust Terminal Velocity yet.

**Verification:** `docs/research/original-ev-classic-runtime-observations.md` has one start-state section with capture references and uncertainty labels.

## Task 7: Second observation pass — ship facing and movement

**Objective:** Gather minimal physics/render behavior evidence.

**Steps:**

1. Use a fresh copy of the baseline disk or a named save state.
2. Capture a short video of:
   - no input idle;
   - tap/hold left turn;
   - tap/hold right turn;
   - thrust for fixed real-time duration;
   - drift after releasing thrust.
3. If possible, count frame/facing changes from captured video rather than eyeballing.
4. Record what is measured vs what is impressionistic.

**Verification:** Observation notes distinguish measured values from qualitative feel.

## Task 8: Third observation pass — landing/hyperspace/combat smoke

**Objective:** Capture only high-level state transitions before detailed tuning.

**Steps:**

1. Capture land/takeoff flow.
2. Capture hyperspace selection and transition if available.
3. Capture basic weapon fire and target selection if safe/reachable.
4. Record sounds only as event associations unless exact source mapping is verified.

**Verification:** Behavior checklist updated with evidence labels and remaining unknowns.

## Task 9: Feed evidence into Terminal Velocity safely

**Objective:** Convert observations into bounded implementation/test work.

**Steps:**

1. For each observation, decide whether it is:
   - source-backed enough to test;
   - a question requiring more observation;
   - not actionable.
2. Add deterministic Terminal Velocity tests/logging before changing behavior.
3. Link each behavior change to an observation ID or decoded-resource source.
4. Keep adaptation observations out of this evidence path except as question prompts.

**Verification:** Any future gameplay change references a primary evidence source or is explicitly labeled scaffold.

## Risks / blockers

- Authorized ROM/OS/game runtime materials may not be locally available.
- WSL GUI may be awkward; Windows-host emulator may be more practical.
- EV Classic package may require StuffIt/Classic Mac tooling to unpack; use authorized tools/materials only.
- Captures may include proprietary visuals; decide before committing screenshots/videos.
- Emulator timing may differ from original hardware; treat precise physics timings as emulator-conditioned unless cross-checked.

## Immediate next step

Run Task 1 only: inventory authorized runnable/install media and confirm whether runtime observation is possible with current local materials. If blocked, ask the user where the authorized EV Classic app/installer, compatible Mac OS media, and ROM are located.
