"""Build a MODS-folder mod that resizes the NMS capital freighter.

The vanilla scene sizes the ship with a scene-node scale of 6 on the _Hull_A3
locator, and compensates the player-facing nodes (hangar, inventory) back down
so they render at world scale 1.0:

    HANGARROOTB world scale = 6 (_Hull_A3) x 0.5 (_Hull_A2) x 0.333333 = 1.0

This script raises the hull scale and recomputes that compensation, so the ship
grows but the hangar you land in and the inventory volume stay human sized.
Root-level locators (the maintenance slots) are not children of the hull, so
their positions are scaled by hand to keep them on the hull surface.

Usage:
    python build_scale_mod.py <input.scene.MXML> <hull_scale> <output_dir> [mod_name]

Nothing here has been confirmed in game. Treat the output as NEEDS TESTING.
"""
import shutil
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

VANILLA_HULL_SCALE = 6.0
COMPENSATED_NODES = ("HANGARROOTB", "Freighter_Medium", "Freighter_Medium1")
ROOT_LOCATORS = ("MaintenanceSlot0", "MaintenanceSlot1")
MBINCOMPILER = Path(
    r"C:\Users\johnf\Documents\Codex\2026-09-07"
    r"\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain"
    r"\MBINCompiler-v7.03.2-pre1\MBINCompiler.exe"
)
GAME_PATH = "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN"


def prop(node, name):
    for child in node.findall("Property"):
        if child.get("name") == name:
            return child
    return None


def value(node, name):
    found = prop(node, name)
    return found.get("value") if found is not None else None


def set_scale(node, scale):
    transform = prop(node, "Transform")
    for axis in ("ScaleX", "ScaleY", "ScaleZ"):
        prop(transform, axis).set("value", "%.6f" % scale)


def scale_position(node, factor):
    transform = prop(node, "Transform")
    for axis in ("TransX", "TransY", "TransZ"):
        field = prop(transform, axis)
        field.set("value", "%.6f" % (float(field.get("value")) * factor))


def walk(node, out=None):
    if out is None:
        out = []
    if value(node, "Name") is not None:
        out.append(node)
    children = prop(node, "Children")
    if children is not None:
        for child in children.findall("Property"):
            walk(child, out)
    return out


def build(source_mxml, hull_scale, out_dir, mod_name):
    tree = ET.parse(source_mxml)
    root = tree.getroot()
    nodes = {value(n, "Name"): n for n in walk(root)}

    factor = hull_scale / VANILLA_HULL_SCALE
    changes = []

    hull = nodes["_Hull_A3"]
    set_scale(hull, hull_scale)
    changes.append(("_Hull_A3", "scale", VANILLA_HULL_SCALE, hull_scale))

    # Keep every player-facing node at world scale 1.0. Each sits under a 0.5
    # hull mesh, so the chain is hull_scale * 0.5 * n == 1.0  ->  n = 2/hull_scale.
    compensated = 2.0 / hull_scale
    for name in COMPENSATED_NODES:
        node = nodes.get(name)
        if node is None:
            continue
        before = float(value(prop(node, "Transform"), "ScaleX"))
        set_scale(node, compensated)
        changes.append((name, "scale", before, compensated))

    for name in ROOT_LOCATORS:
        node = nodes.get(name)
        if node is None:
            continue
        scale_position(node, factor)
        changes.append((name, "position x", factor, factor))

    staged = Path(out_dir) / mod_name / Path(GAME_PATH).parent
    staged.mkdir(parents=True, exist_ok=True)
    mxml_out = staged / "CAPITALFREIGHTER_PROC.SCENE.MXML"
    tree.write(mxml_out, encoding="utf-8", xml_declaration=True)

    result = subprocess.run(
        [str(MBINCOMPILER), str(mxml_out)], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise SystemExit("MBINCompiler failed:\n" + result.stdout + result.stderr)
    mxml_out.unlink()

    mbin = staged / "CAPITALFREIGHTER_PROC.SCENE.MBIN"
    if not mbin.exists():
        produced = list(staged.glob("*.MBIN")) + list(staged.glob("*.mbin"))
        if not produced:
            raise SystemExit("no MBIN produced in %s" % staged)
        produced[0].rename(mbin)

    return mbin, changes, compensated


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    source = sys.argv[1]
    hull_scale = float(sys.argv[2])
    out_dir = sys.argv[3]
    mod_name = sys.argv[4] if len(sys.argv) > 4 else "XystonFreighterScale"

    mbin, changes, compensated = build(source, hull_scale, out_dir, mod_name)

    print("hull scale %.4f  (vanilla %.0f, factor %.3fx)"
          % (hull_scale, VANILLA_HULL_SCALE, hull_scale / VANILLA_HULL_SCALE))
    print("player-facing nodes compensated to %.6f so they stay world scale 1.0"
          % compensated)
    for name, what, before, after in changes:
        print("  %-18s %-10s %s -> %s" % (name, what, before, after))
    print("\nbuilt: %s  (%d bytes)" % (mbin, mbin.stat().st_size))
    print("install: copy the '%s' folder into GAMEDATA\\MODS\\" % mod_name)
    print("remove : delete that folder. Nothing else in the game is touched.")


if __name__ == "__main__":
    main()
