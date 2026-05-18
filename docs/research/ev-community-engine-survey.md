# EV / EV Nova Community Engine Survey

Date: 2026-05-18

Purpose: preserve a source-backed snapshot of community-developed Escape Velocity / EV Nova engine, runtime, and conversion projects that may inform Terminal Velocity's fidelity and engine/data architecture work.

Follow-on decision: `docs/decisions/2026-05-18-ev-family-profile-architecture.md`

Follow-on checklist: `docs/checklists/ev-family-profile-architecture-checklist.md`

## Summary

The strongest bespoke-engine references found are **KestrelEngine** and **NovaJS**.

- **KestrelEngine** is the closest match to a community bespoke EV-family engine: it is a C++ cross-platform engine for classic Mac-era game remasters, explicitly shaped by **Cosmic Frontier: Override**, a remaster of **Escape Velocity: Override**, and by EV plug-in/resource compatibility needs.
- **NovaJS** is the most direct EV Nova runtime reimplementation attempt: a TypeScript/browser project intended to run EV Nova from Nova data files and support Nova plug-ins.
- **OpenNova** is directly relevant in intent but stale.
- **EVNToEndlessSky**, **evnova-utils**, and related tools are not engines, but are useful source references for EV Nova data/resource semantics.
- **EV Nova Community Edition**, **novafix**, and EV Stuff are compatibility/preservation surfaces rather than clean-room engines.

## Best engine candidates

### KestrelEngine

- URL: https://github.com/Evocation-Games/KestrelEngine
- Type: bespoke classic-Mac/remaster game engine
- Language: C++
- License: MIT
- GitHub metadata observed: 60 stars, last pushed 2023-10-31
- Upstream description: "The Kestrel Game Engine"
- Key README claims:
  - aims to develop a modern, cross-platform engine for recreating/remastering Classic Macintosh-era games;
  - provides APIs/facilities for reading and handling old classic-era formats;
  - is being used by **Cosmic Frontier: Override**, a remastering of **Escape Velocity: Override**;
  - games are developed in Lua and assembled into resource files;
  - can use modernized formats, old classic formats, or a mix;
  - is reimplementing ResourceForks, QuickDraw, and QuickTime sound resources;
  - old Escape Velocity plug-in compatibility is a design driver.

Relevance to Terminal Velocity:

- Highest-value architecture reference for classic Mac resource compatibility, plugin/resource replacement semantics, and native cross-platform runtime design.
- Worth mining for how it models resource forks, QuickDraw-era graphics, sound resources, game scripting, resource-pack assembly, and compatibility boundaries.

Caveats:

- It is not an EV Nova-specific implementation.
- Last observed push was 2023; verify current activity before treating it as actively maintained.
- Do not import code/assets without license and compatibility review.

### NovaJS

- URL: https://github.com/mattsoulanille/NovaJS
- Demo: https://novajs.net
- Type: EV Nova browser/runtime reimplementation attempt
- Language: TypeScript
- License: MIT
- GitHub metadata observed: 45 stars, last pushed 2026-04-26
- Upstream description: "An attempt to implement EV Nova in the browser"
- Key README claims:
  - experiment in making Escape Velocity Nova run in the browser;
  - goal: function as a Nova Engine that can, given Nova files, run EV Nova;
  - goal: support Nova plug-ins;
  - goal: improve some EV Nova engine limitations where gameplay is not harmed;
  - goal: support multiplayer to an extent.

Relevance to Terminal Velocity:

- Best living reference for EV Nova gameplay/data semantics and runtime behavior outside the original engine.
- Useful for comparing ship control, targeting, landing, jump/map flow, outfitter/shipyard behavior, data loading, and plugin assumptions.

Caveats:

- Browser/TypeScript architecture differs from Terminal Velocity's native Godot/Python tooling.
- Project includes or expects copyrighted EV Nova data paths; keep any use limited to reference behavior and local authorized data.

### OpenNova

