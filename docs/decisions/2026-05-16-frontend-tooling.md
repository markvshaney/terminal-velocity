# Front-end tooling decision: replace WPF presentation with a game engine

Date: 2026-05-16

## Problem

The current PowerShell/WPF front end proves the local data/model loop works, but it does not look or feel like Escape Velocity / EV Nova. WPF is acceptable as a native fallback and test harness, not as the long-term presentation layer for a 2D sprite-heavy space game with map, landing, shipyard, outfitter, mission computer, scanner, weapon effects, and EV-style panels.

## Recommendation

Use **Godot 4** as the primary front-end/runtime and keep the current `native_ev/` data, extraction tools, assets, Python tests, and self-test logic as the source-of-truth backend/scaffold.

Do not continue investing in the WPF UI beyond regression/self-test support. Port the visual layer to Godot in a new project root, e.g. `godot_ev/`, loading the same local JSON manifests and extracted frame folders.

## Why Godot

Evidence checked:

- Godot official docs: stable 4.6 documentation, 2D tutorials, UI docs, and Windows export docs.
- Godot repository: `godotengine/godot`, MIT, large active project.
- GitHub metadata checked 2026-05-16: ~110k stars, C++, active updates.

Fit:

- Strong native 2D scene/sprite/camera workflow.
- Native Windows export path.
- Built-in UI system suitable for EV-style panels: landing screen, mission computer, outfitter, shipyard, map, scanner HUD.
- GDScript is lightweight enough for quick iteration; no browser and no .NET dependency required.
- Good match for 36-frame pre-rendered ship facings: use frame-indexed texture loading rather than arbitrary rotation.
- Can keep all proprietary/local EV assets local and out of redistribution.

Risk:

- Godot was not found on the current PATH during the research pass. Windows `winget.exe` is available, so install/setup is straightforward but requires a system mutation decision.

## Alternatives checked

### MonoGame

Evidence checked:

- MonoGame official docs homepage.
- GitHub metadata: `MonoGame/MonoGame`, ~13.9k stars, active, C#.

Pros:

- Good low-level 2D framework.
- Familiar game loop/sprites, more direct control than WPF.

Cons for this project:

- Requires .NET/C# toolchain; `dotnet` was not found locally in WSL/Windows command discovery.
- More custom UI work than Godot for EV-like panels.
- Better for an engine-minded rewrite than a fast fidelity front-end port.

Verdict: viable second choice, but slower here.

### Defold

Evidence checked:

- Defold manuals and project docs.
- GitHub metadata: `defold/defold`, ~6k stars, active.

Pros:

- Lightweight, cross-platform, good 2D focus.
- Can build desktop games.

Cons for this project:

- Smaller ecosystem than Godot.
- Lua/runtime model adds another layer without a clear payoff over Godot.
- EV-style complex UI/data tooling likely more convenient in Godot.

Verdict: viable but not best default.

### LÖVE / Lua

Evidence checked:

- GitHub metadata: `love2d/love`, ~8.3k stars, active. Wiki blocked direct fetch with HTTP 403 during this pass.

Pros:

- Simple, fast 2D iteration.
- Good for handcrafted retro games.

Cons for this project:

- UI and tooling would be mostly custom.
- Less convenient for EV-style multi-screen application UI.

Verdict: good toy/retro framework, but not the strongest fit for this front end.

### Keep WPF

Evidence checked:

- Current project state and runtime constraints.

Pros:

- Already runs locally with no extra dependency.
- Useful as a smoke-test host and emergency fallback.

Cons:

- Not a game engine; rendering, animation, effects, camera, input feel, and game-specific UI are all uphill.
- The current complaint is specifically about front-end fidelity, which WPF is unlikely to solve efficiently.

Verdict: keep for fallback/self-test; stop using it as the main visual target.

## EV-like reference implementations checked

### Endless Sky

Evidence checked:

- `endless-sky/endless-sky` README and GitHub metadata.
- Described as a space exploration, trading, and combat game; supports Windows.

Use as reference for:

- Open-source structure for space trading/combat loops.
- UI/UX comparison for map, outfitters, shipyards, mission/combat systems.

Do not copy assets/text wholesale; use for design reference and implementation pattern study.

### Naev

Evidence checked:

- Naev website and GitHub mirror metadata.
- Naev describes itself as space exploration, trade, and combat, with missions, trading, and fighting.

Use as reference for:

- Open-source mission/economy/front-end interaction patterns.
- Comparing scanner/map/landing workflows.

Do not treat its GitHub mirror as canonical source; project notes say it moved to Codeberg.

## Proposed migration plan

1. Install or locate Godot 4 on Windows.
2. Create `godot_ev/` with a minimal scene: starfield, ship sprite, camera, HUD.
3. Load existing `native_ev/data/*.json` and `native_ev/assets/ships/**/frame_*.png` directly.
4. Recreate EV-style primary screens before adding new gameplay:
   - flight HUD/scanner/target panel
   - galaxy map
   - landing screen
   - mission computer
   - commodity exchange
   - outfitter
   - shipyard
5. Add a Godot headless/smoke path or script-level self-test that verifies data loading and frame availability.
6. Keep Python model tests as the gameplay-rule regression suite until/unless logic moves into Godot.
7. Once Godot front end reaches parity, demote WPF to fallback or archive it.

## Decision

Adopt Godot 4 for the visual/front-end rewrite. Keep the current local data and asset pipeline. Treat WPF as a runnable scaffold, not the target user experience.

## Sources checked

Primary/project sources:

- https://docs.godotengine.org/en/stable/
- https://docs.godotengine.org/en/stable/tutorials/2d/index.html
- https://docs.godotengine.org/en/stable/tutorials/ui/index.html
- https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_windows.html
- https://github.com/godotengine/godot
- https://docs.monogame.net/
- https://github.com/MonoGame/MonoGame
- https://defold.com/manuals/
- https://github.com/defold/defold
- https://github.com/love2d/love
- https://github.com/endless-sky/endless-sky
- https://naev.org/
- https://github.com/naev/naev

Local checks:

- `godot`, `godot4`, and `dotnet` not found on PATH.
- `powershell.exe` and `winget.exe` are available from WSL.
