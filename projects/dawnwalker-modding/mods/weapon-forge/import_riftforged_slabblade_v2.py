"""Import the V2 Riftforged source asset into the isolated Unreal project.

Never writes to Dawnwalker.  The destination asset is a new V2 name, so the
retired blockout remains intact for comparison and rollback.
"""
import os
import unreal

PROJECT = r"D:/Dawnwalker-Modding/Projects/DawnwalkerWeaponForge"
SOURCE = os.path.join(PROJECT, "SourceArt", "Weapons", "SM_RiftforgedSlabblade_V2.obj")
DESTINATION = "/Game/Weapons/Meshes"
MATERIAL_PATH = "/Game/Weapons/Materials/M_Riftforged_V2"
MESH_PATH = DESTINATION + "/SM_RiftforgedSlabblade_V2"

if not os.path.isfile(SOURCE):
    raise RuntimeError("Missing V2 OBJ: " + SOURCE)

if unreal.EditorAssetLibrary.does_asset_exist(MESH_PATH):
    raise RuntimeError("Refusing to overwrite existing V2 mesh: " + MESH_PATH)

task = unreal.AssetImportTask()
task.filename = SOURCE
task.destination_path = DESTINATION
task.automated = True
task.replace_existing = False
task.save = True
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
if not task.imported_object_paths:
    raise RuntimeError("Unreal did not report an imported mesh")

mesh = unreal.load_asset(MESH_PATH)
if not mesh:
    raise RuntimeError("Imported object is not available at " + MESH_PATH)
if mesh.get_bounds().box_extent.z < 100:
    raise RuntimeError("V2 mesh is unexpectedly short")

tools = unreal.AssetToolsHelpers.get_asset_tools()
material = unreal.load_asset(MATERIAL_PATH)
if not material:
    material = tools.create_asset("M_Riftforged_V2", "/Game/Weapons/Materials", unreal.Material, unreal.MaterialFactoryNew())

unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
def color(value, x, y):
    node = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant3Vector, x, y)
    node.constant = unreal.LinearColor(*value, 1.0)
    return node
def scalar(value, x, y):
    node = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant, x, y)
    node.r = value
    return node

unreal.MaterialEditingLibrary.connect_material_property(
    color((0.055, 0.070, 0.090), -420, -80), "", unreal.MaterialProperty.MP_BASE_COLOR)
unreal.MaterialEditingLibrary.connect_material_property(
    color((0.0, 0.12, 0.34), -420, 80), "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
unreal.MaterialEditingLibrary.connect_material_property(
    scalar(0.92, -420, 210), "", unreal.MaterialProperty.MP_METALLIC)
unreal.MaterialEditingLibrary.connect_material_property(
    scalar(0.27, -420, 300), "", unreal.MaterialProperty.MP_ROUGHNESS)
unreal.MaterialEditingLibrary.recompile_material(material)

slots = mesh.get_editor_property("static_materials")
if not slots:
    raise RuntimeError("Imported mesh has no material slots")
for index in range(len(slots)):
    mesh.set_material(index, material)
unreal.EditorAssetLibrary.save_loaded_asset(material)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)
unreal.log("RIFTFORGED_V2_IMPORT=PASS mesh=" + MESH_PATH + " slots=" + str(len(slots)))
