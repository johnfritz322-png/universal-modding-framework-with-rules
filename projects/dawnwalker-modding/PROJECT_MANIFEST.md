# Project Manifest — Dawnwalker Modding

**Last updated: 2026-09-04 by Claude.** This is the review/handoff record for this
project. Codex: the open items for you are in **§ Handoff** at the bottom.

## Identity
- Project name: Dawnwalker Modding
- Game: The Blood of Dawnwalker (Rebel Wolves) — internal codename **Dogwood**
- Exact game version/build: not exposed as a string in the binary. Container
  fingerprint instead: base TOC v8, container-header v4, `Dawnwalker-Windows.utoc`
  70,109,154 B / 778,643 chunks, `global.ucas` 3,837,488 B. Use those to detect a
  game patch.
- Platform: Windows / Steam
- Engine: Unreal Engine 5 (**likely 5.5** — ASSUMPTION, see game rules §1)
- Mod version: profile `john-rtx5080-quality` **revision 1.1** (installed)

## Toolchain
- Mod loader/framework: none — stock UE pak/IoStore mounting
- SDK/toolkit: none available (no editor, no `.usmap`)
- Script extender: none
- Compiler/runtime: PowerShell 5.1, Python 3.14
- Packaging tool: `repak v0.2.3` — `C:\Users\johnf\Documents\Codex\Tools\repak-v0.2.3\repak.exe`
- Other tools:
  - `UnrealPak.exe` (2021 build) — `D:\Vortex Mods\palworld\UnrealPakTool\UnrealPakTool\UnrealPak.exe`.
    Reads simple config paks. **Cannot** read this game's `.ucas`/`.utoc`.
  - `games/blood-of-the-dawnwalker/tools/*.py` — dependency-free readers for
    `.utoc`/`.ucas`/Zen packages/container headers/legacy paks.

## Dependencies
| Dependency | Version / range | Required? | Verified source |
|---|---|---|---|
| repak | v0.2.3 | yes, to build | present on disk, invoked by `build.ps1` |
| UnrealPak | UE4-era 2021 | optional cross-check | present on disk |
| Python | 3.x | optional, for verification | 3.14.7 present |
| AES-256 key for base container | unknown | **only for asset mods** | **NOT AVAILABLE** — see KNOWN_LIMITATIONS L1 |
| `.usmap` mappings | n/a | **only for data-asset edits** | **NOT AVAILABLE** — L3 |

## Repository state
- Project root: `projects/dawnwalker-modding`
- Default branch: `main`
- Current work branch: `claude/dawnwalker-iostore-format`
- Last known-good build: `~JohnRTX5080Quality_P.pak` rev 1.1,
  SHA-256 `4C6CD96937480E29C05FD0DE4744AD91D0E1ABA21401F8298530C097CFF1B00B`
- Current milestone: format fully decoded; config-mod surface mapped
- Next milestone: obtain a `.usmap`, then test the character-development config
  hypothesis (see below)

## ⚠ Known desync — needs Codex action
The **installed** package is revision 1.1. The **repo source** in
`profiles/john-rtx5080-quality/pak-root/` is still the older revision.

| | INI bytes | SHA-256 (first 16) |
|---|---|---|
| installed (in `~mods`) | 2,833 | `a739cc960ae66b04` |
| repo source | 2,634 | `536058214623129c` |

Revision 1.1 (installed, **not** in the repo) changes:

```diff
+; Revision 1.1 - high-refresh stability pass.
+r.Streaming.MaxNumTexturesToStreamPerFrame=24
+r.Streaming.NumStaticComponentsProcessedPerFrame=32
+r.Streaming.ParallelRenderAssetsNumWorkgroups=8
-; Nanite: reduce geometry cache churn while retaining several GB of GPU headroom.
-r.Nanite.Streaming.StreamingPoolSize=2048
-r.Nanite.Streaming.MaxPageInstallsPerFrame=128
+; Nanite: stay below the game's observed 2048 MB allocation failure point.
+r.Nanite.Streaming.StreamingPoolSize=1792
+r.Nanite.Streaming.MaxPageInstallsPerFrame=64
+s.AllowMultithreadedLoading=1
+s.AdaptiveAddToWorld.Enabled=1
+s.AsyncLoadingTimeLimit=5.0
-s.IoDispatcherBufferMemoryMB=64      → +128
-s.IoDispatcherCacheSizeMB=512        → +2048
-s.IoDispatcherDecompressionWorkerCount=6 → +8
```

