# Changelog

## Unreleased — 2026-08-25 (claude/bg3-verified-findings)
### Added
- Universal rules 37-42, the six earned from real failures rather than published guidance:
  change one variable per test; a null search result is not proof of absence; present is
  not valid; prove every check fails on broken input; let test-cycle cost set batch size;
  build the verification substrate before the feature. Each carries its incident.
- `games/baldurs-gate-3/BG3_RULES.md`: 25 verified findings for class mods on Patch 8 —
  structure and loading (subclass dialects, mandatory fields, `using`, localisation),
  measured stats syntax, summons, and the two mandatory icon registrations.
- `games/baldurs-gate-3/KNOWN_LIMITATIONS.md`: confirmed engine limits and a
  silent-failure catalogue for things that fail with no error at all.
- `games/baldurs-gate-3/SOURCES.md`: shipped game data, LSLib/Divine, texconv, bg3.wiki,
  and three known-working reference mods, each with date checked.
- `projects/bg3-cursed-arts/`: manifest and README for a playable JJK class mod.

### Resolved
- **Can `FactionOverride` make a summon hostile? YES** — verified in-game. Summons
  normally inherit the caster's faction; a status carrying `FactionOverride` plus
  `LoseControl` overrides it. Hostile-summon mechanics need no Script Extender.

### Added (second pass)
- BG3 findings 26-28: fields are **type-scoped**, and a field on the wrong entry type is
  **ignored rather than rejected**. `StatsFunctorContext`/`Conditions`/`StatsFunctors` are
  PassiveData-only; a status attaches logic by granting a passive. Found the hard way, by
  a mechanic whose hostile half worked and whose reward never fired.

### Added (third pass)
- BG3 findings 29-33: one spell can carry several `GROUND:IF(...):Summon(...)` branches,
  so a single button changes behaviour by state and by `CharacterLevelGreaterThan(n)`
  tier. More reliable than `UnlockSpell` on a status boost, which did not surface a new
  button in testing. Negative `DamageBonus` is not attested; weaken through HP and AC.
- **The full defeat-to-tame summon loop is confirmed working in pure stats, no Script
  Extender**: hostile summon, killing blow detected, permanent reward status, and a later
  cast reading that status to summon the same creature as an ally.

### Notes
- BG3 findings are labelled individually. Most are VERIFIED against shipped data or
  in-game observation; `SharedDev` template addressability remains HIGH CONFIDENCE.
- A guaranteed critical hit is **not expressible** in BG3 stats. Recorded as a hard limit.

## Unreleased
### Added
- Universal AI game modding hard rules.
- `AGENTS.md` operating instructions for AI coding agents.
- Project manifest, test-plan, and compatibility-report templates.
- Baldur's Gate 3 starter rules, source registry, and limitation tracker.
- BG3 Copy Ninja project design and manifest.
- Contribution workflow for branch/PR-based collaboration.

### Notes
- BG3 technical implementation remains intentionally unverified until the exact game build, toolchain, and APIs are checked for the project.
