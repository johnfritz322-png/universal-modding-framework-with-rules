# BG3 Eight Gates — Project Manifest

## Identity
- Project name: BG3 Eight Gates
- Game: Baldur's Gate 3
- Inspiration: Might Guy / Eight Gates from Naruto
- Local mod folder: `C:\Users\johnf\Documents\BG3Mods\EightGates`
- Separate from CursedArts: yes
- Exact game version/build: **UNVERIFIED — record before release**
- Platform: Windows 11, Steam (`D:\steam\steamapps\common\Baldurs Gate 3`) — VERIFIED 2026-08-28
- Mod version: **v1.3.0.0** (`Version64` 36451009484029952) — VERIFIED against `meta.lsx` 2026-08-28

## Toolchain
- Official BG3 toolkit: installed at `D:\steam\steamapps\common\Baldurs Gate 3 Toolkit` — VERIFIED
  present 2026-08-28, but **not used**; this mod is hand-authored and packed with Divine.
- BG3 Script Extender: **not used by this mod** (the separate CombatLogLog telemetry mod needs it)
- Packaging/build system: `tools/build.ps1` — validate gate, stage, Divine `create-package`,
  deploy, hash-verify, then load-order repair. VERIFIED working 2026-08-28.
- Validators: `tools/validate.py` (24 checks) and `tools/check_refs.py` — both present and passing

## Current Milestone

**Content-complete at v1.3.0.0; package loading and CursedArts coexistence verified.**

Definition-of-done state (highest verified only): **Loads**. Validation, references,
packing, deployment, and load-order survival pass. On 2026-08-28, BG3's own Installed
Mods screen showed both CursedArts and EightGates enabled during the same launch.
Gameplay behavior is not yet verified.

### Resolved blocker: BG3 Mod Manager had a stale one-mod `Current` order

The manager's saved `Current` order contained only EightGates. Manual repairs to
`modsettings.lsx` were temporary because a later manager refresh, export, or launch
could write that stale order back and remove CursedArts.

Resolved 2026-08-28 by making BG3 Mod Manager the source of truth: CursedArts is active
at position 0, EightGates at position 1, and the order was saved and exported to the
game. The exported profile contains GustavX, CursedArts 1.22.6.0, and EightGates
1.3.0.0. BG3 launched successfully and showed green enabled checks for both mods.

`tools/build.ps1` now treats BG3 Mod Manager as a profile writer and refuses to repair
`modsettings.lsx` while it is running. This prevents an in-memory manager order from
silently overwriting a build-time repair.

## Required Architecture
- Standalone mod folder and metadata
- Unique mod UUID
- Unique class/progression UUIDs
- Unique Chakra resource
- Level 1-12 progression
- One evolving Eight Gates mechanic
- Taijutsu-focused spell/passive/status package
- Verified icons and localization
- No CursedArts file edits

## Stable Identifiers

Recorded 2026-08-28, read directly out of the shipped files. **Do not regenerate any of
these without a migration plan** — the mod UUID and folder are written into
`modsettings.lsx`, and changing either unloads the mod.

| Identifier | Value | Where it lives |
|---|---|---|
| Mod UUID | `74d4d589-44b2-4dc8-8d2a-932d669357ec` | `meta.lsx` ModuleInfo |
| Mod folder | `EightGates_74d4d589-44b2-4dc8-8d2a-932d669357ec` | pak root, `meta.lsx` Folder |
| Class UUID | `5241fe2c-70f4-4253-8719-92726b222793` | `ClassDescriptions.lsx` |
| Progression table UUID | `d76908a4-d5aa-413f-ac3a-9d0d0bd3f146` | every `Progression` row |
| Chakra resource UUID | `d1e83269-ae98-4577-94ea-e8e4ebc708b5` | `ActionResourceDefinitions.lsx` |
| Localisation prefix | `he8a70001g0000g0000g0000g...` | `english.xml` — chosen so it can never collide with CursedArts' `hca000001...` |

Spell-list UUIDs (one per granting level): L1 `3a4b0a53-…`, L2 `44d3e473-…`,
L3 `9cbe7c39-…`, L5 `37fe83b0-…`, L9 `e4ad4d16-…`, L10 `5e7533d0-…`, L11 `c37494a8-…`,
L12 `9edcce6d-…`.

**This is a BASE class and therefore deliberately has NO `ParentGuid`.** That single
absence is what makes it a class rather than a subclass; adding one breaks it.

## Verified Features

**No gameplay feature is verified. The mod remains unplayed.**

What *is* verified, at the evidence level stated and no higher:

| Claim | Level | Evidence |
|---|---|---|
| Validates clean | VERIFIED | `validate.py` 21 pass / 0 fail / **3 SKIP** |
| Every reference resolves | VERIFIED | `check_refs.py` — 19 stats, 8 spell lists, 1 class, 1 resource, 1 table |
| Packs with correct internal paths | VERIFIED | `divine list-package` asserts `Mods/<Folder>/meta.lsx` and the `Public` tree |
| Deployed pak == built pak | VERIFIED | SHA-256 `da569ee88a3ad69c…` identical both sides, 2026-08-28 |
| Load-order entry matches `meta.lsx` | VERIFIED | written then reparsed from disk; Folder/Name/Version64 compared |
| CursedArts and EightGates load together | VERIFIED | BG3 Installed Mods showed both enabled, 2026-08-28 |
| Class appears in game | **NOT VERIFIED** | never observed |