- URL: https://github.com/dmaulikr/OpenNova
- Type: modern EV Nova engine/reimplementation attempt
- Language: Objective-C
- License: MIT
- GitHub metadata observed: 13 stars, last pushed 2017-05-29
- Upstream description: "A modern clone of the classic Mac game Escape Velocity Nova"
- Key README claims:
  - aims to document and reimplement underlying technologies used by the EV games;
  - ResourceForks and QuickDraw are named as major aspects;
  - goal is a newer modern version of the Nova game engine;
  - goal is to take original game data files unmodified;
  - total conversions such as Polycon EV are intended to work.

Relevance to Terminal Velocity:

- Useful historical/design reference for a clean-ish reimplementation strategy focused on original data compatibility.

Caveats:

- Stale; likely not a practical base.
- Objective-C/macOS assumptions may limit direct reuse.

### AhemOne/Escape-Velocity

- URL: https://github.com/AhemOne/Escape-Velocity
- Type: HTML5 implementation of the original Escape Velocity
- Language: HTML/JavaScript
- GitHub metadata observed: 0 stars, last pushed 2024-01-03
- Upstream description: "An HTML5 implementation of the 90's Mac shareware classic Escape Velocity."
- README notes:
  - includes research discussion of Mac resource forks and EV file layout;
  - explicitly says graphics/audio/story placeholders are copyrighted and not licensed.

Relevance to Terminal Velocity:

- Compact reference for original EV structure and reconstruction notes.

Caveats:

- Much smaller and less directly useful than KestrelEngine or NovaJS.
- Asset licensing warnings require caution.

## Data/conversion/reference projects

### EVNToEndlessSky

- URL: https://github.com/edelventhal/EVNToEndlessSky
- Type: EV Nova to Endless Sky conversion tooling
- Language: HTML/Node.js scripts in repo
- License: MIT
- GitHub metadata observed: 14 stars, last pushed 2019-03-23
- Upstream description: scripts/resources for porting the entirety of EV Nova to Endless Sky.
- README notes:
  - uses Rezilla to export EVN data files and TMPL resources to XML;
  - parses base64-encoded resource bytes into a monolithic JSON data file;
  - then converts EVN data toward Endless Sky;
  - documents template quirks, including a manual flët/ActivateOn type correction.

Relevance:

- High-value resource semantics and data conversion reference.
- Useful for comparing Terminal Velocity's extracted JSON manifests against another EVN interpretation path.

Caveats:

- Not a runtime engine.
- In-progress and acknowledges imperfect adaptation because Endless Sky gameplay differs.

### evn2es

- URL: https://github.com/julbouln/evn2es
- Type: EV Nova to Endless Sky converter
- Language: Ruby
- GitHub metadata observed: 3 stars, last pushed 2021-08-17
- Upstream description: "Escape Velocity Nova to Endless Sky data converter"

Relevance:

- Secondary conversion reference; potentially useful for cross-checking specific resource mappings.

Caveats:

- Sparse documentation observed.

### endless-sky-rez

- URL: https://github.com/warp-core/endless-sky-rez
- Type: Endless Sky fork with EV Nova `.rez` parsing support
- Language: C++
- License: GPL-3.0
- GitHub metadata observed: 1 star, last pushed 2024-05-04
- Upstream description: "A fork of endless-sky with support for parsing data from Escape Velocity Nova .rez files."

Relevance:

- Narrow but technically interesting reference for `.rez` parsing in an EV-like C++ game codebase.

Caveats:

- GPL-3.0 license: do not copy code into Terminal Velocity without license review.
- Appears small/fork-specific.

### evnova-utils

- URL: https://github.com/vasi/evnova-utils
- Type: EV/EVO/EVN inspection utilities
- Language: Perl
- GitHub metadata observed: 13 stars, last pushed 2023-05-26
- Upstream description: tools for examining Escape Velocity Nova files.
- README notes:
  - includes context data for EV Classic, EV Override, EV Nova, Frozen Heart, and Miners;
  - includes docs for reverse-engineered EV pilot-file format;
  - includes scripts for listing and inspecting internal game data;
  - `old.pl` is the main script with many EV-relevant commands.

