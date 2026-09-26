# Resume here — Death Star Freighter

Checkpoint: 2026-09-25 UTC. NMSDK dependency repair is complete.
Review branch: `codex/death-star-nmsdk-fix`, based on canonical branch
`claude/death-star-freighter-mod-iteration` at `2a57866`.

## What is saved

- `NMSDK-REPAIR-2026-09-25.md`: exact dependency repair, local paths,
  commands, hashes, passing restart checks, scope, and rollback.
- `tools/verify_nmsdk_load.py`: repeatable registration and archive-access
  check with a real failure exit code.
- `FREIGHTER-SELECTION-FINDINGS.md`: confirmed capital scene/descriptor,
  AI model mapping, hangar locators, file hashes and two additional passing
  no-edit MBIN round trips.
- Dedicated local Blender 5.0.1 profile with NMSDK enabled:
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-blender-profile`.
- Existing Blender 4.5.14's Python now imports HGPAKtool and registers
  NMSDK successfully. Use 5.0.1 for further testing because the extension
  manifest requires >=5.0.0.
- Prior MBINCompiler/HGPAKtool sample round-trip results remain recorded.

## Next actions, in order

1. Fetch this review branch and incorporate it into the canonical branch
   after reviewing the diff. It includes all canonical work through `2a57866`;
   preserve any newer Claude commits. Do not reset to an older audit branch.
2. Use the dedicated Blender 5.0.1 profile and the startup check documented
   in `NMSDK-REPAIR-2026-09-25.md`. No further dependency repair is currently
   required for the tested loading/archive operations.
3. Follow the actual capital-freighter chain:
   `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`.
   Current data identifies `BIGGS` as Corvette. Examine the corresponding
   descriptor and ship-manager references before choosing an architecture.
   A literal seed-to-hull lookup table has not been established.
   The descriptor and `METADATA/SIMULATION/SPACE/AISPACESHIPMANAGER.MBIN`
   are in `NMSARC.Precache.pak`; preserve the literal model ID
   `FREIGHTER_CAPTIAL`. See `FREIGHTER-SELECTION-FINDINGS.md` for exact
   `_HULL_` choices and local `HANGARROOTA/B` transforms.
4. Identify `Mothership`'s save/profile and actual resource/seed fields
   read-only. A same-name ship or a file path alone does not establish the
   correct target. Do not copy the Corvette project's ship-slot assumptions.
5. Prove a minimal current-build scene import/export in Blender, preserving
   stock functional nodes and transforms. Add-on loading and one globals
   round-trip do not establish working geometry export or boardability.
6. After selection and geometry gates pass, create the spherical exterior
   with the specified dish, trench, and clear hangar approach. Measure the
   donor's transformed bounds and docking route before final dimensions.
7. Before any game/save installation, make and verify a fresh backup and
   define rollback. Test docking, walking, exit, reload, summon/warp,
   freighter base behavior, and unchanged class/stats/crew. Keep each
   expensive test to one changed variable.

## Where to resume locally

- Review checkout:
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-nmsdk-fix`
- Previous extracted data and round-trip artifacts:
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-toolchain`
- Follow-up asset investigation:
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\freighter-selection-followup`

Source game data and local runtime packages remain on this computer. GitHub
contains documentation, findings, and our verification script, not proprietary
game assets or saves. The user does not need to repeat setup when resuming.

## Highest verified state

Tooling: add-on enables after restart and reads a current-build archive.
Death Star mod: **Designed**. No Death Star mesh/package or in-game test yet.
