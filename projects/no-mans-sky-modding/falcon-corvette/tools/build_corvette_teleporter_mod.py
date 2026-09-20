"""Make the ordinary base teleporter buildable inside a Corvette.

What gates the Corvette build menu is a single field on each product in
`metadata/reality/tables/nms_basepartproducts.mbin`:

    <Property name="CorvettePartCategory" value="GcCorvettePartCategory">
      <Property name="CorvettePartCategory" value="Access" />   <- B_ALK_C, an airlock
      <Property name="CorvettePartCategory" value="None" />     <- TELEPORTER
    </Property>

Every structural Corvette part carries a category (Hull, Engine, Cockpit, Access,
Interior, Decor...). This gives TELEPORTER the `Interior` category so it appears in
the ship builder.

Two outputs are produced:

  patch/       an EXML partial patch, the 5.50+ recommended form. Touches only the
               one field, so it coexists with any other mod.
  replacement/ a full MBIN replacement of the table, as a fallback if the patch form
               is not picked up. Conflicts with any other mod editing this table.

Nothing here has been confirmed in game. Treat both as NEEDS TESTING.
"""
import shutil
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

PART_ID = "TELEPORTER"
NEW_CATEGORY = "Interior"
GAME_PATH = "METADATA/REALITY/TABLES/NMS_BASEPARTPRODUCTS"
MBINCOMPILER = Path(
    r"C:\Users\johnf\Documents\Codex\2026-09-07"
    r"\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain"
    r"\MBINCompiler-v7.03.2-pre1\MBINCompiler.exe"
)

PATCH = """<?xml version="1.0" encoding="utf-8"?>
<!--Makes the base teleporter buildable inside a Corvette-->
<Data template="cGcProductTable">
  <Property name="Table">
    <Property name="Table" value="GcProductData" _id="{part}">
      <Property name="CorvettePartCategory" value="GcCorvettePartCategory">
        <Property name="CorvettePartCategory" value="{category}" />
      </Property>
    </Property>
  </Property>
</Data>
"""


def prop(node, name):
    for child in node.findall("Property"):
        if child.get("name") == name:
            return child
    return None


def find_product(root, part_id):
    table = prop(root, "Table")
    if table is None:
        raise SystemExit("no Table property at the root - wrong file?")
    for entry in table.findall("Property"):
        if entry.get("_id") == part_id:
            return entry
    raise SystemExit("product %s not found" % part_id)


def verify_target(source_mxml):
    """Confirm the patch targets exactly one real entry, shaped as expected."""
    root = ET.parse(source_mxml).getroot()
    if root.get("template") != "cGcProductTable":
        raise SystemExit("unexpected root template: %s" % root.get("template"))

    table = prop(root, "Table")
    matches = [e for e in table.findall("Property") if e.get("_id") == PART_ID]
    if len(matches) != 1:
        raise SystemExit("expected exactly 1 %s entry, found %d" % (PART_ID, len(matches)))

    entry = matches[0]
    cat = prop(entry, "CorvettePartCategory")
    if cat is None:
        raise SystemExit("%s has no CorvettePartCategory field" % PART_ID)
    inner = prop(cat, "CorvettePartCategory")
    print("  target found: %s, CorvettePartCategory currently %r"
          % (PART_ID, inner.get("value")))
    return root, entry, inner


def build_patch(out_dir):
    staged = Path(out_dir) / "CorvetteTeleporter" / Path(GAME_PATH).parent
    staged.mkdir(parents=True, exist_ok=True)
    target = staged / (Path(GAME_PATH).name + ".EXML")
    text = PATCH.format(part=PART_ID, category=NEW_CATEGORY)
    target.write_text(text, encoding="utf-8")

    # The patch must be well formed, and must describe the same shape as the
    # real table, or the game has nothing to match against.
    patched = ET.fromstring(text)
    entry = find_product(patched, PART_ID)
    inner = prop(prop(entry, "CorvettePartCategory"), "CorvettePartCategory")
    assert inner.get("value") == NEW_CATEGORY, "patch does not set the category"
    return target


def build_replacement(source_mxml, out_dir):
    staged = Path(out_dir) / "CorvetteTeleporter_Replacement" / Path(GAME_PATH).parent
    staged.mkdir(parents=True, exist_ok=True)

    tree = ET.parse(source_mxml)
    entry = find_product(tree.getroot(), PART_ID)
    inner = prop(prop(entry, "CorvettePartCategory"), "CorvettePartCategory")
    inner.set("value", NEW_CATEGORY)

    mxml = staged / (Path(GAME_PATH).name + ".MXML")
    tree.write(mxml, encoding="utf-8", xml_declaration=True)

    result = subprocess.run([str(MBINCOMPILER), str(mxml)], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit("MBINCompiler failed:\n" + result.stdout + result.stderr)
    mxml.unlink()

    produced = list(staged.glob("*.MBIN")) + list(staged.glob("*.mbin"))
    if not produced:
        raise SystemExit("no MBIN produced")
    final = staged / (Path(GAME_PATH).name + ".MBIN")
    if produced[0] != final:
        produced[0].rename(final)
    return final


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    source_mxml, out_dir = sys.argv[1], sys.argv[2]

    print("verifying the patch target against the real table...")
    verify_target(source_mxml)

    patch = build_patch(out_dir)
    print("\npatch mod     : %s (%d bytes)" % (patch, patch.stat().st_size))

    replacement = build_replacement(source_mxml, out_dir)
    print("replacement   : %s (%s bytes)" % (replacement, f"{replacement.stat().st_size:,}"))

    print("\ninstall ONE of them into GAMEDATA\\MODS\\, not both.")
    print("remove: delete the folder. No save data is touched either way.")


if __name__ == "__main__":
    main()
