import struct, sys, os, zlib, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from utoc import parse, CHUNK_TYPES

def extract(utoc_path, outdir):
    info = parse(utoc_path, list_files=False)
    d = info["data"]; methods = info["methods"]
    ucas = open(utoc_path[:-5]+".ucas","rb").read()
    blocks=[]
    o=info["blocks_off"]
    for i in range(info["cb_count"]):
        raw=d[o:o+12]; o+=12
        blocks.append((int.from_bytes(raw[0:5],"little"),
                       int.from_bytes(raw[5:8],"little"),
                       int.from_bytes(raw[8:11],"little"), raw[11]))
    cbs=info["cblock_size"]
    os.makedirs(outdir, exist_ok=True)
    manifest=[]
    for i,((cid,idx,ct),(off,ln)) in enumerate(zip(info["chunks"],info["offlen"])):
        first=off//cbs
        n=(off%cbs + ln + cbs-1)//cbs
        buf=bytearray()
        for b in range(first, first+n):
            boff,csz,usz,m=blocks[b]
            raw=ucas[boff:boff+csz]
            if methods[m].lower()=="zlib": raw=zlib.decompress(raw)
            elif methods[m]=="None": raw=raw[:usz]
            else: raw=b"<UNSUPPORTED:"+methods[m].encode()+b">"
            buf+=raw
        data=bytes(buf[off%cbs : off%cbs + ln])
        name = info["files"].get(i)
        if not name:
            name = f"_chunk{i:04d}_{CHUNK_TYPES.get(ct,ct)}_{cid:016x}.bin"
        name = name.replace("/", os.sep)
        p=os.path.join(outdir,name)
        os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,"wb").write(data)
        manifest.append((i,CHUNK_TYPES.get(ct,str(ct)),f"0x{cid:016x}",len(data),name))
    print(f"\nExtracted {len(manifest)} chunks -> {outdir}")
    return manifest

if __name__=="__main__":
    m=extract(sys.argv[1], sys.argv[2])
    for r in m[:12]: print(r)
