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
- `SAVE-READONLY-FINDINGS-2026-09-25.md`: the live owned-freighter resource
  and seed, verified without editing either current save.
- `BLENDER-ROUNDTRIP-2026-09-25.md`: passing root-scene import/export control
  for the actual capital freighter, plus its precise evidence boundary.
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
4. **Complete:** Mothership's live resource and seed were read-only verified;
   see `SAVE-READONLY-FINDINGS-2026-09-25.md`. The current record references
   `CAPITALFREIGHTER_PROC.SCENE.MBIN`, but that does not prove custom
   registration or personal-only selection.
5. **Capital root control verified:** the actual capital-freighter root scene
   imports and exports with the dedicated-profile NMSDK patch and a read-only
   current-game dependency closure. Its referenced component tree was not
   recursively imported; see `BLENDER-ROUNDTRIP-2026-09-25.md`.
6. **Original-mesh path verified:** a scratch sphere based on the donor's
   measured full-length envelope exports and re-imports. Stage 1 adds the
   dish and trench. Next add uniform surface-panel treatment, then use the
   recorded hangar anchors to design a clear trench opening. The selection
   architecture is still unverified, so do not package or install.
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
Death Star mod: **Designed; capital root geometry path verified.** No Death
Star mesh/package or in-game test yet.
