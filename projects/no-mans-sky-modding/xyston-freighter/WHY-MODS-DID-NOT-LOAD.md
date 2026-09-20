# Why nothing loaded — two causes, both confirmed 2026-09-19

The Star Destroyer was installed and the game showed the stock freighter. Two
separate faults, found by checking rather than guessing.

## 1. Every mod on the machine was switched off — THE cause

`D:\steam\steamapps\common\No Man's Sky\Binaries\SETTINGS\GCMODSETTINGS.MXML`

```xml
<Property name="DisableAllMods" value="true" />
```

Nothing in `GAMEDATA\MODS` was ever going to load, including the player's own
pre-existing Corvette Overhaul. The file was dated 2025-08-29 and listed one stale
entry, `ACCELERATED SETTLEMENTS 5.75.0`.

Set to `false`. Backup of the original:
`outputs/NMS-Before-EnableMods-20260919-213843`.

**The game does not rewrite this file on exit** — it still carried its 2025 timestamp
after a full session — so the edit holds. But it must be made with the game closed,
in case a future version writes settings on shutdown.

### How the timeline proved it was not a restart problem

| Time | Event |
|---|---|
| 21:31:03 | Star Destroyer scene and geometry installed |
| 21:33:58 | `FullLog.txt` written — the game's startup check for `DISABLEMODS` |
| 21:35:51 | `save.hg` written — player in game, freighter unchanged |

The mod was on disk more than two minutes before the game started. So "it needs a
restart" was already ruled out before looking further.

`FullLog.txt` is worth knowing about: it logs the startup mod check and is the only
log the game leaves.

## 2. NMSDK stamps the wrong template GUID on scene files

Bytes at offset `0x10` of the MBIN header:

| File | GUID |
|---|---|
| vanilla `capitalfreighter_proc.scene.mbin` | `d8 02 1f 59 63 a8 96 ad` |
| NMSDK export | `16 f2 83 f6 94 77 a5 42` |
| after an MBINCompiler round trip | `d8 02 1f 59 63 a8 96 ad` |

MBINCompiler resolves the template by name, so decompiling and recompiling restores
the correct GUID. **Geometry files are unaffected** — their GUIDs already match
vanilla, so this is specific to the scene.

Whether the game would have rejected the wrong GUID is **untested** — cause 1 meant
nothing loaded either way. It is corrected because it is cheap and provably right.

`normalise_scene_guid()` in `tools/build_xyston_hull.py` now runs automatically after
every export.

### The subtlety that made the first attempt silently fail

**MBINCompiler will not overwrite an existing MBIN.** Decompiling to MXML and then
recompiling leaves the original MBIN untouched, and the function reported the GUID
unchanged. The MBIN has to be deleted between the two steps. The function now does
that, and prints `UNCHANGED, check this` if the GUID does not actually move.

## Still unknown

Whether the ship loads and renders. Both faults are fixed and the mod is installed,
but the game has not been launched since.
