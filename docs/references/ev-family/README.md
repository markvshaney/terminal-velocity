# EV-family primary/manual references

Local reference copies for Terminal Velocity source-and-fidelity work. Treat these as **primary or manual-adjacent technical references for EV-family resource/plugin semantics**, not as automatic proof of original EV Classic runtime behavior. Original EV Classic runtime observations remain the highest-fidelity source for exact player-visible behavior.

## Saved references

- `ev-classic-resource-bible.pdf` / `ev-classic-resource-bible.txt`
  - Source URL: `https://macos.retro-os.live/jdownloads/MacOS%20Files/Color%20Apps/Escape_Velocity_Resource_Bible.pdf`
  - SHA256: `8d406bc48baa8044a209b9cf778d80d58c4ac7835ed16d8b4f6d29c4c5f742d3`
  - Use for: EV Classic resource/plugin fields and terminology. Text extracted locally with `pypdf` for searchability.

- `ev-override-resource-bible-1.0.2.pdf` / `ev-override-resource-bible-1.0.2.txt`
  - Source URL: `http://www.cytheraguides.com/archives/ambrosia_addons/evo/Guides/2386_OverrideBible102.pdf`
  - SHA256: `78a5c89bc07179dd71432367a09567527cf995cff10485bb8fe4f77750356f5d`
  - Use for: Override-era resource/plugin semantics that often bridge EV Classic and Nova, with source-family labeling. Text extracted locally with `pypdf` for searchability.

- `ev-nova-bible.html`
  - Source URL: `https://andrews05.github.io/evstuff/guides/evnbible.html`
  - SHA256: `02c06417892edf9c6115711743a0a573e58d04571f8bfff88e5831bfb76bc4b8`
  - Use for: Nova technical resource semantics, including government fields such as `CrimeTol` and `ScanFine`, mission bits/control bits, plugin replacement behavior, and legal/mission/resource modeling guidance.

- `ev-bible-app-page.html`
  - Source URL: `http://www.youtellme.meadowsweetfarm.com/software/evBible.htm`
  - SHA256: `8af39a1ce02ff1f9f1dcfdadabaadcfb21076cb619ff4172f7efa3a3b37a6a41`
  - Use for: provenance/discovery page for the EV Bible application, which describes EV/Override and EV Nova Bible coverage.

- `escape-velocity-games-docs.html`
  - Source URL: `https://escape-velocity.games/docs`
  - SHA256: `fc3f92d8d950ef4e2c8d0aff6da5f0453d7e107726cc16e6be71c3c37269aed9`
  - Use for: modern community documentation around EV Nova data/plugin installation/conversion context. This is not primary Classic behavior evidence.

## Fidelity rule

When implementing Terminal Velocity behavior from these references:

1. Prefer `ev-classic-resource-bible.pdf` for Classic resource semantics.
2. Use Override/Nova Bibles as EV-family structured guidance when Classic evidence is missing.
3. Label inferred mechanics as `Terminal Velocity scaffold` or `approved inference pending EV Classic confirmation` until runtime/resource evidence confirms exact Classic behavior.
4. Cross-link implemented slices back to `docs/checklists/ev-classic-fidelity-implementation-backlog.md`.
