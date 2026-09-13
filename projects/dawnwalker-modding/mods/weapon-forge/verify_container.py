#!/usr/bin/env python3
"""Report which base-game packages a Dawnwalker IoStore mod container replaces.

Collision is the normal override mechanism, not a fault: a replacement mod is
*supposed* to collide. Measured on this install, `SkillsNoTimeCost` collides on
112 of its 113 chunks and `DualSenseAtlas` on 4 of 5 -- that is them working.

The question this tool answers is whether a container collides on what its author
*intended*. For an additive mod that only adds new assets, the correct answer is
zero, and anything above zero means the cook swept in files it should not ship.

IoStore resolves packages by chunk ID, and the chunk-ID table sits in the .utoc
header region in the clear -- it is NOT inside the encrypted directory index.
So this works on the encrypted base container with no AES key and no Oodle.

Standard library only. Python 3.

Usage
-----
    python verify_container.py <mod.utoc> [--base <Dawnwalker-Windows.utoc>]

Exit codes
----------
    0  no collisions
    1  collisions found (pass --expect-none to treat that as failure)
    2  could not read a file

A zero result does not mean the mod works, only that it adds rather than replaces.
See AUDIT-2026-09-09.md for the case that motivated this tool: a weapon mod that
should have had zero collisions and had 390.
"""

import argparse
import os
import struct
import sys
from collections import Counter

DEFAULT_BASE = (
    r"D:\steam\steamapps\common\The Blood of Dawnwalker"
    r"\Dawnwalker\Content\Paks\Dawnwalker-Windows.utoc"
)

MAGIC = b"-==--==--==--==-"

# IoStore chunk types we care about naming in output.
CHUNK_TYPES = {
    0: "Invalid",
    1: "ExportBundleData",
    2: "BulkData",
    3: "OptionalBulkData",
    4: "MemoryMappedBulkData",
    5: "ScriptObjects",
    6: "ContainerHeader",
    7: "ExternalFile",
    8: "ShaderCodeLibrary",
    9: "ShaderCode",
    10: "PackageStoreEntry",
}


def chunk_ids(path):
    """Return [(chunk_id, chunk_type), ...] for every entry in a .utoc."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:16] != MAGIC:
        raise ValueError("%s is not an IoStore .utoc" % os.path.basename(path))

    # Header: magic(16) version(1) pad(3) then 9 uint32s from offset 20.
    header_size, entry_count = struct.unpack_from("<2I", data, 20)

    offset = header_size
    out = []
    for _ in range(entry_count):
        raw = data[offset:offset + 12]
        offset += 12
        # 12-byte FIoChunkId: 8-byte id, 2-byte index (big endian), pad, type.
        out.append((struct.unpack_from("<Q", raw, 0)[0], raw[11]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mod", help="the mod .utoc to check")
    ap.add_argument("--base", default=DEFAULT_BASE,
                    help="base game .utoc (default: the standard Steam path)")
    ap.add_argument("--show", type=int, default=8,
                    help="how many colliding ids to print (default 8)")
    ap.add_argument("--expect-none", action="store_true",
                    help="for additive mods: treat any collision as a failure")
    args = ap.parse_args()

    try:
        mod = chunk_ids(args.mod)
        base = chunk_ids(args.base)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    print("base container : %-45s %8d chunks" % (os.path.basename(args.base), len(base)))
    print("mod container  : %-45s %8d chunks" % (os.path.basename(args.mod), len(mod)))

    base_set = set(base)
    collisions = [c for c in mod if c in base_set]

    print()
    if not collisions:
        print("RESULT: 0 collisions. This container only adds new packages.")
        print("        (It may still do nothing useful -- this only measures overrides.)")
        return 0

    pct = 100.0 * len(collisions) / len(mod)
    print("RESULT: %d of %d chunks (%.1f%%) replace base game packages."
          % (len(collisions), len(mod), pct))
    print()
    print("Containers in ~mods load after the base container, so these copies win.")
    if args.expect_none:
        print("--expect-none was set: for an additive mod this is a FAILURE.")
    else:
        print("For a replacement mod this is expected. For an additive mod that only")
        print("means to add new assets, every one of these is an accident.")
    print()
    by_type = Counter(t for _, t in collisions)
    print("by chunk type:")
    for t, n in by_type.most_common():
        print("    %-22s %d" % (CHUNK_TYPES.get(t, "type %d" % t), n))
    if args.show:
        print()
        print("first %d colliding ids:" % args.show)
        for cid, t in collisions[:args.show]:
            print("    0x%016x  %s" % (cid, CHUNK_TYPES.get(t, "type %d" % t)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
