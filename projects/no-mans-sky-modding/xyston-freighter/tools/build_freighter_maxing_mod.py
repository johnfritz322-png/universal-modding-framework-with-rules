"""Max the freighter's upgrade rolls and double its ship parking.

Two EXML partial patches, built from the live game tables so the targets are
verified rather than assumed:

1. `NMS_REALITY_GCPROCEDURALTECHNOLOGYTABLE` — for every `UP_FR*` entry, set each
   stat's `ValueMin` equal to its `ValueMax`. Procedural upgrade stats are rolled at
   runtime from this table using the seed stored in the save, so pinning the range
   makes **modules the player already owns** roll their maximum. No save edit and no
   seed hunting needed.

   Only `UP_FR*` is touched. Ship, multi-tool, exosuit and Corvette upgrades keep
   their normal ranges.

2. `GCFLEETGLOBALS` — `MaxNumberOfPlayerShipsInFreighterHangar`, which is what
   decides how many of your ships are parked in the freighter hangar.

Usage:
    python build_freighter_maxing_mod.py <proc_table.MXML> <fleet_globals.MXML> <out_dir>

Nothing here has been confirmed in game. NEEDS TESTING.
"""
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

PREFIX = "UP_FR"
PARKING_FIELD = "MaxNumberOfPlayerShipsInFreighterHangar"
PARKING_VALUE = 12          # vanilla is 6
MOD_NAME = "XystonFreighterMaxed"

PROC_PATH = "METADATA/REALITY/TABLES/NMS_REALITY_GCPROCEDURALTECHNOLOGYTABLE.EXML"
FLEET_PATH = "GLOBALS/GCFLEETGLOBALS.GLOBAL.EXML"


def prop(node, name):
    for child in node.findall("Property"):
        if child.get("name") == name:
            return child
    return None


def build_proc_patch(mxml_path):
    root = ET.parse(mxml_path).getroot()
    if root.get("template") != "cGcProceduralTechnologyTable":
        raise SystemExit("unexpected template: %s" % root.get("template"))
    table = prop(root, "Table")

    lines = ['<?xml version="1.0" encoding="utf-8"?>',
             "<!--Freighter upgrade modules always roll their maximum stat-->",
             '<Data template="cGcProceduralTechnologyTable">',
             '  <Property name="Table">']
    changed = []
    for entry in table.findall("Property"):
        pid = entry.get("_id") or ""
        if not pid.startswith(PREFIX):
            continue
        stat_levels = prop(entry, "StatLevels")
        if stat_levels is None:
            continue
        pinned = []
        for index, level in enumerate(stat_levels.findall("Property")):
            vmin, vmax = prop(level, "ValueMin"), prop(level, "ValueMax")
            if vmin is None or vmax is None:
                continue
            lo, hi = float(vmin.get("value")), float(vmax.get("value"))
            if lo == hi:
                continue                      # already fixed, nothing to gain
            stat = prop(prop(level, "Stat"), "StatsType").get("value")
            pinned.append((index, hi, stat, lo))
        if not pinned:
            continue
        lines.append('    <Property name="Table" value="GcProceduralTechnologyData" '
                     '_id="%s">' % pid)
        lines.append('      <Property name="StatLevels">')
        for index, hi, stat, lo in pinned:
            lines.append('        <Property name="StatLevels" '
                         'value="GcProceduralTechnologyStatLevel" _index="%d">' % index)
            lines.append('          <Property name="ValueMin" value="%.6f" />' % hi)
            lines.append('        </Property>')
            changed.append((pid, stat, lo, hi))
        lines.append("      </Property>")
        lines.append("    </Property>")
    lines += ["  </Property>", "</Data>", ""]
    return "\n".join(lines), changed


def build_fleet_patch(mxml_path):
    root = ET.parse(mxml_path).getroot()
    template = root.get("template")
    field = prop(root, PARKING_FIELD)
    if field is None:
        raise SystemExit("%s not found in %s" % (PARKING_FIELD, mxml_path))
    before = int(field.get("value"))
    text = "\n".join([
        '<?xml version="1.0" encoding="utf-8"?>',
        "<!--Double the ships parked in the freighter hangar-->",
        '<Data template="%s">' % template,
        '  <Property name="%s" value="%d" />' % (PARKING_FIELD, PARKING_VALUE),
        "</Data>",
        "",
    ])
    return text, before


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    proc_mxml, fleet_mxml, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]

    proc_text, changed = build_proc_patch(proc_mxml)
    fleet_text, parking_before = build_fleet_patch(fleet_mxml)

    base = Path(out_dir) / MOD_NAME
    for rel, text in ((PROC_PATH, proc_text), (FLEET_PATH, fleet_text)):
        target = base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        # a patch that will not parse is a patch the game cannot match
        ET.fromstring(text)
        print("wrote %-62s %5d bytes" % (rel, target.stat().st_size))

    print("\nship parking: %d -> %d" % (parking_before, PARKING_VALUE))
    print("stat rolls pinned to maximum: %d" % len(changed))
    by_module = {}
    for pid, stat, lo, hi in changed:
        by_module.setdefault(pid, []).append((stat, lo, hi))
    for pid in sorted(by_module):
        for stat, lo, hi in by_module[pid]:
            print("   %-11s %-42s %8.2f..%.2f -> %.2f" % (pid, stat, lo, hi, hi))


if __name__ == "__main__":
    main()
