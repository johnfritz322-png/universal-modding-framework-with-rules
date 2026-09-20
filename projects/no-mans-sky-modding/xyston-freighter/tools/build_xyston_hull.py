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
import random
import os
import sys

import subprocess

import addon_utils
import bmesh
import bpy

MBINCOMPILER = os.path.join(
    r"C:\Users\johnf\Documents\Codex\2026-09-07",
    "referenced-chatgpt-conversation-this-is-an", "work", "nms-toolchain",
    "MBINCompiler-v7.03.2-pre1", "MBINCompiler.exe")

# --- proportions -----------------------------------------------------------
# Xyston-class: 2,400 m long. Beam 1,450 m gives the 0.60 width-to-length ratio
# an Imperial Star Destroyer actually has - 1,150 read far too narrow from above.
LENGTH = 2400.0
BEAM = 1450.0
DRAUGHT = 300.0

HULL_SCALE = 2.0          # 2,400 m x 2 = 4,800 m. 4.0 filled the whole screen in game
MATERIAL = ("MODELS/COMMON/SPACECRAFT/INDUSTRIAL/"
            "CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN")
# Red emissive, shipped with the mod. Built by build_cannon_material.py from the
# Corvette's own hull-light material, which is unlit and does not billboard.
GLOW_MATERIAL = ("MODELS/COMMON/SPACECRAFT/INDUSTRIAL/"
                 "CAPITALFREIGHTER_PROC/XYSTON_CANNON_GLOW.MATERIAL.MBIN")
# Any part whose name contains this gets the glow material instead of hull plating.
GLOW_TAG = "Glow"

# "full"  = every detail pass, ~5,700 faces across 20 meshes
# "plain" = hull, superstructure and tower only, 4 meshes of flat boxes
#
# The plain build exists to bisect in-game rendering faults. If a four-box ship
# renders solid and clean, the fault is in the detail geometry; if it still tears,
# the fault is structural — the scene, the export or the engine's handling of a
# mesh this size — and no amount of adjusting greebles will touch it.
DETAIL_LEVEL = os.environ.get("XYSTON_DETAIL", "full")

def _out_dir():
    """Output directory: whatever follows `--` on the Blender command line.

    This used to test `endswith("nmsexport")` and silently fall back to a home
    directory for any other name, which made variant builds write nothing where
    they were expected and fail only at the copy step.
    """
    if "--" in sys.argv:
        tail = sys.argv[sys.argv.index("--") + 1:]
        if tail:
            return tail[0]
    return os.path.join(os.path.expanduser("~"), "xyston_out")


OUT_DIR = _out_dir()


