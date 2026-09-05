# Reader/writer for legacy UE .pak archives (the format used by config/INI mods).
import struct, sys, os, hashlib, io

MAGIC = 0x5A6F12E1
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def read_pak(path):
    d = open(path, "rb").read()
    n = len(d)
    # Footer size depends on version; probe known layouts by locating the magic.
    for footer in (44, 45, 65, 205, 221, 224):
        off = n - footer
        if off < 0:
            continue
        if struct.unpack_from("<I", d, off)[0] == MAGIC:
            ver = struct.unpack_from("<I", d, off + 4)[0]
            idx_off, idx_size = struct.unpack_from("<QQ", d, off + 8)
            idx_hash = d[off + 24:off + 44]
            enc_guid, enc_idx = None, False
            break
        # versions >= 8 put EncryptionKeyGuid(16) + bEncryptedIndex(1) BEFORE the magic
        if off - 17 >= 0 and struct.unpack_from("<I", d, off)[0] != MAGIC:
            pass
    else:
        # search backwards for the magic
        pos = d.rfind(struct.pack("<I", MAGIC))
        if pos < 0:
            raise SystemExit("no pak magic found")
        off = pos
        ver = struct.unpack_from("<I", d, off + 4)[0]
        idx_off, idx_size = struct.unpack_from("<QQ", d, off + 8)
        idx_hash = d[off + 24:off + 44]
        enc_guid = d[off - 17:off - 1] if off >= 17 else None
        enc_idx = bool(d[off - 1]) if off >= 1 else False

    print(f"PAK   : {os.path.basename(path)} ({n:,} bytes)")
    print(f"  magic at 0x{off:x}  footer size {n-off}")
    print(f"  version      : {ver}")
    print(f"  index offset : {idx_off:,}   size {idx_size:,}   (ends {idx_off+idx_size:,})")
    print(f"  index sha1   : {idx_hash.hex()}")
    actual = hashlib.sha1(d[idx_off:idx_off + idx_size]).digest()
    print(f"  index hash OK: {actual == idx_hash}")

    idx = d[idx_off:idx_off + idx_size]
    r = io.BytesIO(idx)

    def fstr():
        (ln,) = struct.unpack("<i", r.read(4))
        if ln == 0:
            return ""
        if ln < 0:
            return r.read(-ln * 2).decode("utf-16-le").rstrip("\0")
        return r.read(ln).decode("utf-8", "replace").rstrip("\0")

    mount = fstr()
    (count,) = struct.unpack("<i", r.read(4))
    print(f"  mount point  : {mount}")
    print(f"  file count   : {count}")
    entries = []
    for i in range(count):
        name = fstr()
        e_off, e_size, e_usize = struct.unpack("<QQQ", r.read(24))
        (e_cm,) = struct.unpack("<I", r.read(4))
        e_hash = r.read(20)
        if e_cm != 0:
            (nblocks,) = struct.unpack("<i", r.read(4))
            r.read(nblocks * 16)
        enc = r.read(1)[0]
        (blocksize,) = struct.unpack("<I", r.read(4))
        entries.append(dict(name=name, offset=e_off, size=e_size, usize=e_usize,
                            method=e_cm, encrypted=bool(enc)))
        print(f"    [{i}] {name}")
        print(f"        offset={e_off:,} size={e_size:,} uncompressed={e_usize:,} "
              f"method={e_cm} encrypted={bool(enc)}")
    return dict(version=ver, mount=mount, entries=entries, data=d)


def extract_pak(path, outdir):
    p = read_pak(path)
    d = p["data"]
    os.makedirs(outdir, exist_ok=True)
    for e in p["entries"]:
        # Re-read the per-file header that precedes the payload.
        o = e["offset"]
        h_off, h_size, h_usize = struct.unpack_from("<QQQ", d, o)
        (h_cm,) = struct.unpack_from("<I", d, o + 24)
        hdr = 24 + 4 + 20
        if h_cm != 0:
            nb = struct.unpack_from("<i", d, o + hdr)[0]
            hdr += 4 + nb * 16
        hdr += 1 + 4
        payload = d[o + hdr: o + hdr + e["size"]]
        dest = os.path.join(outdir, e["name"].replace("/", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(payload)
        print(f"  -> {dest}  ({len(payload):,} bytes)")


if __name__ == "__main__":
    if sys.argv[1] == "x":
        extract_pak(sys.argv[2], sys.argv[3])
    else:
        read_pak(sys.argv[1])
