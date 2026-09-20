# The custom mesh pipeline works on 7.03.1 — VERIFIED 2026-09-19

This was the project's main risk: NMSDK's last tagged release predates the 5.50
format change, and no custom mesh mod for the new format could be found on Nexus.
It now works on this machine, end to end, with one small source patch.

## Working toolchain

| Component | Version | Note |
|---|---|---|
| No Man's Sky | 7.03.1 "Cosmos", build 25351301 | |
| **Blender** | **5.0.1** | NMSDK's `blender_manifest.toml` sets `blender_version_min = "5.0.0"`. Blender 4.5 LTS was installed first and **cannot** run it |
| NMSDK | `cosmos_fixes` branch, 0.10.0-alpha14 | head commit 2026-09-16, "Update for Cosmos". Not the tagged release |
| MBINCompiler | 7.03.2-pre1 | used by NMSDK to convert, and to validate the output |

## The one code fix NMSDK needs

`NMS/classes/Object.py`, in `construct_data`, builds a `TkSceneNodeData` without
the `InstanceTransforms` field. The struct in
`serialization/NMS_Structures/Structures.py` requires it:

```python
@dataclass
class TkSceneNodeData(datatype):
    Attributes: ...
    Children: ...
    InstanceTransforms: Annotated[list[TkInstanceTransformData], ...]
```

Export fails with:

    TypeError: TkSceneNodeData.__init__() missing 1 required positional argument:
    'InstanceTransforms'

Fix — add one keyword argument:

```python
self.NodeData = TkSceneNodeData(Name=self.Name,
                                NameHash=self.NameHash,
                                Type=self._Type,
                                Transform=self.Transform,
                                Attributes=self.Attributes,
                                InstanceTransforms=[],
                                Children=child_nodes)
```

Empty is correct: the vanilla capital freighter scene carries
`<Property name="InstanceTransforms" />` with no entries.

## Driving the exporter headless

Two things cost time and are worth recording:

1. **Never call `bpy.ops.wm.read_factory_settings()`** — it unloads the extension and
   every `bpy.ops.nmsdk.*` call then fails with "could not be found". Clear objects
   with `bpy.data.objects.remove` instead.
2. **The addon must be enabled explicitly in every background run.**
   `addon_utils.enable("bl_ext.user_default.nmsdk", default_set=True, persistent=True)`.
   The install-time enable does not carry into `--background`.

## Skipping texture authoring

`parse_material` refuses a material with no texture nodes labelled diffuse/normal/mask.
That is avoidable entirely — set `NMSMesh_props.material_path` on the mesh and the
exporter uses that path and never parses a material:

```python
obj.NMSMesh_props.material_path = (
    "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/"
    "CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN")
```

This points a custom mesh at the game's own freighter material, so the hull gets
Hello Games' textures and shader with no DDS work. Note the custom property
`ob['MATERIAL']` looks equivalent but is **not** — the exporter reads
`material_slots[0]` before checking it and raises `IndexError` when there is none.

## Proof

A 4-unit box exported to `CUSTOMMODELS/SMOKETEST/`:

    SCENE.SCENE.MBIN               1,293 bytes
    SCENE.GEOMETRY.MBIN.PC           689 bytes
    SCENE.GEOMETRY.DATA.MBIN.PC      584 bytes

`MBINCompiler 7.03.2-pre1` decompiles `SCENE.SCENE.MBIN` without error, and the result
has the same shape as a vanilla scene: a `MODEL` root carrying `GEOMETRY` and `NUMLODS`
attributes, an empty `InstanceTransforms`, and a `MESH` child.

**Still unverified:** that the game loads and renders such a scene. Producing a valid
file and the engine accepting it are different claims. That is the next test.

---

## The hull — BUILT, EXPORTED, INSTALLED, NOT SEEN IN GAME

`tools/build_xyston_hull.py` generates the ship procedurally and exports it. 12 parts,
503 faces:

| Part | What it is |
|---|---|
| `XystonHull` | the wedge: flat ventral triangle, narrower dorsal triangle, blade bow |
| `Superstructure` | tapered block across the stern third |
| `BridgeTower` | tower on the superstructure |
| `ShieldGlobePort` / `Starboard` | the twin domes |
| `Engine0`-`4` | engine bank, centre bell larger, protruding aft of the stern face |
| `AxialCannonTrench` | the Xyston's ventral cannon channel |
| `AxialCannonMuzzle` | the bow aperture |

Modelled at the canon 2,400 m, then `HULL_SCALE = 4.0` on each mesh node gives a
**9,600 m** ship. Changing that one constant changes the size.

**The scale sits on the mesh nodes, not the root.** That leaves `HANGARROOTB` and both
maintenance locators at world scale 1.0 with no compensation arithmetic — the thing the
vanilla scene achieved with its 6 x 0.5 x 0.333333 chain.

Two further gotchas found while exporting:

- **Every mesh needs a UV map** or the export dies with `Object <name> missing UV map`.
  The script box-projects UVs at 60 m per repeat, which suits the borrowed tiled hull
  texture.
- **NMSDK names output files after the root object**, minus the `NMS_` prefix — not
  after the `scene_name` argument. Renaming the root to `NMS_CAPITALFREIGHTER_PROC` is
  what makes the file land as `CAPITALFREIGHTER_PROC.SCENE.MBIN`.

Installed as `GAMEDATA\MODS\XystonFreighter\`, replacing the scale-only mod:

    MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN       13,193
    MODELS/.../CAPITALFREIGHTER_PROC/CAPITALFREIGHTER_PROC.GEOMETRY.MBIN.PC     8,128
    MODELS/.../CAPITALFREIGHTER_PROC/CAPITALFREIGHTER_PROC.GEOMETRY.DATA.MBIN.PC 33,207

MBINCompiler 7.03.2 decompiles the scene cleanly. Structure verified: a `MODEL` root
named `CAPITALFREIGHTER_PROC` carrying the geometry attribute, 12 `MESH` children at
scale 4, and the three `LOCATOR` nodes at scale 1.

Renders of the hull are in `renders/`. **These are Blender renders, not screenshots.**
The game has never been launched with this installed. Whether it loads, renders,
collides or lets a ship land is entirely untested.

### Known rough edges, for the next pass

- Beam is 1,150 m against the Xyston's ~1,270 m, so it reads slightly narrow from above
- The axial cannon has no red emissive material yet — it is geometry only, because every
  part currently borrows the one vanilla freighter material
- The hangar locator's height offset is a guess and will likely need moving once the
  ship is seen in game
