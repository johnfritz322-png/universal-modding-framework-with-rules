# Blender/NMSDK scene round-trip gate

Recorded 2026-09-25, America/Denver. This test used the dedicated Blender
5.0.1 profile and NMSDK extension documented in
`NMSDK-REPAIR-2026-09-25.md`. It wrote only to scratch output directories;
no game archive, mod package, save, or repository source was modified.

## Initial result: BLOCKED — reproducible importer/exporter failure

Two current-build controls were attempted with `NMSDK 0.10.0-alpha14` from
the `cosmos_fixes` checkout:

1. The copied capital-freighter scene, including its extracted geometry.
2. A separate current-build `TOY_CUBE` control with its scene, geometry,
   material, and entity files freshly extracted from the installed game.

Both imports reached NMSDK rendering but raised the same error while creating
a material:

```text
TypeError: expected str, bytes or os.PathLike object, not NoneType
  material_node.py:96, realize_path(tex_path, local_root_directory)
```

NMSDK then left at least one imported mesh without a material slot. Export of
both controls failed reproducibly with:

```text
IndexError: bpy_prop_collection[index]: index 0 out of range, size 0
  ModelExporter/addon_script.py:1060, ob.material_slots[0].material
```

The capital test also correctly reported missing referenced component scenes
because the prior extraction intentionally contained only the capital scene
and geometry. The toy-cube control removes that incomplete-capital-tree
explanation: it has a self-contained scene/geometry/material/entity set and
still produces the same material-path and material-slot failure.

## Evidence boundary

The extension loads, registers, and reads a current-build archive; that is
still VERIFIED. Scene import/export is **BLOCKED**. No partially generated
output was treated as a pass, and no Death Star geometry work may begin.

## Root cause and recovery

The initial toy-cube extraction omitted the material-referenced DDS textures.
With the complete current-build toy-cube scene, geometry, material, entity,
and texture closure extracted into a scratch `MODELS`/`TEXTURES` tree, import
completed. Export then reached a separate NMSDK source mismatch:
`TkSceneNodeData` now requires `InstanceTransforms`, but the exporter did not
provide it.

Dedicated local NMSDK branch `codex/cosmos-instance-transforms`, commit
`2d8c239`, supplies an empty `InstanceTransforms` list for non-instanced
exported nodes. The rebuilt extension was installed only in the dedicated
Blender profile. The toy-cube control then passed current-build
scene → Blender → scene/geometry export, producing a scene plus both geometry
files with exit code 0.

This is **VERIFIED for the minimal current-build control**, not proof that the
capital freighter imports or exports intact. The capital scene has a large
referenced component tree that must be extracted as a dependency closure.

## Next bounded investigation

Build a complete, read-only extracted dependency closure for the capital
scene, including its referenced scenes, materials, textures, and geometry.
Then repeat the same import/export control before modeling any Death Star
geometry. Do not treat the small toy-cube pass as freighter boardability or
full-capital compatibility proof.
