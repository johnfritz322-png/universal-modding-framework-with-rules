# Parse global.ucas ScriptObjects: the engine-wide name + class/property table.
import struct, sys, os, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PAKS = r"D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks"
d = open(os.path.join(PAKS, "global.ucas"), "rb").read()
print(f"global.ucas = {len(d):,} bytes")

o = 0
num_strings, num_bytes = struct.unpack_from("<II", d, o)
hash_version = struct.unpack_from("<Q", d, o + 8)[0]
print(f"names={num_strings:,} stringbytes={num_bytes:,} hashver=0x{hash_version:x}")

p = o + 16 + num_strings * 8
headers = []
for i in range(num_strings):
    b0, b1 = d[p], d[p + 1]
    p += 2
    headers.append((bool(b0 & 0x80), ((b0 & 0x7f) << 8) | b1))

names = []
for u16, ln in headers:
    if u16:
        names.append(d[p:p + ln * 2].decode("utf-16-le", "replace")); p += ln * 2
    else:
        names.append(d[p:p + ln].decode("utf-8", "replace")); p += ln
print(f"parsed {len(names):,} names, cursor at {p:,}")

num_objs = struct.unpack_from("<I", d, p)[0]
p += 4
print(f"script objects: {num_objs:,}")

objs = []
for i in range(num_objs):
    nidx, nnum, gidx, outer, cdo = struct.unpack_from("<IIQQQ", d, p)
    p += 32
    objs.append((nidx, nnum, gidx, outer, cdo))
print(f"cursor after objects: {p:,} / {len(d):,}")

# FMappedName packs a 2-bit type in the high bits; the real index is the low 30 bits.
MASK = 0x3FFFFFFF
byidx = {g: (names[n & MASK] if (n & MASK) < len(names) else f"?{n}", outer)
         for n, _, g, outer, _ in objs}


def full(gidx, depth=0):
    if gidx not in byidx or depth > 16:
        return None
    nm, outer = byidx[gidx]
    par = full(outer, depth + 1)
    return (par + "/" + nm) if par else nm


out = {}
for n, _, g, outer, cdo in objs:
    out[f"0x{g:016x}"] = full(g)

here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "scriptobjects.json"), "w", encoding="utf-8"),
          indent=0, ensure_ascii=False)
open(os.path.join(here, "global_names.txt"), "w", encoding="utf-8").write("\n".join(names))
print(f"\nwrote scriptobjects.json ({len(out):,}) and global_names.txt ({len(names):,})")

for probe in ["0x593115e0cb25f002", "0x72c621fceb8a1d5b", "0x6399e61b42adb4c4"]:
    print(f"  {probe} -> {out.get(probe)}")
