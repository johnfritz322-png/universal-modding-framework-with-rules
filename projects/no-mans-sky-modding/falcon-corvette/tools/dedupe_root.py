"""Remove the duplicate ^U_PARAGON root from slot 7, and any exact duplicate
objects the delivery may have stacked. Touches nothing else in the build."""
import os, sys, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED = 7, 8

def base(bases, slot):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == slot]
    if len(hits) != 1:
        sys.exit(f"expected 1 PlayerShipBase in slot {slot}, found {len(hits)}")
    return hits[0]

def sig(o):
    return (o["r<7"], tuple(round(v, 3) for v in o["wMC"]),
            tuple(round(v, 3) for v in o["wJ0"]), tuple(round(v, 3) for v in o["aNu"]))

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    before8 = len(base(bases, PROTECTED)["@ZJ"])
    tgt = base(bases, TARGET)
    objs, ident = tgt["@ZJ"], tgt.get("J=S")
    before = len(objs)

    kept, seen, dropped_root, dropped_dup = [], set(), 0, 0
    root_seen = False
    for o in objs:
        if o["r<7"] == "^U_PARAGON":
            if root_seen:
                dropped_root += 1
                continue
            root_seen = True
            kept.append(o)
            continue
        s = sig(o)
        if s in seen:
            dropped_dup += 1
            continue
        seen.add(s)
        kept.append(o)

    tgt["@ZJ"] = kept
    roots = sum(1 for o in kept if o["r<7"] == "^U_PARAGON")
    assert roots == 1, f"root count is {roots}"
    assert len(base(bases, PROTECTED)["@ZJ"]) == before8 == 163, "slot 8 changed!"
    assert tgt.get("J=S") == ident, "slot 7 identity changed"
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} {before} -> {len(kept)} parts  "
          f"(dropped {dropped_root} duplicate root, {dropped_dup} exact duplicates) | slot8 {before8} ok")

print("\nverified from disk:")
for fn in ("save.hg", "save2.hg"):
    d, _ = hgsave.read(os.path.join(SAVE_DIR, fn))
    for b in sorted([x for x in d["vLc"]["6f="]["F?0"]
                     if (x.get("peI") or {}).get("DPp") == "PlayerShipBase"],
                    key=lambda b: b["CVX"]):
        r = sum(1 for o in b["@ZJ"] if o["r<7"] == "^U_PARAGON")
        print(f"   {fn} slot {b['CVX']} {b['NKm']!r:22s} {len(b['@ZJ']):5d} parts, {r} root")
