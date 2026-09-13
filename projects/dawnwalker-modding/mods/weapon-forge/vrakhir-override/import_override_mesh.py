"""Import the custom blade AT an existing game mesh's package path.

The game resolves packages by chunk id, which is a hash of the package name, so
publishing a mesh at exactly this path makes the mod's version win on load order.
That is the same mechanism SkillsNoTimeCost and DualSenseAtlas already use here.

Target is The Vrakhir's blade.
"""
import unreal

TARGET_DIR = "/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01"
TARGET_NAME = "L_Sword_Vampiric_01"
OBJ = r"D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge\SourceArt\Override\SM_RiftforgedSlabblade_V2.obj"

task = unreal.AssetImportTask()
task.filename = OBJ
task.destination_path = TARGET_DIR
task.destination_name = TARGET_NAME
task.automated = True
task.replace_existing = True
task.save = True

opts = unreal.FbxImportUI()
opts.import_mesh = True
opts.import_as_skeletal = False
opts.import_materials = False
opts.import_textures = False
opts.static_mesh_import_data.set_editor_property("combine_meshes", True)
opts.static_mesh_import_data.set_editor_property("generate_lightmap_u_vs", True)
task.options = opts

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

full = "%s/%s" % (TARGET_DIR, TARGET_NAME)
if unreal.EditorAssetLibrary.does_asset_exist(full):
    unreal.log("OVERRIDE_MESH_READY %s" % full)
else:
    raise RuntimeError("import failed: %s" % full)