**I deliberately did not commit revision 1.1 into `pak-root/`.** Codex was mid-work
and owns that content; the comment "the game's observed 2048 MB allocation failure
point" implies an in-game observation I have no evidence for and must not
paraphrase or claim. Codex should push the 1.1 source and the evidence behind it.

Also stale: `Dawnwalker-Modding-Map.md` recorded SHA-256
`C3F13F82…D8F06` for the installed package. That is revision 1.0. Corrected there.

## Owned files
```
projects/dawnwalker-modding/
├─ README.md
├─ PROJECT_MANIFEST.md                      (this file)
├─ Dawnwalker-Modding-Map.md
├─ profiles/john-rtx5080-quality/
│  ├─ README.md
│  ├─ build.ps1                             (repak-based build — Codex)
│  ├─ verify.py                             (dependency-free verification — Claude)
│  └─ pak-root/
│     ├─ Dawnwalker/John RTX 5080 Profile.txt
│     └─ Engine/Config/Windows/WindowsEngine.ini
└─ reference/mod42_optimized_tweaks_base/   (VynnGfx reference, extracted)

games/blood-of-the-dawnwalker/              (format research — Claude)
├─ DAWNWALKER_RULES.md
├─ KNOWN_LIMITATIONS.md
├─ CONFIG_SURFACE.md
├─ SOURCES.md
└─ tools/*.py
```

Generated artifact (not in repo): `dist/~JohnRTX5080Quality_P.pak`.

## Stable identifiers
| Identifier | Value | Notes |
|---|---|---|
| Package filename | `~JohnRTX5080Quality_P.pak` | `~` prefix + `_P` steer mount order — do not rename casually |
| Mount point | `../../../` | required; matches every shipped mod |
| Pak version | 3 | matches the VynnGfx reference mod |
| Base container id | `0x8fc20dab729a0600` | changes on a game patch |
| `global.ucas` chunk | `ScriptObjects`, 3,837,478 B | fingerprint for patch detection |

## Vanilla systems touched
Currently **only engine console variables** via `Engine/Config/Windows/WindowsEngine.ini`
(streaming, Nanite, PSO/shader cache, async loading, task graph, D3D12, input).
**No game assets and no gameplay data are modified by this project.**

Observed on this install but owned by third-party mods, not this project:
`/Script/Quest.QuestSettings` (Better Story Timer), the Xbox controller glyph atlas
(DualSense mod), 112 `DA_Trait_*` data assets (Perks Have No Time Cost).

## Architecture
A source tree (`pak-root/`) mirroring the game's mount layout, packed by `repak`
into a version-3 pak mounted at `../../../`, dropped into `Content/Paks/~mods/`.
Unreal reads the packed `WindowsEngine.ini` at startup as if it were on disk.
No code, no hooks, no runtime component.

## Verified features
| Feature | Verification state | Evidence | Last tested |
|---|---|---|---|
| Package is a structurally valid v3 pak | **VERIFIED** | `verify.py`: index SHA-1 recomputed and matched; independent of repak | 2026-09-04 |
| Mount point / file set / no encryption / no compression | **VERIFIED** | `verify.py` assertions all pass | 2026-09-04 |
| Package is installed and active | **VERIFIED** | present in `Content/Paks/~mods/` | 2026-09-04 |
| Config-mod technique works on this game | **VERIFIED (third-party)** | VynnGfx mod 42 uses the identical shape | 2026-09-04 |
| Loose `Game.ini` override technique | **VERIFIED on disk** | Better Story Timer; `/Script/Quest/QuestSettings` confirmed in shipped tables | 2026-09-04 |
| 67 game settings classes exist | **VERIFIED** | parsed from `global.ucas` → `CONFIG_SURFACE.md` | 2026-09-04 |
| **Does rev 1.1 improve anything in game?** | **NOT VERIFIED HERE** | Codex's own testing; no evidence in this repo | — |

