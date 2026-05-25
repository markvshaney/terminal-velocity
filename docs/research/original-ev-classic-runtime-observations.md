# Original EV Classic runtime observations

Date: 2026-05-19

Purpose: source-backed observation log for original Escape Velocity Classic running locally in Basilisk II. Raw captures remain local-only; this file records derived observations with evidence labels and provenance caveats so original-system behavior can be preserved for future Terminal Velocity implementation.

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
7. For every original-system observation that may affect Terminal Velocity later, store the derived fact here with capture/provenance references before promoting it into `docs/checklists/ev-classic-fidelity-implementation-backlog.md` or game data/code.

## Observation seed format

When playing original EV Classic, seed future Terminal Velocity work by adding compact observation blocks here. Each seed should include:

- `Seed:` short stable title.
- `Surface:` the Terminal Velocity area it may affect, such as universe data, economy, missions, UI, controls, ship/outfit data, combat, hazards, audio, or tests.
- `Evidence:` evidence label plus local-only capture/log paths or decoded-resource references.
- `Observed behavior:` derived fact, written without guessing beyond the evidence.
- `Learned skill/use:` any player skill, tactic, route-planning habit, risk judgment, trade/mission pairing, outfitting decision, or control fluency learned from the observation that could later inform Terminal Velocity tutorials, mechanics, AI hints, balance, tests, or design. Note whether the skill is reusable by other pilots/test profiles or specific to the current pilot/context.
- `Play report:` for mission/travel runs, summarize what mission was pursued, route chosen, cargo/passenger constraints, fuel/credit changes, completion/failure state, pirate/hostile/asteroid encounters, avoidance tactics, damage/risk outcome, and what should be reused by future pilots.
- `Implementation hint:` likely Terminal Velocity incorporation target, or `unknown` if not yet clear.
- `Backlog link/status:` corresponding item in `docs/checklists/ev-classic-fidelity-implementation-backlog.md`, with status such as `needs evidence`, `candidate`, `ready`, or `implemented`.

Seeds are allowed to be incomplete if they preserve a real observation, but they must say what evidence is missing before implementation.

## 2026-05-19 new-pilot/start-state observation

Local-only captures:

- `C:\Games\BasiliskII\ev-new-pilot-after-ship-name.png`
- `C:\Games\BasiliskII\ev-new-pilot-enter-ship.png`
- `C:\Games\BasiliskII\ev-new-pilot-enter-ship-5s.png`
- `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`
- `C:\Games\BasiliskII\ev-new-pilot-player-info.png`
- `C:\Games\BasiliskII\ev-start-equipment-landing-postmessage-l.png`
- `C:\Games\BasiliskII\ev-start-equipment-landed-levo.png`
- `C:\Games\BasiliskII\ev-start-equipment-levo-commodity-screen.png`
- `C:\Games\BasiliskII\ev-levo-food-after-buy.png`
- `C:\Games\BasiliskII\ev-levo-food-after-sell.png`
- `C:\Games\BasiliskII\ev-levo-industrial-after-buy.png`
- `C:\Games\BasiliskII\ev-levo-industrial-after-sell.png`
- `C:\Games\BasiliskII\ev-levo-medical-after-buy.png`
- `C:\Games\BasiliskII\ev-levo-medical-after-sell.png`
- `C:\Games\BasiliskII\ev-levo-metal-after-buy.png`
- `C:\Games\BasiliskII\ev-levo-metal-after-sell.png`
- `C:\Games\BasiliskII\ev-levo-equipment-after-buy.png`
- `C:\Games\BasiliskII\ev-levo-equipment-after-sell.png`

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
- Landing flow at Levo:
  - first `L`: target brackets appear around Levo and message `Cleared to land, Starseeker. Commence final approach.`; HUD nav text changes to `Stellar Navigation` / `Levo`.
  - second `L`: Levo landed screen opens with buttons `Spaceport Bar`, `Mission Computer`, `Commodity Exchange`, and `Leave`; no visible outfitter button on Levo.
  - Levo description text: `Levo is an independent world that has resisted joining the Confederation. Anyone is welcome at the tiny but neutral Levo Spaceport, located on the island of Locanda in Levo's southern ocean.`
  - Commodity Exchange opens without buying/selling; visible rows: `Food` price status `Med` price `120`; `Industrial` `Low` `192`; `Medical` `Med` `600`; `Metal` `Low` `144`; `Equipment` `Med` `360`; `Buy` and `Leave` buttons are visible. `In Hold:` column is blank for all rows.
  - Commodity buy/sell loop at Levo: the `Buy` button buys 10 tons at a time from the starting shuttle state, not 1 ton. Buying 10 tons of each commodity reduced credits by exactly 10 times the visible price, and selling those 10 tons restored credits to `10,000`. Observed same-port sale prices therefore equal visible buy prices at Levo: `Food` 120, `Industrial` 192, `Medical` 600, `Metal` 144, `Equipment` 360.

