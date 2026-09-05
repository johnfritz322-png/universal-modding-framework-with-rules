# Parser for UE5 "Zen" packages (the .uasset form stored inside IoStore containers)
import struct, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SUMMARY_FIELDS = ["bHasVersioningInfo","HeaderSize","NameIdx","NameNum","PackageFlags",
 "CookedHeaderSize","ImportedPublicExportHashesOffset","ImportMapOffset","ExportMapOffset",
 "ExportBundleEntriesOffset","DependencyBundleHeadersOffset","DependencyBundleEntriesOffset",
 "ImportedPackageNamesOffset"]

def parse_pkg(data):
    s = dict(zip(SUMMARY_FIELDS, struct.unpack_from("<13I", data, 0)))
    o = 52
    num_strings, num_bytes = struct.unpack_from("<II", data, o)
    hash_version = struct.unpack_from("<Q", data, o+8)[0]
    p = o + 16 + num_strings*8
    headers = []
    for i in range(num_strings):
        b0, b1 = data[p], data[p+1]; p += 2
        headers.append((bool(b0 & 0x80), ((b0 & 0x7f) << 8) | b1))
    names = []
    for utf16, ln in headers:
        if utf16:
            names.append(data[p:p+ln*2].decode("utf-16-le", "replace")); p += ln*2
        else:
            names.append(data[p:p+ln].decode("utf-8", "replace")); p += ln
    name_end = p

    # locate BulkDataMapSize: 8-aligned slot where pos+8+size == ImportedPublicExportHashesOffset
    bulk = []
    target = s["ImportedPublicExportHashesOffset"]
    q = (name_end + 7) & ~7
    bdm_off = None
    while q + 8 <= target:
        v = struct.unpack_from("<Q", data, q)[0]
        if q + 8 + v == target:
            bdm_off = q; break
        q += 8
    if bdm_off is not None:
        sz = struct.unpack_from("<Q", data, bdm_off)[0]
        for i in range(sz // 32):
            so, dso, ssz, fl, _pad = struct.unpack_from("<QQQII", data, bdm_off+8+i*32)
            bulk.append(dict(SerialOffset=so, DuplicateSerialOffset=dso, SerialSize=ssz, Flags=fl))

    imports = []
    n_imp = (s["ExportMapOffset"] - s["ImportMapOffset"]) // 8
    for i in range(n_imp):
        imports.append(struct.unpack_from("<Q", data, s["ImportMapOffset"]+i*8)[0])

    exports = []
    n_exp = (s["ExportBundleEntriesOffset"] - s["ExportMapOffset"]) // 72
    for i in range(n_exp):
        b = s["ExportMapOffset"] + i*72
        (co, cs) = struct.unpack_from("<QQ", data, b)
        nidx, nnum = struct.unpack_from("<II", data, b+16)
        outer, klass, sup, tmpl, pubhash = struct.unpack_from("<QQQQQ", data, b+24)
        flags = struct.unpack_from("<I", data, b+64)[0]
        filt = data[b+68]
        exports.append(dict(CookedSerialOffset=co, CookedSerialSize=cs, NameIdx=nidx,
                            Name=names[nidx] if nidx < len(names) else f"?{nidx}",
                            OuterIndex=outer, ClassIndex=klass, SuperIndex=sup,
                            TemplateIndex=tmpl, PublicExportHash=pubhash,
                            ObjectFlags=flags, FilterFlags=filt))
    return dict(summary=s, names=names, hash_version=hash_version, bulk=bulk,
                imports=imports, exports=exports, name_end=name_end, bdm_off=bdm_off)

def dump(path, show_names=True, show_props=False):
    data = open(path,"rb").read()
    r = parse_pkg(data)
    s = r["summary"]
    print("="*100)
    print(f"PACKAGE: {os.path.basename(path)}   ({len(data):,} bytes)")
    print(f"  HeaderSize={s['HeaderSize']}  CookedHeaderSize={s['CookedHeaderSize']}  PackageFlags=0x{s['PackageFlags']:08x}")
    print(f"  PackageName: {r['names'][s['NameIdx']] if s['NameIdx']<len(r['names']) else '?'}")
    print(f"  imports={len(r['imports'])}  exports={len(r['exports'])}  bulkdata={len(r['bulk'])}  names={len(r['names'])}")
    if show_names:
        print(f"  NAME MAP:")
        for i,n in enumerate(r["names"]): print(f"    [{i:3}] {n}")
    print(f"  IMPORTS (FPackageObjectIndex):")
    for i,v in enumerate(r["imports"]):
        kind = v >> 62
        kindname = {0:"Export",1:"ScriptImport",2:"PackageImport",3:"Null"}[kind]
        print(f"    [{i:3}] 0x{v:016x}  {kindname}")
    print(f"  EXPORTS:")
    for i,e in enumerate(r["exports"]):
        print(f"    [{i}] {e['Name']}  serial off={e['CookedSerialOffset']} size={e['CookedSerialSize']} "
              f"class=0x{e['ClassIndex']:016x} flags=0x{e['ObjectFlags']:08x}")
    for i,b in enumerate(r["bulk"]):
        print(f"  BULK[{i}] off={b['SerialOffset']} size={b['SerialSize']} flags=0x{b['Flags']:08x}")
    return r, data

if __name__=="__main__":
    for p in sys.argv[1:]:
        dump(p)
