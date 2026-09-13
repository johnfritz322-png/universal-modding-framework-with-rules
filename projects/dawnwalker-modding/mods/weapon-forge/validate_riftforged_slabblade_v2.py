"""Validate the isolated V2 Riftforged Unreal assets."""
import unreal

mesh = unreal.load_asset("/Game/Weapons/Meshes/SM_RiftforgedSlabblade_V2")
material = unreal.load_asset("/Game/Weapons/Materials/M_Riftforged_V2")
if not mesh or not material:
    raise RuntimeError("Missing V2 mesh or material")
extent = mesh.get_bounds().box_extent
if extent.z < 100 or extent.x < 20 or extent.y < 3:
    raise RuntimeError("V2 mesh bounds do not match a usable greatsword")
slots = mesh.get_editor_property("static_materials")
if len(slots) < 1:
    raise RuntimeError("V2 mesh has no material slots")
for index, slot in enumerate(slots):
    if slot.material_interface != material:
        raise RuntimeError("V2 material mismatch in slot " + str(index))
unreal.log("RIFTFORGED_V2_VALIDATE=PASS extent=" + str(extent) + " slots=" + str(len(slots)))
