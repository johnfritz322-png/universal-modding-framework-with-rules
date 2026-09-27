"""Add the Death Star shell reference through NMSDK's scene exporter.

This preserves imported scene metadata instead of compiling a hand-edited
MXML scene with MBINCompiler. It reads a copied dependency closure only and
writes a fresh staging tree.
"""
from __future__ import annotations

import sys
from pathlib import Path

import bpy


SHELL_SCENE = "//CUSTOMMODELS\\DEATH_STAR_SILHOUETTE_STAGE3\\DEATH_STAR_SILHOUETTE_STAGE3.SCENE.MBIN"


def main() -> None:
    scene_path = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
    output_dir = Path(sys.argv[sys.argv.index("--") + 2]).resolve()
    assert scene_path.is_file(), scene_path
    assert output_dir.is_dir(), output_dir

    result = bpy.ops.nmsdk.import_scene(
        path=str(scene_path), clear_scene=True, import_recursively=False,
        dump_extracted_files=False, import_collisions=False, show_collisions=False,
        import_bones=False, import_idle_anims=False, import_anims=False,
        max_anims=0, draw_hulls=False,
    )
    assert result == {"FINISHED"}, result
    roots = [obj for obj in bpy.context.scene.objects if obj.parent is None]
    candidates = [obj for obj in roots if obj.NMSNode_props.node_types == "Reference"]
    assert len(candidates) == 1, [(obj.name, obj.NMSNode_props.node_types) for obj in roots]
    root = candidates[0]

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    overlay = bpy.context.active_object
    overlay.name = "DeathStarExteriorOverlay"
    overlay.parent = root
    overlay.NMSNode_props.node_types = "Reference"
    overlay.NMSReference_props.reference_path = SHELL_SCENE

    # The imported root carries the original scene name; retain it and every
    # available original-node field during export.
    result = bpy.ops.nmsdk.export_scene(
        output_directory=str(output_dir),
        export_directory="MODELS/COMMON/SPACECRAFT/INDUSTRIAL",
        group_name="",
        scene_name="",
        preserve_node_info=True,
        AT_only=False,
        no_vert_colours=False,
        no_convert=True,
        idle_anim="",
    )
    assert result == {"FINISHED"}, result
    print(f"NMSDK_OVERLAY=created root={root.name} reference={SHELL_SCENE}")


if __name__ == "__main__":
    main()
