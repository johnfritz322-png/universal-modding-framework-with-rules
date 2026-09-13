import unreal
ASSET = "/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01/L_Sword_Vampiric_01"
lines = []
def rec(s):
    lines.append(str(s))
try:
    mesh = unreal.EditorAssetLibrary.load_asset(ASSET)
    rec("loaded=%s" % (mesh is not None))
    sub = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    rec("subsystem=%s" % (sub is not None))
    rec("has_set_nanite_settings=%s" % (hasattr(sub, "set_nanite_settings") if sub else False))
    s = unreal.MeshNaniteSettings()
    s.set_editor_property("enabled", True)
    rec("fresh_struct_enabled=%s" % s.get_editor_property("enabled"))
    if sub and hasattr(sub, "set_nanite_settings"):
        try:
            sub.set_nanite_settings(mesh, s, True)
            rec("set_nanite_settings=called")
        except Exception as e:
            rec("set_nanite_settings_ERROR=%s" % e)
    try:
        mesh.set_editor_property("nanite_settings", s)
        rec("direct_set=ok")
    except Exception as e:
        rec("direct_set_ERROR=%s" % e)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    again = unreal.EditorAssetLibrary.load_asset(ASSET)
    rec("readback=%s" % again.get_editor_property("nanite_settings").get_editor_property("enabled"))
except Exception as e:
    rec("FATAL=%s" % e)
open(r"D:\Dawnwalker-Modding\nanite_probe.txt", "w").write("\n".join(lines))
