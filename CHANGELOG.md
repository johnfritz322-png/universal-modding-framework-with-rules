# Changelog

## Unreleased — 2026-09-04 (claude/dawnwalker-iostore-format) — usmap research

### Added
- `projects/dawnwalker-modding/USMAP_PLAN.md`: a researched, step-by-step plan to
  dump a `.usmap`, which is the cheapest remaining unlock — it would turn
  `CONFIG_SURFACE.md` from "67 verified section names, unknown properties" into
  real property names, **without needing the AES key**.

### Verified
- **Real game build string** from the exe's PE version resource:
  `dw1-pc-257186-shipping-patch2-all-CL-257186` — patch 2, changelist 257186.
  Rebel Wolves replaced the stock Unreal version string, which is why earlier
  `++UE5+Release-5.x` searches found nothing.
- Engine narrowed to **UE 5.4 or 5.5**: the build ships `UniversalObjectLocator`
  and `WorldConditions` (both 5.4+), alongside libcurl 8.4.0, TOC v8, header v4.
- **No anti-cheat** in the install — runtime dumping is viable.
- **Property names DO ship in the exe.** `DaysToPass` sits at `0x8e84c10` inside a
  length-bucketed name pool (10-char names padded to 16 bytes). Recorded together
  with why this is *not* a shortcut: a flat name pool carries no class→property
  association, which is the whole point of a `.usmap`.

### Recorded, unverified
- Stock UE4SS is expected to **crash this game** — it cannot auto-detect the engine
  version, and two default hooks crash it even when the version is set manually.
  A Dawnwalker-specific preconfigured UE4SS package exists and is the right start.
- That package targets Steam build `25107392`; this install is `25129649`
  (patch 2), so its signatures may be stale. First launch is a test, not routine.
- Community discussion indicates a public AES key for this game exists. **Not
  obtained, not tested** — recorded only so the option is visible.

## Unreleased — 2026-09-04 (claude/dawnwalker-iostore-format) — update check

### Added
- `projects/dawnwalker-modding/GAME_VERSION.md`: the installed build fingerprint —
  Steam app **3751260**, build **25129649**, installed 2026-09-04 23:49 UTC, plus
  SHA-256 of `global.utoc` / `global.ucas` / `Dawnwalker-Windows.utoc` / the exe and
  the base container's structural fingerprint. Also records what a future patch
  would and would not break.
- `games/blood-of-the-dawnwalker/tools/gameversion.py`: regenerates that fingerprint
  in seconds. Run it first in any session — if it matches, all format findings hold.

### Verified
- **The game is on the newest build and the research already reflects it.** The
  install was patched 2026-09-04 at 17:49 local (~2.19 GB); the format research was
  carried out from ~21:00 the same evening, i.e. **after** the patch.
- Re-checked after the update: base container id `0x8fc20dab729a0600`, TOC v8,
  778,643 chunks, 1,056,336 blocks, flags `0x0b` — **all identical** to the recorded
  values. `global.ucas` still parses to exactly 54,880 names and 58,720 script
  objects. `CONFIG_SURFACE.md` needs no revision.
- Steam reports nothing queued (`ScheduledAutoUpdate 0`), install complete
  (`StateFlags 4`), last update clean (`UpdateResult 0`).

### Labelled honestly
- That build `25129649` **is** Hotfix 1.0.2 / console update 1.004 (released
  2026-09-03) is **HIGH CONFIDENCE, not VERIFIED** — matched by patch date and
  download size only. No public source publishes Steam build ids for this game.

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

### Resolved same day
- The repo/install desync is **fixed**. Codex pushed revision 1.1 to `main`; this
  branch merged it and re-verified — `verify.py` now passes every check including
  drift. Codex's recorded SHA-256 and the value computed here by unrelated code
  **agree**, so the installed artifact is confirmed by two toolchains.
- Fixed a false positive in `verify.py`: a trailing blank line was reported as
  drift. A noisy check gets ignored, which is worse than no check, so the
  comparison now normalises line endings and trailing whitespace.

### Open — for Codex
- The **2048 MB Nanite allocation failure** is referenced only in an INI comment.
  The observation behind it — what was seen, where, on what settings — is written
  down nowhere. It is the only in-game observation either agent has on this game
  and belongs in `games/blood-of-the-dawnwalker/KNOWN_LIMITATIONS.md`.

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