## Terminal Velocity comparison notes

- `godot_ev/scripts/main.gd` already selected `shuttlecraft`; this matches the observed starting ship type.
- `godot_ev/scripts/main.gd` used `credits := 5000`; corrected to `credits := 10000` after this observation.
- `native_ev/data/universe.json` now starts at `Levo`, with `Levo Spaceport` backed by the decoded landing-name evidence text in `native_ev/data/sourced_ev_names.json`.
- `godot_ev/scripts/main.gd` now resolves `START_SYSTEM_NAME := "Levo"` by name instead of depending only on index `0`.
- Levo routing/coordinates are intentionally minimal integration scaffolding pending fuller decoded system-topology work; the start-state mismatch is closed, but complete EV galaxy topology remains partial.
- Starting equipment remains partial: the first HUD proves no secondary weapon and free cargo space 20; the Levo Commodity Exchange proves no starting commodity cargo visible in the `In Hold:` column and that Levo has no visible outfitter button. A full weapon/outfit inventory/status screen was not captured in this automation pass.
- `native_ev/data/economy.json` now sets Levo same-port sell prices equal to the observed buy prices because the original EV Classic buy/sell loop restored credits exactly after selling back the purchased 10-ton lot.
- `godot_ev/scripts/main.gd` now uses a 10-ton commodity trade lot for buy/sell actions, bounded by available cargo space, credits, and held quantity. This promotes the directly observed Levo transaction granularity while leaving exact partial-capacity EV behavior as a future edge-case observation if needed.

## 2026-05-20 Strict Play investigation

Evidence gathered:

- Existing original EV Classic prefs capture `C:\Games\BasiliskII\ev-prefs-correct-coords-2.png` shows the Set Prefs controls for key bindings, `Sound Volume: Quiet`, `Intro Music`, `Game Speed...`, `Cancel`, and `OK`; it does **not** show a `Strict Play` checkbox or control on that prefs screen.
- Live Basilisk II state was restored/captured on 2026-05-20 and was still the non-strict `Starseeker` pilot landed at Levo; no Strict Play control is visible on the landed/commodity screens.
- Local disk string/manual evidence from `System7_5_3.img` says: `To start a new game in Escape Velocity, click on the New Pilot button.  A dialog box appears, allowing you to name your pilot, and decide whether you'd like to play by Strict rules or not.` It also says that if playing by Strict rules, `when your pilot dies, he's truly dead`, while not playing by Strict rules lets the player click `Open Pilot` and resume from the last landed planet.
- Local disk string evidence places UI strings `Strict Play` near `Enter your name, pilot:`, `Edit Text`, and `Cancel`, supporting New Pilot dialog placement.
- External reference source `Hardcore Gaming 101: Escape Velocity` describes `strict play` mode as one-life play where, if the player dies, they cannot re-open the pilot file to continue from the last landed planet.
- Ambrosia forum archive material for EV pilot-file structure identifies a `strictPlayFlag` in pilot-file resource `129` (`MpďL`) and notes `0 = strict play off`; this supports Strict Play as stored per-pilot state, not merely a global display preference.
- A disposable-disk boot path was created for live UI observation (`local/disks/strictplay-disposable/*20260520-003550*`). The run reached Finder but direct New Pilot dialog capture was not completed in that pass because Windows-to-Basilisk mouse/key automation stopped reliably controlling Finder windows after boot. No Strict Play option was selected, and the original Basilisk prefs were restored.
- Original-runtime recapture on 2026-05-20 reached the `New Pilot` flow from the EV title screen. After confirming `There's already a pilot file loaded. Are you sure you want to create a new one?`, the next dialog read `Enter your name, pilot:` with default name `Rick Hardslab`, an unchecked `Strict Play` checkbox, explanatory text `If you check this box, when you're dead, you're dead. No reincarnation allowed.`, and `Cancel` / `OK` buttons. Local-only capture: `C:\Games\BasiliskII\ev-new-pilot-strict-play-unchecked.png`.

