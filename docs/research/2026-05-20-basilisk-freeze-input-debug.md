# Basilisk II EV Classic freeze/input debug pass

Date: 2026-05-20

Purpose: classify the reported frozen EV/Basilisk state and start a source-backed debugging track before scaling gameplay observation.

## Current-state evidence

User report: Basilisk froze again during EV Classic gameplay/observation.

Process inspection from WSL -> PowerShell:

- `BasiliskII` process present: PID `9860`.
- Windows `Responding=True`.
- Main window title: `Basilisk II`.
- Process CPU advanced by roughly 3 CPU seconds over a 3 second wall-clock sample, so some emulator thread was actively running.
- Thread sample showed one running thread accumulating nearly all CPU time, plus several waiting threads.

Local-only captures:

- `C:\Games\BasiliskII\ev-freeze-debug-capture1-20260520.png`
- `C:\Games\BasiliskII\ev-freeze-debug-capture2-20260520.png`
- `C:\Games\BasiliskII\ev-freeze-debug-after-i-20260520.png`
- `C:\Games\BasiliskII\ev-freeze-debug-after-focus-click-vk-i-20260520.png`

Visible state from captures:

- EV is in space, not landed.
- HUD: `Hyperspace / Unexplored System`, `No Secondary Weapon`, `No Target`, `Free: 2`, `Special: Multiple`, `Credits: 15,000`, shield/fuel full.
- No modal dialog or watch cursor was visible.
- Between captures, the starfield/ship/message state changed; a hail/message appeared: `S.S. Oppenheimer: Ahoy, Starseeker.`

## Classification

This is not currently proven to be a total emulator freeze.

Current best classification: **EV/Basilisk emulation and display are still alive, but scripted keyboard input is not producing expected EV actions.**

Evidence for live emulation/display:

- Windows process is responding.
- CPU advances continuously.
- EV visible state changes between captures.
- In-game hail/message appears after the reported freeze.

Evidence for input/control problem:

- Sending `i` via existing `sendkeys-basilisk.ps1` did not open Mission Info.
- After explicit focus + client click + `send-vk-basilisk.ps1` VK `0x49`, Mission Info still did not open.
- After releasing keys, explicit focus + client click + hardware-scancode `I` (`send-scancode-basilisk.ps1 -Scan 0x17 -HoldMs 250`), Mission Info still did not open; the HUD remained in-space at `Hyperspace / Unexplored System`, `Free: 2`, `Special: Multiple`, `Credits: 15,000`.
- Prior gameplay pass had the same shape: arrow input and animation worked, but `J`/`I`/`H`/`A` command keys did not reliably reach EV after movement/hyperspace selection.
- 2026-05-21 rotation regression probe: user reported the ship could no longer rotate. Initial `SetForegroundWindow`/`AppActivate` attempts left Telegram/Chrome foreground while Basilisk was only visible through `PrintWindow`; `topmost-basilisk.ps1` made Basilisk visible, and a stronger `AttachThreadInput` focus probe verified foreground title `Basilisk II`. Even with Basilisk foreground, `release-keys-basilisk.ps1`, `hold-key-basilisk-extended.ps1` Left/Right arrow holds, a WM_KEYDOWN/KEYUP extended-lParam Right-arrow probe, `Ctrl+F5` mouse-grab toggle, and `M` via SendKeys produced no visible rotation or map opening. Local-only captures: `C:\Games\BasiliskII\ev-rotation-input-triage-before-20260521.png`, `ev-rotation-input-triage-after-forcefocus-left-20260521.png`, `ev-rotation-input-triage-after-forcefocus-right4s-20260521.png`, `ev-rotation-input-triage-after-map-key-20260521.png`.

Open question: whether a physical keyboard currently works. If physical input works while scripted input does not, the root cause is the automation/input route. If physical input also fails while animation continues, the root cause is likely inside Mac OS/EV input state or Basilisk SDL/ADB delivery. The 2026-05-21 probe narrowed this by verifying that Basilisk can be foregrounded, but scripted rotation/command input still fails.

## Current Basilisk environment

Installed binary:

- `C:\Games\BasiliskII\BasiliskII.exe`
- Size: `4,491,278` bytes
- Last write time: `2022-12-03 19:23:46`
- No embedded Windows file/product version.
- Existing manifest identifies the source package as `Basilisk II Emulator v2022-12-03`, archive SHA256 `aa2167c12f350d0ccfade9f304c19fb85d7f813727f93b5d9a4b076d1bb9c81d`.

