"""My interior variation. The exterior is left exactly as delivered."""
import os, sys, math, copy, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED = 7, 8
DECK, STAND = 3.1, 0.13
BAY_R, BAY_ZMIN = 6.5, 0.0
STAIR = [(4.5, 5.6, 2.40), (4.5, 4.6, 1.60), (4.5, 3.6, 0.80), (4.5, 2.6, 0.05)]
AMEN = ["^TELEPORTER", "^BUILDTERMINAL", "^MAPTABLE",
        "^HEALTHSTATION", "^SHIELDSTATION", "^FRE_ROOM_SCAN"]
WANT = {"^TELEPORTER": (0.0, -1.5), "^BUILDTERMINAL": (-4.5, -1.0),
        "^MAPTABLE": (4.5, -1.0), "^HEALTHSTATION": (7.5, -4.0),
        "^SHIELDSTATION": (-7.5, -4.0), "^FRE_ROOM_SCAN": (-9.0, 1.5)}

def s7(bases):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == TARGET]
    if len(hits) != 1:
        sys.exit("slot 7 lookup failed")
    return hits[0]

def in_bay(x, z):
    return math.hypot(x, z) < BAY_R and z > BAY_ZMIN

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    prot = next(b for b in bases if (b.get("peI") or {}).get("DPp") == "PlayerShipBase"
                and b["CVX"] == PROTECTED)
    before8 = len(prot["@ZJ"])
    tgt = s7(bases); objs = tgt["@ZJ"]; before = len(objs)
    sig = lambda o: (o["r<7"], tuple(round(v, 2) for v in o["wMC"]))
    ext_before = {sig(o) for o in objs if o["wMC"][1] < 3.0 or o["wMC"][1] > 5.35}
    floor_tpl = copy.deepcopy(next(o for o in objs if o["r<7"] == "^L_FLOOR_Q"))

    kept, cut, displaced = [], 0, []
    for o in objs:
        x, y, z = o["wMC"]
        if o["r<7"] == "^L_FLOOR_Q" and in_bay(x, z):
            cut += 1
            continue
        if 3.15 < y < 4.2 and in_bay(x, z) and o["r<7"] not in AMEN:
            displaced.append(o)
        kept.append(o)

    steps = 0
    for sx, sz, sy in STAIR:
        st = copy.deepcopy(floor_tpl)
        st["wMC"] = [sx, sy, sz]; st["wJ0"] = [0.0, 1.0, 0.0]; st["aNu"] = [0.0, 0.0, 1.0]
        kept.append(st); steps += 1

    floors = [o["wMC"] for o in kept
              if o["r<7"] == "^L_FLOOR_Q" and not in_bay(o["wMC"][0], o["wMC"][2])
              and o["wMC"][1] > 2.5]
    used = []
    for pid in AMEN:
        a = next((o for o in kept if o["r<7"] == pid), None)
        if a is None: continue
        wx, wz = WANT[pid]
        best, bd = None, 1e9
        for f in floors:
            if any(math.hypot(f[0]-u[0], f[2]-u[2]) < 2.2 for u in used): continue
            dd = math.hypot(f[0]-wx, f[2]-wz)
            if dd < bd: best, bd = f, dd
        if best is None: continue
        a["wMC"] = [best[0], round(best[1] + STAND, 3), best[2]]
        a["wJ0"] = [0.0, 1.0, 0.0]
        used.append(a["wMC"])

    for o in displaced:
        best, bd = None, 1e9
        for f in floors:
            if any(math.hypot(f[0]-u[0], f[2]-u[2]) < 1.4 for u in used): continue
            dd = math.hypot(f[0]-o["wMC"][0], f[2]-o["wMC"][2])
            if dd < bd: best, bd = f, dd
        if best:
            o["wMC"] = [best[0], round(best[1] + STAND, 3), best[2]]
            used.append(o["wMC"])

    tgt["@ZJ"] = kept
    ext_after = {sig(o) for o in kept}
    lost = ext_before - ext_after
    assert not lost, f"EXTERIOR LOST {len(lost)} objects: {list(lost)[:4]}"
    assert sum(1 for o in kept if o["r<7"] == "^U_PARAGON") == 1
    assert sum(1 for o in kept if o["wMC"][1] >= 5.4) >= 660, "roof damaged"
    for must in ("^B_COK_A", "^B_LND_A", "^B_ALK_C", "^B_HAB1_C", "^TELEPORTER"):
        assert any(o["r<7"] == must for o in kept), f"lost {must}"
    assert len(prot["@ZJ"]) == before8 == 163
    hgsave.write(path, d, fmt)
    if fn == "save.hg":
        print(f"   bay cut           : {cut} floor panels over the hab")
        print(f"   staircase         : {steps} steps, y 2.40 -> 0.05")
        print(f"   amenities seated  : {len(used)} placements")
        print(f"   loose items moved : {len(displaced)} (moved, not deleted)")
        print(f"   EXTERIOR          : all {len(ext_before)} objects still present  UNCHANGED")
    print(f"{fn:10s} {before} -> {len(kept)} parts")
