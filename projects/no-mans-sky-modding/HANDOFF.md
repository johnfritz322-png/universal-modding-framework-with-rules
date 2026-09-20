# No Man's Sky work — handoff

Written 2026-09-19. Everything below is either verified against the game's own files
or explicitly marked as untested. **The single most important fact: the game has
never been launched with any of this installed.** Every visual is a Blender render.
Nothing about in-game behaviour is known.

Two projects: a Xyston-class Sith Star Destroyer replacing the capital freighter, and
some Corvette work on an existing ship called the Millennium Falcon.

---

## 1. Target platform — VERIFIED

| Item | Value |
|---|---|
| Game | No Man's Sky **7.03.1 "Cosmos"**, Steam build `25351301` |
| Install | `D:\steam\steamapps\common\No Man's Sky` |
| Saves | `C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576` |
| Mod format | plain folders under `GAMEDATA\MODS\`, `.MBIN` (replace) or `.EXML` (patch). `.pak` mods stopped working at 5.50 |

The game writes `save.hg` and `save2.hg` alternately and loads whichever is newer, so
**any save edit must be written to both.**

## 2. Toolchain — all present and version-matched

| Tool | Version | Path |
|---|---|---|
| HGPAKtool | 1.1.3 | `work/nms-toolchain/HGPAKtool-1.1.3/hgpaktool.exe` |
| MBINCompiler | 7.03.2-pre1 | `work/nms-toolchain/MBINCompiler-v7.03.2-pre1/` |
| Blender | **5.0.1** | `work/nms-toolchain/blender/blender-5.0.1-windows-x64/` |
| NMSDK | 0.10.0-alpha14, `cosmos_fixes` branch | `work/NMSDK` |

`work` = `C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work`

**Blender must be 5.0, not 4.5.** NMSDK's manifest sets `blender_version_min = 5.0.0`.
Blender 4.5 LTS was installed first and cannot load the add-on at all.

**NMSDK must be the `cosmos_fixes` branch**, not the tagged release, which predates
the 5.50 format change by two major versions.

### NMSDK needs three source patches

`tools/patch_nmsdk.py` applies them and is idempotent — run it and confirm every
line reports `already`. Without patch 1 nothing exports at all.

### Driving Blender headless — two traps

1. **Never call `bpy.ops.wm.read_factory_settings()`.** It unloads the extension and
   every `bpy.ops.nmsdk.*` call then fails with "could not be found". Clear the scene
   with `bpy.data.objects.remove` instead.
2. **Enable the add-on explicitly in every background run:**
   `addon_utils.enable("bl_ext.user_default.nmsdk", default_set=True, persistent=True)`.
   The install-time enable does not carry into `--background`.

---

## 3. What is installed in the game right now

`D:\steam\steamapps\common\No Man's Sky\GAMEDATA\MODS\`

| Folder | Contents | Purpose |
|---|---|---|
| `XystonFreighter` | scene 21,583 B, geometry 13,136 + 702,879 B, material 990 B | the Star Destroyer hull |
| `XystonFreighterMaxed` | 2 EXML patches | max freighter upgrade rolls, ship parking 6 -> 12 |
| `CorvetteExtras` | 1 EXML patch, 900 B | teleporter + flush hatch in the Corvette builder |

Pre-existing and **not** ours: `CorvetteOverhaul` (Vortex-deployed, edits
`GCCAMERAGLOBALS` and `GCSPACESHIPGLOBALS`) and `Buy All Corvette Parts`.
**No conflicts** — checked file by file.

Revert any of it by deleting the folder. No save data depends on any mod, by design.

---

## 4. The Xyston freighter

### Build and install

```
blender.exe --background --python tools/build_xyston_hull.py -- <out_dir>
```

Then copy from `<out_dir>/MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/`:

- `CAPITALFREIGHTER_PROC.SCENE.MBIN` -> `MODS/XystonFreighter/MODELS/COMMON/SPACECRAFT/INDUSTRIAL/`
- both `.GEOMETRY.*.MBIN.PC` -> the `CAPITALFREIGHTER_PROC/` subfolder alongside it
- `XYSTON_CANNON_GLOW.MATERIAL.MBIN` (from `tools/build_cannon_material.py`) -> same subfolder

