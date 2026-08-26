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
- BG3 findings 29-32, confirmed only: **the defeat-to-tame summon loop works in pure
  stats with no Script Extender** (hostile summon, killing blow detected, permanent
  reward status — both halves observed in game); a single `SpellProperties` may hold
  several `GROUND:IF(...):Summon(...)` branches, per `Target_MageHand`; negative
  `DamageBonus` is not attested anywhere; and `UnlockSpell` on a status boost did not
  surface a new hotbar button in one observed attempt.

### Confirmed since
- BG3 finding 33: `CharacterLevelGreaterThan(n)` works inside a summon branch, so a
  shipped creature can be tiered to the summoner's level. Observed in game: a worg
  weakened by `IncreaseMaxHP(-13);AC(-2)` is a winnable level 1 fight where the
  unmodified creature is not. This is the piece that makes summoning real game creatures
  viable as a player mechanic at all.

### Added (fourth pass)
- BG3 findings 34-35, both verified against shipped data: the `Level` field on creature
  stats is not the encounter level and reads `1` for almost everything (Ansur at 400 HP
  included), so it cannot be used to judge creature strength; and `Vitality` is often
  inherited and must be resolved through `using` or real creatures silently read as
  having no HP.

### Corrected
- The summon-patterns section was first published claiming five findings were "verified
  in-game". Two were deployed but untested and one was an inference never observed. The
  section now separates confirmed from not-yet-confirmed, and the untested material is
  held out of the repo until a test result exists.

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
