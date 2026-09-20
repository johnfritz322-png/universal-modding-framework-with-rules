import bpy, sys, os, importlib.util

SRC = (r"C:\Users\johnf\Documents\BG3Mods\universal-modding-framework-with-rules"
       r"\projects\no-mans-sky-modding\xyston-freighter\tools\build_xyston_hull.py")
OUT = (r"C:\Users\johnf\AppData\Local\Temp\claude"
       r"\C--Users-johnf-Downloads-files\eb89a711-9d8f-4d87-bb01-babfe1d02d79"
       r"\scratchpad\glow_renders")

spec = importlib.util.spec_from_file_location("xy", SRC)
xy = importlib.util.module_from_spec(spec)
sys.modules["xy"] = xy
spec.loader.exec_module(xy)

xy.clear_scene()
parts = xy.build()

# Workbench renders one flat colour per object, so tint by object to show which
# meshes carry the glow material in the exported scene.
for ob in parts:
    if xy.GLOW_TAG in ob.name:
        ob.color = (1.0, 0.06, 0.05, 1.0)
    else:
        ob.color = (0.36, 0.37, 0.40, 1.0)

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x, scene.render.resolution_y = 1700, 1000
scene.world = bpy.data.worlds.new("W")
scene.world.color = (0.02, 0.02, 0.035)
sh = scene.display.shading
sh.light = "STUDIO"
sh.color_type = "OBJECT"
sh.show_shadows = True
sh.show_cavity = True

L = xy.LENGTH
target = bpy.data.objects.new("T", None)
scene.collection.objects.link(target)
target.location = (0.0, -L * 0.02, xy.DRAUGHT * 0.2)

cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.lens = 42
cam_data.clip_start = 1.0
cam_data.clip_end = 200000.0
con = cam.constraints.new(type="TRACK_TO")
con.target = target
con.track_axis = "TRACK_NEGATIVE_Z"
con.up_axis = "UP_Y"

views = {
    "underside": (L * 0.45, -L * 0.75, -L * 0.95),
    "bow_low": (L * 0.30, L * 1.15, -L * 0.30),
    "three_quarter": (L * 1.25, -L * 1.75, L * 0.62),
}
os.makedirs(OUT, exist_ok=True)
for name, loc in views.items():
    cam.location = loc
    scene.render.filepath = os.path.join(OUT, "glow_" + name + ".png")
    bpy.ops.render.render(write_still=True)
    print("rendered", name)