Relevant current prefs:

- `frameskip 6`
- `cpu 3`
- `fpu false`
- `nosound false`
- `jit false`
- `keycodes false`
- `idlewait true`
- `sdlrender software`
- `sdl_vsync false`
- `ignoresegv true`

## Source/debuggability evidence

Basilisk II source was cloned for local inspection:

- Path: `/home/bh/workspaces/loki/ev-classic-emulator/src/basiliskii`
- Remote: `https://github.com/tycho/basiliskii.git`
- Checked commit during this pass: `d9eab4d` (`SDLMain.{m,h}: upgrade to SDL 1.2.14 versions`)
- License: GPL, per upstream README/COPYING.

Relevant source surfaces for this input/display problem:

- `src/SDL/video_sdl.cpp`
  - `handle_events()` uses `SDL_PeepEvents(...)` and routes `SDL_KEYDOWN` / `SDL_KEYUP` to `ADBKeyDown(code)` / `ADBKeyUp(code)`.
  - `do_video_refresh()` calls `handle_events()` then `video_refresh()`.
  - `redraw_func()` loops at 60Hz and calls `do_video_refresh()`.
- `src/adb.cpp`
  - `ADBKeyDown()` and `ADBKeyUp()` enqueue Mac keycodes, update key state, set `INTFLAG_ADB`, and trigger an interrupt.
  - `ADBInterrupt()` drains keyboard events and calls the Mac keyboard ADB handler via `Execute68k(...)`.
- `src/Windows/main_windows.cpp`
  - `tick_func()` triggers the 60Hz interrupt loop.
  - `GetMainWindowHandle()` retrieves SDL's Windows HWND.

## 10:40 pm short-plan iteration status

The short plan was iterated locally through the safe non-mutating/build-prep stages.

1. Preserve current known-working Basilisk install:
   - Done. Backed up `BasiliskII.exe`, `BasiliskIIGUI.exe`, `BasiliskII_prefs`, and the installed manifest to `/home/bh/workspaces/loki/ev-classic-emulator/debug-backups/20260520-2240-short-plan/`.
   - Backup hashes are in that directory's `SHA256SUMS` file.
   - Raw ROM/disk images were not copied into this debug backup.

2. Clone/build separately:
   - Source clone exists at `/home/bh/workspaces/loki/ev-classic-emulator/src/basiliskii`.
   - Also cloned the actively referenced `hghpublic/kanjitalk755-macemu` fork to `/home/bh/workspaces/loki/ev-classic-emulator/src/kanjitalk755-macemu` for build-path comparison; current checked commit `23ea263e`.
   - The fork includes `BasiliskII/src/Unix/autogen.sh`, but running it currently stops at missing `autoconf`/`aclocal`.
   - Build is currently blocked by missing local build toolchains/deps, not by source availability.

3. Reproduce current blocker:
   - Reproduced/classified as live display/emulation with failing scripted command-key input; see current-state evidence above.
   - Additional scancode probe: after releasing keys, focus/clicking the playfield, and sending hardware scancode `I` (`0x17`) via `send-scancode-basilisk.ps1`, Mission Info still did not open.

4. Add logging around likely chokepoints:
   - Done in the separate source tree only; live install untouched.
   - Patch saved at `/home/bh/workspaces/loki/ev-classic-emulator/debug-artifacts/basiliskii-ev-input-debug-logging.patch`.
   - Patch SHA256: `48630db77e4ed32dd9835ff8ff386065bce6c6d3822087806ed3fcea54130f1c`.
   - Instrumented chokepoints:
     - `src/SDL/video_sdl.cpp`: SDL event receipt, mouse events, key down/up raw sym/scancode/mod/unicode, Mac keycode translation, redraw heartbeat.
     - `src/adb.cpp`: `ADBKeyDown`, `ADBKeyUp`, keyboard buffer drain in `ADBInterrupt`.
     - `src/Windows/main_windows.cpp`: 60Hz tick heartbeat.
   - Intended Windows log output path for a diagnostic build: `C:\Games\BasiliskII\basilisk-ev-debug.log`.

5. Decide from evidence:
   - Current live binary cannot expose the SDL/ADB boundary without a diagnostic build.
   - Since no Windows C/C++ build toolchain was found and WSL lacks required autoconf/SDL dev tooling, the immediate next path is either install/build prerequisites for a diagnostic build or switch to conservative black-box stabilization tests.

