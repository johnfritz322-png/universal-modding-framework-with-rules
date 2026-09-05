# Changelog

## Unreleased — 2026-09-04 (claude/dawnwalker-iostore-format)

First game added to the framework besides BG3.

### Added
- `games/blood-of-the-dawnwalker/DAWNWALKER_RULES.md`: the UE5 IoStore, Zen package,
  container-header and legacy-pak formats, decoded by direct binary analysis of the
  shipped files and validated structurally — section sizes sum to file size, index
  SHA-1s recomputed, container-header arrays tile exactly to the declared end.
- `games/blood-of-the-dawnwalker/CONFIG_SURFACE.md`: **67 settings classes that
  shipped in the retail build**, addressable as `[/Script/Module.Class]` from an INI.
  This is the practical route to more mods while the AES key is unavailable, and it
  is the single most useful artifact of this pass.
- `games/blood-of-the-dawnwalker/KNOWN_LIMITATIONS.md` and `SOURCES.md`.
- `games/blood-of-the-dawnwalker/tools/`: six dependency-free Python readers for
  `.utoc`, `.ucas`, Zen `.uasset`, `global.ucas`, container headers and legacy paks.
  They read this game's mod containers, which the local UnrealPak cannot.
- `projects/dawnwalker-modding/PROJECT_MANIFEST.md`: the project's review record.
- `projects/dawnwalker-modding/profiles/john-rtx5080-quality/verify.py`: structural
  verification that shares no code with repak or UnrealPak, plus drift detection
  between the installed package and the repo source.

### Resolved
- **"What do we need for bigger mods?"** — mostly answered. Reading mod containers,
  reading `global.ucas`, and building config mods all need **no** extra tooling.
  Only three things remain blocked: the AES-256 key (base assets), an Oodle
  decompressor (reading the base container), and a `.usmap` (interpreting cooked
  data assets). Practical order: config mods now, `.usmap` next, AES key last.
- **Mod containers do not have to match the base game.** The base container is
  Oodle + AES; shipped working mods use `None`/`Zlib` with no encryption. Writing
  Oodle or AES is never necessary.
- **The engine resolves packages by chunk ID, not path.** A shipped mod stores bare
  filenames with no directory structure and works. The directory index is cosmetic.

### Corrections
- Two UE struct readings that silently produce garbage *resembling encryption*:
  `FIoStoreTocHeader`'s perfect-hash seed count is at offset **84**, not 52; and
  `FFilePackageStoreEntry`'s `CArrayView` offset is relative to the **array-view
  member's own address**, not to the offset field. Both are recorded because both
  cost real time and both mimic a legitimate-looking failure.
- Corrected my own earlier claim that `00000000_SkillsNoTimeCost_P` ships no `.pak`.
  It does — a 347-byte stub. That was a misread of a directory listing.
- `Dawnwalker-Modding-Map.md`: the recorded installed-package SHA-256 was stale
  (revision 1.0); the installed package is revision 1.1. Both now recorded.

### Open — for Codex
- The repo source for `john-rtx5080-quality` is **behind** the installed package,
  and the version in the repo carries `r.Nanite.Streaming.StreamingPoolSize=2048`,
  which revision 1.1's own comment says hits an allocation failure. Revision 1.1
  was deliberately **not** auto-committed: it encodes an in-game observation that
  cannot be verified from this side (AGENTS.md rules 1 and 9). Codex should push it
  with its evidence.

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
