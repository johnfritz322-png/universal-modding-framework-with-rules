"""Import the custom blade at The Vrakhir's package path, with a material and collision.

v1 crashed the game on equip. The original mesh package references a material
instance (MI_L_Sword_Vampiric_01) and carries BodySetup/NavCollision; ours was
imported with materials off and no collision, leaving a null material slot -
which is what the access violation looked like.

This version ships its own material at a NEW path (so it adds rather than
collides) and generates collision.
"""
import unreal

DIR = "/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01"
MESH = "L_Sword_Vampiric_01"
MAT = "MI_Riftforged_Blade"          # new path: additive, no collision
OBJ = r"D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge\SourceArt\Override\SM_RiftforgedSlabblade_V2.obj"

tools = unreal.AssetToolsHelpers.get_asset_tools()

mat_path = "%s/Materials/%s" % (DIR, MAT)
if unreal.EditorAssetLibrary.does_asset_exist(mat_path):
    material = unreal.EditorAssetLibrary.load_asset(mat_path)
else:
    material = tools.create_asset(MAT, "%s/Materials" % DIR, unreal.Material,
                                  unreal.MaterialFactoryNew())
    unreal.EditorAssetLibrary.save_loaded_asset(material)
unreal.log("material ready: %s" % mat_path)

task = unreal.AssetImportTask()
task.filename = OBJ
task.destination_path = DIR
task.destination_name = MESH
task.automated = True
task.replace_existing = True
task.save = True
opts = unreal.FbxImportUI()
opts.import_mesh = True
opts.import_as_skeletal = False
opts.import_materials = False
opts.import_textures = False
sm = opts.static_mesh_import_data
sm.set_editor_property("combine_meshes", True)
sm.set_editor_property("generate_lightmap_u_vs", True)
sm.set_editor_property("auto_generate_collision", True)      # BodySetup
task.options = opts
tools.import_asset_tasks([task])

full = "%s/%s" % (DIR, MESH)
mesh = unreal.EditorAssetLibrary.load_asset(full)
if mesh is None:
    raise RuntimeError("import failed: %s" % full)

# a null material slot is the prime suspect for the crash - fill every slot
mats = mesh.static_materials
if not mats:
    mesh.add_material(material)
else:
    for i in range(len(mats)):
        mesh.set_material(i, material)
# The game's meshes are Nanite. Ours was not, and the package size gap says so:
# the original is 570,479 bytes of which only 2,520 is the export - the rest is
# bulk render data. A non-Nanite mesh handed to a Nanite render path is the best
# remaining explanation for the access violation.
nanite = mesh.get_editor_property("nanite_settings")
nanite.set_editor_property("enabled", True)
mesh.set_editor_property("nanite_settings", nanite)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)
unreal.log("nanite enabled=%s" % mesh.get_editor_property("nanite_settings").enabled)

slots = mesh.static_materials
unreal.log("OVERRIDE_MESH_READY %s slots=%d collision=%s"
           % (full, len(slots), mesh.get_editor_property("body_setup") is not None))
