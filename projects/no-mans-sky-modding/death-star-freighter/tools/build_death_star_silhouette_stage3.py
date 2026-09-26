"""Build scratch-only Stage 3 Death Star shell geometry with QA renders.

The aperture is a visual prototype, not an installable docking claim: the
runtime root-to-hangar attachment transform remains unverified.
"""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


output_dir = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
assert output_dir.is_dir(), f"Missing output directory: {output_dir}"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Measured capital-root bounding-box centre and HANGARROOTA accumulated point.
donor_center = Vector((1.020752, 1956.979401, -135.783936))
hangar_root = Vector((0.0, 295.910309, 226.413742))
aperture_direction = (hangar_root - donor_center).normalized()

# Orient the trench so the measured hangar direction lies on its equator.
trench_axis = aperture_direction.cross(Vector((1.0, 0.0, 0.0))).normalized()
if trench_axis.length == 0:
    trench_axis = Vector((0.0, 0.0, 1.0))
side_axis = trench_axis.cross(aperture_direction).normalized()

bpy.ops.object.empty_add(type="PLAIN_AXES", location=donor_center)
root = bpy.context.active_object
root.name = "DeathStarSilhouetteStage3Root"
root.NMSNode_props.node_types = "Reference"
root.NMSReference_props.scene_name = "death_star_silhouette_stage3"

radius = 2131.2010195
segments = 96
rings = 48
trench_depth = 96.0
trench_half_width = 0.085
dish_depth = 330.0
dish_radius = 0.37
dish_axis = (0.5 * trench_axis + 0.8660254 * side_axis).normalized()
panel_relief = 10.0
# 90.66 units is the unpadded approach-grid width. This is deliberately a
# generous visual aperture, not a measured safe collision opening.
aperture_half_width = 0.075
aperture_half_height = 0.055

vertices = []
for ring in range(rings + 1):
    theta = math.pi * ring / rings
    for segment in range(segments):
        phi = 2 * math.pi * segment / segments
        direction = Vector((
            math.sin(theta) * math.cos(phi),
            math.sin(theta) * math.sin(phi),
            math.cos(theta),
        ))
        equator_delta = abs(math.asin(max(-1.0, min(1.0, direction.dot(trench_axis)))))
        trench_factor = max(0.0, 1.0 - (equator_delta / trench_half_width) ** 2)
        dish_angle = math.acos(max(-1.0, min(1.0, direction.dot(dish_axis))))
        dish_factor = max(0.0, 1.0 - (dish_angle / dish_radius) ** 2)
        panel_factor = 0.0 if (trench_factor or dish_factor) else (1.0 if (ring + segment) % 2 else -0.35)
        local_radius = radius - trench_depth * trench_factor - dish_depth * dish_factor**2 + panel_relief * panel_factor
        vertices.append(tuple(direction * local_radius))

faces = []
for ring in range(rings):
    for segment in range(segments):
        next_segment = (segment + 1) % segments
        a = ring * segments + segment
        b = ring * segments + next_segment
        c = (ring + 1) * segments + next_segment
        d = (ring + 1) * segments + segment
        face_direction = (Vector(vertices[a]) + Vector(vertices[b]) + Vector(vertices[c]) + Vector(vertices[d])).normalized()
        forward = face_direction.dot(aperture_direction)
        lateral = abs(math.asin(max(-1.0, min(1.0, face_direction.dot(side_axis)))))
        vertical = abs(math.asin(max(-1.0, min(1.0, face_direction.dot(trench_axis)))))
        if forward > 0.99 and lateral < aperture_half_width and vertical < aperture_half_height:
            continue
        faces.append((a, b, c, d))

# Compact after face removal so exporter validation has no orphaned vertices.
used_indices = sorted({index for face in faces for index in face})
index_map = {old: new for new, old in enumerate(used_indices)}
vertices = [vertices[index] for index in used_indices]
faces = [tuple(index_map[index] for index in face) for face in faces]

mesh = bpy.data.meshes.new("DeathStarSilhouetteStage3Mesh")
mesh.from_pydata(vertices, [], faces)
mesh.update()
shell = bpy.data.objects.new("DeathStarSilhouetteStage3", mesh)
bpy.context.collection.objects.link(shell)
shell.parent = root
shell.NMSNode_props.node_types = "Mesh"
shell.NMSMesh_props.material_path = (
    "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/"
    "FREIGHTERPROC_MAT.MATERIAL.MBIN"
)
uv_layer = mesh.uv_layers.new(name="UVMap")
for polygon in mesh.polygons:
    for loop_index in polygon.loop_indices:
        vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co.normalized()
        uv_layer.data[loop_index].uv = (
            (math.atan2(vertex.y, vertex.x) / (2 * math.pi)) % 1.0,
            math.acos(max(-1.0, min(1.0, vertex.z))) / math.pi,
        )


def point_at(object_, target):
    object_.rotation_euler = (Vector(target) - object_.location).to_track_quat("-Z", "Y").to_euler()


# Render before export because NMSDK normalizes scene state during export.
camera_distance = radius * 4.8
bpy.ops.object.camera_add(location=donor_center + aperture_direction * camera_distance)
camera = bpy.context.active_object
camera.data.lens = 52
camera.data.clip_end = 20000
point_at(camera, donor_center)
bpy.context.scene.camera = camera

for direction, energy, size in (
    (aperture_direction, 2700, 2200),
    ((aperture_direction + side_axis).normalized(), 1600, 1500),
    ((aperture_direction - trench_axis).normalized(), 1100, 1200),
):
    bpy.ops.object.light_add(type="AREA", location=donor_center + direction * radius * 2.2)
    light = bpy.context.active_object
    light.data.energy = energy
    light.data.shape = "DISK"
    light.data.size = size
    point_at(light, donor_center)

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.studiolight_rotate_z = 0.45
scene.display.shading.studiolight_background_alpha = 1.0
scene.display.shading.studiolight_background_blur = 0.35
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(output_dir / "stage3-aperture-overview.png")
scene.world.color = (0.004, 0.004, 0.008)
bpy.ops.render.render(write_still=True)

camera.location = donor_center + dish_axis * camera_distance
point_at(camera, donor_center)
scene.render.filepath = str(output_dir / "stage3-dish-overview.png")
bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(camera, do_unlink=True)
for object_ in list(bpy.data.objects):
    if object_.type == "LIGHT":
        bpy.data.objects.remove(object_, do_unlink=True)

result = bpy.ops.nmsdk.export_scene(
    output_directory=str(output_dir), export_directory="CUSTOMMODELS",
    group_name="death_star_silhouette_stage3",
    scene_name="death_star_silhouette_stage3", preserve_node_info=False,
    AT_only=False, no_vert_colours=False, no_convert=True, idle_anim="",
)
assert result == {"FINISHED"}, result

files = sorted(str(path.relative_to(output_dir)) for path in output_dir.rglob("*") if path.is_file())
assert files, "Export produced no files"
print("DEATH_STAR_SILHOUETTE_STAGE3=" + json.dumps({
    "aperture_direction": [round(value, 6) for value in aperture_direction],
    "aperture_face_removals": rings * segments - len(faces),
    "donor_center": [round(value, 6) for value in donor_center],
    "faces": len(mesh.polygons), "vertices": len(mesh.vertices),
    "exported_files": files,
}, sort_keys=True))