**Rule 21 — the 3 skipped checks are NOT passes.** `icon atlas registration`,
`GUI metadata registration` and `DDS header sanity` all skip because the mod ships no
art. They are untested surface, not clean surface. Eight Gates borrows
`Action_Monk_FlurryOfBlows` for every icon; the class-list icon may render blank.

## Experimental / Unverified Features
| Feature | Status | Main uncertainty |
|---|---|---|
| Chakra resource | EXPECTED | resource definition and recharge wiring |
| Eight Gates evolving mechanic | EXPECTED | progression/status structure |
| Level 1-12 class progression | EXPECTED | every grant must resolve and appear in game |
| Taijutsu strikes | EXPECTED | attack/animation validity |
| Lotus techniques | EXPECTED | supported multi-hit or burst implementation |
| Morning Peacock-inspired attack | EXPECTED | animation/projectile/area pattern |
| Daytime Tiger-inspired attack | EXPECTED | impact pattern and balance |
| Dynamic Entry (L5) | IMPLEMENTED, UNPLAYED | `IF(not HasStatus('EG_GATE_1'))` bonus-damage branch |
| Evening Elephant (L10) | IMPLEMENTED, UNPLAYED | Cast2 multiattack, same shape as Morning Peacock |
| Daytime Tiger (L11) | IMPLEMENTED, UNPLAYED | Con-save area burst copied from `Target_Shatter`; save branch could be inverted |
| Night Guy / Gate of Death | IMPLEMENTED, UNPLAYED | **KILLS the caster — see the design reversal below** |

## Canon Constraints
- Keep the fantasy close to Might Guy: taijutsu, discipline, speed, physical sacrifice, and escalating gates.
- Avoid turning the class into a generic Naruto caster.
- Avoid broad ninjutsu packages unless they are minor utility and do not dilute the Might Guy identity.
- The ultimate should feel like Night Guy.

### DESIGN REVERSAL — Night Guy kills the caster (user decision, 2026-08-27)

**This manifest previously required "downed-at-0-HP behavior without accidental death"
and "self-downing mechanics". The user explicitly reversed that**, wanting Night Guy to
be an absolute last resort. Recorded here because an agent reading the old wording would
"fix" the ability back and undo a deliberate decision.

As built: Night Guy applies `EG_COLLAPSE` to self after the blow lands; `EG_COLLAPSE`
runs `OnApplyFunctors "RemoveStatus(EG_GATE_8);Kill()"`. That is a true death — no death
saving throws, no ally pickup, only Revivify-tier magic. The earlier non-lethal
`DownedStatus(EG_COLLAPSE,3)` catch on `EG_GATE_8` was **removed on purpose**.

`Kill()` in `OnApplyFunctors` is VERIFIED attested — 6 vanilla uses, including the
Steelwatcher self-destruct. The *behaviour* is UNPLAYED: nobody has confirmed in game
that the target takes its damage before the caster dies, or that Revivify works on the
body. Do not re-add a downed catch without the user asking.

## Animation Review Checklist
- Every ability uses an existing valid animation or a proven local reference.
- No hallucinated animation IDs or cinematic-only references.
- No ability is accepted as done if it will likely play invisible or with missing effects.
- Suspected animation issues must be marked separately from verified breakage.

## Save / Persistence Notes
All persistence behavior is **NEEDS TESTING**. Gate states, resource changes, long-rest cleanup, respec behavior, and save/load behavior must be tested before public release.

## Release Blockers (Rule 59 — not hidden)

1. **No completed gameplay test.** Loading is verified; class mechanics are not.
2. **No original art.** Every icon borrows `Action_Monk_FlurryOfBlows`. Not a licensing
   problem (it is vanilla), but 3 validator checks skip and icons may render blank.
3. **No mod.io presence, so no in-manager tile image.** Measured 2026-08-28: the tile
   picture comes only from media uploaded to mod.io — there is no in-pak or `meta.lsx`
   path. `PhotoBooth` is a photo-mode *level name*, not an image (confirmed: the
   published CombatLogLog mod ships a 1234x727 logo while its `PhotoBooth` is empty).
   **A blank tile is therefore NOT evidence that a local pak failed to load.**
4. **Save/persistence behaviour untested** — gate states across save/load, long rest,
   and respec.

## GitHub / Framework Note
This project folder records design and review rules only. It does not mean the EightGates
mod itself has been pushed or verified.

**The EightGates code repository is local only:**
`C:\Users\johnf\Documents\BG3Mods\EightGates`, branch `master`, **no git remote**.
Nothing about this mod exists on GitHub. Rollback points are local commits; the last
known-validating one is `564e8a9`.

## Branch / Baseline Policy
- Shared framework repository: `https://github.com/johnfritz322-png/universal-modding-framework-with-rules`
- Correct project folder for this mod: `projects/bg3-eight-gates/`
- Do not save Eight Gates material over `projects/bg3-cursed-arts/`.
- Treat `main` as the stable baseline unless the user explicitly says otherwise.
- Use branches for meaningful changes and prefer pull requests over direct `main` edits.
- Any actual EightGates code repository/remote must be recorded here before claiming the mod itself is on GitHub.
