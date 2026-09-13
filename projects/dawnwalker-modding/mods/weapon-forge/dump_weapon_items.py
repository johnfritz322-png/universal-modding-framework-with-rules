#!/usr/bin/env python3
"""Read and verify Dawnwalker's weapon item data assets.

This tool reads the encrypted base archive only.  It neither writes to the
game nor creates a mod.  Each decoded item must consume its export payload
except for the observed four-byte zero trailer; any other size is reported as
a decode failure and causes a non-zero exit.

    python dump_weapon_items.py > weapon_items.csv
"""

import argparse
import csv
import struct
import sys
from pathlib import Path

from cityhash64 import package_id
from dump_weapon_appearances import DEFAULT_USMAP, package_names
from iostore_read import open_base
from unversioned import Decoder, Reader
from usmap import Usmap


def export_payload(data):
    header_size = struct.unpack_from("<I", data, 4)[0]
    export_map_offset = struct.unpack_from("<i", data, 32)[0]
    serial_offset, serial_size = struct.unpack_from("<2Q", data, export_map_offset)
    return header_size + serial_offset, serial_size


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--usmap", default=DEFAULT_USMAP)
    ap.add_argument("--item", action="append", dest="items",
                    help="short item filename, e.g. ITM_Weapon_SwordGreatMaster1a")
    args = ap.parse_args()

    # Keep the default scope grounded in the already verified appearance map.
    if args.items:
        items = args.items
    else:
        source = Path(__file__).with_name("weapon_appearances.csv")
        with source.open(newline="", encoding="utf-8") as fh:
            items = [row["Item"] for row in csv.DictReader(fh)]

    base = open_base()
    mappings = Usmap(args.usmap)
    fields = ["Package", "ItemId", "WeaponType", "WeaponBlueprint",
              "Weapon_Damage_Min", "Weapon_Damage_Max", "ItemRarity",
              "ItemMaterial", "ItemWeight", "SellCost", "BuyCost", "ItemImage"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    decoded = missing = failed = 0

    for item in items:
        path = "/Game/_Dawnwalker/Inventory/Items/" + item
        data = base.read_chunk(package_id(path))
        if data is None:
            missing += 1
            print("missing package: " + item, file=sys.stderr)
            continue
        start, size = export_payload(data)
        reader = Reader(data, start)
        try:
            values = Decoder(mappings, package_names(data)).props(reader, "ItemWeaponDataAsset")
            used = reader.o - start
            # All 191 present packages in the appearance-map test set leave the
            # same four-byte all-zero trailer.  Do not silently accept any other
            # offset: that would hide a bad schema or a game-format change.
            if used != size - 4 or data[reader.o:start + size] != b"\0\0\0\0":
                raise ValueError("consumed %d of %d bytes" % (used, size))
        except Exception as exc:
            failed += 1
            print("decode failed for %s: %s" % (item, exc), file=sys.stderr)
            continue
        values["Package"] = item
        writer.writerow({field: values.get(field, "") for field in fields})
        decoded += 1

    print("decoded %d; missing %d; failed %d" % (decoded, missing, failed), file=sys.stderr)
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
