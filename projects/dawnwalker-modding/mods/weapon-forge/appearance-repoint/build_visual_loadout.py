#!/usr/bin/env python3
"""Build the verified two-sword visual loadout from a clean legacy table copy.

This changes only four FName references in ``DT_WeaponAppearances.uexp``:

* The Vrakhir -> L_Sword_Unique_01 (+ matching scabbard)
* Imbued Sword of St. Mihai -> M_Sword_Ancient_Hero_01 (+ matching scabbard)

It intentionally creates a *replacement appearance* mod.  It does not add an
inventory item, edit a save, or modify any game file.  The input directory must
be a clean ``retoc to-legacy`` extraction containing ``scriptobjects.bin``.

The script refuses to patch unless the row identifier and all four expected
source FName indices are found exactly where the verified serialization places
them.  It copies the input to a new output directory; it never changes input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import sys
from pathlib import Path


TABLE_RELATIVE = Path("Dawnwalker/Content/_Dawnwalker/Inventory/Items")
TABLE_STEM = "DT_WeaponAppearances"

# All indices are from the current retail table's own FName map, independently
# verified against the decrypted package by dump_weapon_appearances.py.
MAPPINGS = (
    {
        "label": "The Vrakhir",
        "row_name": "ITM_Weapon_SwordVampiric1a",
        "row_index": 523,
        "source": (103, 583, 104, 584),
        "target": (101, 581, 102, 582),
        "target_blade": "L_Sword_Unique_01",
        "target_scabbard": "L_Sword_Unique_01_Scabbard",
    },
    {
        "label": "Imbued Sword of St. Mihai",
        "row_name": "ITM_Weapon_SwordDawnwalker5a",
        "row_index": 360,
        "source": (210, 657, 211, 658),
        "target": (105, 585, 106, 586),
        "target_blade": "M_Sword_Ancient_Hero_01",
        "target_scabbard": "M_Sword_Ancient_Hero_01_Scabbard",
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pair(value: int) -> bytes:
    return struct.pack("<II", value, 0)


def find_unique(data: bytes, needle: bytes, description: str) -> int:
    positions = []
    start = 0
    while True:
        position = data.find(needle, start)
        if position < 0:
            break
        positions.append(position)
        start = position + 1
    if len(positions) != 1:
        raise ValueError("%s must occur exactly once; found %d" % (description, len(positions)))
    return positions[0]


def read_name_indices(data: bytes, offset: int) -> tuple[int, int, int, int]:
    # In this table's verified WeaponAppearance row layout the row FName is
    # followed by a 10-byte property marker.  The four FName indices are at
    # +10, +18, +30 and +38; each index has a zero FName-number field.
    fields = (offset + 10, offset + 18, offset + 30, offset + 38)
    values = []
    for field in fields:
        index, number = struct.unpack_from("<II", data, field)
        if number != 0:
            raise ValueError("unexpected non-zero FName number at offset %d" % field)
        values.append(index)
    return tuple(values)


def write_name_indices(data: bytearray, offset: int, values: tuple[int, int, int, int]) -> None:
    for field, value in zip((offset + 10, offset + 18, offset + 30, offset + 38), values):
        struct.pack_into("<II", data, field, value, 0)


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
    placements = []
    for mapping in MAPPINGS:
        row_offset = find_unique(original, pair(mapping["row_index"]), mapping["row_name"])
        found = read_name_indices(original, row_offset)
        if found != mapping["source"]:
            raise ValueError(
                "%s source indices differ: expected %r, found %r" %
                (mapping["row_name"], mapping["source"], found)
            )
        placements.append((mapping, row_offset))

    shutil.copytree(input_root, output_root)
    output_uexp = output_root / TABLE_RELATIVE / (TABLE_STEM + ".uexp")
    patched = bytearray(original)
    for mapping, row_offset in placements:
        write_name_indices(patched, row_offset, mapping["target"])
        if read_name_indices(patched, row_offset) != mapping["target"]:
            raise AssertionError("post-write verification failed for %s" % mapping["row_name"])
    output_uexp.write_bytes(patched)

    manifest = {
        "format": 1,
        "purpose": "verified visual replacement loadout; not an inventory-item mod",
        "input_uexp_sha256": sha256(input_uexp),
        "output_uexp_sha256": sha256(output_uexp),
        "changes": [
            {
                "weapon": mapping["label"],
                "row": mapping["row_name"],
                "row_offset": row_offset,
                "source_indices": mapping["source"],
                "target_indices": mapping["target"],
                "target_blade": mapping["target_blade"],
                "target_scabbard": mapping["target_scabbard"],
            }
            for mapping, row_offset in placements
        ],
    }
    (output_root / "visual-loadout-manifest.json").write_text(
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
