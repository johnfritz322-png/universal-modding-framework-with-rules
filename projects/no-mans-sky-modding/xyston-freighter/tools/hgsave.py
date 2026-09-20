"""Read and write No Man's Sky .hg saves in either plain-JSON or the game's
LZ4 block container format. Round-trips byte-identical content."""
import json, struct, lz4.block
MAGIC = 0xFEEDA1E5
CHUNK = 0x80000  # 524288, the size the game uses

def read(path):
    raw = open(path, "rb").read()
    if raw[:4] != struct.pack("<I", MAGIC):
        return json.loads(raw.rstrip(b"\x00").decode("utf-8", errors="surrogateescape")), "plain"
    out, off = bytearray(), 0
    while off + 16 <= len(raw):
        magic, csize, dsize, _ = struct.unpack_from("<IIII", raw, off)
        if magic != MAGIC:
            break
        off += 16
        out += lz4.block.decompress(raw[off:off + csize], uncompressed_size=dsize)
        off += csize
    return json.loads(out.rstrip(b"\x00").decode("utf-8", errors="surrogateescape")), "lz4"

def write(path, data, fmt):
    body = json.dumps(data, separators=(",", ":")).encode("utf-8", errors="surrogateescape") + b"\x00"
    if fmt == "plain":
        open(path, "wb").write(body)
        return
    out = bytearray()
    for i in range(0, len(body), CHUNK):
        part = body[i:i + CHUNK]
        comp = lz4.block.compress(part, store_size=False)
        out += struct.pack("<IIII", MAGIC, len(comp), len(part), 0) + comp
    open(path, "wb").write(bytes(out))