Derived status:

- Strict Play is a real EV-family/original-EV concept and should be treated as a per-pilot permadeath/ironman flag.
- To set Strict Play off in original EV, create a New Pilot and choose the non-strict/default path: leave the `Strict Play` option unselected in the `Enter your name, pilot:` dialog. At the pilot-file level, off corresponds to `strictPlayFlag = 0`.
- Do **not** enable or test Strict Play in the local observation pilot; destructive death behavior is too risky for the reusable original-runtime state.
- Direct original-runtime checkbox/default-state capture is now complete for the visible New Pilot dialog: `Strict Play` defaults unchecked/off. The dialog was cancelled after capture; no strict-play option was selected and no new pilot was completed in this recapture pass.

## 2026-05-20 Non-strict gameplay learning pass

Evidence gathered:

- Reused the visible title-screen pilot `Rick Hardslab` / ship `Starseeker` with no Strict Play UI visible after loading; this aligns with the reusable non-strict pilot policy.
- Local-only captures: `C:\Games\BasiliskII\ev-gameplay-learning-levo-mission-computer-20260520.png`, `C:\Games\BasiliskII\ev-gameplay-learning-levo-spaceport-bar-20260520.png`, `C:\Games\BasiliskII\ev-gameplay-learning-levo-spaceport-bar-menu-20260520.png`, `C:\Games\BasiliskII\ev-gameplay-learning-levo-watch-holovids-20260520.png`, `C:\Games\BasiliskII\ev-gameplay-learning-mission-accepted-passengers-20260520.png`, `C:\Games\BasiliskII\ev-gameplay-learning-hyperselect-rigel-20260520.png`, and `C:\Games\BasiliskII\ev-gameplay-learning-levo-departure-accelerate-20260520.png`.
- Levo Mission Computer listed: `Ferry Passengers to New Istanbul`, `Rush Delivery to Port Oread`, `Rush Delivery to Darkstar`, `Transport Cargo to Opal`, `Cargo Shipment to Hikeba`, `Cargo Delivery to Palshife`, and `Freight Delivery to New Japan`. The highlighted first mission read `Ferry Passengers to New Istanbul`; description: `A group of people ask to be taken to New Istanbul in the Yemuro system, in return for 10,000 credits.`
- Accepted the first passenger mission. After acceptance, the HUD special-cargo panel showed `Special: Psngrs`, credits remained `10,000`, and the pilot was safely re-landed at Levo before closeout.
- Levo Spaceport Bar first produced a mission prompt: `Two men at the next table are arguing. "I'm telling ya, Jenkins," one of them is saying, "We don't have the capacity to run this excess today!" The other one notices you staring at them. "Hey, you're the captain of the Starseeker, aren't you?" he asks. "Interested in an easy 10,000 credits?"` Buttons: `No`, `Yes`. The prompt was declined.
- After declining, the Levo Bar menu text read: `Welcome to the Levo Bar & Grill - home of the best plastiburgers this side of the Gamma Quadrant!` Buttons: `Hire An Escort`, `Gamble`, `Watch Holo-Vid`, and `Leave`.
- `Watch Holo-Vid` opened an ISN panel: `ISN` / `The Interstellar News Network` / `Hypertext-Captioned`; visible item: `Sponsored in part by the Sirius Cybernetics Corporation.` and `Reader Survey: 95% of Martian citizens believe the first moon landing was a hoax.`
- Preferences capture confirms original EV navigation keys: `Hyper Mode: H`, `Hyper Select: Backslash`, `Jump: J`, `Land: L`, `Autopilot: A`, `Accelerate: Up`, `Rotate Left/Right: Left/Right`, `Afterburner: Z`.
- Runtime hyperspace behavior: pressing `H` switches the nav panel to `Hyperspace`; pressing Backslash selected `Rigel` from Levo. Pressing `J` while still close to Levo failed with `Can't initiate hyperspace jump - not yet far enough away from system center.`
- Continued departure observation: clicking `Leave` at Levo only launched when the actual button interior was clicked around client y≈348, not the lower border around y≈374. Launch text showed `Leaving Levo on May 23rd, 2276.` With the ship in space, holding `Up` for about 3 seconds visibly moved the shuttle down/right of Levo; HUD remained `Stellar Navigation / No Destination`, `No Secondary Weapon`, `No Target`, `Free: 20`, `Special: Psngrs`, `Credits: 10,000`. Successful hyperspace distance threshold is still not verified.
- Mission Info (`I`) in space opened a dialog listing `Ferry Passengers to New Istanbul`; visible description: `These passengers need to get to New Istanbul in the Yemuro system.` Local-only capture: `C:\Games\BasiliskII\ev-gameplay-learning-mission-info-new-istanbul-20260520.png`.
- Continued hyperspace attempt: after clicking the playfield and using the extended-key helper, holding `Up` successfully moved the ship far enough that Levo was no longer visible while `Hyperspace / Rigel` remained selected. Subsequent `J`/`I`/`H` key attempts did not visibly trigger jump, mission info, or mode changes, despite the game continuing to animate and showing a periodic shareware message (`Cap'n Hector says: "Don't forget to send in your shareware registration fee!"`). Local-only capture: `C:\Games\BasiliskII\ev-gameplay-learning-rigel-drift-input-blocker-20260520.png`. Treat this as an input-control blocker, not proof of EV hyperspace behavior.
- Input recovery pass from the same in-space `Hyperspace / Rigel` state tried bounded local recovery without changing pilot settings: `release-keys-basilisk.ps1`, foreground/topmost + playfield click, `post-vk-basilisk.ps1` for `J` and `I`, `send-vk-basilisk.ps1`, `sendkeys-basilisk.ps1`, Windows Forms `SendKeys`, and direct scancode `SendInput` for `I`. None opened Mission Info or visibly initiated jump; the game continued animating in space with HUD still showing `Hyperspace / Rigel`, `No Secondary Weapon`, `No Target`, `Free: 20`, `Special: Psngrs`, `Credits: 10,000`. Local-only capture: `C:\Games\BasiliskII\ev-gameplay-learning-rigel-input-recovery-failed-20260520.png`. This strengthens the local Basilisk post-movement input-control blocker and leaves successful hyperspace transit unverified.
- 2026-05-20 evening continuation from the same live state started in space with `Hyperspace / Rigel`, `Special: Psngrs`, `Free: 20`, `Credits: 10,000`, full shield/fuel, and no visible target/secondary weapon. The map could be closed by clicking the actual `Done` button using screen coordinates corrected by the Basilisk window origin. Holding `Up` continued to accelerate/move the ship while nearby asteroids drifted across the playfield, so arrow input and game animation were still live. Bounded attempts to press `J`, `A`, and `M` via SendKeys/keybd_event/post-message/scancode helpers produced no visible hyperspace jump, autopilot, map, or failure message. Local-only capture: `C:\Games\BasiliskII\ev-gameplay-learning-continuation-input-blocker-20260520.png`. Treat this as the same input-control blocker; do not infer EV hyperspace/autopilot/map behavior from these no-ops.
- Follow-up iteration after user correction continued instead of stopping after a single failed attempt: accelerated away from Levo with repeated safe `Up` holds of roughly 6s, 12s, 30s, and 60s, plus one bounded `Up+Z` afterburner segment, retrying `J` via SendKeys, keybd_event, scan-code-only SendInput, and long-hold `J`. The ship remained in `Hyperspace / Rigel` with shields/fuel/credits visually unchanged and asteroids still animating; no hyperspace animation or distance-failure message appeared. Local-only captures: `C:\Games\BasiliskII\ev-gameplay-learning-iterative-jump-attempt1-20260520.png`, `...attempt2-20260520.png`, `...attempt3-scancode-20260520.png`, `...attempt4-afterburner-20260520.png`, `...attempt5-holdj-20260520.png`, `...attempt6-longaccel-20260520.png`, `...farther-before-jump-20260520.png`, and `...attempt7-after-longaccel-20260520.png`. This confirms the play tactic should iterate through distance before declaring failure, but the automation run still did not verify successful hyperspace transit.
- Human takeover/observation mode then demonstrated successful route progress: user reported hyperspacing to Kathoon and landing on the planet. Screenshot-confirmed state after the report: landed panel with description text beginning `Maxwell's Purchase is a peaceful, independent world dedicated mainly to farming and some light manufacturing. The delicious junga root is grown primarily on this planet.` Visible buttons: `Refuel Ship`, `Commodity Exchange`, `Spaceport Bar`, `Mission Computer`, and `Leave`. HUD remained `Free: 2`, `Special: Multiple`, `Credits: 10,000`. Local-only capture: `C:\Games\BasiliskII\ev-kathoon-landed-user-demonstrated-2026-05-20.png`. Treat successful hyperspace-to-Kathoon route execution as user-demonstrated until the exact map clicks/keys are separately captured; treat the landed planet UI/HUD as screenshot-confirmed.
- Stability note from user report: Basilisk II froze again during/after gameplay observation. A live process check from WSL/PowerShell still showed `BasiliskII` present and Windows-responding, but this does not disprove an in-emulator Mac/game freeze. Treat this as a recurring emulator stability risk for extended gameplay testing and separate it from EV gameplay mechanics. Follow-up debug captured the live state in `docs/research/2026-05-20-basilisk-freeze-input-debug.md`: the process was responding and consuming CPU, EV display state changed between captures, and a hail appeared, so the current state is better classified as live emulation/display with failed scripted command-key input rather than proven total freeze.