Build/debug caveat:

- The current Windows binary is not a local debug build.
- Windows build docs are old and refer to Visual C++ 5.0 or later; no `cl.exe`, `msbuild.exe`, `devenv.exe`, `cmake.exe`, Visual Studio VC toolchain, MSYS2, MinGW, or Strawberry GCC was found in this pass.
- WSL has `gcc`, `g++`, and `make`, but no `autoconf`/`automake`, `sdl-config`, or SDL 1.x dev tooling was found. `sudo` requires a password, so I cannot install missing packages autonomously in this session.
- A diagnostic source patch is ready, but building/running it is explicitly gated on installing or locating a suitable build environment.

## Root-cause hypotheses to test next

1. **Scripted input path not reaching SDL event queue.**
   - Windows-level `SendKeys`/VK helpers may not generate SDL 1.2 keyboard events after certain focus/state transitions.
   - Test: instrument or externally observe SDL event receipt; compare physical keyboard vs scripted key injection.

2. **SDL event queue receives key events, but key translation drops them.**
   - `keycodes false` uses symbolic mapping in `event2keycode()` / `kc_decode()`.
   - Test: debug build logs SDL key symbol/scancode -> Mac code decisions for `I`, `J`, `H`, `A`, arrows.

3. **ADB queue/interrupt path receives keys, but Mac/EV side does not handle command letters in the current state.**
   - Test: log `ADBKeyDown/Up`, `ADBInterrupt()` drain count, and current key buffer pointers; compare arrows vs command letters.

4. **Game/app state is live but not accepting command keys due to an unseen input mode or stuck key/modifier.**
   - Test: physical keyboard check; release all modifier keys; attempt low-risk keys such as Mission Info (`I`) or Map (`M`) with capture before/after.

5. **Stability/performance setting contributes to timing/input loss.**
   - Current prefs use `frameskip 6`, `idlewait true`, `nosound false`, UNC paths to WSL-hosted ROM/disk images, and `ignoresegv true`.
   - Test only after input classification: conservative copied-local disk/ROM path, sound-off A/B, frameskip/fps A/B, idlewait A/B. Back up prefs and disk images first.

## Safe next action / decision

The 10:40 pm short plan was completed through the safe local stages: current install preserved, source cloned, blocker reproduced/classified, logging patch prepared, and build path checked.

## 2026-05-21 stabilization result

User approved doing whatever is needed locally to fix Basilisk and improve future debugging, without requiring babysitting.

Actions taken:

1. Backed up current Basilisk install/config before mutation:
   - `/home/bh/workspaces/loki/ev-classic-emulator/debug-backups/20260521-082713-basilisk-stabilization/`
   - Included `BasiliskII.exe`, `BasiliskIIGUI.exe`, `BasiliskII_prefs`, `manifest.md`, and `SHA256SUMS`.
