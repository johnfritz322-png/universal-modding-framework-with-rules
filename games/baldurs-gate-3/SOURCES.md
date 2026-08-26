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
