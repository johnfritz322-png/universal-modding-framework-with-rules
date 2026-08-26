# Project Manifest — CursedArts

## Identity
- Project name: CursedArts (a Jujutsu Kaisen class mod)
- Game: Baldur's Gate 3
- Exact game version/build: Patch 8
- Platform: Windows 11 (26200), Steam
- Engine: Divinity 4.0
- Mod version: **1.10.0.0**

## Toolchain
- Mod loader/framework: native `modsettings.lsx` (no mod manager in the loop)
- SDK/toolkit: none; data authored directly and packed with LSLib
- Script extender: installed on the machine, but **the mod does not require or use it**
- Compiler/runtime: Python 3.14, PowerShell
- Packaging tool: LSLib / Divine.exe (`C:\Tools\LSLib\Packed\Tools\Divine.exe`)
- Other required tools: texconv (DirectXTex) for DDS encoding

## Dependencies
| Dependency | Version / range | Required? | Verified source |
|---|---|---|---|
| AnimationUnlocker | as installed | **Yes, for melee animations** | In the active load order; melee attacks play without animation when absent (observed in-game) |
| BG3 Script Extender | n/a | No | Nothing in the shipping mod calls it; the dev telemetry link is disabled |

## Repository state
- Project root: `C:\Users\johnf\Documents\BG3Mods\CursedArts` (local git repo, not yet on GitHub)
- Default branch: `master`
- Current work branch: `master`
- Last known-good commit/build: `27d1873`; tags `blue-works`, `working-ds-dialect`, `working-blue-pending`, `v1.2.0.0-working`
- Current milestone: balance the level tiers, then replicate the loop for the remaining 11 shikigami
- Next milestone: if it holds, build the remaining 11 shikigami; if not, redesign first

## Owned files
```
Mods/<Folder>/          meta.lsx, Localization/English/english.xml,
                        GUI/ (loose icons + metadata.lsf)
Public/<Folder>/        ClassDescriptions, Progressions, Lists,
                        ActionResourceDefinitions, Stats/Generated/Data,
                        GUI/Icons_CursedArts.lsx,
                        Content/[PAK]_CursedArts/<atlas-uuid>.lsf,
                        Assets/Textures/Icons/Icons_CursedArts.dds
tools/                  build + validation toolchain
art_src/                per-subclass portrait overrides
```
**Generated — never hand-edit:** `GUI/Icons_CursedArts.lsx`, `Icons_CursedArts.dds`,
`Content/[PAK]_CursedArts/<uuid>.lsf`, `Mods/<Folder>/GUI/metadata.lsf`, and everything
under `Mods/<Folder>/GUI/Assets*/`. All produced by `python tools/build_icons.py`.

## Stable identifiers
Never regenerate these (universal rule 23).

| What | Value |
|---|---|
| Mod folder / UUID | `CursedArts_f770ccc5-d803-5b08-17d2-fc1652689767` |
| Base class `Limitless` | `eff0eda1-5c98-4f72-97b1-0f7024af47e9` |
| Subclass `LimitlessAdept` | `46ed75bf-a3db-4ae3-8673-11b067603291` |
| Subclass `BlackfistVessel` | `ecb5d7a3-c0b2-4c6d-9cc3-a7a86b0c9dd6` |
| Subclass `TenShadows` | `41b597a5-f464-4798-b2de-942af9cee8b7` |
| Icon atlas | `5c9d4b21-7f3a-4e18-9c66-2d8ba4e71f03` — **must** equal the `TextureBank` Resource `ID` |
| Spell list `TenShadows 1` | `7a1c0d52-3e64-4b8a-9f21-5d0e6c4b9a13` |
| Stats namespace | `CA_` prefix on every entry |
| Localisation handles | `hca000001g0000g0000g0000g0000000000NN`, currently NN = 01–26 |

## Vanilla systems touched
**None replaced.** The mod adds records only. No `using` points at shipping content — see
`games/baldurs-gate-3/BG3_RULES.md` finding 4, which cost two crashes.

Referenced (read-only): vanilla RootTemplates for summons, vanilla faction UUIDs, vanilla
icon names, and `EQP_CC_Sorcerer` class equipment.

## Architecture
A base class **Limitless** ("Jujutsu Sorcerer") with three subclasses chosen at level 1.
All abilities are fuelled by a custom **Cursed Energy** action resource.

- **Limitless Adept** (CHA) — Infinity, Blue, Red, Purple
- **Blackfist Vessel** (DEX) — Divergent Fist, Melting Strike, Black Flash, King's Cleave
- **Ten Shadows** (WIS) — defeat-to-tame shikigami; 1 of 12 built

Ten Shadows loop: a trial spell summons a creature carrying a status with
`FactionOverride` + `LoseControl` so it fights the player. That status also carries an
`OnDamaged` functor conditioned on `(HasHPPercentageEqualOrLessThan(0) or IsKillingBlow())`
which does `ApplyStatus(SWAP, CA_TS_TAMED_<NAME>, 100, -1)` — marking whoever killed it.
The permanent tamed status carries `UnlockSpell(...)` for the real ally summon, which is
in no spell list and unreachable any other way.

