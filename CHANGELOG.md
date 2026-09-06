# Changelog

## Unreleased — 2026-09-05 (claude/dlss5-second-pass) — DLSS 5 second cross-check

Status unchanged: **Researched only.** Still nothing installed, injected, or run.

Codex made a second pass over `platform/nvidia-dlss/DLSS5_NEURAL_RENDERING.md`.
Most of it was an improvement and is kept; three points were adjusted.

### Kept from the second pass
- Brittle relative wording ("two days after launch") removed.
- "Only native title" softened to "only native title found in NVIDIA public
  material" — accurate about the limits of the search, not just the result.
- **Supply-chain risk downgraded from VERIFIED to HIGH CONFIDENCE**, and the risk
  restated more precisely: a one-click wrapper may well have buildable source, but
  the DLSS 5 add-on/model path it pulls in is the leaked, closed-source, third-party
  hosted part. That is the part that matters, and the original wording aimed at the
  wrong target.
- Real URLs added for every primary source, with secondary and community-only
  sources listed separately — including an explicit note that the VideoCardz article
  behind the App-override claim was **never read** (HTTP 402).

### Corrected against the second pass
- **The GTC 2026 line was removed as unsourced. It was not unsourced, and is
  restored — with the citation it should have carried in the first place.** NVIDIA's
  own GeForce article of 2026-03-17 states DLSS 5 was unveiled at GTC by the
  company's CEO. The criticism was still fair: an uncited claim is
  indistinguishable from an unsourced one.
- **Re-check date corrected from 2026-09-06 back to 2026-09-05.** The second pass
  ran the same evening, roughly twenty minutes later; 09-06 is only true in UTC,
  while every other date in this repository is local. A document whose value rests
  on precise dating should not imply a day of new information arrived when none did.
  The local-time convention is now stated explicitly at the top.
- **Restored the specific driver-store finding** that `nvngx_dlssg.dll` *is* present
  under `DriverStore/FileRepository/nv_dispi.inf_amd64_*`, alongside the second
  pass's broader search scope. The positive hit is what shows the search could have
  found `nvngx_dlssnr.dll` had it been there; without it the absence proves less.
- Restored the Unreal Engine 5 plugin alongside Streamline in the agreed-claims
  list — it is stated in NVIDIA's own DLSS 5 article and the fact table already
  carried it.

### Unchanged
- Claim 1 stands as VERIFIED: at inference the model consumes the rendered frame,
  engine motion vectors, carried temporal state and artistic-direction values;
  G-buffer and scene attributes are training-time supervision.
- `nvngx_dlssnr.dll` stays HIGH CONFIDENCE. "No NVIDIA App override" stays HIGH
  CONFIDENCE. All five open questions in section 7 remain open.

## Unreleased — 2026-09-05 (claude/research-dlss5-neural-rendering) — DLSS 5

Status: **Researched only.** Nothing installed, injected, or run. No in-game evidence.

### Added
- `platform/` — a new top-level area for cross-game hardware, driver and vendor
  technology reference. DLSS 5 is not game-specific, so it fits neither `games/`
  nor `projects/`. Registered in `AGENTS.md`.
- `platform/nvidia-dlss/DLSS5_NEURAL_RENDERING.md` — what DLSS 5 is, what it needs
  at runtime, and a three-tier feasibility assessment of forcing it into games that
  lack native support.

### Verified
- **DLSS 5 is not an upscaler.** It is a one-step pixel-space diffusion model that
  generates the final displayed appearance — the first DLSS to generate rather than
  reconstruct. Launched 2026-09-03; native support today is **NBA 2K27 only**;
  requires driver **616.64** and an **RTX 50** GPU; runtime DLL `nvngx_dlssnr.dll`.
- **The decisive finding, which most public coverage gets wrong:** at inference the
  model consumes only the rendered frame, engine motion vectors, carried temporal
  state and artistic-direction values. The albedo / normals / semantics / light-position
  data that articles list as inputs is **training-time consistency supervision**, not a
  runtime requirement. This is why injection is possible at all — the hard dependency
  is genuine engine motion vectors, exactly as with earlier DLSS.
- **NVIDIA has confirmed there is no DLSS 5 override in the NVIDIA App**, per-game or
  global. There is no supported route to force it on.
- **The Blood of Dawnwalker ships DLSS Super Resolution** (upgradeable to DLSS 4.5 via
  the NVIDIA App), **not DLSS 5** — but having an upscaler makes it a tier-2 candidate.
- Research machine environment, via `nvidia-smi`: RTX 5080, driver 616.64, 16,303 MiB —
  meets the DLSS 5 requirement, so no patched DLL or hardware bypass is needed here.

### Recorded, unverified
- Tier-2 injection over an existing upscaler (`OptiScaler_DLSSNR`) is COMMUNITY-CLAIMED
  and untested here; its own notes admit flashing or missing lights in some titles and a
  VRAM leak fixed only recently.
- Tier-3 injection via a ReShade optical-flow feeder is treated as unreliable: optical
  flow is inferred from pixels, engine motion vectors are ground truth, and no
  image-quality comparison against a native reference was found.
- RTX 40 bypass by patching CUDA binaries inside the model DLL is reported working on
  4090/4080 with mixed per-game results. Whether the RTX 50 gate sits in the DLL or the
  driver is UNVERIFIED.

