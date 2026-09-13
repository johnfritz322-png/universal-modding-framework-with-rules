#!/usr/bin/env python3
"""Extract one file out of Dawnwalker's encrypted legacy .pak.

Needed for AssetRegistry.bin and the Config/*.ini files, which live in the .pak
rather than the IoStore container and so are invisible to utoc-based tooling.

    python pak_extract.py Dawnwalker/AssetRegistry.bin out.bin

Two traps, both of which produce convincing garbage if missed:

1. In the encoded entry table, a block-size field of 0x3f is an ESCAPE - a real
   uint32 block size follows before the offset. Miss it and every subsequent
   field shifts by four bytes, yielding a plausible-looking offset that is
   actually the block size.
2. The duplicated FPakEntry header at the data offset is PLAINTEXT even when the
   payload is encrypted, and it carries absolute block start/end pairs. Read the
   block table from there rather than rebuilding it from the encoded entry.
"""
import io, json, os, re, struct, sys
from Crypto.Cipher import AES
from iostore_read import oodle_decompress

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


def entry_offset(f, key, wanted):
    """Walk the encrypted indexes to find a file's data offset."""
    size = os.path.getsize(PAK)
    f.seek(size - 1024); tail = f.read()
    pos = [i for i in range(len(tail) - 4) if tail[i:i + 4] == MAGIC]
    f.seek(size - 1024 + pos[-1])
    struct.unpack("<II", f.read(8))
    idx_off, idx_size = struct.unpack("<QQ", f.read(16))
    f.read(20); encrypted = f.read(1)[0]
    f.seek(idx_off); blob = f.read(idx_size)
    dec = AES.new(key, AES.MODE_ECB).decrypt(blob) if encrypted else blob
    _mount, o = fstr(dec, 0)
    o += 4 + 8
    o = o + 4 + 16 + 20 if struct.unpack_from("<i", dec, o)[0] else o + 4
    if not struct.unpack_from("<i", dec, o)[0]:
        raise RuntimeError("pak has no full directory index")
    o += 4
    fd_off, fd_size = struct.unpack_from("<2q", dec, o); o += 16 + 20
    enc_size = struct.unpack_from("<i", dec, o)[0]; o += 4
    encoded = dec[o:o + enc_size]

    f.seek(fd_off); raw = f.read(fd_size)
    fd = AES.new(key, AES.MODE_ECB).decrypt(raw) if encrypted else raw
    q = 0; ndirs = struct.unpack_from("<i", fd, q)[0]; q += 4
    slot = None
    for _ in range(ndirs):
        dname, q = fstr(fd, q)
        nfiles = struct.unpack_from("<i", fd, q)[0]; q += 4
        for _ in range(nfiles):
            fname, q = fstr(fd, q)
            idx = struct.unpack_from("<I", fd, q)[0]; q += 4
            if dname + fname == wanted:
                slot = idx
    if slot is None:
        raise KeyError(wanted)

    p = slot
    v = struct.unpack_from("<I", encoded, p)[0]; p += 4
    if (v & 0x3f) == 0x3f:            # escape - real block size follows
        p += 4
    def rd(safe):
        nonlocal p
        r = struct.unpack_from("<I" if safe else "<Q", encoded, p)[0]
        p += 4 if safe else 8
        return r
    return rd((v >> 31) & 1)


def extract(wanted):
    key = aes_key()
    with open(PAK, "rb") as f:
        data_off = entry_offset(f, key, wanted)
        f.seek(data_off); head = f.read(1024)
        _o, _size, usize = struct.unpack_from("<3q", head, 0)
        nblocks = struct.unpack_from("<i", head, 48)[0]
        blocks = [struct.unpack_from("<2q", head, 52 + i * 16) for i in range(nblocks)]
        tail_o = 52 + nblocks * 16
        flags = head[tail_o]
        block_size = struct.unpack_from("<I", head, tail_o + 1)[0]
        encrypted = bool(flags & 1)

        out = bytearray()
        for start, end in blocks:
            clen = end - start
            padded = (clen + 15) // 16 * 16
            f.seek(start); raw = f.read(padded)
            if encrypted:
                raw = AES.new(key, AES.MODE_ECB).decrypt(raw)
            out += oodle_decompress(bytes(raw[:clen]), min(block_size, usize - len(out)))
    if len(out) != usize:
        raise RuntimeError("got %d bytes, expected %d" % (len(out), usize))
    return bytes(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    blob = extract(sys.argv[1])
    open(sys.argv[2], "wb").write(blob)
    print("wrote %s (%d bytes)" % (sys.argv[2], len(blob)), file=sys.stderr)
