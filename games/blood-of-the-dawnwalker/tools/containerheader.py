# Parse + validate FIoContainerHeader (the chunk that tells the engine which
# packages a container provides, and what each one imports).
import struct, sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SIG = 0x496F436E  # 'nCoI'
VERNAMES = {0: "Initial", 1: "LocalizedPackages", 2: "OptionalSegmentPackages",
            3: "NoExportInfo", 4: "SoftPackageReferences"}


def parse(path):
    d = open(path, "rb").read()
    sig, ver = struct.unpack_from("<II", d, 0)
    cid = struct.unpack_from("<Q", d, 8)[0]
    assert sig == SIG, f"bad signature 0x{sig:08x}"
    print(f"{os.path.basename(path)}  ({len(d):,} bytes)")
    print(f"  signature      : 0x{sig:08x} ('nCoI')")
    print(f"  header version : {ver} ({VERNAMES.get(ver,'?')})")
    print(f"  container id   : 0x{cid:016x}")

    o = 16
    npkg = struct.unpack_from("<I", d, o)[0]; o += 4
    pkgs = [struct.unpack_from("<Q", d, o + i * 8)[0] for i in range(npkg)]
    o += npkg * 8
    print(f"  package ids    : {npkg}")

    se_len = struct.unpack_from("<I", d, o)[0]; o += 4
    se_base = o
    print(f"  store entries  : {se_len:,} bytes at 0x{se_base:x}")

    stride = 16
    ents = []
    ok = True
    for i in range(npkg):
        b = se_base + i * stride
        ip_num, ip_off, sm_num, sm_off = struct.unpack_from("<IIII", d, b)
        # TFilePackageStoreEntryCArrayView offsets are relative to the address of
        # the view member itself: ImportedPackages sits at b+0, ShaderMapHashes at b+8.
        ip_at = b + ip_off if ip_num else None
        sm_at = (b + 8) + sm_off if sm_num else None
        ents.append((ip_num, ip_at, sm_num, sm_at))
    # validate: imported-package arrays must tile the data region contiguously
    data_start = se_base + npkg * stride
    cursor = data_start
    for i, (ip_num, ip_at, sm_num, sm_at) in enumerate(ents):
        if ip_num:
            if ip_at != cursor:
                print(f"  !! entry {i}: imports at 0x{ip_at:x}, expected 0x{cursor:x}")
                ok = False
                break
            cursor = ip_at + ip_num * 8
    print(f"  data region    : 0x{data_start:x} .. 0x{cursor:x} "
          f"(declared end 0x{se_base+se_len:x})")
    print(f"  TILING VALID   : {ok and cursor <= se_base + se_len}")

    tot = sum(e[0] for e in ents)
    print(f"  total imported-package refs: {tot}")
    print(f"  first 8 entries (importedPackages count -> ids):")
    for i, (ip_num, ip_at, sm_num, sm_at) in enumerate(ents[:8]):
        ids = [struct.unpack_from("<Q", d, ip_at + k * 8)[0] for k in range(ip_num)] if ip_num else []
        print(f"    pkg 0x{pkgs[i]:016x}  imports={ip_num}  " +
              (", ".join(f"0x{x:016x}" for x in ids[:3]) + (" ..." if len(ids) > 3 else "")))
    return pkgs, ents


if __name__ == "__main__":
    for p in sys.argv[1:]:
        parse(p); print()
