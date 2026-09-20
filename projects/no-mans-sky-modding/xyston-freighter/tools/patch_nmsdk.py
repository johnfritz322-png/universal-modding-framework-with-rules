"""Apply the three NMSDK source fixes this project needs. Idempotent.

NMSDK's `cosmos_fixes` branch gets custom models into NMS 7.03.1, but three things
break before anything usable comes out. All three were found the hard way and all
three are one-liners.

1. **Export dies immediately.** `TkSceneNodeData` gained an `InstanceTransforms`
   field that the exporter never passes:

       TypeError: TkSceneNodeData.__init__() missing 1 required positional
       argument: 'InstanceTransforms'

   Empty is correct — the vanilla capital freighter scene carries
   `<Property name="InstanceTransforms" />` with no entries.

2 & 3. **Import dies on missing textures.** Only matters when importing vanilla
   scenes from an unpacked tree that has geometry but no DDS files, which is how the
   size comparison against the stock freighter was measured. Without these the
   import aborts after 3 meshes instead of completing all 732.

Usage:
    python patch_nmsdk.py [path-to-installed-nmsdk]

Default path is the Blender 5.0 user extensions directory.
"""
import sys
from pathlib import Path

DEFAULT = Path(r"C:\Users\johnf\AppData\Roaming\Blender Foundation\Blender\5.0"
               r"\extensions\user_default\nmsdk")

PATCHES = [
    (
        "NMS/classes/Object.py",
        "export: TkSceneNodeData requires InstanceTransforms",
        """                                        Attributes=self.Attributes,
                                        Children=child_nodes)""",
        """                                        Attributes=self.Attributes,
                                        InstanceTransforms=[],
                                        Children=child_nodes)""",
    ),
    (
        "utils/io.py",
        "import: realize_path must tolerate a missing NMS directory",
        """    base = get_NMS_dir("")
    if base == "":
        raise ValueError
    try:
        return op.join(base, fpath)
    except ValueError:
        return None""",
        """    base = get_NMS_dir("")
    if not base:
        return None
    try:
        return op.join(base, fpath)
    except (ValueError, TypeError):
        return None""",
    ),
    (
        "NMS/material_node.py",
        "import: colorspace must not be set on a texture that failed to load",
        """            img.colorspace_settings.name = 'Linear Rec.2020'""",
        """            if img is not None:
                img.colorspace_settings.name = 'Linear Rec.2020'""",
    ),
]


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not root.is_dir():
        raise SystemExit("NMSDK not found at %s" % root)
    print("patching %s\n" % root)

    for rel, why, old, new in PATCHES:
        path = root / rel
        if not path.is_file():
            print("  MISSING  %-26s %s" % (rel, why))
            continue
        text = path.read_text(encoding="utf-8")
        if new in text:
            print("  already  %-26s %s" % (rel, why))
            continue
        if old not in text:
            print("  FAILED   %-26s pattern not found - has NMSDK changed?" % rel)
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        print("  patched  %-26s %s" % (rel, why))

    print("\nRun again to confirm every line reports 'already'.")


if __name__ == "__main__":
    main()
