"""Strip useless props from INSIDE the ship and refit the usable amenities.

Anything outside the floor footprint is exterior greebling - 92 objects of it on
this build, including 57 BUILDWORKTOP and 10 B_CARRIAGEWHEEL - and is never
touched. Only decorative props standing on the deck are removed.

The guard is an identity check over the whole build: every object not on the
explicit removal list must still exist afterwards."""
import os, math, copy, sys, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED, STAND = 7, 8, 0.13
JUNK = ("CEMENTMIXER","WHEELBARROW","BRICKSWRAPPED","PALLET","CARRIAGE","BUCKET",
        "COMPOSTBIN","MILKCRATE","BARREL","PAN0","TRAY0","TABLEPOT","FABROLLPILE",
        "SPARKPLUG","SIGN_BAR","RUG","LARGETRYE","CRATE","CANISTER","CEMENTBAG",
        "MACHINE0","BURNER0","MILKBOTTLE","TOYCUBE","ROBOTOY")
FURNITURE = ("SERVERSTACK","SERVERBOX","BUILDWORKTOP","HOLOFILES","BUILDCANRACK",
             "DRAWS","CRATEFRAME","BUILDAMCRATE","BUILDHCABINET","SHELFPANEL")
KEEP = ("TELEPORTER","BUILDTERMINAL","MAPTABLE","HEALTHSTATION","SHIELDSTATION",
        "FRE_ROOM_SCAN","BUILDSAVE","ARCHIVE","WEAPONRACK","BUILDBED","BUILDCHAIR",
        "BUILDSIMPLEDESK","MEDTUBE")
AMEN = [("^TELEPORTER",(0.0,-1.5)), ("^BUILDTERMINAL",(-4.0,-1.0)),
        ("^MAPTABLE",(4.0,-1.0)),   ("^HEALTHSTATION",(7.0,-3.5)),
        ("^SHIELDSTATION",(-7.0,-3.5)), ("^FRE_ROOM_SCAN",(-9.0,1.0))]

def psb(bases, slot):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == slot]
    if len(hits) != 1: sys.exit(f"slot {slot} lookup failed")
    return hits[0]

sig = lambda o: (o["r<7"], tuple(round(v, 2) for v in o["wMC"]))

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    ships = d["vLc"]["6f="]["@Cs"]
    prot = psb(bases, PROTECTED); before8 = len(prot["@ZJ"])
    tgt = psb(bases, TARGET); objs = tgt["@ZJ"]; before = len(objs)
    tech_before = len(ships[TARGET]["PMT"][":No"])

    floors = [o["wMC"] for o in objs if o["r<7"] == "^L_FLOOR_Q"]
    def inside(o):
        x, y, z = o["wMC"]
        return 3.0 < y < 5.4 and any(math.hypot(f[0]-x, f[2]-z) <= 2.2 for f in floors)
    def removable(o):
        b = o["r<7"].lstrip("^")
        if any(k in b for k in KEEP): return False
        return inside(o) and any(k in b for k in JUNK + FURNITURE)

    doomed = {id(o) for o in objs if removable(o)}
    survivors_expected = {sig(o) for o in objs if id(o) not in doomed}
    removed = collections.Counter(o["r<7"] for o in objs if id(o) in doomed)
    kept = [o for o in objs if id(o) not in doomed]

    # refit the amenities on real floor panels
    lib = {}
    for b in bases:
        for o in b.get("@ZJ") or []:
            lib.setdefault(o["r<7"], o)
    taken = [o["wMC"] for o in kept if 3.18 < o["wMC"][1] < 3.45]
    added = []
    for pid, (wx, wz) in AMEN:
        if any(o["r<7"] == pid for o in kept): continue
        src = lib.get(pid)
        if src is None:
            print(f"   {pid} not available anywhere"); continue
        best, bd = None, 1e9
        for f in floors:
            if any(math.hypot(f[0]-t[0], f[2]-t[2]) < 1.8 for t in taken): continue
            dd = math.hypot(f[0]-wx, f[2]-wz)
            if dd < bd: best, bd = f, dd
        if best is None: continue
        it = copy.deepcopy(src)
        it["wMC"] = [best[0], round(best[1] + STAND, 3), best[2]]
        it["wJ0"] = [0.0, 1.0, 0.0]; it["aNu"] = [0.0, 0.0, 1.0]
        kept.append(it); taken.append(it["wMC"]); added.append(pid)

    tgt["@ZJ"] = kept
    # the strong guard: nothing outside the removal list may have vanished
    lost = survivors_expected - {sig(o) for o in kept}
    assert not lost, f"LOST {len(lost)} objects that were not on the list: {list(lost)[:4]}"
    assert sum(1 for o in kept if o["r<7"] == "^U_PARAGON") == 1
    assert sum(1 for o in kept if o["r<7"] == "^L_FLOOR_Q") == len(floors), "floor changed"
    assert len(prot["@ZJ"]) == before8 == 163, "slot 8 changed"
    assert len(ships[TARGET]["PMT"][":No"]) == tech_before, "technology disturbed"
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} {before} -> {len(kept)} objects | removed {sum(removed.values())} | refitted {len(added)}")
    if fn == "save.hg":
        print("   removed:", ", ".join(f"{k.lstrip('^')} x{v}" for k, v in removed.most_common(10)), "...")
        print("   amenities back:", ", ".join(a.lstrip('^') for a in added))
