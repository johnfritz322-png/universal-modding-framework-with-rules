# Baldur's Gate 3 — Game-Specific Modding Rules

Status: **starter ruleset**. Every implementation detail must still be verified against the exact current BG3 build and chosen toolchain before coding.

## BG3-specific rules
1. Record the exact BG3 game build before implementing or debugging version-sensitive behavior.
2. Decide explicitly whether a feature belongs in the official toolkit/data layer, Script Extender Lua/Osiris, or another verified BG3 mechanism. Do not mix layers without a reason.
3. Treat UUIDs, stat names, spell/status/passive identifiers, localization keys, resource references, and internal names as stable project data. Never invent or casually regenerate them.
4. Verify spell/status/passive/stat syntax against actual game data or known-working examples before creating records.
5. For Script Extender work, verify the required extender version and API behavior against Norbyte's current repository/documentation before use.
6. Keep client and server behavior conceptually separate when using Script Extender. Do not assume an event or API exists on both sides.
7. Prefer reusable, isolated systems for statuses, passives, spells, resources, and scripted mechanics rather than one monolithic script.
8. Do not claim a packaged mod works until BG3 loads it and the target feature is tested in-game.
9. Any mechanic that manipulates spells/actions dynamically must define persistence rules: temporary, until rest, until unequipped, per-save, or permanent.
10. Any mechanic that observes/copies enemy abilities must maintain an explicit eligibility filter and deny-list. Boss-only, quest-only, transformation, environmental, cinematic, internal/debug, and structurally incompatible actions must not be assumed safe to copy.
11. Keep a registry of every custom UUID/internal ID and the system that owns it.
12. Preserve a minimal test character/save for repeatable class, spell, status, resource, and Script Extender testing.

## Script Extender facts currently verified from maintainer sources
- Norbyte's BG3 Script Extender adds Lua/Osiris scripting support.
- Its maintainer documentation exposes APIs covering areas including Stats, timers, JSON, mod info, localization, templates, static data, resources, levels, engine events, networking, and UI-related facilities.
- A mod using Script Extender supplies a `Mods/<ModName>/ScriptExtender/Config.json` configuration describing required features/version.

These statements are a starting point, not permission to invent specific functions. Verify exact API names and signatures before coding.

## Required evidence before adding a BG3 technical rule
Use at least one of:
- actual BG3 project/game data,
- Larian-maintained toolkit/documentation,
- Norbyte BG3 Script Extender maintainer docs/repository,
- compiler/validator/log output,
- direct in-game test,
- a known-working open-source BG3 mod using the same mechanism.

## Project-specific extension
Each BG3 mod under `projects/` should maintain its own manifest, stable-ID registry, tested-game-build note, and implementation/verification status.
