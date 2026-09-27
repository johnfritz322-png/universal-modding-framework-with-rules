# Claude continuation handoff — Death Star freighter

## Immediate state

- Game: No Man's Sky Steam build, `D:\Steam\steamapps\common\No Man's Sky`.
- Current game process was running when this handoff was written. Do **not**
  alter deployed mod files until it is closed.
- The requested Death Star visual replacement is **not working**. Every
  screenshot through this point showed the stock Mothership exterior.
- The most recent direct capital-scene attempt removed runtime anchors, so the
  player reported that Mothership could not be summoned. It must remain
  disabled before further normal play.
- `UI_HAIL_ALIEN_NAV_OSD` text in the centre of the screen came from the
  separate `NoCoordsPrompt` loose mod, not the Death Star work.

## Current on-disk deployment

The active loose-mod directory is:

`D:\Steam\steamapps\common\No Man's Sky\GAMEDATA\MODS`

Two folders were renamed, but the game's mod loader still treats renamed
folders as mods. They therefore must be moved *out of* `GAMEDATA\MODS` after
the game closes (preserve them; do not delete):

- `DeathStarFreighterOverlay.disabled-20260926`
- `NoCoordsPrompt.disabled-20260926`

Move them to this existing recoverable location, or another directory outside
`GAMEDATA\MODS`:

`C:\Users\johnf\Documents\Codex\2026-09-26\who-x20\work\backups\`

Then relaunch NMS. This restores stock Mothership summoning and removes the
broken HUD key text. `GCMODSETTINGS.MXML` currently has `DisableAllMods=false`
and sees renamed folders as enabled mods; renaming alone is not a disable.

## What has been proven

- Mothership's save record references
  `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`.
- Other loose mods load successfully from `GAMEDATA\MODS`; the raw
  `UI_HAIL_ALIEN_NAV_OSD` string is visible in game and proves this.
- The Death Star geometry was exported successfully with Blender/NMSDK and
  has local visual QA renders, but has not been successfully loaded in NMS.
- A direct compiled binary was produced at:
  `C:\Users\johnf\Documents\Codex\2026-09-26\who-x20\work\death-star-direct-capital\MODELS\COMMON\SPACECRAFT\INDUSTRIAL\CAPITALFREIGHTER_PROC\`
- The direct source has a matching scene and mesh metadata count: 55,248
  indexes for its doubled shell. It still lacks the original capital scene's
  runtime hangar/locator/attachment graph, which is why it is unsafe as a
  usable freighter replacement.

## Failed approaches — do not repeat as success claims

1. `CUSTOMMODELS` additive scene reference injected into the capital scene.
   The loose-file loader did not visibly resolve/register the new custom
   runtime resource.
2. Alternate polygon winding, double-sided mesh, and 25% larger shell. Those
   variants were never shown to load; screenshots were stock Mothership.
3. Scene files deployed as EXML/MXML. Current modding reference says `.SCENE`
   is an MBIN-only hard exception, but the direct scene MBIN test lost runtime
   anchors.
4. A Stage 6 MXML custom scene copied from Stage 3 was structurally invalid:
   it declared 27,624 indices while its doubled geometry has 55,248. A later
   directly decompiled MXML matched the data but triggered an NMS mod crash.
5. Direct replacement of `CAPITALFREIGHTER_PROC` scene + geometry was launched
   but did not yield a usable summonable freighter.

## Relevant tools and paths

- Project root (the folder Claude was connected to):
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-nmsdk-fix`
- Project folder:
  `projects\no-mans-sky-modding\death-star-freighter`
- Blender:
  `C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain\blender\blender-5.0.1-windows-x64\blender.exe`
- NMSDK profile:
  `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-blender-profile`
- MBINCompiler used for current-game assets:
  `C:\Users\johnf\Documents\Codex\2026-09-26\who-x20\work\MBINCompiler-v7.04.0-pre1\MBINCompiler.exe`
- Earlier compiler that could decompile generated scene files (with a warning):
  `C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain\MBINCompiler-v7.03.2-pre1\MBINCompiler.exe`

## Source commits made during this work

- `9db4fda` — documentation/handoff groundwork
- `c1a2626`, `33c8d57` — earlier overlay attempts
- `5f4633e`, `ce820f8`, `6332063` — Stage 4–6 shell variants
- `9ce7de0`, `87be9c0` — loader and matching-scene corrections
- `4cbfcdd` — direct capital replacement exporter

Untracked tools must be treated as user/work-in-progress files and preserved:

- `tools/build_hangar_root_markers.py`
- `tools/build_overlay_via_nmsdk.py`
- `tools/clear_scene_compiler_version.py`

## Recommended next direction

1. Restore stock first by moving the two renamed folders outside the live MODS
   directory.
2. Do not make another scene-only replacement. A usable freighter needs the
   original capital scene's hangar locators, entity references, attachments,
   collision, and runtime graph preserved.
3. Build a replacement by retaining the stock capital scene graph and replacing
   only its renderable mesh/geometry through a current, known-working binary
   packaging workflow. Verify first with an intentionally obvious but harmless
   stock-geometry change before attempting the Death Star mesh.
4. Require an in-game proof image that visibly differs from the stock
   Mothership before claiming a build loaded.