**NMSDK names output after the root object, not the `scene_name` argument.** The
script renames the root to `NMS_CAPITALFREIGHTER_PROC`, which is what makes the file
land with the right name.

### Current shape — 20 meshes, 5,723 faces

Hull wedge, superstructure, bridge tower, twin shield globes, 5 engine bells, the
ventral axial cannon (housing + glow strip + muzzle + emitter blisters), and five
procedural detail passes: dorsal greebles, dorsal trenches, flank ridges, flank bays,
command tiers, ventral plating.

Modelled at the canon 2,400 m, `HULL_SCALE = 4.0` gives **9,600 m**. One constant
changes the size. Measured extents 10,032 x 5,800 x 2,810 m — the extra length is the
muzzle projecting past the bow.

### Geometry rules that were learned by getting them wrong

The hull tapers in two directions and the belly is the plane `z = 0` with hull above
it. Four failures, none visible in the face count or export log, all only caught in a
render:

1. **Anything at positive z on the belly is invisible** — swallowed by the hull. The
   cannon trench, glow strip and the entire ventral detail pass were all buried this
   way. Ventral detail must sit at **negative z**, and the glow must be the *lowest*
   surface or the housing hides it.
2. **Flank detail placed at the ventral width floats off the hull** like railings,
   because the flank leans inward as it rises. Use `flank_x(y, frac)`, which
   interpolates between ventral and dorsal widths.
3. **Long boxes along the ship rise out of the sloping deck** and shoot past the hull
   edge near the bow. Build them as segments that sample `dorsal_z(y)` and stop once
   the offset exceeds `dorsal_half_width(y)`.
4. **Camera clip_end defaults to 100 m.** A 2.4 km ship renders as an empty frame.

### Materials

Hull borrows the game's own `FREIGHTERPROC_MAT` — no texture authoring needed.

The red cannon glow is `XYSTON_CANNON_GLOW.MATERIAL.MBIN`, built by
`tools/build_cannon_material.py` by retinting the Corvette's hull-light material
(`BiggsLightsMAT`): `GlowTranslucent` class, `_F01_DIFFUSEMAP` + `_F07_UNLIT`,
`CastShadow=false`, `gMaterialColourVec4` set to `(1.0, 0.055, 0.045, 1.0)`.

The engine-glow material was rejected as a template: it carries `_F19_BILLBOARD`,
which turns geometry to face the camera. Right for a flare sprite, wrong for a hull.

Parts are assigned the glow material by name — anything containing `Glow`.

### Size against the stock freighter — measured, not estimated

`tools/compare_against_vanilla.py` imports the live vanilla scene and builds the
Xyston in the same Blender scene.

| | Stock | Xyston |
|---|---|---|
| Length | 4,301 m | 10,032 m (2.33x) |
| Width | 2,624 m | 5,800 m (2.21x) |
| Height | 2,259 m | 2,810 m (1.24x) |
| Faces | 76,996 | 5,723 (7%) |

**Two measurement traps.** The vanilla scene contains six `FXSphere` effect volumes
that wrap the whole ship — include them and it "measures" 6,083 m. And every LOD
level imports simultaneously, so the same wing appears four times. Filter
`FXSphere*` and `LOD[1-9]`; that drops 398 of 732 meshes.

An earlier figure of "about 708 m" for the stock freighter is **wrong** — it read
only the root node's geometry and missed every referenced sub-scene.

### Why the scale sits on the mesh nodes

Vanilla sizes the ship with `_Hull_A3` scale 6, then compensates the hangar and
inventory back to world scale 1.0 via `6 x 0.5 x 0.333333 = 1.0`. Our scene puts the
scale on the mesh nodes and leaves `HANGARROOTB` and both maintenance locators at
scale 1, achieving the same thing with no arithmetic.

**`HANGARROOTB` is an empty locator** — the game attaches the hangar at runtime, so
no file can prove the game honours the locator when it does. This is the largest
open unknown.

---

## 5. Freighter stats, storage and parking

Findings, all read from the live save and game tables:

- **Already S-class.** All three inventories carry `B@N = {"1o6": "S"}`.
- **Storage already at the engine ceiling.** General `8ZP` 120/120, technology `0wS`
  60/60. Cargo `FdP` is 7x5 but `MaxCargoSlots = 0` for `FreighterLarge`, so that tab
  does not exist for this class and expanding it writes a number the game ignores.
- **All 26 installed items healthy** — `b76 = True`, `eVk = 0.0`, all tier 4.

Changed:

- **Stat rolls pinned** via `nms_reality_gcproceduraltechnologytable`: for all 28
  `UP_FR*` entries, `ValueMin = ValueMax`. Rolls happen at runtime from the save's
  seed, so this maxes modules already owned with no save edit. **Only 2 of the 7
  S-class types the player owns had a range at all** — hyperdrive jump distance
  (200-250 -> 250) and fleet fuel (0.80-0.85 -> 0.85). The other five were already
  fixed at their ceiling.
- **Ship parking 6 -> 12** — `MaxNumberOfPlayerShipsInFreighterHangar` in
  `GCFLEETGLOBALS`, not in the freighter globals where you would look. Found by
  decompiling all 38 globals. **Untested whether the hangar can display 12**; the
  long-standing community mod for this only goes to 9.
- **Hyperdrive charge 64/120 -> 120/120** — stored state no mod can reach, so this
  is the only save edit made. `tools/top_up_freighter_tech.py`, backed up first,
  written to both slots, verified by re-reading from disk.

---

## 6. The Corvette work (falcon-corvette project)

On branch `claude/nms-falcon-parts-catalog`, not this one.

- **`CorvettePartCategory` gates the Corvette build menu.** Airlocks are `Access`,
  the teleporter was `None`. `CorvetteExtras` sets `TELEPORTER` to `Interior` and
  unlocks `B_ALK_D` / `B_ALK_Z_D` as `Access`. Every change reuses a vanilla part id,
  so uninstalling cannot orphan anything placed.
- **`B_ALK_D` may not work as a door.** Unlike A, B and C it ships no `entities`
  folder at all, so it lacks `shipaccesswaydata`. `B_ALK_A` (a plain ramp) is the
  safe fallback and needs no mod.
- **The Falcon's entrance is `B_ALK_C`, the lift** — confirmed by `liftdata.entity.mbin`.
- **There is nowhere to put stairs.** 227 deck tiles, 1,068 objects overhead, zero
  tiles with a clear column 4 m from both airlocks. Largest clear radius anywhere is
  1.52 m against a 3 m module. Space must be cleared first.
- **Standing rule: do not edit a Corvette interior by writing save files.** Three of
  three attempts failed, each invisible until launch. Technology and inventory edits
  are fine; geometry is not. See `falcon-corvette/OUTCOME-AND-LESSONS.md`.

---

## 7. Save backups

`C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\outputs\`

Most recent from this session:

- `NMS-Before-RampAndStairs-20260919-210205` — taken before an edit that was then
  **not** made
- `NMS-Before-TechTopUp-20260919-211754` — before the hyperdrive refill

Rule carried over from the Falcon work: four-file backup (`save.hg`, `save2.hg`,
`mf_save.hg`, `mf_save2.hg`) before every write.

---

## 8. What to do next

1. **Launch the game.** Everything is blocked on this. Summon the freighter and look.
   Watch for: does it load at all; is the hangar approach usable (the globals still
   place you 300 m out, deep inside a 10 km hull); can you land; is the hangar
   human-sized; do 12 ships fit without overlapping.
2. If it loads, fix the hangar locator height — currently a guess.
3. If it does not load, suspect the geometry size (703 KB against the vanilla's own)
   or the borrowed material paths, and bisect by reinstalling the earlier scale-only
   variants in `variants/`.
4. Surface detail is at 7% of vanilla density. More would help up close: panel insets
   on the flanks, stepped bays, finer clutter near the bow.

## 9. Branches

| Branch | Contents |
|---|---|
| `claude/nms-xyston-freighter` | this project, freighter stats, comparison |
| `claude/nms-falcon-parts-catalog` | Corvette parts, teleporter, entry parts |
| `main` | stable; neither branch is merged |

Nothing is merged to `main` and no pull request has been opened — `gh` on this
machine is not signed in to GitHub.
