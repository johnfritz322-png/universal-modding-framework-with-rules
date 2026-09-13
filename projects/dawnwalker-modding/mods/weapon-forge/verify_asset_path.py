#!/usr/bin/env python3
"""Prove whether a package path exists in a Dawnwalker IoStore container.

Needs NO AES key and NO Oodle. IoStore derives a package's chunk id from a
CityHash64 of the lowercased package name in UTF-16LE, and the chunk-id table
sits in the .utoc outside the encrypted directory index. So you can confirm or
refute a claimed asset path without decrypting anything.

What this proves: that a package with that exact name exists in the container.
What it does NOT prove: anything about the package's *contents* -- component
names, mesh assignments, transforms, socket positions. Those need decryption
and Oodle. Do not let a FOUND result be read as verification of internals.

Usage
-----
    python verify_asset_path.py /Game/_Dawnwalker/Player/BP_PlayerCharacter
    python verify_asset_path.py --file paths.txt
    python verify_asset_path.py --utoc <other.utoc> /Game/...

Always include a deliberately fake path as a control; it must come back absent.

Git Bash trap: a bare /Game/... argument gets rewritten into a Windows path by
MSYS path conversion, and every lookup silently comes back absent. Either prefix
the command with MSYS_NO_PATHCONV=1 or use --file, as example-paths.txt does.
"""

import argparse
import struct
import sys

from cityhash64 import package_id

DEFAULT_UTOC = (
    r"D:\steam\steamapps\common\The Blood of Dawnwalker"
    r"\Dawnwalker\Content\Paks\Dawnwalker-Windows.utoc"
)

EXPORT_BUNDLE_DATA = 1


def chunk_set(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:16] != b"-==--==--==--==-":
        raise ValueError("not an IoStore .utoc: %s" % path)
    header_size, entry_count = struct.unpack_from("<2I", data, 20)
    offset = header_size
    out = set()
    for _ in range(entry_count):
        raw = data[offset:offset + 12]
        offset += 12
        out.add((struct.unpack_from("<Q", raw, 0)[0], raw[11]))
    return out, entry_count


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="package paths, e.g. /Game/Foo/Bar")
    ap.add_argument("--utoc", default=DEFAULT_UTOC, help="container to search")
    ap.add_argument("--file", help="read paths from a file, one per line")
    args = ap.parse_args()

    paths = list(args.paths)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            paths += [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]
    if not paths:
        ap.error("give at least one package path")

    try:
        chunks, count = chunk_set(args.utoc)
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    print("container: %s (%d chunks)" % (args.utoc, count))
    print()
    print("%-8s %-18s %s" % ("RESULT", "CHUNK ID", "PACKAGE PATH"))
    print("-" * 100)
    missing = 0
    for p in paths:
        pid = package_id(p)
        found = (pid, EXPORT_BUNDLE_DATA) in chunks
        missing += not found
        print("%-8s 0x%016x  %s" % ("FOUND" if found else "absent", pid, p))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
