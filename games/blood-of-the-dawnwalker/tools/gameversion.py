#!/usr/bin/env python3
"""
Fingerprint the installed Dawnwalker build.

Run this FIRST in any new session. If the output still matches
projects/dawnwalker-modding/GAME_VERSION.md, every format finding in
games/blood-of-the-dawnwalker/ still applies. If it does not, the game was
patched and findings must be re-verified before being trusted.

It reads Steam's own manifest for the build id, then hashes the small
version-defining containers. It deliberately does NOT hash the 43 GB .ucas.

Usage:  python gameversion.py [--json]
Exit 0 always; this is a reporting tool.
"""
import hashlib, os, sys, struct, datetime, json, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GAME = r"D:\steam\steamapps\common\The Blood of Dawnwalker"
ACF = r"D:\steam\steamapps\appmanifest_3751260.acf"
PAKS = os.path.join(GAME, r"Dawnwalker\Content\Paks")
EXE = os.path.join(GAME, r"Dawnwalker\Binaries\Win64\Dawnwalker.exe")

HASH_TARGETS = ["global.utoc", "global.ucas", "Dawnwalker-Windows.utoc"]


def sha256_file(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
            n += len(b)
    return h.hexdigest(), n


def read_acf(path):
    """Steam .acf is a simple quoted key/value format."""
    out = {}
    if not os.path.isfile(path):
        return out
    txt = open(path, encoding="utf-8", errors="replace").read()
    for k in ("appid", "name", "buildid", "LastUpdated", "StateFlags",
              "SizeOnDisk", "BytesDownloaded", "ScheduledAutoUpdate", "UpdateResult"):
        m = re.search(r'"%s"\s+"([^"]*)"' % k, txt)
        if m:
            out[k] = m.group(1)
    return out


def toc_summary(path):
    d = open(path, "rb").read(200)
    if d[:16] != b"-==--==--==--==-":
        return None
    hdr, ec, cbc, cbs, cmc, cml, cblk, dirsz, pc = struct.unpack_from("<9I", d, 20)
    return dict(version=d[16], chunks=ec, blocks=cbc, flags=d[80],
                container_id=struct.unpack_from("<Q", d, 56)[0])


def main():
    report = {"generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds")}

    acf = read_acf(ACF)
    report["steam"] = acf
    print("STEAM MANIFEST")
    if acf:
        ts = int(acf.get("LastUpdated", "0"))
        when = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
        print(f"  appid               : {acf.get('appid')}")
        print(f"  name                : {acf.get('name')}")
        print(f"  buildid             : {acf.get('buildid')}")
        print(f"  LastUpdated         : {ts}  ->  {when:%Y-%m-%d %H:%M:%S UTC}")
        print(f"  SizeOnDisk          : {int(acf.get('SizeOnDisk', 0)):,}")
        print(f"  BytesDownloaded     : {int(acf.get('BytesDownloaded', 0)):,}")
        sf = acf.get("StateFlags")
        print(f"  StateFlags          : {sf}" + ("  (4 = fully installed)" if sf == "4" else ""))
        print(f"  UpdateResult        : {acf.get('UpdateResult')}"
              + ("  (0 = no error)" if acf.get('UpdateResult') == '0' else ""))
        print(f"  ScheduledAutoUpdate : {acf.get('ScheduledAutoUpdate')}"
              + ("  (0 = nothing queued)" if acf.get('ScheduledAutoUpdate') == '0' else ""))
        report["steam"]["LastUpdatedUTC"] = f"{when:%Y-%m-%d %H:%M:%S UTC}"
    else:
        print(f"  !! manifest not found at {ACF}")
    print()

    print("CONTENT HASHES")
    files = {}
    for name in HASH_TARGETS:
        p = os.path.join(PAKS, name)
        if not os.path.isfile(p):
            print(f"  {name:<26} MISSING")
            continue
        digest, n = sha256_file(p)
        files[name] = {"bytes": n, "sha256": digest}
        print(f"  {name:<26} {n:>12,} B  {digest}")
    if os.path.isfile(EXE):
        digest, n = sha256_file(EXE)
        files["Dawnwalker.exe"] = {"bytes": n, "sha256": digest}
        print(f"  {'Dawnwalker.exe':<26} {n:>12,} B  {digest}")
    report["files"] = files
    print()

    print("CONTAINER STRUCTURE")
    conts = {}
    for name in ("Dawnwalker-Windows.utoc", "global.utoc"):
        p = os.path.join(PAKS, name)
        if not os.path.isfile(p):
            continue
        s = toc_summary(p)
        conts[name] = s
        print(f"  {name}")
        print(f"    TOC v{s['version']}  chunks {s['chunks']:,}  blocks {s['blocks']:,}"
              f"  flags 0x{s['flags']:02x}  id 0x{s['container_id']:016x}")
    report["containers"] = {k: {**v, "container_id": f"0x{v['container_id']:016x}"}
                            for k, v in conts.items()}

    if "--json" in sys.argv:
        print()
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
