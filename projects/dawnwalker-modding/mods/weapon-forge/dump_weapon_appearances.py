#!/usr/bin/env python3
"""Dump Dawnwalker's item -> weapon-mesh mapping from DT_WeaponAppearances.

Reads the encrypted base archive directly (AES + Oodle), then decodes the
DataTable's rows using the .usmap schema. Output is CSV on stdout:

    Item,WeaponMesh,ScabbardMesh

Verified byte-exact: 206 of 206 rows consume exactly 10,939 of 10,939 export
bytes, so nothing is being skipped or misaligned.

    python dump_weapon_appearances.py > weapon_appearances.csv
"""

import argparse
import csv
import struct
import sys

from cityhash64 import package_id
from iostore_read import open_base
from unversioned import Decoder, Reader
from usmap import Usmap

TABLE = "/Game/_Dawnwalker/Inventory/Items/DT_WeaponAppearances"
DEFAULT_USMAP = r"C:\Users\johnf\Downloads\Dawnwalker.usmap"


def package_names(data):
    """The package's own name map — export data indexes into this."""
    p = 52
    count, _strbytes = struct.unpack_from("<2I", data, p)
    p += 8 + 8 + count * 8
    headers = []
    for _ in range(count):
        b0, b1 = data[p], data[p + 1]
        p += 2
        headers.append((bool(b0 & 0x80), ((b0 & 0x7F) << 8) | b1))
    names = []
    for is_utf16, length in headers:
        if is_utf16:
            names.append(data[p:p + length * 2].decode("utf-16-le", "replace"))
            p += length * 2
        else:
            names.append(data[p:p + length].decode("utf-8", "replace"))
            p += length
    return names


def strip(path):
    if not path or path == "None":
        return ""
    return path.split(".")[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--usmap", default=DEFAULT_USMAP)
    args = ap.parse_args()

    data = open_base().read_chunk(package_id(TABLE))
    if data is None:
        print("error: %s not found in the base container" % TABLE, file=sys.stderr)
        return 2
    header_size = struct.unpack_from("<I", data, 4)[0]
    export_map_off = struct.unpack_from("<i", data, 32)[0]
    # Trust the export map's declared size. The chunk carries a few trailing
    # bytes past the export, so len(data) is NOT the right yardstick.
    exp_off, exp_size = struct.unpack_from("<2Q", data, export_map_off)

    dec = Decoder(Usmap(args.usmap), package_names(data))
    r = Reader(data, header_size + exp_off)
    dec.props(r, "DataTable")     # the table object itself (RowStruct)
    r.i32()                       # gap between the object's properties and the rows
    num_rows = r.i32()

    rows = {}
    for _ in range(num_rows):
        name = dec.name(r)
        rows[name] = dec.props(r, "WeaponAppearance")

    used = r.o - (header_size + exp_off)
    expected = exp_size
    if used != expected:
        print("warning: consumed %d of %d export bytes - decode may be misaligned"
              % (used, expected), file=sys.stderr)

    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(["Item", "WeaponMesh", "ScabbardMesh"])
    for k in sorted(rows):
        w.writerow([k, strip(rows[k].get("WeaponMesh")), strip(rows[k].get("ScabbardMesh"))])
    print("decoded %d rows, %d/%d bytes" % (len(rows), used, expected), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