Derived status:

- Safe non-strict gameplay learning path is active: pursue trading, missions, exploration, factions, upgrades, and ship purchases; avoid intentionally getting blown up for now, even though the pilot is non-strict.
- User framing: EV progression should be treated as multiple learnable player skills/strategies, not one generic credit grind: mission running, commodity trading, piracy/privateering/looting, faction progression, and upgrade/ship-ladder planning. Current safe learning should emphasize mission/trade/navigation before destructive or piracy-oriented tests.
- User guidance added during the same pass: learn when commodity trading should be paired with missions, and learn ship modification as its own player skill. Treat this as strategy-learning scope, not source-backed EV economy/outfitter behavior until observed or decoded.
- User authorization/framing: multiple non-strict pilots may be created for separate strategy learning tracks, so the reusable mission/trade pilot does not need to carry piracy/combat-risk experiments.
- Mission/Bar/Holo-Vid flows are now source-backed enough to inform Terminal Velocity UI/backlog work. Hyperspace travel is now user-demonstrated to Kathoon with a screenshot-confirmed landed state, but the exact route-selection/jump input sequence still needs a captured step-by-step pass before being treated as screenshot-confirmed original-runtime control behavior.

## 2026-05-25 movement turn-rate capture

Evidence gathered:

- Live Basilisk II was initially minimized; it was restored to a visible `646x509` window and captured successfully.
- Starting state was EV Classic in space near a planet, HUD showing full Shield/Fuel bars, `Nav System Off`, `No Secondary Weapon`, `No Target`, `Free: 2`, `Special: Multiple`, and `Credits: 15,000`.
- Local-only captures:
  - `C:\Games\BasiliskII\ev-movement-measure-before-20260525-131902.png`
  - `C:\Games\BasiliskII\ev-movement-measure-right1s-after-20260525-131902.png`
  - `C:\Games\BasiliskII\ev-movement-before-shipcrop-20260525-131902.png`
  - `C:\Games\BasiliskII\ev-movement-after-shipcrop-20260525-131902.png`
  - `C:\Games\BasiliskII\ev-movement-measure-left1s-return-20260525-131902.png`
