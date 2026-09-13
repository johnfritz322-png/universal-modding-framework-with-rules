"""Create the single probe asset. Run inside UnrealEditor-Cmd with -ExecutePythonScript.

Deliberately a plain Material: it needs no source data, no private game module,
and no geometry, so the probe tests registry mounting and nothing else. The name
is unique so a runtime lookup cannot match anything the game already ships.
"""
import unreal

PACKAGE_PATH = "/ForgeRegistryProbe"
ASSET_NAME = "M_ForgeRegistryProbe0001"
FULL = "%s/%s" % (PACKAGE_PATH, ASSET_NAME)

tools = unreal.AssetToolsHelpers.get_asset_tools()

if unreal.EditorAssetLibrary.does_asset_exist(FULL):
    unreal.log("probe asset already exists: %s" % FULL)
else:
    asset = tools.create_asset(ASSET_NAME, PACKAGE_PATH, unreal.Material,
                               unreal.MaterialFactoryNew())
    if asset is None:
        raise RuntimeError("failed to create %s" % FULL)
    unreal.EditorAssetLibrary.save_loaded_asset(asset)
    unreal.log("created probe asset: %s" % FULL)

unreal.log("PROBE_ASSET_READY %s" % FULL)
