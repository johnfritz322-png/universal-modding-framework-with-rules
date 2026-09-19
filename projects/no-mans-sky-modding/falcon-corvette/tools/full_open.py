"""Finish opening the interior, and put every usable item on the deck.

A panel with floor on BOTH sides is an internal wall and goes. A panel with floor
on only one side is the outer hull and stays, or the ship gets holes in its sides.
The ceiling (5.4+) and the floor are never touched."""
import os, sys, math, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED = 7, 8
DECK, BODY_LO, BODY_HI, STAND = 3.1, 3.35, 5.35, 0.13
WALLISH = ("STORAGEPANEL","BUILDFLATPANEL","BLDWALLUNIT","TECHPANEL","BUILDSIDEPANEL",
           "WALLSCREEN","BOXEDSCREEN","BUILDHCABINET","SHELFPANEL","SERVERSTACK",
           "SERVERBOX","BUILDWORKTOP","B_WALL","M_WALL","C_WALL","B_CHEV_WALL")
FIT = ("WALLLIGHT","S_WALLLIGHT","WALLHANGING","DECAL","POSTER","HOLO_SMALL",
       "CEILINGLIGHT","WALLFAN","BILLBOARD")
USABLE = ("TELEPORTER","BUILDTERMINAL","MAPTABLE","HEALTHSTATION","SHIELDSTATION",
          "FRE_ROOM_SCAN","BUILDSAVE","ARCHIVE","WEAPONRACK","BUILDCHAIR",
          "BUILDBED","BUILDSIMPLEDESK","MEDTUBE")

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
    tgt = s7(bases); objs = tgt["@ZJ"]; before = len(objs)
    floors = [o["wMC"] for o in objs if o["r<7"] == "^L_FLOOR_Q"]

    def floor_near(x, z, r=2.0):
        return any(math.hypot(f[0]-x, f[2]-z) <= r for f in floors)
    def is_partition(o):
        x, y, z = o["wMC"]
        return any(floor_near(x+dx, z+dz) and floor_near(x-dx, z-dz)
                   for dx, dz in ((2.6,0), (0,2.6)))

    kept, removed = [], collections.Counter()
    for o in objs:
        body = o["r<7"].lstrip("^")
        in_band = BODY_LO < o["wMC"][1] < BODY_HI
        if in_band and any(w in body for w in WALLISH) and is_partition(o):
            removed["partition " + body] += 1; continue
        if in_band and any(f in body for f in FIT) and is_partition(o):
            removed["orphan fitting " + body] += 1; continue
        kept.append(o)

    # every usable item onto the deck
    taken = [o["wMC"] for o in kept if 3.18 < o["wMC"][1] < 3.45]
    moved = []
    for o in kept:
        body = o["r<7"].lstrip("^")
        if not any(u in body for u in USABLE):
            continue
        off = o["wMC"][1] - DECK
        if 0.08 < off < 0.40:
            continue                                   # already sitting on the deck
        x, y, z = o["wMC"]
        best, bd = None, 1e9
        for f in floors:
            if any(math.hypot(f[0]-t[0], f[2]-t[2]) < 1.5 for t in taken if t is not o["wMC"]):
                continue
            dd = math.hypot(f[0]-x, f[2]-z)
            if dd < bd: best, bd = f, dd
        if best is None: continue
        o["wMC"] = [best[0], round(best[1] + STAND, 3), best[2]]
        o["wJ0"] = [0.0, 1.0, 0.0]
        taken.append(o["wMC"]); moved.append((body, round(y,2), o["wMC"][1]))

    tgt["@ZJ"] = kept
    assert sum(1 for o in kept if o["r<7"] == "^U_PARAGON") == 1
    assert sum(1 for o in kept if o["r<7"] == "^L_FLOOR_Q") == 142, "floor damaged!"
    assert sum(1 for o in kept if o["wMC"][1] >= 5.4) >= 660, "ceiling damaged!"
    for must in ("^B_COK_A","^B_LND_A","^B_ALK_C","^B_HAB1_C","^TELEPORTER"):
        assert any(o["r<7"] == must for o in kept), f"lost {must}!"
    assert len(next(b for b in bases if (b.get("peI") or {}).get("DPp")=="PlayerShipBase"
                    and b["CVX"]==PROTECTED)["@ZJ"]) == before8 == 163
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} {before} -> {len(kept)}  (removed {sum(removed.values())}, moved {len(moved)} items to the deck)")
    if fn == "save.hg":
        for k,v in removed.most_common(8): print(f"      {k:34s} {v}")
        for b,o,n in moved: print(f"      moved {b:16s} y {o} -> {n}")
