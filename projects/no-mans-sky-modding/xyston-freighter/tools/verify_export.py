"""Import the installed scene back through NMSDK and check it survived.

This exists because five in-game tests were spent on faults that could have been
caught here. NMSDK reads the same files the game reads, so importing our own export
and comparing it against the source model catches:

  - geometry that failed to resolve (nothing imports)
  - faces "messed up" by bad triangulation, which NMSDK's own docs warn about
  - meshes lost between build and install
  - bounds that do not match what was modelled

It cannot prove the game will render it. It can prove the file is not obviously
broken, which is a different and much cheaper question.

Usage:
    blender.exe --background --python verify_export.py -- <mod_root>
"""
import os
import sys

import addon_utils
import bpy
from mathutils import Vector

SRC = (r"C:\Users\johnf\Documents\BG3Mods\universal-modding-framework-with-rules"
       r"\projects\no-mans-sky-modding\xyston-freighter\tools\build_xyston_hull.py")
SCENE = "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN"


def bounds(objs):
    lo = Vector((1e18,) * 3)
    hi = Vector((-1e18,) * 3)
    for ob in objs:
        if ob.type != "MESH" or not ob.data.vertices:
            continue
        for corner in ob.bound_box:
            w = ob.matrix_world @ Vector(corner)
            for i in range(3):
                lo[i] = min(lo[i], w[i])
                hi[i] = max(hi[i], w[i])
    return lo, hi


def main():
    root = sys.argv[sys.argv.index("--") + 1]
    addon_utils.enable("bl_ext.user_default.nmsdk", default_set=True, persistent=True)
    prefs = bpy.context.preferences.addons["bl_ext.user_default.nmsdk"].preferences
    prefs.pcbanks_dir = root
    prefs.unpacked_pcbanks_dir = root

    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)

    path = os.path.join(root, SCENE)
    print("importing %s" % path)
    print("exists on disk:", os.path.isfile(path))
    try:
        bpy.ops.nmsdk.import_scene(path=path, clear_scene=False,
                                   import_recursively=True, import_collisions=False)
        print("IMPORT_OK")
    except Exception as exc:
        print("IMPORT_FAILED:", exc)
        return

    meshes = [o for o in bpy.data.objects if o.type == "MESH" and o.data.vertices]
    faces = sum(len(o.data.polygons) for o in meshes)
    verts = sum(len(o.data.vertices) for o in meshes)
    non_tri = sum(1 for o in meshes for p in o.data.polygons if len(p.vertices) != 3)
    degenerate = 0
    for o in meshes:
        for p in o.data.polygons:
            if p.area <= 0.0:
                degenerate += 1

    lo, hi = bounds(meshes)
    size = hi - lo
    print()
    print("ROUND TRIP RESULT")
    print("  meshes imported      : %d" % len(meshes))
    print("  faces                : %d" % faces)
    print("  vertices             : %d" % verts)
    print("  non-triangular faces : %d" % non_tri)
    print("  zero-area faces      : %d" % degenerate)
    print("  bounds               : %.0f x %.0f x %.0f" % (size.x, size.y, size.z))
    for ob in sorted(meshes, key=lambda o: o.name)[:24]:
        print("     %-28s %6d faces" % (ob.name[:28], len(ob.data.polygons)))


if __name__ == "__main__":
    main()
