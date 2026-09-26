# Blender/NMSDK scene round-trip gate

Recorded 2026-09-25, America/Denver. This test used the dedicated Blender
5.0.1 profile and NMSDK extension documented in
`NMSDK-REPAIR-2026-09-25.md`. It wrote only to scratch output directories;
no game archive, mod package, save, or repository source was modified.

## Result: BLOCKED — reproducible importer/exporter failure

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

## Next bounded investigation

Inspect the current NMSDK material-sampler handling and compare it with a
known passing bundled fixture before any source patch or workaround. A fix
must be validated with both the toy-cube control and the capital scene's full
dependency tree. Do not lower this gate merely because operators register.
