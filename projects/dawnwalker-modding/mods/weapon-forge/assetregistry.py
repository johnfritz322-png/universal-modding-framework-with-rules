#!/usr/bin/env python3
"""Parse Dawnwalker's cooked AssetRegistry.bin — header and name table.

This is the foundation for an AssetRegistry override. It reads the parts that
are fully understood; the body is mapped but not yet parsed. See
REGISTRY-OVERRIDE-PROGRESS-2026-09-12.md for what remains.

    python assetregistry.py                 # summary
    python assetregistry.py SwordGreat      # find names matching a substring

Layout as measured on build 25232147 (5,426,463 bytes):

    +0      16  version GUID   e79e7f713a49b0e93291b3880781381b
    +16      4  version        17
    +20      4  bFilterEditorOnlyData = 1
    +24      4  name count       = 40,908
    +28      4  name string bytes = 2,090,524
    +32      8  hash version     = 0x00000000c1640000
    +40         name hashes      (count * 8)
    ...         name headers     (count * 2)  - bit 15 = UTF-16, low 15 = length
    ...         name strings     (string bytes)
    2,499,644   BODY: fixed tag store, magic 0x12345679, then asset entries
                and the dependency graph. NOT yet parsed.

Name table verified byte-exact: strings consume 2,090,524 of 2,090,524.
"""
import os
import struct
import sys

DEFAULT = os.path.join(os.environ.get("TEMP", "."), "AssetRegistry.bin")
STORE_MAGIC = 0x12345679


class AssetRegistry:
    def __init__(self, data):
        self.data = data
        self.guid = data[:16]
        self.version = struct.unpack_from("<i", data, 16)[0]
        self.filter_editor_only = struct.unpack_from("<I", data, 20)[0]
        count, string_bytes = struct.unpack_from("<2I", data, 24)
        self.name_count = count
        self.name_string_bytes = string_bytes
        self.hash_version = struct.unpack_from("<Q", data, 32)[0]

        p = 40 + count * 8                      # skip hashes
        headers = []
        for _ in range(count):
            b0, b1 = data[p], data[p + 1]
            p += 2
            headers.append((bool(b0 & 0x80), ((b0 & 0x7F) << 8) | b1))
        start = p
        self.names = []
        for is_utf16, length in headers:
            if is_utf16:
                self.names.append(data[p:p + length * 2].decode("utf-16-le", "replace"))
                p += length * 2
            else:
                self.names.append(data[p:p + length].decode("utf-8", "replace"))
                p += length
        consumed = p - start
        if consumed != string_bytes:
            raise ValueError("name strings consumed %d, header says %d" % (consumed, string_bytes))
        self.body_offset = p
        self.body_magic = struct.unpack_from("<I", data, p)[0]

    def find(self, needle):
        low = needle.lower()
        return [(i, n) for i, n in enumerate(self.names) if low in n.lower()]


def main():
    path = DEFAULT
    if not os.path.exists(path):
        print("extract it first:\n"
              "  python -c \"from pak_extract import extract;"
              " open(r'%s','wb').write(extract('Dawnwalker/AssetRegistry.bin'))\"" % path,
              file=sys.stderr)
        return 2
    r = AssetRegistry(open(path, "rb").read())
    print("version        : %d" % r.version)
    print("names          : %d  (%d string bytes, verified exact)"
          % (r.name_count, r.name_string_bytes))
    print("body offset    : %d  magic 0x%08x %s"
          % (r.body_offset, r.body_magic,
             "(fixed tag store)" if r.body_magic == STORE_MAGIC else "(UNEXPECTED)"))
    print("body size      : %d bytes - not yet parsed" % (len(r.data) - r.body_offset))
    if len(sys.argv) > 1:
        print()
        for i, n in r.find(sys.argv[1])[:20]:
            print("  [%d] %s" % (i, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
