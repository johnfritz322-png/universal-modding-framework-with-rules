"""Control: put a known-good engine cube at The Vrakhir's blade path.

The previous control was invalid - it hand-split an IoStore package into
.uasset/.uexp, which is not the legacy cooked layout, so the package was
malformed before it ever reached the game.

This one goes through the ordinary cook pipeline with an asset the engine itself
ships, so the only variable left is the pipeline.
"""
import unreal

DIR = "/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01"
NAME = "L_Sword_Vampiric_01"
SRC = "/Engine/BasicShapes/Cube"

src = unreal.EditorAssetLibrary.load_asset(SRC)
if src is None:
    raise RuntimeError("engine cube not found")

dst = "%s/%s" % (DIR, NAME)
if unreal.EditorAssetLibrary.does_asset_exist(dst):
    unreal.EditorAssetLibrary.delete_asset(dst)
unreal.EditorAssetLibrary.duplicate_asset(SRC, dst)

mesh = unreal.EditorAssetLibrary.load_asset(dst)
if mesh is None:
    raise RuntimeError("duplicate failed")
unreal.EditorAssetLibrary.save_loaded_asset(mesh)
open(r"D:\Dawnwalker-Modding\control_cube.txt", "w").write(
    "duplicated=%s materials=%d" % (dst, len(mesh.static_materials)))
