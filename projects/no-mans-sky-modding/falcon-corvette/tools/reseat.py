"""Sit the amenities ON the deck instead of inside it.

The creator's own floor items sit 0.09-0.14 above the floor panels. Mine were
placed level with the panels, so they were buried - the game still offered the
interact prompt but there was nothing to see or walk to.

Each amenity is now snapped onto a real floor panel, at that panel's own height
plus the same offset the creator uses."""
import os, sys, math, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED = 7, 8
STAND_OFFSET = 0.13
MINE = ["^TELEPORTER", "^BUILDTERMINAL", "^MAPTABLE",
        "^HEALTHSTATION", "^SHIELDSTATION", "^FRE_ROOM_SCAN"]

def s7(bases):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == TARGET]
    if len(hits) != 1: sys.exit("slot 7 lookup failed")
    return hits[0]

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    before8 = len(next(b for b in bases if (b.get("peI") or {}).get("DPp")=="PlayerShipBase"
                       and b["CVX"]==PROTECTED)["@ZJ"])
    tgt = s7(bases); objs = tgt["@ZJ"]

    floors = [o for o in objs if o["r<7"] == "^L_FLOOR_Q"]
    # things already standing on the deck, so we don't drop an amenity on top of one
    taken = [o["wMC"] for o in objs
             if o["r<7"] not in MINE and 3.18 < o["wMC"][1] < 3.45]

    used = []
    for pid in MINE:
        a = next((o for o in objs if o["r<7"] == pid), None)
        if a is None:
            continue
        want = a["wMC"]
        best, bestd = None, 1e9
        for f in floors:
            fx, fy, fz = f["wMC"]
            if any(math.hypot(fx - t[0], fz - t[2]) < 1.6 for t in taken):   continue
            if any(math.hypot(fx - u[0], fz - u[2]) < 2.2 for u in used):    continue
            dd = math.hypot(fx - want[0], fz - want[2])
            if dd < bestd:
                best, bestd = f, dd
        if best is None:
            print(f"   no free floor panel for {pid}"); continue
        fx, fy, fz = best["wMC"]
        a["wMC"] = [fx, round(fy + STAND_OFFSET, 3), fz]
        a["wJ0"] = [0.0, 1.0, 0.0]
        used.append(a["wMC"])
        if fn == "save.hg":
            print(f"   {pid.lstrip('^'):15s} -> {[round(v,2) for v in a['wMC']]}  "
                  f"(moved {bestd:.2f} onto a floor panel)")

    assert sum(1 for o in objs if o["r<7"] == "^U_PARAGON") == 1
    assert sum(1 for o in objs if o["r<7"] == "^L_FLOOR_Q") == 142
    assert len(next(b for b in bases if (b.get("peI") or {}).get("DPp")=="PlayerShipBase"
                    and b["CVX"]==PROTECTED)["@ZJ"]) == before8 == 163
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} reseated {len(used)} amenities, {len(objs)} parts total")