def clear_scene():
    """Empty the scene without touching preferences, which would unload NMSDK."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


# Metres of FINISHED SHIP per texture repeat. The borrowed freighter texture is
# hull plating, which needs to repeat every few metres to read as plating at all.
# UVs are generated in model units and the whole mesh is then multiplied by
# HULL_SCALE, so the divide is what keeps the plating the same physical size no
# matter how big the ship is set to.
#
# This was 60 model units with no divide, i.e. a 240 m repeat at HULL_SCALE 4 —
# stretched roughly fifty-fold, which is why the hull rendered as flat grey.
TILE_WORLD_METRES = 5.0
TILE = TILE_WORLD_METRES / HULL_SCALE


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


def triangulate(mesh):
    """Triangulate every face before export.

    NMSDK's own documentation (docs/exporting/exporting.md) warns:

        "When exporting an object it may be exported with edges and faces messed
        up. This happens when the mesh is improperly triangulated. Whilst NMSDK
        should triangulate a mesh properly it sometimes doesn't work as well as
        it should."

    and prescribes triangulating in Blender before exporting. Every face this
    script builds is a quad — boxes, the hull's flanks and stern, every greeble —
    so the entire model was relying on that unreliable path. "Edges and faces
    messed up" is exactly the torn, shredded hull seen in game.
    """
    bm = bmesh.new()
    bm.from_mesh(mesh)
    # Degenerate triangles first — the cylinder cap fans produce a few zero-area
    # faces, and a zero-area triangle has no usable normal, which is a classic
    # source of rendering artefacts.
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def recalculate_normals(mesh):
    """Force every face to point outward.

    Face winding here is written by hand, and `make_sphere` and `make_cylinder`
    both had it backwards — their signed volumes came out negative, meaning every
    polygon faced inward. Blender's Workbench render does not backface cull, so
    they looked perfectly fine in every preview while the game, which does cull,
    rendered them inside out.

    Checking signed volume is the reliable test: positive is outward. Counting
    faces that point away from the mesh centroid is not, because a greeble field
    is hundreds of separate islands and roughly half of any island's faces point
    towards the middle of the ship quite correctly.
    """
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def signed_volume(mesh):
    """Positive means the normals face outward."""
    total = 0.0
    for poly in mesh.polygons:
        pts = [mesh.vertices[i].co for i in poly.vertices]
        for i in range(1, len(pts) - 1):
            total += pts[0].dot(pts[i].cross(pts[i + 1])) / 6.0
    return total


def mesh_from_geometry(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    mesh.update()
    triangulate(mesh)
    recalculate_normals(mesh)
    if any(len(p.vertices) != 3 for p in mesh.polygons):
        raise SystemExit("%s still has non-triangular faces after triangulation"
                         % name)
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


class Greebler:
    """Accumulates many small boxes into ONE mesh.

    Surface detail has to be thousands of faces to stop the hull reading as flat,
    but it must not become thousands of scene nodes — the vanilla freighter carries
    76,996 faces across only 334 meshes. Every greeble field here collapses into a
    single mesh with many disconnected islands.
    """

    def __init__(self):
        self.verts = []
        self.faces = []

    def box(self, cx, cy, cz, sx, sy, sz, taper=1.0):
        hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
        tx, ty = hx * taper, hy * taper
        base = len(self.verts)
        self.verts += [
            (cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
            (cx - tx, cy - ty, cz + hz), (cx + tx, cy - ty, cz + hz),
            (cx + tx, cy + ty, cz + hz), (cx - tx, cy + ty, cz + hz),
        ]
        for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                  (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.faces.append(tuple(base + i for i in f))

    def emit(self, name):
        if not self.faces:
            return None
        return mesh_from_geometry(name, self.verts, self.faces)


# --- where the hull surface actually is, so detail sits on it ---------------

def dorsal_z(y):
    """Height of the sloped top surface at a given point along the ship."""
    half_l = LENGTH / 2.0
    t = (half_l - y) / LENGTH          # 0 at the bow, 1 at the stern
    return DRAUGHT * 0.06 + (DRAUGHT - DRAUGHT * 0.06) * t


def dorsal_half_width(y):
    """Half width of the top surface at a given point. Zero at the bow."""
    half_l = LENGTH / 2.0
    return (BEAM / 2.0) * 0.82 * (half_l - y) / LENGTH


def ventral_half_width(y):
    half_l = LENGTH / 2.0
    return (BEAM / 2.0) * (half_l - y) / LENGTH


def dorsal_greebles(rng):
    """Panel clutter across the top surface, thinning towards the bow."""
    g = Greebler()
    half_l = LENGTH / 2.0
    # keep clear of the command block so detail does not poke through it
    block_y0, block_y1 = -LENGTH * 0.42, -LENGTH * 0.17
    block_x = BEAM * 0.20

    y = -half_l + LENGTH * 0.02
    while y < half_l - LENGTH * 0.06:
        row_depth = LENGTH * rng.uniform(0.008, 0.020)
        limit = dorsal_half_width(y) * 0.94
        if limit > BEAM * 0.02:
            x = -limit
            while x < limit:
                w = BEAM * rng.uniform(0.009, 0.034)
                if x + w > limit:
                    break
                inside_block = (block_y0 < y < block_y1 and abs(x) < block_x)
                if not inside_block and rng.random() < 0.80:
                    h = DRAUGHT * rng.uniform(0.018, 0.085)
                    g.box(x + w / 2.0, y + row_depth / 2.0,
                          dorsal_z(y) + h / 2.0 - DRAUGHT * 0.012,
                          w, row_depth * rng.uniform(0.55, 0.95), h,
                          taper=rng.choice((1.0, 1.0, 0.86)))
                x += w + BEAM * rng.uniform(0.004, 0.016)
        y += row_depth + LENGTH * rng.uniform(0.004, 0.012)
    return g.emit("DorsalGreebles")


def dorsal_trenches():
    """The long channels either side of the command block.

    Built as segments rather than one long box: the top surface slopes and the
    hull narrows towards the bow, so a single box would rise out of the deck and
    shoot past the hull edge near the nose.
    """
    g = Greebler()
    half_l = LENGTH / 2.0
    for side in (-1, 1):
        for i in range(3):
            offset = BEAM * (0.11 + i * 0.055)
            y0, y1 = -half_l + LENGTH * 0.06, half_l - LENGTH * 0.06
            steps = 34
            for s in range(steps):
                y = y0 + (y1 - y0) * s / steps
                seg = (y1 - y0) / steps
                if offset > dorsal_half_width(y) * 0.88:
                    continue                       # past the hull edge here
                g.box(side * offset, y + seg / 2.0,
                      dorsal_z(y) - DRAUGHT * 0.015,
                      BEAM * 0.016, seg * 0.94, DRAUGHT * 0.05)
    return g.emit("DorsalTrenches")


def flank_x(y, frac):
    """X on the sloped flank at a fraction of the way up it.

    The flank runs from the ventral edge at z=0 to the narrower dorsal edge at
    z=dorsal_z(y), so it leans inward. Interpolating between the two widths is
    what keeps detail flush against it instead of floating off in mid air.
    """
    return (ventral_half_width(y)
            + (dorsal_half_width(y) - ventral_half_width(y)) * frac)


def flank_ridges():
    """Horizontal strakes down both sloped flanks, sunk flush into the plating."""
    g = Greebler()
    half_l = LENGTH / 2.0
    for side in (-1, 1):
        for i in range(5):
            frac = 0.14 + i * 0.18
            y0, y1 = -half_l + LENGTH * 0.03, half_l - LENGTH * 0.10
            steps = 30
            for s in range(steps):
                y = y0 + (y1 - y0) * s / steps
                seg = (y1 - y0) / steps
                x = flank_x(y, frac) * 0.975      # slightly inside the surface
                if x < BEAM * 0.01:
                    continue
                g.box(side * x, y + seg / 2.0, dorsal_z(y) * frac,
                      BEAM * 0.010, seg * 0.90, DRAUGHT * 0.030)
    return g.emit("FlankRidges")


def flank_bays():
    """Recessed bay blocks along the flanks, the big shapes that break up a slab."""
    g = Greebler()
    half_l = LENGTH / 2.0
    for side in (-1, 1):
        for i in range(6):
            y = -half_l + LENGTH * (0.10 + i * 0.12)
            frac = 0.30 if i % 2 else 0.58
            x = flank_x(y, frac) * 0.96
            if x < BEAM * 0.02:
                continue
            g.box(side * x, y, dorsal_z(y) * frac,
                  BEAM * 0.022, LENGTH * 0.055, DRAUGHT * 0.16, taper=0.9)
    return g.emit("FlankBays")


def command_tiers():
    """Stepped tiers on the command block, the way a real Star Destroyer steps up."""
    g = Greebler()
    base_z = DRAUGHT + DRAUGHT * 0.5
    for i, (w, d, h, taper) in enumerate((
            (0.30, 0.185, 0.10, 0.92),
            (0.24, 0.150, 0.10, 0.90),
            (0.185, 0.115, 0.10, 0.88))):
        g.box(0.0, -LENGTH * (0.305 + i * 0.012), base_z + DRAUGHT * (0.05 + i * 0.10),
              BEAM * w, LENGTH * d, DRAUGHT * h, taper=taper)
    # sensor and comms clutter on the tower deck
    for side in (-1, 1):
        for i in range(3):
            g.box(side * BEAM * (0.03 + i * 0.022), -LENGTH * 0.335,
                  base_z + DRAUGHT * 0.36, BEAM * 0.012,
                  LENGTH * 0.012, DRAUGHT * (0.10 + i * 0.04))
    return g.emit("CommandTiers")


def ventral_detail(rng):
    """Hangar bays and belly plating.

    The belly is the plane z = 0 and the hull occupies z > 0, so anything meant to
    be seen from underneath has to sit at NEGATIVE z. Detail placed at positive z
    is entirely swallowed by the hull — which is exactly what happened to the first
    version of this function, the cannon trench and the glow strip.
    """
    g = Greebler()
    # main ventral hangar bay, hanging proud of the belly
    g.box(0.0, -LENGTH * 0.335, -DRAUGHT * 0.030,
          BEAM * 0.30, LENGTH * 0.11, DRAUGHT * 0.060)
    for side in (-1, 1):
        g.box(side * BEAM * 0.20, -LENGTH * 0.30, -DRAUGHT * 0.026,
              BEAM * 0.08, LENGTH * 0.07, DRAUGHT * 0.052)
    half_l = LENGTH / 2.0
    y = -half_l + LENGTH * 0.06
    while y < half_l - LENGTH * 0.10:
        depth = LENGTH * rng.uniform(0.02, 0.04)
        limit = ventral_half_width(y) * 0.90
        if limit > BEAM * 0.05:
            x = -limit
            while x < limit:
                w = BEAM * rng.uniform(0.03, 0.07)
                if x + w > limit:
                    break
                if rng.random() < 0.55 and abs(x + w / 2.0) > BEAM * 0.06:
                    g.box(x + w / 2.0, y + depth / 2.0, -DRAUGHT * 0.014,
                          w, depth * 0.85, DRAUGHT * 0.028)
                x += w + BEAM * rng.uniform(0.01, 0.03)
        y += depth + LENGTH * rng.uniform(0.01, 0.03)
    return g.emit("VentralDetail")


def build():
    rng = random.Random(24601)      # fixed, so the ship is the same every build
    parts = [make_hull()]

    if DETAIL_LEVEL == "plain":
        parts.append(make_box(
            "Superstructure",
            0.0, -LENGTH * 0.30, DRAUGHT + DRAUGHT * 0.25,
            BEAM * 0.34, LENGTH * 0.22, DRAUGHT * 0.5, taper=0.78))
        parts.append(make_box(
            "BridgeTower",
            0.0, -LENGTH * 0.355, DRAUGHT + DRAUGHT * 0.5 + DRAUGHT * 0.30,
            BEAM * 0.13, LENGTH * 0.05, DRAUGHT * 0.6, taper=0.85))
        parts.append(make_box(
            "AxialCannonHousing",
            0.0, LENGTH * 0.04, -DRAUGHT * 0.045,
            BEAM * 0.075, LENGTH * 0.76, DRAUGHT * 0.09))
        return parts

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

    # The Xyston's signature: the axial cannon along the belly. The housing hangs
    # below the hull (negative z) and the glowing channel hangs lower still, so the
    # red is the lowest surface and is actually visible from underneath.
    parts.append(make_box(
        "AxialCannonHousing",
        0.0, LENGTH * 0.04, -DRAUGHT * 0.045,
        BEAM * 0.075, LENGTH * 0.76, DRAUGHT * 0.09, taper=1.0))

    glow = Greebler()
    y0, y1 = -LENGTH * 0.33, LENGTH * 0.44
    steps = 44
    for s in range(steps):
        y = y0 + (y1 - y0) * s / steps
        seg = (y1 - y0) / steps
        glow.box(0.0, y + seg / 2.0, -DRAUGHT * 0.080,
                 BEAM * 0.032, seg * 0.96, DRAUGHT * 0.060)
    strip = glow.emit("AxialCannonGlowStrip")
    if strip is not None:
        parts.append(strip)

    # The muzzle, projecting forward past the bow blade.
    parts.append(make_cylinder(
        "AxialCannonMuzzleGlow",
        0.0, LENGTH * 0.50, -DRAUGHT * 0.045,
        DRAUGHT * 0.075, LENGTH * 0.055))

    # Emitter blisters flanking the channel, so the belly reads as charged.
    blisters = Greebler()
    for side in (-1, 1):
        for i in range(5):
            blisters.box(side * BEAM * (0.055 + i * 0.013),
                         LENGTH * (0.34 - i * 0.075), -DRAUGHT * 0.055,
                         BEAM * 0.014, LENGTH * 0.035, DRAUGHT * 0.050)
    blister = blisters.emit("AxialCannonEmitterGlow")
    if blister is not None:
        parts.append(blister)

    # Surface detail. Without this the hull is 503 faces of flat plane and reads
    # as a blocky primitive next to the vanilla freighter's 76,996.
    for detail in (dorsal_greebles(rng), dorsal_trenches(), flank_ridges(),
                   flank_bays(), command_tiers(), ventral_detail(rng)):
        if detail is not None:
            parts.append(detail)

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
        glowing = GLOW_TAG in obj.name
        obj.NMSMesh_props.material_path = GLOW_MATERIAL if glowing else MATERIAL
        obj.scale = (HULL_SCALE, HULL_SCALE, HULL_SCALE)
        total_faces += len(obj.data.polygons)
        vol = signed_volume(obj.data)
        if vol <= 0:
            raise SystemExit(
                "%s has inward normals after recalculation (volume %.0f)"
                % (obj.name, vol))
        print("  part %-26s %5d verts %5d faces  vol %+12.0f %s"
              % (obj.name, len(obj.data.vertices), len(obj.data.polygons), vol,
                 "GLOW" if glowing else ""))

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
    normalise_scene_guid()
    print("EXPORT_DONE")


def _backslash_paths(text):
    """Rewrite every MODELS/... attribute value to use backslashes.

    Only touches values that look like internal asset paths, so the rest of the
    XML is left alone. Returns the text and how many values were changed.
    """
    import re

    changed = [0]

    def fix(match):
        value = match.group(1)
        if "MODELS" not in value.upper() or "/" not in value:
            return match.group(0)
        changed[0] += 1
        return 'value="%s"' % value.replace("/", "\\")

    out = re.sub(r'value="([^"]*)"', fix, text)
    return out, changed[0]


def normalise_scene_guid():
    """Round-trip the exported scene through MBINCompiler to fix its header.

    NMSDK stamps its own template GUID into the MBIN header. The vanilla capital
    freighter scene carries `d8 02 1f 59 63 a8 96 ad` at offset 0x10; NMSDK writes
    something else. Decompiling and recompiling with MBINCompiler restores the
    correct value, because MBINCompiler resolves the template by name.

    The geometry files are unaffected — their GUIDs already match vanilla, so this
    is specific to the scene.
    """
    scene = os.path.join(OUT_DIR, "MODELS", "COMMON", "SPACECRAFT", "INDUSTRIAL",
                         "CAPITALFREIGHTER_PROC", "CAPITALFREIGHTER_PROC.SCENE.MBIN")
    if not os.path.exists(scene):
        print("  GUID normalise: no scene at %s" % scene)
        return
    before = open(scene, "rb").read()[16:24].hex(" ")
    mxml = scene[:-len(".MBIN")] + ".MXML"

    subprocess.run([MBINCOMPILER, scene], capture_output=True, text=True)
    if not os.path.exists(mxml):
        print("  GUID normalise: decompile produced no MXML, leaving scene as is")
        return

    # Every internal path must use backslashes. NMSDK keeps whatever separator it
    # was handed for `export_directory` and `material_path`, and joins the rest with
    # backslashes, producing hybrids like
    #
    #   MODELS/COMMON/SPACECRAFT/INDUSTRIAL\CAPITALFREIGHTER_PROC\...GEOMETRY.MBIN
    #
    # Vanilla scenes are backslash throughout. A path the engine cannot resolve
    # means the geometry never loads and the ship renders as nothing at all.
    text = open(mxml, "r", encoding="utf-8").read()
    fixed, count = _backslash_paths(text)

    # NMSDK always nests its output in a folder named after the scene, so the
    # scene ends up calling itself
    #
    #   MODELS\...\INDUSTRIAL\CAPITALFREIGHTER_PROC\CAPITALFREIGHTER_PROC
    #
    # where vanilla is simply MODELS\...\INDUSTRIAL\CAPITALFREIGHTER_PROC. The
    # scene's Name is its identity to the engine and the GEOMETRY attribute is how
    # it finds its mesh data, so both have to match vanilla exactly. Collapsing the
    # doubled segment fixes both at once.
    #
    # Material paths are deliberately untouched: those really do live in a
    # subfolder named after the model, in vanilla too.
    doubled = "INDUSTRIAL\\CAPITALFREIGHTER_PROC\\CAPITALFREIGHTER_PROC"
    flat = "INDUSTRIAL\\CAPITALFREIGHTER_PROC"
    collapsed = fixed.count(doubled)
    fixed = fixed.replace(doubled, flat)

    open(mxml, "w", encoding="utf-8").write(fixed)
    print("  paths normalised to backslashes: %d" % count)
    print("  doubled scene-name segments collapsed: %d" % collapsed)

    # MBINCompiler will not overwrite an existing MBIN, so the NMSDK one has to
    # go before the recompile. This is why an earlier attempt silently no-opped.
    os.remove(scene)
    subprocess.run([MBINCOMPILER, mxml], capture_output=True, text=True)
    os.remove(mxml)

    if not os.path.exists(scene):
        raise SystemExit("recompile did not produce %s" % scene)
    after = open(scene, "rb").read()[16:24].hex(" ")
    print("  scene GUID %s -> %s%s"
          % (before, after, "" if before != after else "   UNCHANGED, check this"))


if __name__ == "__main__":
    main()
