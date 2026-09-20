"""Build a Xyston-class Sith Star Destroyer hull and export it as an NMS scene.

Run inside Blender 5.0.1 with the NMSDK `cosmos_fixes` add-on installed and the
`InstanceTransforms=[]` fix applied to `NMS/classes/Object.py` — see
MESH-PIPELINE-WORKS.md.

    blender.exe --background --python build_xyston_hull.py

The hull is modelled at the Xyston's canon 2,400 m and then scaled on its own mesh
node. Keeping the scale on the hull rather than the root means the locators the game
needs — the hangar and the maintenance slots — stay at world scale 1.0 with no
compensation arithmetic, which is where the vanilla scene's 6 x 0.5 x 0.333333
chain came from.

Nothing here has been seen in game. Treat every claim about how it looks or behaves
as NEEDS TESTING.
"""
import math
import os
import sys

import addon_utils
import bmesh
import bpy

# --- proportions -----------------------------------------------------------
# Xyston-class: 2,400 m long. Beam and draught follow the Imperial wedge.
LENGTH = 2400.0
BEAM = 1150.0
DRAUGHT = 300.0

HULL_SCALE = 4.0          # 2,400 m x 4 = 9,600 m, the size asked for
MATERIAL = ("MODELS/COMMON/SPACECRAFT/INDUSTRIAL/"
            "CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN")

OUT_DIR = sys.argv[-1] if sys.argv[-1].endswith("nmsexport") else os.path.join(
    os.path.expanduser("~"), "xyston_out")


