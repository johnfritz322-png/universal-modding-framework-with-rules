"""Read one package out of Dawnwalker's encrypted + Oodle IoStore container.

This closes the gap the format notes recorded as a hard blocker. Two pieces:

AES  - the key already configured in FModel's AppSettings.json. Verified valid on
       build 258042. Blocks are AES-256-**ECB**.
Oodle- Epic ships a signed oo2core_9_win64.dll inside Unreal Engine itself. Use
       that one, NOT the unsigned copy FModel downloads into its .data folder.
       Signature checked: "Epic Games Inc.", status Valid.

    from iostore_read import open_base
    from cityhash64 import package_id
    data = open_base().read_chunk(package_id("/Game/Some/Package"))

What this gives you is the raw cooked package: header, name map, import/export
maps. The name map alone answers a lot -- every asset a package references shows
up there as a readable string.

What it does NOT give you is decoded property *values*. Cooked UE5 packages use
unversioned property serialization, so row and field contents need the .usmap
schema applied on top. Reading a DataTable's actual rows still needs that step or
FModel. Do not guess row contents from byte patterns; index 0 decodes to the first
name in the map and will happily produce convincing nonsense.
"""
import ctypes, json, io, re, struct, os
from Crypto.Cipher import AES
from cityhash64 import package_id

OODLE = r"D:\UE55\UE_5.5\Engine\Binaries\DotNET\AutomationTool\AutomationScripts\BuildGraph\oo2core_9_win64.dll"
PAKS = r"D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks"

_lib = None
def _oodle():
    global _lib
    if _lib is None:
        _lib = ctypes.CDLL(OODLE)
        _lib.OodleLZ_Decompress.restype = ctypes.c_int64
        _lib.OodleLZ_Decompress.argtypes = [
            ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64,
            ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
            ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_int64, ctypes.c_int32]
    return _lib

def oodle_decompress(src, out_size):
    lib = _oodle()
    dst = ctypes.create_string_buffer(out_size)
    n = lib.OodleLZ_Decompress(src, len(src), dst, out_size,
                               1, 0, 0, None, 0, None, None, None, 0, 3)
    if n != out_size:
        raise RuntimeError("Oodle returned %d, expected %d" % (n, out_size))
    return dst.raw[:out_size]

def aes_key():
    cfg = json.load(io.open(os.path.expandvars(r"%APPDATA%\FModel\AppSettings.json"), encoding="utf-8"))
    return bytes.fromhex(sorted(set(re.findall(r'0x([0-9A-Fa-f]{64})', json.dumps(cfg))))[0])

class Container:
    def __init__(self, utoc):
        d = open(utoc, "rb").read()
        self.ucas = utoc[:-5] + ".ucas"
        ver = d[16]
        (hdr, cnt, cb, cbs, cm, cml, self.blocksize, dirsz, parts) = struct.unpack_from("<9I", d, 20)
        self.flags = d[80]
        seed = struct.unpack_from("<I", d, 84)[0]
        wo = struct.unpack_from("<I", d, 96)[0]
        o = hdr
        self.ids = {}
        for i in range(cnt):
            raw = d[o:o+12]; o += 12
            self.ids[(struct.unpack_from("<Q", raw, 0)[0], raw[11])] = i
        self.offlen = []
        for i in range(cnt):
            raw = d[o:o+10]; o += 10
            self.offlen.append((int.from_bytes(raw[0:5], "big"), int.from_bytes(raw[5:10], "big")))
        if ver >= 4:
            o += seed*4 + wo*4
        self.blocks = []
        for i in range(cb):
            raw = d[o:o+12]; o += 12
            self.blocks.append((int.from_bytes(raw[0:5], "little"),
                                int.from_bytes(raw[5:8], "little"),
                                int.from_bytes(raw[8:11], "little"),
                                raw[11]))
        self.methods = ["None"]
        for i in range(cm):
            self.methods.append(d[o:o+cml].rstrip(b"\0").decode()); o += cml
        self.key = aes_key() if (self.flags & 2) else None

    def read_chunk(self, cid, ctype=1):
        idx = self.ids.get((cid, ctype))
        if idx is None:
            return None
        off, length = self.offlen[idx]
        first = off // self.blocksize
        out = b""
        with open(self.ucas, "rb") as fh:
            b = first
            while len(out) < (off % self.blocksize) + length:
                boff, csize, usize, method = self.blocks[b]
                fh.seek(boff)
                raw = fh.read((csize + 15) // 16 * 16 if self.key else csize)
                if self.key:
                    raw = AES.new(self.key, AES.MODE_ECB).decrypt(raw)[:csize]
                if self.methods[method] == "None":
                    out += raw[:usize]
                else:
                    out += oodle_decompress(raw, usize)
                b += 1
        start = off % self.blocksize
        return out[start:start+length]

def open_base():
    return Container(os.path.join(PAKS, "Dawnwalker-Windows.utoc"))
