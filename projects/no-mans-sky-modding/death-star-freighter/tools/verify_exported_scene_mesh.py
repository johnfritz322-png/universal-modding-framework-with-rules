"""Load a generated NMS scene and directly exercise its mesh stream loader.

Run through the dedicated Blender 5.0.1 + NMSDK profile:
    blender --background --python-exit-code 1 --python verify_exported_scene_mesh.py -- <scene.mbin>
"""
import sys
from pathlib import Path

from bl_ext.nmsdk_local.nmsdk.ModelImporter.import_scene import ImportScene


scene_path = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
scene = ImportScene(str(scene_path), settings={"import_recursively": False})
nodes = list(scene.scene_node_data.iter()) if scene.requires_render else []
assert nodes, "Expected a renderable scene with at least one node"

mesh_node = nodes[-1]
assert mesh_node.info.Type == "MESH", mesh_node.info.Type
mesh_node.metadata = scene._handle_duplicate_mesh_names(mesh_node.Name.upper())
scene.geometry_stream_data = __import__(
    "bl_ext.nmsdk_local.nmsdk.utils.io", fromlist=["load_file_unsafe"]
).load_file_unsafe(
    scene.geometry_stream_file, scene.root_dir, scene.from_pak, scene.pak_data_mapping
)
scene.load_mesh(mesh_node)
print("EXPORTED_SCENE_MESH_LOAD=passed")