def clear_scene():
    """Empty the scene without touching preferences, which would unload NMSDK."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


TILE = 60.0   # metres per texture repeat, so the hull plating reads at ship scale


def add_uvs(obj):
    """Box-project UVs. NMSDK refuses any mesh without a UV map, and a world
    space projection suits the tiled hull texture we are borrowing."""
    mesh = obj.data
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        nx, ny, nz = (abs(c) for c in poly.normal)
        for loop_index in poly.loop_indices:
            x, y, z = mesh.vertices[mesh.loops[loop_index].vertex_index].co
            if nz >= nx and nz >= ny:
                u, v = x, y
            elif nx >= ny:
                u, v = y, z
            else:
                u, v = x, z
            uv_layer.data[loop_index].uv = (u / TILE, v / TILE)


def mesh_from_geometry(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    add_uvs(obj)
    return obj


def make_hull():
    """The main wedge: flat ventral triangle, dorsal triangle, sharp bow."""
    half_l, half_b = LENGTH / 2.0, BEAM / 2.0
    bow_thickness = DRAUGHT * 0.06      # the bow is a thin blade, not a point
    dorsal_inset = 0.82                 # the top face is narrower than the bottom

    verts = [
        # ventral (flat bottom)
        (0.0, half_l, 0.0),                       # 0 bow
        (-half_b, -half_l, 0.0),                  # 1 stern port
        (half_b, -half_l, 0.0),                   # 2 stern starboard
        # dorsal
        (0.0, half_l, bow_thickness),             # 3 bow
        (-half_b * dorsal_inset, -half_l, DRAUGHT),   # 4 stern port
        (half_b * dorsal_inset, -half_l, DRAUGHT),    # 5 stern starboard
    ]
    faces = [
        (0, 2, 1),          # ventral
        (3, 4, 5),          # dorsal
        (1, 2, 5, 4),       # stern
        (0, 1, 4, 3),       # port flank
        (2, 0, 3, 5),       # starboard flank
    ]
    return mesh_from_geometry("XystonHull", verts, faces)


def make_box(name, cx, cy, cz, sx, sy, sz, taper=1.0):
    """A box, optionally tapered towards its top, for the superstructure."""
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
    tx, ty = hx * taper, hy * taper
    verts = [
        (cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
        (cx - tx, cy - ty, cz + hz), (cx + tx, cy - ty, cz + hz),
        (cx + tx, cy + ty, cz + hz), (cx - tx, cy + ty, cz + hz),
    ]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_from_geometry(name, verts, faces)


def make_cylinder(name, cx, cy, cz, radius, depth, segments=16):
    """An engine bell, axis along Y, open end facing aft."""
    verts, faces = [], []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        y, z = math.cos(a) * radius, math.sin(a) * radius
        verts.append((cx + y, cy - depth / 2.0, cz + z))
        verts.append((cx + y, cy + depth / 2.0, cz + z))
    for i in range(segments):
        a, b = 2 * i, 2 * ((i + 1) % segments)
        faces.append((a, b, b + 1, a + 1))
    verts.append((cx, cy - depth / 2.0, cz))
    verts.append((cx, cy + depth / 2.0, cz))
    cap_a, cap_b = len(verts) - 2, len(verts) - 1
    for i in range(segments):
        a, b = 2 * i, 2 * ((i + 1) % segments)
        faces.append((a, cap_a, b))
        faces.append((b + 1, cap_b, a + 1))
    return mesh_from_geometry(name, verts, faces)


def make_sphere(name, cx, cy, cz, radius, rings=8, segments=12):
    verts, faces = [], []
    for r in range(rings + 1):
        phi = math.pi * r / rings
        for s in range(segments):
            theta = 2.0 * math.pi * s / segments
            verts.append((
                cx + radius * math.sin(phi) * math.cos(theta),
                cy + radius * math.sin(phi) * math.sin(theta),
                cz + radius * math.cos(phi),
            ))
    for r in range(rings):
        for s in range(segments):
            a = r * segments + s
            b = r * segments + (s + 1) % segments
            faces.append((a, b, b + segments, a + segments))
    return mesh_from_geometry(name, verts, faces)


def build():
    parts = [make_hull()]

    # Command superstructure: the raised block across the stern third.
    parts.append(make_box(
        "Superstructure",
        0.0, -LENGTH * 0.30, DRAUGHT + DRAUGHT * 0.25,
        BEAM * 0.34, LENGTH * 0.22, DRAUGHT * 0.5, taper=0.78))

    # Bridge tower and its two shield globes.
    tower_z = DRAUGHT + DRAUGHT * 0.5 + DRAUGHT * 0.30
    parts.append(make_box(
        "BridgeTower",
        0.0, -LENGTH * 0.355, tower_z,
        BEAM * 0.13, LENGTH * 0.05, DRAUGHT * 0.6, taper=0.85))
    globe_z = tower_z + DRAUGHT * 0.38
    for side, tag in ((-1, "Port"), (1, "Starboard")):
        parts.append(make_sphere(
            "ShieldGlobe" + tag,
            side * BEAM * 0.085, -LENGTH * 0.355, globe_z, DRAUGHT * 0.16))

    # Engine bank across the stern face.
    for i, offset in enumerate((-0.30, -0.15, 0.0, 0.15, 0.30)):
        radius = DRAUGHT * (0.30 if abs(offset) < 0.01 else 0.22)
        parts.append(make_cylinder(
            "Engine%d" % i,
            offset * BEAM, -LENGTH * 0.5 - DRAUGHT * 0.18,
            DRAUGHT * 0.55, radius, DRAUGHT * 0.36))

    # The Xyston's signature: the axial cannon trench along the belly.
    parts.append(make_box(
        "AxialCannonTrench",
        0.0, LENGTH * 0.06, DRAUGHT * 0.12,
        BEAM * 0.07, LENGTH * 0.72, DRAUGHT * 0.24, taper=1.0))
    parts.append(make_cylinder(
        "AxialCannonMuzzle",
        0.0, LENGTH * 0.40, DRAUGHT * 0.12,
        DRAUGHT * 0.11, LENGTH * 0.06))

    return parts


def main():
    addon_utils.enable("bl_ext.user_default.nmsdk",
                       default_set=True, persistent=True)
    clear_scene()

    bpy.ops.nmsdk.create_root_scene()
    root = bpy.data.objects["NMS_Scene"]
    # NMSDK names the output after the root object, minus the NMS_ prefix, so
    # this is what makes the file land as CAPITALFREIGHTER_PROC.SCENE.MBIN.
    root.name = "NMS_CAPITALFREIGHTER_PROC"

    parts = build()
    total_faces = 0
    for obj in parts:
        obj.parent = root
        obj.NMSNode_props.node_types = "Mesh"
        obj.NMSMesh_props.material_path = MATERIAL
        obj.scale = (HULL_SCALE, HULL_SCALE, HULL_SCALE)
        total_faces += len(obj.data.polygons)
        print("  part %-22s %4d verts %4d faces"
              % (obj.name, len(obj.data.vertices), len(obj.data.polygons)))

    # Locators the game attaches things to. Left at scale 1.0 deliberately, so
    # the hangar the player lands in stays human sized however big the hull is.
    for name, pos in (
        ("HANGARROOTB", (0.0, -LENGTH * 0.22 * HULL_SCALE, -8.0)),
        ("MaintenanceSlot0", (0.0, -LENGTH * 0.40 * HULL_SCALE, DRAUGHT * HULL_SCALE)),
        ("MaintenanceSlot1", (0.0, LENGTH * 0.20 * HULL_SCALE, DRAUGHT * 0.3 * HULL_SCALE)),
    ):
        empty = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(empty)
        empty.parent = root
        empty.location = pos
        empty.NMSNode_props.node_types = "Locator"

    print("total: %d parts, %d faces, hull %.0f m"
          % (len(parts), total_faces, LENGTH * HULL_SCALE))

    bpy.ops.nmsdk.export_scene(
        output_directory=OUT_DIR,
        export_directory="MODELS/COMMON/SPACECRAFT/INDUSTRIAL",
        group_name="",
        scene_name="CAPITALFREIGHTER_PROC",
    )
    print("EXPORT_DONE")


if __name__ == "__main__":
    main()
