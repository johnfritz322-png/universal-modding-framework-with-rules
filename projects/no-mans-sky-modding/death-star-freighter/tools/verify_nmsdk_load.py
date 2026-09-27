"""Run inside Blender with --background --factory-startup --python-exit-code 1.

Pass -- <path-to-NMSDK-checkout> <copied-NMSARC.globals.pak> after --python.
This registers the add-on for this process only; no preferences are saved.
"""
import argparse
import hashlib
import importlib
import importlib.metadata
import json
import sys
from pathlib import Path

import addon_utils
import bpy

parser = argparse.ArgumentParser()
parser.add_argument("sdk", type=Path)
parser.add_argument("pak", type=Path)
parser.add_argument("--module", default="nmsdk")
parser.add_argument("--require-startup-enabled", action="store_true")
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
sdk, pak_path = args.sdk.resolve(), args.pak.resolve()
if args.module == "nmsdk":
    sys.path.insert(0, str(sdk / "src" / "addon"))
if args.require_startup_enabled:
    assert addon_utils.check(args.module)[1], "Add-on did not enable on fresh process startup"

# This import is deliberately allowed to raise. Blender's default exit code
# alone did not detect the missing dependency in the original check.
import hgpaktool
nmsdk = importlib.import_module(args.module)

def raise_enable_error():
    raise RuntimeError("NMSDK add-on enable failed") from sys.exc_info()[1]

module = addon_utils.enable(args.module, default_set=True, handle_error=raise_enable_error)
assert module is nmsdk, "Blender did not return the NMSDK module"
assert addon_utils.check(args.module)[1], "NMSDK is not enabled"
assert hasattr(bpy.types.Scene, "nmsdk_settings"), "Scene properties missing"
assert isinstance(bpy.context.preferences.addons[args.module].preferences, nmsdk.NMSDKPreferences)
assert bpy.ops.nmsdk.import_scene.get_rna_type().identifier == "NMSDK_OT_import_scene"
assert bpy.ops.nmsdk.export_scene.get_rna_type().identifier == "NMSDK_OT_export_scene"

# Prove the dependency can actually decode Windows archive data, not only import.
with hgpaktool.HGPAKFile(str(pak_path)) as pak:
    filenames = list(pak.filenames)
    assert filenames, "Archive returned no filenames"
    extracted = list(pak.extract("gcscratchpadglobals.global.mbin"))
    assert len(extracted) == 1, "Expected exactly one scratchpad globals file"
    asset_hash = hashlib.sha256(extracted[0][1]).hexdigest()
    assert asset_hash == "324d4af5975fa023ad06dddcba18a06899ec5b15d35c69341ea0daec25a7601d", "Archive payload differs from baseline"

print("NMSDK_LOAD_RESULT=" + json.dumps({
    "status": "PASS",
    "blender": bpy.app.version_string,
    "python": sys.version,
    "hgpaktool": importlib.metadata.version("hgpaktool"),
    "hgpaktool_module": hgpaktool.__file__,
    "nmsdk_module": nmsdk.__file__,
    "enabled": addon_utils.check(args.module)[1],
    "fresh_startup_enabled": args.require_startup_enabled,
    "asset_sha256": asset_hash,
    "pak_entries": len(filenames),
    "pak_sha256": hashlib.sha256(pak_path.read_bytes()).hexdigest(),
}, sort_keys=True))
addon_utils.disable(args.module, default_set=True)
assert not addon_utils.check(args.module)[1], "NMSDK stayed enabled after disable"
assert not hasattr(bpy.types.Scene, "nmsdk_settings"), "Scene properties not removed"
print("NMSDK_UNREGISTER=PASS")
