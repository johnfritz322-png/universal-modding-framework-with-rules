"""Build the red emissive material for the Xyston's axial cannon.

Rather than authoring a material from nothing, this retints a vanilla one that is
already proven to glow on hull geometry: `BiggsLightsMAT`, the Corvette's own hull
lights. It carries exactly the combination wanted here —

    MaterialClass = GlowTranslucent
    _F01_DIFFUSEMAP + _F07_UNLIT      (unlit, so it ignores scene lighting)
    CastShadow = false

— and points at a vanilla lights texture, so no DDS authoring is needed. The only
change is `gMaterialColourVec4`, white to red.

The engine glow material was the other candidate and was rejected: it carries
`_F19_BILLBOARD`, which makes geometry turn to face the camera. Correct for an engine
flare sprite, wrong for a trench cut into a hull.

Usage:
    python build_cannon_material.py <biggslightsmat.MXML> <out_dir>
"""
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

NAME = "XYSTON_CANNON_GLOW"
RED = (1.000000, 0.055000, 0.045000, 1.000000)
GAME_DIR = "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC"
MBINCOMPILER = Path(
    r"C:\Users\johnf\Documents\Codex\2026-09-07"
    r"\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain"
    r"\MBINCompiler-v7.03.2-pre1\MBINCompiler.exe"
)


def prop(node, name):
    for child in node.findall("Property"):
        if child.get("name") == name:
            return child
    return None


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    source, out_dir = sys.argv[1], sys.argv[2]

    tree = ET.parse(source)
    root = tree.getroot()
    if root.get("template") != "cTkMaterialData":
        raise SystemExit("not a material: %s" % root.get("template"))

    # sanity check the template really is unlit and glowing before trusting it
    flags = {prop(f, "MaterialFlag").get("value")
             for f in prop(root, "Flags").findall("Property")}
    klass = prop(prop(root, "Class"), "MaterialClass").get("value")
    print("template class  : %s" % klass)
    print("template flags  : %s" % ", ".join(sorted(flags)))
    if "_F07_UNLIT" not in flags:
        raise SystemExit("template is not unlit, it will not glow")
    if "_F19_BILLBOARD" in flags:
        raise SystemExit("template billboards, wrong for hull geometry")

    prop(root, "Name").set("value", NAME)

    colour = None
    for uniform in prop(root, "Uniforms_Float").findall("Property"):
        if prop(uniform, "Name").get("value") == "gMaterialColourVec4":
            colour = prop(uniform, "Values")
    if colour is None:
        raise SystemExit("no gMaterialColourVec4 to retint")
    before = tuple(float(prop(colour, a).get("value")) for a in "XYZW")
    for axis, value in zip("XYZW", RED):
        prop(colour, axis).set("value", "%.6f" % value)
    print("colour          : %s -> %s" % (before, RED))

    staged = Path(out_dir) / GAME_DIR
    staged.mkdir(parents=True, exist_ok=True)
    mxml = staged / (NAME + ".MATERIAL.MXML")
    tree.write(mxml, encoding="utf-8", xml_declaration=True)

    result = subprocess.run([str(MBINCOMPILER), str(mxml)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit("MBINCompiler failed:\n" + result.stdout + result.stderr)
    mxml.unlink()

    produced = list(staged.glob(NAME + "*.MBIN")) + list(staged.glob(NAME + "*.mbin"))
    if not produced:
        raise SystemExit("no MBIN produced in %s" % staged)
    final = staged / (NAME + ".MATERIAL.MBIN")
    if produced[0] != final:
        produced[0].rename(final)

    print("built           : %s (%d bytes)" % (final, final.stat().st_size))
    print("reference it as : %s/%s.MATERIAL.MBIN" % (GAME_DIR, NAME))


if __name__ == "__main__":
    main()
