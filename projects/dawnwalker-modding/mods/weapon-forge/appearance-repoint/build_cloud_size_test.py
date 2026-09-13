#!/usr/bin/env python3
"""Build a one-weapon, highly visible greatsword appearance test.

This changes only the Vrakhir row in ``DT_WeaponAppearances.uexp``.  It maps
the existing Vrakhir item to the retail game's ``L_Sword_NPC_50`` greatsword
and its matching scabbard.  The model is an existing game asset, so this does
not import new geometry, patch a save, or add an inventory item.

The script is deliberately separate from the normal two-sword build.  It only
accepts a clean ``retoc to-legacy`` extraction, copies it to a new directory,
and refuses to write unless the current Vrakhir row is found exactly once with
the verified retail source values.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from build_visual_loadout import (
    TABLE_RELATIVE,
    TABLE_STEM,
    find_unique,
    pair,
    read_name_indices,
    sha256,
    write_name_indices,
)


# These FName indices are from the current retail DT_WeaponAppearances name map.
# They were read from the decrypted current-game table, not inferred from names.
MAPPING = {
    "label": "The Vrakhir — giant greatsword visibility test",
    "row_name": "ITM_Weapon_SwordVampiric1a",
    "row_index": 523,
    "source": (103, 583, 104, 584),
    "target": (99, 529, 100, 580),
    "target_blade": "L_Sword_NPC_50",
    "target_scabbard": "L_Sword_NPC_50_Scabbard",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_legacy", type=Path, help="clean retoc to-legacy directory")
    parser.add_argument("output_legacy", type=Path, help="new directory to create")
    args = parser.parse_args()

    input_root = args.input_legacy.resolve()
    output_root = args.output_legacy.resolve()
    if not input_root.is_dir():
        parser.error("input directory does not exist: %s" % input_root)
    if output_root.exists():
        parser.error("output directory already exists; refusing to overwrite: %s" % output_root)
    if not (input_root / "scriptobjects.bin").is_file():
        parser.error("scriptobjects.bin is required in the input directory")

    input_uexp = input_root / TABLE_RELATIVE / (TABLE_STEM + ".uexp")
    input_uasset = input_root / TABLE_RELATIVE / (TABLE_STEM + ".uasset")
    if not input_uexp.is_file() or not input_uasset.is_file():
        parser.error("clean DT_WeaponAppearances .uasset and .uexp are required")

    original = input_uexp.read_bytes()
    row_offset = find_unique(original, pair(MAPPING["row_index"]), MAPPING["row_name"])
    found = read_name_indices(original, row_offset)
    if found != MAPPING["source"]:
        raise ValueError(
            "%s source indices differ: expected %r, found %r"
            % (MAPPING["row_name"], MAPPING["source"], found)
        )

    shutil.copytree(input_root, output_root)
    output_uexp = output_root / TABLE_RELATIVE / (TABLE_STEM + ".uexp")
    patched = bytearray(original)
    write_name_indices(patched, row_offset, MAPPING["target"])
    if read_name_indices(patched, row_offset) != MAPPING["target"]:
        raise AssertionError("post-write verification failed for Vrakhir")
    output_uexp.write_bytes(patched)

    manifest = {
        "format": 1,
        "purpose": "one-row giant-greatsword visual test; not a custom Cloud model or inventory-item mod",
        "input_uexp_sha256": sha256(input_uexp),
        "output_uexp_sha256": sha256(output_uexp),
        "change": {
            "weapon": MAPPING["label"],
            "row": MAPPING["row_name"],
            "row_offset": row_offset,
            "source_indices": MAPPING["source"],
            "target_indices": MAPPING["target"],
            "target_blade": MAPPING["target_blade"],
            "target_scabbard": MAPPING["target_scabbard"],
        },
    }
    (output_root / "cloud-size-test-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, AssertionError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(2)
