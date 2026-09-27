"""Create a diagnostic-only marker scene at the two measured hangar roots.

This does not modify a game asset. It produces original marker geometry that
can later be referenced by a separately reviewed stock-root override.
"""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


output_dir = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
assert output_dir.is_dir(), f"Missing output directory: {output_dir}"
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
root = bpy.context.active_object
root.name = "DeathStarHangarMarkersRoot"
root.NMSNode_props.node_types = "Reference"
root.NMSReference_props.scene_name = "death_star_hangar_markers"

material = "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN"
markers = {
    # Accumulated positions measured from the current capital root.
    "HANGARROOTA_MARKER": (0.0, 295.910309, 226.413742),
    "HANGARROOTB_MARKER": (0.0, 184.549149, 553.673706),
}

for index, (name, location) in enumerate(markers.items()):
    if index == 0:
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=45, radius2=0, depth=180, location=location)
    else:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=55, location=location)
    marker = bpy.context.active_object
    marker.name = name
    marker.parent = root
    marker.NMSNode_props.node_types = "Mesh"
    marker.NMSMesh_props.material_path = material
    uv_layer = marker.data.uv_layers.new(name="UVMap")
    for loop in uv_layer.data:
        loop.uv = (0.5, 0.5)

result = bpy.ops.nmsdk.export_scene(
    output_directory=str(output_dir), export_directory="CUSTOMMODELS",
    group_name="death_star_hangar_markers", scene_name="death_star_hangar_markers",
    preserve_node_info=False, AT_only=False, no_vert_colours=False,
    no_convert=True, idle_anim="",
)
assert result == {"FINISHED"}, result
print("HANGAR_ROOT_MARKERS=" + json.dumps(markers, sort_keys=True))