## Experimental / unverified features
| Feature | Status | Main uncertainty | Next verification step |
|---|---|---|---|
| Perk time cost via config instead of 112 asset replacements | HYPOTHESIS | Is the cost a `config` property on `DogwoodCharacterDevelopmentSettings`, or baked into each data asset? | Dump a `.usmap`, inspect that class's properties |
| Editor/debug settings classes active in retail | UNVERIFIED | Cooked builds usually strip editor behaviour | Probe `[/Script/DogwoodDebug.DogwoodDebugSettings]` |
| `Game.ini` must be read-only to persist | HIGH CONFIDENCE | Standard UE behaviour, untested here | Clear read-only, relaunch, re-read the file |
| Property names on any settings class | UNVERIFIED | Not in `global.ucas` | `.usmap` |

## Compatibility
- Known compatible: DualSense Atlas (UI textures), Perks Have No Time Cost
  (data assets), Better Story Timer (loose `Game.ini`). **No overlap** — this
  project only writes `Engine/Config/Windows/WindowsEngine.ini`.
- Known conflicts: **any other performance-tweaks pak.** `~TBODoptimizedTweaksBASE_P.pak`
  writes the same file. Only one may be active; the retired one is in
  `Content/Paks/PerformanceTweaks-backup-20260904-213547/`.
- Shared edit surfaces: `Engine/Config/Windows/WindowsEngine.ini`.

## Save / persistence notes
- Safe on existing saves? **Yes, HIGH CONFIDENCE** — engine CVars only, no game state.
- Safe to update mid-save? Yes, same reasoning.
- Safe to uninstall mid-save? Yes — delete the pak, settings revert.
- Fresh-save testing required? No.
- Caveat: this reasoning does **not** extend to gameplay config mods
  (`CONFIG_SURFACE.md`). Changing `DaysToPass` mid-playthrough alters a live story
  clock and is **NEEDS TESTING** for save safety.

## Known bugs and limitations
1. Repo source is **behind** the installed package (see desync above).
2. `r.Nanite.Streaming.StreamingPoolSize=2048` in the repo source is reported by
   the rev 1.1 comment to hit an allocation failure. Building from current repo
   source may therefore produce a **known-bad** package. Fix the desync first.
3. Asset mods blocked on the AES key (L1) and Oodle (L2).
4. Data-asset edits additionally blocked on `.usmap` (L3).
5. `build.ps1` hard-codes tool paths under `C:\Users\johnf\Documents\Codex\Tools\`;
   not portable, but fine for this machine.

## Test procedure
- Launch steps: place the pak in `Content/Paks/~mods/`, ensure no other
  performance pak is present, restart the game.
- Build: `powershell -File profiles/john-rtx5080-quality/build.ps1`
- Validate (independent): `python profiles/john-rtx5080-quality/verify.py`
  — exit 0 = pass. Also run it against the **installed** file to catch drift.
- Regression: confirm the other three mods still behave (controller glyphs, perk
  time cost, story timer at 91 days).
- Logs: `%LOCALAPPDATA%\Dawnwalker\Saved\Logs\` — UE logs unknown INI keys, which
  is the cheapest way to test whether a guessed config property exists.

## Build and release
- Build: `build.ps1` (repak `pack --version V3 --mount-point '../../../'`)
- Validation: `build.ps1` runs `repak info` / `repak list` / `UnrealPak -Test`;
  `verify.py` adds an independent structural check and drift detection
- Artifact: `profiles/john-rtx5080-quality/dist/~JohnRTX5080Quality_P.pak`
- Rollback: timestamped `*-backup-*` folders in `Content/Paks/`

---

## Handoff — for Codex

1. **Push revision 1.1's source** into `pak-root/Engine/Config/Windows/WindowsEngine.ini`.
   The repo currently ships a configuration your own comment says fails.
   I did not commit your file because I cannot verify the in-game observation
   behind it (AGENTS.md rules 1 and 9).
2. **Record the evidence** for the 2048 MB Nanite allocation failure — what was
   observed, where. That is a genuine engine-limit finding and belongs in
   `games/blood-of-the-dawnwalker/KNOWN_LIMITATIONS.md` once written down.
3. **Review `games/blood-of-the-dawnwalker/`** — format reference, limitations,
   config surface, and six dependency-free parsers.
4. **`CONFIG_SURFACE.md` is the main new capability.** 67 shipped settings classes
   reachable by the technique Better Story Timer already proves works. Section
   names are VERIFIED; property names are not — don't guess them.
5. **Decide the AES-key question** (KNOWN_LIMITATIONS L1). Everything asset-related
   is blocked behind it; everything config-related is not.
6. Consider running `verify.py` from `build.ps1` so drift is caught at build time.