## Verified features
| Feature | Verification state | Evidence | Last tested |
|---|---|---|---|
| Class + 3 subclasses appear and are playable | Tested in-game | Character created and played | 2026-08-25 |
| Subclass picker at level 1 | Tested in-game | All three offered and selectable | 2026-08-25 |
| Cursed Energy resource | Tested in-game | Displays, spends, recharges on short rest | 2026-08-25 |
| Blue — Force damage + pull | Tested in-game | Target pulled toward caster | 2026-08-25 |
| Infinity — bubble VFX + damage immunity | Tested in-game | Shield of Thralls bubble visible | 2026-08-25 |
| Melee animations (with AnimationUnlocker) | Tested in-game | Animations play | 2026-08-25 |
| Per-subclass class icons | Tested in-game | Distinct art on all three subclasses | 2026-08-25 |
| `metadata.lsf` registration | Tested in-game | Missing MetaData popup gone | 2026-08-25 |
| Spell icon atlas via `TextureBank` | Tested in-game | Spell icons render on the hotbar | 2026-08-25 |
| Build gate | Validates | 24 checks, each proven to fail on its broken input | 2026-08-25 |

## Experimental / unverified features
| Feature | Status | Main uncertainty | Next verification step |
|---|---|---|---|
| Ten Shadows — Worg trial (1 of 12) | **Tested in-game** | Full loop works: hostile summon, defeat, permanent Bound: Worg. One button now branches bound/unbound and by level tier | Balance pass on the level tiers |
| Ten Shadows — remaining 11 shikigami | Designed only | Blocked on the tame trigger only; the hostile half is proven | Build after one full loop completes |
| Purple as a purple beam | Loads | Visual only | Cast and observe |
| Reversal Bloom, Divergent Fist, Melting Strike, Iron Body, King's Cleave, RCT | Implemented, validates | Untested behaviour | Cast each in combat |
| Black Flash guaranteed critical | **Not possible as designed** | `AlwaysSucceed` exists nowhere; see KNOWN_LIMITATIONS | Redesign around a different mechanic |
| Ten Shadows roster templates from `SharedDev` | HIGH CONFIDENCE | Whether Dev-module templates are addressable by a mod | Covered by the Worg test only if a `SharedDev` creature is used; Worg is `Shared` |

## Compatibility
- Known compatible mods: AnimationUnlocker (required); tested alongside an XP mod
- Known conflicts: none observed
- Shared edit surfaces: none — the mod adds records and overrides nothing
- Existing compatibility patches: none
- Needed compatibility patches: none known. Other class mods are the likeliest surface,
  since class list and progression tables are shared UI space.

## Save / persistence notes
- Safe on existing saves? **UNVERIFIED.** Adding a class mod mid-save has not been tested.
- Safe to update mid-save? **UNVERIFIED.** All testing to date is on fresh characters.
- Safe to uninstall mid-save? **Assume not.** A save containing a character of a removed
  class is a known-risky configuration in BG3 generally.
- Fresh-save testing required? **Yes**, and it is what has been done throughout.
- Note: the tamed-shikigami design stores progress as a **permanent status on the
  character**, so it lives in the save. Persistence across save/reload and long rest is
  NEEDS TESTING.

## Known bugs and limitations
- Ten Shadows has 1 of 12 shikigami; the subclass is otherwise near-empty.
- Black Flash's guaranteed critical is not implementable as designed.
- **Art is copyrighted anime/fan art. This blocks any public release** (universal rule 31).
- Several abilities are implemented and validated but never cast in combat.
- A mis-staged pak once caused BG3 to silently delete the mod from `modsettings.lsx`;
  the build script now verifies internal archive paths, but the failure mode is worth
  knowing.

## Test procedure
- Test save/profile: fresh character each time; no dedicated test save yet
- Launch steps: fully restart BG3 (the pak is **not** hot-reloaded), New Game, choose
  Jujutsu Sorcerer, choose a subclass
- Feature test steps: check the class list art, check hotbar icons render, cast each
  ability, watch resource spend
- Regression test steps: re-confirm Blue pulls and Infinity's bubble appears, since those
  were the first features to work and are the canary for structural breakage
- Logs to inspect: crash minidumps under the BG3 profile folder, parsed with
  `tools/parse_dump.py`
- **Cost: roughly 4 minutes per cycle.** This is why universal rule 37 (one variable per
  test) is not optional on this project.

## Build and release
- Build command/process: `powershell tools/build.ps1` — validate, stage, pack, deploy,
  then verify size, hash **and internal archive paths**
- Validation command/process: `python tools/validate.py` — 23 checks, exits nonzero;
  `build.ps1` refuses to pack on failure
- Icon/asset regeneration: `python tools/build_icons.py` (atlas, TextureBank, class
  icons, metadata.lsf); `python tools/index_templates.py` to rebuild the
  RootTemplate/faction index the validator uses
- Packaging process: Divine `create-package`
- Release artifact location: `%LOCALAPPDATA%\Larian Studios\Baldur's Gate 3\Mods\CursedArts.pak`
- **Not release ready** — see asset rights above.
