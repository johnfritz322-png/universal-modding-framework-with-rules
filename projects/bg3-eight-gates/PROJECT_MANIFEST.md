# BG3 Eight Gates — Project Manifest

## Identity
- Project name: BG3 Eight Gates
- Game: Baldur's Gate 3
- Inspiration: Might Guy / Eight Gates from Naruto
- Local mod folder: `C:\Users\johnf\Documents\BG3Mods\EightGates`
- Separate from CursedArts: yes
- Exact game version/build: **UNVERIFIED — record before release**
- Platform: **UNVERIFIED**
- Mod version: 0.0.1-active-build

## Toolchain
- Official BG3 toolkit: **NEEDS PROJECT-SPECIFIC VERIFICATION**
- BG3 Script Extender: **not assumed**
- Packaging/build system: **UNVERIFIED**
- Validators: run `tools/validate.py` and `tools/check_refs.py` if present in the EightGates repo

## Current Milestone
Claude is building a standalone Eight Gates / Might Guy class mod. Codex is monitoring for BG3-rule safety, canon fit, level 1-12 functionality, and animation validity.

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
None verified here yet. Once Claude assigns UUIDs/internal names in the EightGates folder, record them here and do not regenerate them without a migration plan.

## Verified Features
None yet. The mod must remain labeled unplayed/unverified until tested in BG3.

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
| Night Guy / Gate of Death | EXPECTED | downed-at-0-HP behavior without accidental death |

## Canon Constraints
- Keep the fantasy close to Might Guy: taijutsu, discipline, speed, physical sacrifice, and escalating gates.
- Avoid turning the class into a generic Naruto caster.
- Avoid broad ninjutsu packages unless they are minor utility and do not dilute the Might Guy identity.
- The ultimate should feel like Night Guy but must be implemented using BG3-safe damage and self-downing mechanics.

## Animation Review Checklist
- Every ability uses an existing valid animation or a proven local reference.
- No hallucinated animation IDs or cinematic-only references.
- No ability is accepted as done if it will likely play invisible or with missing effects.
- Suspected animation issues must be marked separately from verified breakage.

## Save / Persistence Notes
All persistence behavior is **NEEDS TESTING**. Gate states, resource changes, long-rest cleanup, respec behavior, and save/load behavior must be tested before public release.

## GitHub / Framework Note
This project folder records design and review rules only. It does not mean the EightGates mod itself has been pushed or verified.

