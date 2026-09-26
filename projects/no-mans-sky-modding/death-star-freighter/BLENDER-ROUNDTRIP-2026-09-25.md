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

## Capital-freighter root control: PASSED

The same dedicated Blender 5.0.1 profile and rebuilt local extension were
used against the actual owned-freighter resource:

`MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`.

A read-only scratch closure was built from the installed Cosmos 7.04 archives:
all `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/` files, plus the three DDS files
referenced by the root `FREIGHTERPROC_MAT.MATERIAL.MBIN`. No game asset was
copied into the repository or modified. With that closure, NMSDK imported 113
objects and exported a scene, descriptor MXML, geometry MBIN, and geometry-data
MBIN with exit code 0. The export log recorded the root geometry and 16 mesh
objects; it did not report a missing material, missing reference, or exporter
exception.

The existing MBINCompiler `7.03.2.1` can emit an MXML representation of the
exported scene but warns that its binary version is unrecognized. That warning
does not invalidate the successful NMSDK export, but it means this older
compiler is not a second binary-format validator for NMSDK's generated scene.

## Evidence boundary and next work

This is **VERIFIED for the actual capital-freighter root scene**, using a
read-only dependency closure and the isolated compatibility patch. It is not
proof of an installed mod, full recursive component-tree fidelity, collision,
docking, or boardability. The importer was intentionally run without recursive
reference importing.

Geometry work may now begin against the build brief. First measure the donor
root's transformed bounds and the hangar/approach location, then make one
minimal original exterior-shell probe. Keep the stock core untouched and do
not package or install it until the required backup and one-variable in-game
test plan exists.
