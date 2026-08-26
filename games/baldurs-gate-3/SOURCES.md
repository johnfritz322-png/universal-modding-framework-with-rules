# Baldur's Gate 3 — Source Registry

Use this file to track technical sources that are trusted enough to support implementation decisions. Re-check version-sensitive sources before major changes.

## Primary / maintainer sources

### Norbyte — BG3 Script Extender
- Repository: https://github.com/Norbyte/bg3se
- API documentation: https://github.com/Norbyte/bg3se/blob/main/Docs/API.md
- Releases: https://github.com/Norbyte/bg3se/releases
- Purpose verified from maintainer README: adds Lua/Osiris scripting support to Baldur's Gate 3.

## Source policy
Before accepting a new technical claim as VERIFIED, record:
- source URL or local game/project file,
- date checked,
- exact BG3/tool version where relevant,
- what claim it verifies,
- whether it was also confirmed by compilation/logs/in-game testing.

## Research still required per project
- Exact current BG3 game build.
- Official toolkit version and documentation relevant to the requested feature.
- Exact Script Extender API functions/events used.
- Exact game-data records, UUIDs, stats, spells, passives, statuses, and localization keys referenced.
- Save/persistence behavior for custom scripted mechanics.

---

## Sources added 2026-08-25

From `projects/bg3-cursed-arts`, BG3 Patch 8, Windows/Steam.

### Primary — shipped game data (highest confidence)

- **The shipped `.pak` files**, unpacked with LSLib/Divine:
  `D:\steam\steamapps\common\Baldurs Gate 3\Data\*.pak`
  Modules used: `Shared`, `Gustav`, `GustavX`, `Icons`, plus `SharedDev`/`GustavDev`.
  Checked 2026-08-25. Verifies: every field-count and vocabulary claim in `BG3_RULES.md`
  (`StatusType` 4631/4631, `SpellAnimation` 9 slots 652/652, `ApplyStatus` keyword
  frequencies, absence of `AlwaysSucceed`, absence of any `OnDeath` context,
  `Summon()` argument positions, `FactionOverride` carriers, faction UUIDs).
  Also confirmed by validator output and, for the icon findings, direct in-game test.

### Tooling

- **LSLib / Divine** — `C:\Tools\LSLib\Packed\Tools\Divine.exe`.
  Repository: https://github.com/Norbyte/lslib
  Used for `extract-package`, `create-package`, `list-package`, `convert-resource`
  (`.lsf` <-> `.lsx`). Checked 2026-08-25.
- **texconv (Microsoft DirectXTex)** —
  https://github.com/microsoft/DirectXTex/releases/latest/download/texconv.exe
  Version 2026.5.8.1, checked 2026-08-25. Verifies the DDS format claims. Required
  because Pillow writes structurally invalid DDS for this use.

### Community documentation

- **bg3.wiki — Modding: Item icons** — https://bg3.wiki/wiki/Modding:Item_icons
  Checked 2026-08-25. **MODERATE**, and corroborated in-game for the part that mattered:
  it correctly states that an atlas must be registered as a resource, which was the
  missing piece behind blank spell icons. **It disagrees with shipped data elsewhere** —
  it advises "no mipmaps" for the atlas, while a working mod ships a full mip chain and
  functions. Where wiki and working mod disagree, **the working mod won**.
- **Larian modding docs** — https://docs.baldursgate3.game/Adding_Skill_and_Item_Icons
  Returned HTTP 403 to automated fetch on 2026-08-25; not usable as a checked source.

### Known-working reference mods (HIGH CONFIDENCE)

Three third-party BG3 class mods, unpacked and diffed field by field. Used only as
technical reference; no assets or code reused.

- **Demon Slayer Class** (`DemonSlayerClass_59755707-…`) — the most structurally complete;
  source of the class-icon DDS format and `metadata.lsf` conventions.
- **JujutsuKaisen** (`JujutsuKaisen_17921de7-…`) — the only one shipping a custom spell
  atlas; source of the `TextureBank` registration pattern.
- **JujutsuSorcerer** (`JujutsuSorcerer_b8b11bc0-…`) — third data point confirming the
  `metadata.lsf` conventions are unanimous rather than incidental.

Diffing against these resolved more than the documentation did. When a claim here is
marked HIGH CONFIDENCE rather than VERIFIED, it usually means "three working mods agree
but it has not been isolated in a controlled test".

### Related local resource

- **bg3-class-forge** — https://github.com/Jwillbur/bg3-class-forge
  A class-mod scaffold generator plus nine deliberately-broken fixtures for measuring a
  validator. Checked 2026-08-25.