### Safety
- A cluster of days-old repositories offering one-click DLSS 5 for every game were
  **read, not run**: precompiled executables with no source, claims contradicting NVIDIA's
  own engineers, and no explanation of how they supply motion vectors. DLSS Swapper's
  developer has separately warned of malware-bearing DLLs and lookalike sites.
- Rule recorded: model DLLs come from an official NVIDIA driver package or a game's own
  install, never from a mod bundle.

### Open questions
- Five items listed in section 7 of the findings document, including model parameter
  count and per-frame cost (NVIDIA Research's paper PDF is 403-blocked) and which SDK
  version first shipped `nvngx_dlssnr.dll`.

### Corrected after independent cross-check (2026-09-05)
Codex reviewed this document against NVIDIA and official sources with a brief to
falsify it. It confirmed the load-bearing claim (the inference-versus-training input
split) and found two places where the label was stronger than the sourcing. Both are
corrected, and section 8 of the findings document records the review.
- **`nvngx_dlssnr.dll` downgraded from VERIFIED to HIGH CONFIDENCE.** No NVIDIA
  primary source names the file. A search of this machine found only
  `nvngx_dlssg.dll` in the driver store and no `nvngx_dlssnr.dll` anywhere, and the
  latest public DLSS SDK (310.7.0) does not contain it either. The only native title,
  NBA 2K27, is not installed here, so this is absence of evidence rather than
  disproof — but it is not VERIFIED.
- **"No DLSS 5 override in the NVIDIA App" downgraded from NVIDIA-STATED to HIGH
  CONFIDENCE.** The basis was a headline reporting an NVIDIA confirmation, but that
  article returned HTTP 402 and was never read. The conclusion still stands on
  indirect evidence: Neural Rendering is absent from NVIDIA's documented App override
  options, and NVIDIA's own instructions point users to NBA 2K27's in-game settings.
- **Launch dating refined** to separate the GTC 2026 announcement, the 2026-09-01
  research-page publication, and 2026-09-03 availability in a shipping game.
- **Dawnwalker conclusion strengthened** with game-file evidence: the install carries
  `nvngx_dlss.dll`, `nvngx_dlssd.dll`, `nvngx_dlssg.dll` and Streamline DLLs, and no
  `nvngx_dlssnr.dll`.

## Unreleased — 2026-09-05 (claude/dawnwalker-doc-fixes) — audit of the 2026-09-04 work

### Re-verified against the live install
- **All seven Dawnwalker tools were re-run 2026-09-05 and all seven still work**:
  `gameversion.py`, `utoc.py`, `pak.py`, `extract.py`, `zen.py`,
  `containerheader.py`, and the profile's `verify.py`.
- The build fingerprint in `projects/dawnwalker-modding/GAME_VERSION.md` **still
  matches exactly** — Steam build `25129649`, all four SHA-256 hashes, and the base
  container's structure (TOC v8, 778,643 chunks, 1,056,336 blocks, flags `0x0b`).
  Every format finding in `games/blood-of-the-dawnwalker/` therefore still applies.
- `globals.py` still parses `global.ucas` to exactly 54,880 names / 58,720 script
  objects, cursor landing at 3,837,478 of 3,837,488.
- `containerheader.py` still reports `TILING VALID: True` on the SkillsNoTimeCost
  container header (528 imported-package refs).

### Fixed
- `games/blood-of-the-dawnwalker/tools/README.md`: the `pak.py` usage examples
  pointed at `~mods/~TBODoptimizedTweaksBASE_P.pak`, which was retired on
  2026-09-04 and moved into a `*-backup-*` folder — the documented command failed
  on a current install. Repointed at `~mods/~JohnRTX5080Quality_P.pak` and both
  forms (list and `x` extract) were run to confirm they work.

### Resolved
- The drift recorded on 2026-09-04 — installed pak at revision 1.1 while the repo
  source was still 1.0 — is **closed**. `verify.py` now reports "packaged INI
  matches repo source" with all five assertions passing.

### Open — UNVERIFIED, flagged not fixed
- `DAWNWALKER_RULES.md` §6 contains an internal tension: it states that mods load
  from `Content/Paks/` **and** from its `~mods/` subfolder, while also calling the
  `*-backup-*` folders kept *inside* `Content/Paks/` "a good rollback pattern".
  If the loader scans Paks subfolders recursively, those backups are not inert —
  three of them currently hold live `.pak`/`.utoc` files, including a **duplicate
  of the still-installed DualSenseAtlas container**. Not tested in game, so no
  claim is made either way; the safe move is to keep backups outside
  `Content/Paks/`. Left for whoever can test it in game.

### Process note
- The 2026-09-04 format research landed on `main` directly and no pull request was
  ever opened, which departs from the repo protocol (branch, PR, `main` stays the
  stable baseline). No work was lost. The `claude/dawnwalker-iostore-format` branch
  remains on origin at `84eed6b7f5165c5b37fe6da66f7d9859cd03ff61`, two commits
  behind `main` with **zero unique commits** — every commit on it is already in
  `main`. It is kept as a historical record of where that research was done.
  **Branches in this repo are not deleted after merging**; a merged branch is a
  record, and a stale-looking ref costs nothing next to losing the trail.
- This entry's own change was made the protocol way, as a correction to the above:
  branch `claude/dawnwalker-doc-fixes`, pull request, `main` untouched.

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
