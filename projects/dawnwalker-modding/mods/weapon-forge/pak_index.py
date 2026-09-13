#!/usr/bin/env python3
"""List files inside Dawnwalker's encrypted legacy .pak.

Config .ini files and AssetRegistry.bin live in the .pak, NOT the IoStore .utoc,
so they are invisible to utoc-based tooling. This decrypts the pak's primary
index and full directory index (AES-256-ECB, same key as the containers) and
prints the paths.

    python pak_index.py                    # every path
    python pak_index.py assetregistry      # filter, case-insensitive regex
"""
import io, json, os, re, struct, sys
from Crypto.Cipher import AES

PAK = (r"D:\steam\steamapps\common\The Blood of Dawnwalker"
       r"\Dawnwalker\Content\Paks\Dawnwalker-Windows.pak")
MAGIC = b"\xe1\x12\x6f\x5a"


def aes_key():
    cfg = json.load(io.open(os.path.expandvars(r"%APPDATA%\FModel\AppSettings.json"),
                            encoding="utf-8"))
    return bytes.fromhex(sorted(set(re.findall(r"0x([0-9A-Fa-f]{64})", json.dumps(cfg))))[0])


def fstr(b, o):
    n = struct.unpack_from("<i", b, o)[0]; o += 4
    if n == 0:
        return "", o
    if n < 0:
        return b[o:o - 2 * n - 2].decode("utf-16-le", "replace"), o - 2 * n
    return b[o:o + n - 1].decode("utf-8", "replace"), o + n


def main():
    pattern = sys.argv[1] if len(sys.argv) > 1 else None
    key = aes_key()
    size = os.path.getsize(PAK)
    with open(PAK, "rb") as f:
        f.seek(size - 1024)
        tail = f.read()
        pos = [i for i in range(len(tail) - 4) if tail[i:i + 4] == MAGIC]
        if not pos:
            print("no pak footer magic found", file=sys.stderr); return 2
        f.seek(size - 1024 + pos[-1])
        _magic, ver = struct.unpack("<II", f.read(8))
        idx_off, idx_size = struct.unpack("<QQ", f.read(16))
        f.read(20)                      # index sha1
        encrypted = f.read(1)[0]

        f.seek(idx_off)
        blob = f.read(idx_size)
        dec = AES.new(key, AES.MODE_ECB).decrypt(blob[:len(blob) // 16 * 16]) if encrypted else blob

        mount, o = fstr(dec, 0)
        count = struct.unpack_from("<i", dec, o)[0]; o += 4
        o += 8                          # path hash seed
        if struct.unpack_from("<i", dec, o)[0]:
            o += 4 + 16 + 20            # path hash index: offset, size, hash
        else:
            o += 4
        if not struct.unpack_from("<i", dec, o)[0]:
            print("pak has no full directory index", file=sys.stderr); return 2
        o += 4
        fd_off, fd_size = struct.unpack_from("<2q", dec, o)

        print("pak v%d  mount %r  %d entries" % (ver, mount, count), file=sys.stderr)
        f.seek(fd_off)
        raw = f.read(fd_size)
        fd = AES.new(key, AES.MODE_ECB).decrypt(raw[:len(raw) // 16 * 16]) if encrypted else raw

    q = 0
    ndirs = struct.unpack_from("<i", fd, q)[0]; q += 4
    rx = re.compile(pattern, re.I) if pattern else None
    shown = 0
    for _ in range(ndirs):
        dname, q = fstr(fd, q)
        nfiles = struct.unpack_from("<i", fd, q)[0]; q += 4
        for _ in range(nfiles):
            fname, q = fstr(fd, q)
            q += 4                      # index into the encoded entry table
            full = dname + fname
            if rx is None or rx.search(full):
                print(full); shown += 1
    print("%d path(s)" % shown, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
