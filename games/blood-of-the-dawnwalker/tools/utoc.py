import struct, sys, os, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHUNK_TYPES = {0:"Invalid",1:"ExportBundleData",2:"BulkData",3:"OptionalBulkData",
 4:"MemoryMappedBulkData",5:"ScriptObjects",6:"ContainerHeader",7:"ExternalFile",
 8:"ShaderCodeLibrary",9:"ShaderCode",10:"PackageStoreEntry",11:"DerivedData",
 12:"EditorDerivedData",13:"PackageResource"}
VERSIONS = {1:"Initial",2:"DirectoryIndex",3:"PartitionSize",4:"PerfectHash",
 5:"PerfectHashWithOverflow",6:"OnDemandMetaData",7:"RemovedOnDemandMetaData",
 8:"ReplaceIoChunkHashWithIoHash"}
FLAGS = [(1,"Compressed"),(2,"Encrypted"),(4,"Signed"),(8,"Indexed"),(16,"OnDemand"),(32,"NoOsWrite")]
NONE = 0xFFFFFFFF

class R:
    def __init__(s,b,o=0): s.b=b; s.o=o
    def u32(s):
        v=struct.unpack_from("<I",s.b,s.o)[0]; s.o+=4; return v
    def i32(s):
        v=struct.unpack_from("<i",s.b,s.o)[0]; s.o+=4; return v
    def fstring(s):
        n=s.i32()
        if n==0: return ""
        if n<0:
            n=-n; raw=s.b[s.o:s.o+n*2]; s.o+=n*2
            return raw.decode("utf-16-le").rstrip("\0")
        raw=s.b[s.o:s.o+n]; s.o+=n
        return raw.decode("utf-8",errors="replace").rstrip("\0")

def parse(path, list_files=True, max_list=None):
    d=open(path,"rb").read()
    assert d[:16]==b"-==--==--==--==-", "not an IoStore utoc"
    ver=d[16]
    (hdr_size,entry_count,cb_count,cb_size,cm_count,cm_len,cblock_size,
     dir_size,part_count)=struct.unpack_from("<9I",d,20)
    container_id=struct.unpack_from("<Q",d,56)[0]
    enc_guid=d[64:80]
    flags=d[80]
    seed_count=struct.unpack_from("<I",d,84)[0]
    part_size=struct.unpack_from("<Q",d,88)[0]
    without=struct.unpack_from("<I",d,96)[0]

    nul16 = b"\x00"*16
    print(f"FILE            : {os.path.basename(path)}  ({len(d):,} bytes)")
    print(f"TOC version     : {ver} ({VERSIONS.get(ver,'?')})")
    print(f"Chunk entries   : {entry_count:,}")
    print(f"Compress blocks : {cb_count:,} (block size {cblock_size:,} = {cblock_size//1024} KiB)")
    print(f"Container ID    : 0x{container_id:016x}")
    print(f"Encryption GUID : {enc_guid.hex()}  {'(all-zero / default key)' if enc_guid==nul16 else '(named key)'}")
    fl=[n for m,n in FLAGS if flags & m]
    print(f"Container flags : 0x{flags:02x} = {' | '.join(fl) if fl else 'None'}")
    print(f"PerfectHashSeeds: {seed_count}   ChunksWithoutHash: {without}")

    o=hdr_size
    chunks=[]
    for i in range(entry_count):
        raw=d[o:o+12]; o+=12
        chunks.append((struct.unpack_from("<Q",raw,0)[0], struct.unpack_from(">H",raw,8)[0], raw[11]))
    offlen=[]
    for i in range(entry_count):
        raw=d[o:o+10]; o+=10
        offlen.append((int.from_bytes(raw[0:5],"big"), int.from_bytes(raw[5:10],"big")))
    if ver>=4:
        o += seed_count*4 + without*4
    blk_off=o
    o += cb_count*12
    methods=["None"]
    for i in range(cm_count):
        methods.append(d[o:o+cm_len].rstrip(b"\0").decode("utf-8",errors="replace")); o+=cm_len
    print(f"Compression     : {methods}")
    if flags & 4:
        hsz=struct.unpack_from("<I",d,o)[0]; o+=4+hsz*2+entry_count*20
    diridx=d[o:o+dir_size]; o+=dir_size
    meta_bytes=len(d)-o
    print(f"Meta entry size : {meta_bytes/entry_count if entry_count else 0} bytes ({meta_bytes:,} total, leftover {meta_bytes%entry_count if entry_count else 0})")

    files={}
    if dir_size:
        r=R(diridx)
        mount=r.fstring()
        nd=r.u32(); dbase=r.o; r.o+=nd*16
        nf=r.u32(); fbase=r.o; r.o+=nf*12
        ns=r.u32(); strs=[r.fstring() for _ in range(ns)]
        print(f"MOUNT POINT     : {mount}   (dirs={nd:,} files={nf:,} strings={ns:,})")
        def name(i): return strs[i] if i!=NONE else ""
        stack=[(0,"")]
        while stack:
            di,prefix=stack.pop()
            while di!=NONE:
                nm,firstchild,nextsib,firstfile=struct.unpack_from("<4I",diridx,dbase+di*16)
                p=prefix+(name(nm)+"/" if nm!=NONE else "")
                fi=firstfile
                while fi!=NONE:
                    fnm,nxt,ud=struct.unpack_from("<3I",diridx,fbase+fi*12)
                    files[ud]=p+name(fnm); fi=nxt
                if firstchild!=NONE: stack.append((firstchild,p))
                di=nextsib
    if list_files:
        print(f"\n{'#':<7} {'TYPE':<18} {'CHUNK ID':<18} {'OFFSET':>13} {'SIZE(unc)':>13}  PATH")
        n = entry_count if max_list is None else min(entry_count,max_list)
        for i in range(n):
            cid,idx,ct=chunks[i]; off,ln=offlen[i]
            print(f"{i:<7} {CHUNK_TYPES.get(ct,'?'+str(ct)):<18} 0x{cid:016x} {off:>13,} {ln:>13,}  {files.get(i,'')}")
    return dict(ver=ver,chunks=chunks,offlen=offlen,files=files,methods=methods,
                blocks_off=blk_off,cb_count=cb_count,cblock_size=cblock_size,flags=flags,data=d)

if __name__=="__main__":
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    ml=None
    for a in sys.argv[1:]:
        if a.startswith("--max="): ml=int(a.split("=")[1])
    for p in args:
        print("="*110); parse(p,max_list=ml); print()
