"""Build a reversible, stock-scene overlay mod staging tree.

This keeps the capital freighter's original scene graph and adds one reference
to the separately generated Death Star shell. It does not write game files,
install a mod, or edit saves. Compile the staged MXML to MBIN, then package
the staged MBIN plus the copied CUSTOMMODELS assets.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


CAPITAL_SCENE_RELATIVE = Path("MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MXML")


def jenkins_one_at_a_time(value: str) -> int:
    """Match NMSDK's exported scene-node hash implementation."""
    result = 0
    for char in value.upper():
        result = (result + ord(char)) & 0xFFFFFFFF
        result = (result + (result << 10)) & 0xFFFFFFFF
        result = (result ^ (result >> 6)) & 0xFFFFFFFF
    result = (result + (result << 3)) & 0xFFFFFFFF
    result = (result ^ (result >> 11)) & 0xFFFFFFFF
    result = (result + (result << 15)) & 0xFFFFFFFF
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capital-scene", type=Path, required=True)
    parser.add_argument("--shell-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shell-name", default="DEATH_STAR_SILHOUETTE_STAGE3")
    parser.add_argument("--trans-x", type=float, default=0.0)
    parser.add_argument("--trans-y", type=float, default=0.0)
    parser.add_argument("--trans-z", type=float, default=0.0)
    args = parser.parse_args()

    source = args.capital_scene.resolve()
    shell_root = args.shell_root.resolve()
    output = args.output.resolve()
    shell_name = args.shell_name.upper()
    shell_scene = f"//CUSTOMMODELS\\{shell_name}\\{shell_name}.SCENE.MBIN"
    assert source.is_file(), source
    assert (shell_root / "CUSTOMMODELS" / shell_name).is_dir(), shell_root
    assert not output.exists(), f"Refusing to overwrite existing staging tree: {output}"

    text = source.read_text(encoding="utf-8")
    marker = "\n\t</Property>\n</Data>"
    assert text.endswith(marker), "Unexpected capital-scene MXML root shape"
    root_indices = [int(value) for value in re.findall(
        r'^\t\t<Property name="Children" value="TkSceneNodeData" _index="(\d+)"',
        text,
        flags=re.MULTILINE,
    )]
    assert root_indices, "Could not find root children"
    next_index = max(root_indices) + 1
    name = "DeathStarExteriorOverlay"
    reference = f'''\n\t\t<Property name="Children" value="TkSceneNodeData" _index="{next_index}">
\t\t\t<Property name="Name" value="{name}" />
\t\t\t<Property name="NameHash" value="{jenkins_one_at_a_time(name)}" />
\t\t\t<Property name="Type" value="REFERENCE" />
\t\t\t<Property name="Transform" value="TkTransformData">
\t\t\t\t<Property name="TransX" value="{args.trans_x:.6f}" />
\t\t\t\t<Property name="TransY" value="{args.trans_y:.6f}" />
\t\t\t\t<Property name="TransZ" value="{args.trans_z:.6f}" />
\t\t\t\t<Property name="RotX" value="0.000000" />
\t\t\t\t<Property name="RotY" value="0.000000" />
\t\t\t\t<Property name="RotZ" value="0.000000" />
\t\t\t\t<Property name="ScaleX" value="1.000000" />
\t\t\t\t<Property name="ScaleY" value="1.000000" />
\t\t\t\t<Property name="ScaleZ" value="1.000000" />
\t\t\t</Property>
\t\t\t<Property name="PlatformExclusion" value="0" />
\t\t\t<Property name="Attributes">
\t\t\t\t<Property name="Attributes" value="TkSceneNodeAttributeData" _index="0">
\t\t\t\t\t<Property name="Name" value="SCENEGRAPH" />
\t\t\t\t\t<Property name="Value" value="{shell_scene}" />
\t\t\t\t</Property>
\t\t\t</Property>
\t\t\t<Property name="InstanceTransforms" />
\t\t\t<Property name="Children" />
\t\t</Property>'''
    updated = text[:-len(marker)] + reference + marker

    destination = output / CAPITAL_SCENE_RELATIVE
    destination.parent.mkdir(parents=True)
    destination.write_text(updated, encoding="utf-8", newline="\r\n")
    shutil.copytree(shell_root / "CUSTOMMODELS" / shell_name, output / "CUSTOMMODELS" / shell_name)
    print(f"OVERLAY_STAGING=created root_children_before={len(root_indices)} added_index={next_index}")
    print(f"OVERLAY_SCENEGRAPH={shell_scene}")
    print(f"OVERLAY_TRANSLATION=({args.trans_x:.6f}, {args.trans_y:.6f}, {args.trans_z:.6f})")


if __name__ == "__main__":
    main()