Relevance:

- High-value reference for data inspection, pilot-file internals, and context/source semantics.

Caveats:

- Utility toolkit, not a runtime engine.

### EVNEW

- URL: https://github.com/EthanSuperior/EVNEW
- Type: EVNEW plugin editor source fork
- Language: C++
- GitHub metadata observed: 3 stars, last pushed 2026-05-03
- Upstream description: fork of original EVNEW v1.0.4 created by Adam Rosenfield in 2003.

Relevance:

- Useful for plugin/resource editor behavior and legacy assumptions.

Caveats:

- Not a runtime engine.
- README was not found during the search pass.

### ev-merge

- URL: https://github.com/ThrosturX/ev-merge
- Type: EVN/EVO merge plugin development kit
- Language: C++
- GitHub metadata observed: 1 star, last pushed 2024-06-13
- Upstream description: "Portable development kit for merging EVN with EVO"
- README notes:
  - allows merging EV:N and EV:O universes into one game/plugin;
  - recommends EV Nova Community Edition for playing;
  - includes EVNEW source for bitrot prevention and reference.

Relevance:

- Useful for understanding community plugin workflows and resource-ID constraints.

Caveats:

- Not a standalone engine.

## Compatibility / preservation surfaces

### EV Nova Community Edition

- URL: https://github.com/andrews05/EV-Nova-CE
- EV Stuff page: https://andrews05.github.io/evstuff/
- Type: patches/fixes for EV Nova Windows 1.0.10
- Language: C / patch tooling
- GitHub metadata observed: 43 stars, last pushed 2024-10-16
- README notes:
  - install by downloading latest EV Nova CE upgrade zip and extracting into EV Nova folder;
  - uses ddraw settings;
  - patch notes live in `dist/EV Nova CE Read Me.txt`.

Relevance:

- Important preservation/community baseline for how people run EV Nova now.
- Useful for behavior comparison against original engine, not clean-room implementation.

Caveats:

- Patch layer over the original binary; not a reimplementation engine.

### novafix

- URL: https://github.com/RyuKojiro/novafix
- Type: modern macOS fix/launcher for EV Nova
- Language: Makefile/shell
- GitHub metadata observed: 79 stars, last pushed 2018-11-14

Relevance:

- Compatibility reference only.

Caveats:

- Not an engine.

### EV Stuff

- URL: https://andrews05.github.io/evstuff/
- Type: community downloads/resources index
- Observed content:
  - EV Nova Community Edition for Windows;
  - EV Nova mod 4 for macOS 10.9–10.14;
  - EV/O plug-ins, Nova plug-ins, utilities, guides;
  - EV Classic and EV Override packaged as Nova ports/TCs.

Relevance:

- Important discovery and preservation hub.
- Use to find canonical community packaging and plug-in resources.

Caveats:

- Treat as community preservation surface; verify individual downloads/resources separately.

### Ambrosia Garden

- URL: https://wiki.ambrosia.garden/doku.php?id=start
- Type: community wiki/archive
- Observed content:
  - resource for old Mac games/software created primarily by Ambrosia Software;
  - community forum, archived webboard, plugin hosting.

Relevance:

- Useful community documentation/archive source.

Caveats:

- Wiki/archive; verify technical claims against implementation/source when possible.

## EV-inspired but not EV-compatible engines/games

### Endless Sky

- URL: https://github.com/endless-sky/endless-sky
- Type: mature open-source EV-like space trading/combat game
- Language: C++
- Relevance: excellent systems reference for missions, economy, outfits, shipyards, combat, map, and data organization.
- Caveat: not an EV data/runtime engine; do not copy content or assume EV fidelity.

### Naev

- URL: https://naev.org/
- Type: open-source space exploration/trade/combat game
- Relevance: EV-adjacent systems/UI/economy reference.
- Caveat: not an EV runtime or compatibility project.