- Bounded input: held extended-key Right Arrow (`VK 39`) for `1000 ms`, then captured; held extended-key Left Arrow (`VK 37`) for `1000 ms`, then captured.
- Pixel comparison between before and right-arrow-after captures changed only the ship sprite area (`254` pixels, bbox `x=240..260`, `y=255..275`), supporting a clean rotation observation without broad UI/state changes.

Derived observations:

- Arrow-key turning input was responsive in this live state; this is not the same command-key input blocker seen in previous hyperspace attempts.
- A 1-second Right Arrow hold visibly changed the shuttle sprite orientation by a large discrete step. Full-capture pixel comparison changed only the ship sprite area (`254` pixels, bbox `x=240..260`, `y=255..275`).
- Offline template matching against the decoded Shuttlecraft frame assets (`native_ev/assets/ships/ev_classic/shuttle/frame_*.png`) found a best-fit scale of about `0.5x` for the original runtime sprite in the full captures. Candidate frame matches were:
  - before Right Arrow hold: `frame_20` best, with `frame_21` and `frame_02` as nearby alternatives depending on color/shape scoring;
  - after 1000 ms Right Arrow hold: `frame_05` best, with `frame_23` as the strongest opposite/symmetric alternative;
  - after the subsequent 1000 ms Left Arrow return: `frame_19` best.