2. Copied the currently referenced ROM/disk images from WSL/UNC paths to local Windows paths under `C:\Games\BasiliskII\local-media\` and wrote `local-media\SHA256SUMS`.
3. Rewrote `BasiliskII_prefs` to reduce input/stability risk:
   - `rom C:\Games\BasiliskII\local-media\roms\F1ACAD13 - Quadra 610,650,maybe 800.ROM`
   - `disk C:\Games\BasiliskII\local-media\disks\System7_5_3.img`
   - `disk C:\Games\BasiliskII\local-media\disks\EV_Installer_Transfer.hfv`
   - `frameskip 1` instead of `6`
   - `nosound true` instead of `false`
   - `idlewait false` instead of `true`
4. Force-restarted Basilisk because the live input state was wedged.
5. Added stronger Windows automation helpers in `C:\Games\BasiliskII\`:
   - `force-focus-send-vk-basilisk.ps1`: uses `AttachThreadInput` before key injection; fixed the Mac shutdown warning dialog with Enter and opened EV map with `M`.
   - `force-focus-click-client-basilisk.ps1`: uses `AttachThreadInput` plus client-to-screen click; successfully launched Escape Velocity and entered the ship.
6. Verified restored gameplay input:
   - Basilisk restarted successfully, Mac OS booted, shutdown warning dismissed with the force-focus key helper.
   - Escape Velocity launched from Finder.
   - Existing pilot entered ship in space.
   - Hardware scancode Right arrow (`send-scancode-basilisk.ps1 -Scan 77 -HoldMs 3000`) rotated the ship; local-only capture: `C:\Games\BasiliskII\ev-stabilized-after-scancode-right-20260521.png`.
   - Force-focused `M` opened the EV map; local-only capture: `C:\Games\BasiliskII\ev-stabilized-after-map-20260521.png`.

Current decision:

- **Basilisk is restored enough for bounded gameplay observation.** Rotation and map command input are verified after restart/stabilization.
- **Use the stronger force-focus helpers for command keys/clicks.** For held arrows, `send-scancode-basilisk.ps1` is currently the verified path.
- **Keep sessions short and capture often.** The diagnostic build remains useful for future recurring failures, but is no longer the immediate blocker.
- **If input wedges again**, first preserve/capture, then restart from the backed-up local-media/stabilized prefs baseline and verify with: Enter on a Mac dialog, EV map `M`, and held Right arrow scancode rotation.

## 2026-05-21 map/modal "freeze" metabug follow-up

User reported after an attempted hyperspace jump that Basilisk/EV appeared frozen, the map was showing, and the ship could not rotate. The first response path misrouted into a Hermes/channel-isolation meta-bug instead of continuing the Basilisk debug loop; corrected on follow-up and resumed local game triage.

Evidence/actions:

1. Live process still existed and was Windows-responsive:
   - `BasiliskII` PID `22872`
   - `Responding=True`
   - Main window title `Basilisk II`
2. Current capture showed the EV map modal open, not a landed or total-emulator-freeze state:
   - Map centered on/current system `Eridani`
   - Right HUD still visible with `Nav System Off`, `No Secondary Weapon`, `No Target`, `Free: 2`, `Special: Multiple`, `Credits: 15,000`
3. The first attempted `Done` click used a too-low client Y coordinate and missed because the capture includes the Windows title-bar offset.
4. Clicking the map `Done` button at corrected Basilisk client coordinate approximately `X=402,Y=420` closed the map.
5. After map close, `release-keys-basilisk.ps1` plus `send-scancode-basilisk.ps1 -Scan 77 -HoldMs 2000` rotated the ship successfully. Local-only verification capture:
   - `C:\Games\BasiliskII\ev-metabug-after-map-close-rotation-ok-20260521.png`

Classification:

- This specific incident is best classified as **map modal open + missed automation click**, not a proven Basilisk freeze.
- Rotation is disabled while the EV map modal is open, so "can't rotate ship" is expected until `Done` is actually clicked.
- Current verified recovery path: force-focus Basilisk, click map `Done` at corrected client coordinates, release stuck keys, then verify with a held Right-arrow scancode.

Operational note:

- Avoid assuming client Y coordinates from screenshots directly; subtract the Basilisk title-bar/client offset or use the known corrected `Done` coordinate from this pass.

Operational policy going forward:

- Treat Basilisk freeze/input problems as **inline blockers first**, not as a detached permanent project lane.
- During normal EV/Terminal Velocity work, if Basilisk freezes, stalls, shows confusing foreground behavior, or input wedges, stop the current gameplay/fidelity slice and classify the emulator failure immediately before making further EV behavior claims.
- Preserve evidence before poking: capture the Basilisk window, wait a few seconds, capture again, and save named local-only screenshots when the result informs a durable observation.
- Classify the blocker explicitly: Windows process responsiveness, CPU time advancement, Mac guest/display changes, EV app state, scripted-input failure versus all-input failure, and whether a modal/window/coordinate mistake explains the symptom.
- Use the known safe recovery ladder before declaring the emulator unusable: release keys, force foreground/topmost, use `AttachThreadInput` helpers, use verified VK/scancode helpers, and restart only when those fail or the guest is clearly wedged.
- Resume the original EV/TV slice after Basilisk is usable again; do not let a one-off emulator failure absorb the gameplay-development thread.
- Split Basilisk debugging into a separate Kanban/debug lane only when the same failure class repeats, the source/build fix is larger than the current EV slice, TV-side development can proceed without original-runtime evidence, or the emulator blocks all useful Basilisk observations.

Open longer-term improvement:

- Build/run the diagnostic Basilisk patch when build tooling is available and a recurring blocker justifies it, so future SDL/ADB input failures can be classified from logs instead of black-box symptoms.

Do not enable Strict Play or death-test during gameplay learning unless explicitly requested.
