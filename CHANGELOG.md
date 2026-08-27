# Changelog

## Unreleased — 2026-08-26

### Added — 2026-08-26 (second pass)
- **BG3 findings 48-53.** Two of them are direct in-game observations rather than corpus
  reads: a melee spell without `TargetRadius` has no reach and fires from any distance,
  and a ground-targeted teleport without `TargetConditions` silently does nothing.
  Also: the `Cast2[...]`/`Cast3[...]` multiattack mechanism and the
  `AlternativeCastTextEvents` field its animations depend on, `DownedStatus()` for
  surviving a killing blow, and evidence that `modsettings.lsx` checksums are not
  enforced.
- **Universal rules 43 and 44**, both from tooling that lied this session: a checker that
  reads its own build output cannot see source rot, and a search tool reporting "never
  used" should be doubted before the engine is.

### Corrected
- **`Summon()` takes character OR item templates.** This file previously published
  "character only", which is wrong: vanilla passes characters 99 times and items 46
  times, and items are how every persistent aura or zone is built. A gate demanding a
  character rejects 46 legitimate patterns.

### Retracted
- **"A guaranteed critical hit is not expressible in BG3" was wrong** and is retracted
  rather than deleted. `CriticalHit(AttackRoll,Success,Always)` and `ForcedAlways` both
  exist and work; the claim came from the absence of a single different token,
  `AlwaysSucceed`, generalised into an engine limitation. Universal rule 38 names this
  exact failure and was already in this repo when it happened.

### Added
- BG3 findings 42-45: guaranteed crits are expressible; `ReduceCriticalAttackThreshold(N)`
  tunes crit chance; a crit needs an attack roll, so "cannot miss" and "can crit" are
  reconciled with a large `RollBonus(Attack,N)`; and Boosts can be scoped to one spell
  with `IF(SpellId('...'))`.
- BG3 findings 36-41: how persistent zones and domains are built (an item template plus
  an aura status); that auras can tell friend from foe (213 of 237 use `IF(...)`); that
  melee spells must declare `MeleeMainWeaponRange` or the character never walks into
  position; that `RegainHitPoints` is not attested in `SpellFail`; and what
  `StatusType "INCAPACITATED"` actually does.
- A silent-failure entry for the missing melee range, which presents as an animation bug.

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

### Corrected (pre-merge review, PR #2)
- Project docs still described `UnlockSpell(...)` on a status boost as granting the ally
  summon. That design **did not work** and was replaced by branch-based summoning; the
  manifest and README now describe the confirmed design and record the failed one as a
  finding.
- README still said the tame half had failed with a retest pending. It has since been
  confirmed working end to end; replaced with the observed result.
- Manifest localisation handle range said `01-26`; actual is `01-83` with **103 handles**
  defined (validator-reported).
- `SOURCES.md` gained a direct in-game evidence table mapping each observation to the
  findings it supports, plus an explicit **NOT verified in game** section naming the
  eleven generated shikigami, the revised difficulty curve, the Worg's own rewritten
  branches, and the summon-tier inference.

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
