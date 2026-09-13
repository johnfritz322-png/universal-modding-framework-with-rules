"""Enable Nanite on the override mesh, and verify it actually stuck.

The previous attempt did get -> modify -> set on nanite_settings. UE Python hands
back a COPY of a struct property, so mutating it changes nothing. This builds a
fresh MeshNaniteSettings, assigns that, saves, then reloads from disk and reads
the value back - because "no error" is not evidence it applied.
"""
import unreal

ASSET = "/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01/L_Sword_Vampiric_01"

mesh = unreal.EditorAssetLibrary.load_asset(ASSET)
if mesh is None:
    raise RuntimeError("asset not found: %s" % ASSET)

before = mesh.get_editor_property("nanite_settings").get_editor_property("enabled")
unreal.log("NANITE before=%s" % before)

settings = unreal.MeshNaniteSettings()
settings.set_editor_property("enabled", True)
mesh.set_editor_property("nanite_settings", settings)

# force the mesh to rebuild its render data with Nanite before saving
sub = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
if sub is not None:
    try:
        sub.set_nanite_settings(mesh, settings, apply_changes=True)
        unreal.log("used StaticMeshEditorSubsystem.set_nanite_settings")
    except Exception as exc:
        unreal.log_warning("subsystem path unavailable: %s" % exc)

unreal.EditorAssetLibrary.save_loaded_asset(mesh)

# reload from disk and read back - the only check that means anything
unreal.EditorAssetLibrary.load_asset(ASSET)
reloaded = unreal.EditorAssetLibrary.load_asset(ASSET)
after = reloaded.get_editor_property("nanite_settings").get_editor_property("enabled")
unreal.log("NANITE after=%s" % after)
if not after:
    raise RuntimeError("Nanite did not persist")
unreal.log("NANITE_OK")