- The frame-match loop therefore supports an approximate one-second right-turn delta of about `15` facing cells for this Shuttlecraft capture (`frame_20 -> frame_05`, modulo 36, followed by a left-turn return near `frame_19`). Confidence is moderate, not final: the capture was not frame-aligned, includes key-posting/OS/emulator latency, and the small shuttle sprite has near-symmetric alternatives.
- Follow-up multi-sample measurement on 2026-05-25 used the same safe in-space state and paired Right Arrow/Left Arrow holds at `250`, `500`, `1000`, and `2000 ms`. Local-only captures are named `C:\Games\BasiliskII\ev-turn-multisample-20260525-152121-<duration>ms-{before,right,return}.png`.
- Multi-sample full-capture diffs stayed localized to the ship sprite area (`247..268` changed pixels; bboxes around `x=240..263`, `y=255..274`). Candidate frame matches from a common `frame_19` baseline were: `250 ms -> frame_24` (`+5` cells), `500 ms -> frame_31` (`+12` cells), `1000 ms -> frame_06` (`+23` cells modulo 36), and `2000 ms -> frame_28` (`+45` cells modulo 36). Return captures mostly returned to `frame_19`, with the `2000 ms` return at `frame_17`.
- This supports an original-runtime Shuttlecraft turn rate near `22.5` facing cells/sec for decoded `turning=60`. Terminal Velocity was retuned from the earlier compatibility mapping to `turning * 0.375` (`60 -> 22.5 cells/sec`). Confidence is higher than the single-sample observation but still partial because the capture is not frame-aligned and uses template matching.

## Open verification items

- Later, confirm the `22.5` cells/sec Shuttlecraft turn-rate mapping with frame-aligned capture or an independent runtime timing method.
- Open a player/ship info screen or an outfitter/status screen at a port that exposes one, without changing inventory, to record exact starting primary weapons/outfits.
- Terminal Velocity now models Strict Play as a New Pilot per-pilot option defaulting off/unchecked, saves it as `strict_play`, and reports the self-test contract `strictPlay=off-by-default`; destructive death semantics remain untested and should not be tested on reusable pilots.
- Complete the accepted `Ferry Passengers to New Istanbul` mission on the non-strict pilot after learning reliable departure/hyperspace movement away from Levo.
- Decode/source-integrate fuller EV Classic system topology and coordinates beyond the Levo start-state bridge.
- Cross-check the `Rendell StarDrive 805R cargo shuttle` prompt against decoded static resources if exact ship variant/resource naming matters.
