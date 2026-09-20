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
