import bpy, os, sys, re, importlib.util, addon_utils
from mathutils import Vector

UNPACKED = (r"C:\Users\johnf\AppData\Local\Temp\claude"
            r"\C--Users-johnf-Downloads-files\eb89a711-9d8f-4d87-bb01-babfe1d02d79"
            r"\scratchpad\unpacked")
VANILLA = "models/common/spacecraft/industrial/capitalfreighter_proc.scene.mbin"
SRC = (r"C:\Users\johnf\Documents\BG3Mods\universal-modding-framework-with-rules"
       r"\projects\no-mans-sky-modding\xyston-freighter\tools\build_xyston_hull.py")
OUT = (r"C:\Users\johnf\AppData\Local\Temp\claude"
       r"\C--Users-johnf-Downloads-files\eb89a711-9d8f-4d87-bb01-babfe1d02d79"
       r"\scratchpad\compare_renders")

addon_utils.enable("bl_ext.user_default.nmsdk", default_set=True, persistent=True)
prefs = bpy.context.preferences.addons["bl_ext.user_default.nmsdk"].preferences
prefs.pcbanks_dir = UNPACKED
prefs.unpacked_pcbanks_dir = UNPACKED

for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)


def bounds(objs):
    lo = Vector((1e18, 1e18, 1e18)); hi = Vector((-1e18, -1e18, -1e18))
    for ob in objs:
        if ob.type != "MESH" or not ob.data.vertices:
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    return lo, hi


bpy.ops.nmsdk.import_scene(path=os.path.join(UNPACKED, VANILLA), clear_scene=False,
                           import_recursively=True, import_collisions=False)

# FXSphere* are effect volumes, not hull. LOD1+ are lower detail copies of the
# same part sitting in the same place. Both would falsify a size comparison.
lod = re.compile(r"LOD[1-9]", re.I)
dropped = 0
for ob in list(bpy.data.objects):
    if ob.type != "MESH":
        continue
    if "FXSphere" in ob.name or lod.search(ob.name):
        bpy.data.objects.remove(ob, do_unlink=True)
        dropped += 1
print("dropped %d effect/LOD meshes" % dropped)

vanilla = [o for o in bpy.data.objects if o.type == "MESH" and o.data.vertices]
vlo, vhi = bounds(vanilla)
vsize = vhi - vlo
vcentre = (vlo + vhi) / 2.0
vfaces = sum(len(o.data.polygons) for o in vanilla)
print("VANILLA HULL length=%.0f width=%.0f height=%.0f meshes=%d faces=%d"
      % (vsize.y, vsize.x, vsize.z, len(vanilla), vfaces))

group = bpy.data.objects.new("VanillaGroup", None)
bpy.context.scene.collection.objects.link(group)
for o in vanilla:
    if o.parent is None or o.parent.type != "MESH":
        o.parent = group

spec = importlib.util.spec_from_file_location("xy", SRC)
xy = importlib.util.module_from_spec(spec)
sys.modules["xy"] = xy
spec.loader.exec_module(xy)
parts = xy.build()
for o in parts:
    o.scale = (xy.HULL_SCALE,) * 3
bpy.context.view_layer.update()
xlo, xhi = bounds(parts)
xsize = xhi - xlo
xcentre = (xlo + xhi) / 2.0
xfaces = sum(len(o.data.polygons) for o in parts)
print("XYSTON  length=%.0f width=%.0f height=%.0f meshes=%d faces=%d"
      % (xsize.y, xsize.x, xsize.z, len(parts), xfaces))
print("RATIO length %.2fx  width %.2fx  height %.2fx  faces %.4fx"
      % (xsize.y / vsize.y, xsize.x / vsize.x, xsize.z / vsize.z, xfaces / vfaces))

gap = max(vsize.x, xsize.x) * 0.18
group.location = (-vcentre.x - vsize.x / 2 - gap, -vcentre.y, -vcentre.z)
xgroup = bpy.data.objects.new("XystonGroup", None)
bpy.context.scene.collection.objects.link(xgroup)
for o in parts:
    o.parent = xgroup
xgroup.location = (-xcentre.x + xsize.x / 2 + gap, -xcentre.y, -xcentre.z)
bpy.context.view_layer.update()

allmesh = [o for o in bpy.data.objects if o.type == "MESH" and o.data.vertices]
alo, ahi = bounds(allmesh)
span = ahi - alo
mid = (alo + ahi) / 2.0

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x, scene.render.resolution_y = 1800, 1100
scene.world = bpy.data.worlds.new("W")
scene.world.color = (0.02, 0.02, 0.035)
sh = scene.display.shading
sh.light = "STUDIO"; sh.color_type = "SINGLE"
sh.single_color = (0.36, 0.37, 0.40)
sh.show_shadows = True; sh.show_cavity = True

target = bpy.data.objects.new("T", None)
scene.collection.objects.link(target)
target.location = mid
cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.lens = 35
cam_data.clip_start = 1.0
cam_data.clip_end = 500000.0
con = cam.constraints.new(type="TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"

reach = max(span.x, span.y)
views = {
    "plan": (mid.x, mid.y - reach * 0.02, mid.z + reach * 1.55),
    "three_quarter": (mid.x + reach * 0.35, mid.y - reach * 1.15, mid.z + reach * 0.50),
}
os.makedirs(OUT, exist_ok=True)
for name, loc in views.items():
    cam.location = loc
    scene.render.filepath = os.path.join(OUT, "compare_" + name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