### WindRider

- URL: https://github.com/wraitii/WindRider
- Type: Godot 3D EV Nova-inspired game
- Language: GDScript
- GitHub metadata observed: 3 stars, last pushed 2020-01-05
- README note: author says they tried coding their own engine but found it too time-consuming, then chose Godot.
- Relevance: useful Godot/EV-like design reference, especially for tradeoffs around custom engines.
- Caveat: 3D and EV-inspired, not EV-compatible.

### JoshuaAFerguson/terminal-velocity

- URL: https://github.com/JoshuaAFerguson/terminal-velocity
- Type: SSH multiplayer EV-inspired Go game
- Language: Go
- License: MIT
- GitHub metadata observed: 2 stars, last pushed 2026-04-26
- Relevance: interesting name collision and multiplayer/TUI reference.
- Caveat: not an EV fidelity or resource-compatibility engine.

## Recommended next actions for Terminal Velocity

1. **Mine KestrelEngine first** for native engine architecture and classic Mac resource compatibility patterns.
   - Look at resource fork handling, QuickDraw/QuickTime abstractions, Lua API, resource-pack assembly, plugin replacement semantics, and Windows build/runtime boundaries.

2. **Mine NovaJS second** for EV Nova gameplay/data semantics.
   - Compare landing, hyperspace, targeting, weapons, outfits, shipyard, NPC traffic, plugin loading, and data contract assumptions against Terminal Velocity.

3. **Use EVNToEndlessSky + evnova-utils as cross-checks** for decoded data semantics.
   - Especially useful when mapping EVN templates, packed fields, mission/resource relationships, and pilot/context records.

4. **Keep OpenNova as historical context only** unless a specific ResourceFork/QuickDraw implementation detail proves useful.

5. **Use EV Nova CE / EV Stuff / Ambrosia Garden as community baseline references**, not as code architecture sources.

## Source-list candidates

These sources are high-value enough to consider adding to a reusable source registry if EV-fidelity research becomes recurring:

- KestrelEngine — primary source for a community bespoke classic-Mac/EV-family remaster engine.
- NovaJS — primary source for a direct EV Nova browser runtime reimplementation attempt.
- evnova-utils — primary-ish community toolkit for EV/EVO/EVN data inspection.
- EVNToEndlessSky — conversion/data-semantics reference.
- EV Stuff — community preservation and downloads hub.
- Ambrosia Garden — community archive/wiki/forum surface.

## Sources checked in this pass

- GitHub repository metadata and READMEs via GitHub API/raw README fetches:
  - https://github.com/Evocation-Games/KestrelEngine
  - https://github.com/mattsoulanille/NovaJS
  - https://github.com/dmaulikr/OpenNova
  - https://github.com/AhemOne/Escape-Velocity
  - https://github.com/edelventhal/EVNToEndlessSky
  - https://github.com/julbouln/evn2es
  - https://github.com/warp-core/endless-sky-rez
  - https://github.com/vasi/evnova-utils
  - https://github.com/EthanSuperior/EVNEW
  - https://github.com/ThrosturX/ev-merge
  - https://github.com/andrews05/EV-Nova-CE
  - https://github.com/RyuKojiro/novafix
  - https://github.com/wraitii/WindRider
  - https://github.com/JoshuaAFerguson/terminal-velocity
- Community/index pages:
  - https://escape-velocity.games/
  - https://wiki.ambrosia.garden/doku.php?id=start
  - https://andrews05.github.io/evstuff/
- Existing curated source registry entries for EV-adjacent engines:
  - Godot Engine docs/repo
  - MonoGame docs
  - Defold manuals
  - Endless Sky repository
  - Naev website

## Confidence

Medium-high for identifying the main visible community projects from GitHub/web search. Medium for completeness: the EV community also has Discord/forum-only knowledge and older archived tools that may not surface well in GitHub search. Treat this as a practical starting map, not an exhaustive bibliography.
