"""Swap every sub-S upgrade module on slot 7 for the best equivalent already
owned somewhere in this save. Nothing is fabricated - each replacement is a real
module instance copied from another ship, with only the slot index changed.

NMS penalises more than 3 upgrade modules on one technology, so a per-system cap
of 3 is enforced."""
import os, re, copy, sys, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED, CAP = 7, 8, 3
RANK = {"1": 1, "2": 2, "3": 3, "4": 4, "X": 5}     # X-class rolls above S

# explicit swaps: low-tier module -> best owned replacement
SWAPS = [
    # LAUN and PULSE are already at the 3-module cap, so these slots go to
    # weapons that are actually installed on this ship (SHIPGUN1, SHIPLAS1).
    ("CV_LAUN2#16546",  "UP_SGUN4#55786",  "S-class Photon Cannon"),
    ("CV_LAUN2#51882",  "UP_SGUNX#59442",  "X-class Photon Cannon"),
    ("CV_PULSE2#69764", "UP_SLASR4#57345", "S-class Mining Laser"),
    ("CV_PULSE2#05106", "UP_S_SHL4#16205", "S-class Shield"),
    ("CV_PULSE2#40443", "UP_S_SHLX#90118", "X-class Shield"),
    ("CV_FIT1#27502",   "CV_FIT3#83586",   "A-class Corvette Fit (best owned)"),
    ("CV_INV1#24496",   "CV_INV2#36262",   "B-class Corvette Inventory (best owned)"),
    ("CV_SLASR3#00176", "UP_SLASR4#25226", "S-class Laser"),
]

def sysname(pid):
    m = re.match(r"(UP|CV)_([A-Z_]+?)(\d|X)#\d+$", pid)
    return m.group(2) if m else None

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    ships = d["vLc"]["6f="]["@Cs"]
    pm = ships[TARGET]["PMT"]
    before8 = len(ships[PROTECTED]["PMT"][":No"])
    before = len(pm[":No"])

    lib = {}
    for s in ships:
        for it in (s.get("PMT") or {}).get(":No") or []:
            if isinstance(it, dict) and it.get("b2n"):
                lib.setdefault(it["b2n"].lstrip("^"), it)

    done = []
    for old, new, label in SWAPS:
        tgt_it = next((i for i in pm[":No"] if i["b2n"].lstrip("^") == old), None)
        if tgt_it is None:
            continue
        src = lib.get(new)
        if src is None:
            print(f"   skip {label}: {new} not owned"); continue
        if any(i["b2n"].lstrip("^") == new for i in pm[":No"]):
            print(f"   skip {label}: {new} already fitted"); continue
        # respect the 3-per-technology cap
        sn = sysname(new)
        count = sum(1 for i in pm[":No"]
                    if sysname(i["b2n"].lstrip("^")) == sn
                    and i["b2n"].lstrip("^") != old)
        if sn and count >= CAP:
            print(f"   skip {label}: {sn} already has {count} modules (cap {CAP})")
            continue
        slot = tgt_it["3ZH"]
        rep = copy.deepcopy(src)
        rep["3ZH"] = copy.deepcopy(slot)
        rep["b76"] = True
        rep["eVk"] = 0.0
        pm[":No"][pm[":No"].index(tgt_it)] = rep
        done.append((old, new, label))

    assert len(ships[PROTECTED]["PMT"][":No"]) == before8, "slot 8 inventory changed!"
    assert len(pm[":No"]) == before, "item count changed"
    assert pm.get("B@N", {}).get("1o6") == "S", "ship class changed"
    slots = [(i["3ZH"][">Qh"], i["3ZH"]["XJ>"]) for i in pm[":No"]]
    assert len(slots) == len(set(slots)), "two items share a slot"
    valid = {(s[">Qh"], s["XJ>"]) for s in pm["hl?"]}
    assert all(s in valid for s in slots), "item in an invalid slot"
    hgsave.write(path, d, fmt)
    if fn == "save.hg":
        for old, new, label in done:
            print(f"   {old:18s} -> {new:18s}  {label}")
        print()
        tiers = collections.Counter()
        for i in pm[":No"]:
            m = re.match(r"(UP|CV)_([A-Z_]+?)(\d|X)#\d+$", i["b2n"].lstrip("^"))
            if m: tiers[m.group(3)] += 1
        names = {"1":"C","2":"B","3":"A","4":"S","X":"X"}
        print("   module tiers now: " + ", ".join(
            f"{names[k]}-class x{v}" for k, v in sorted(tiers.items(), key=lambda t: RANK[t[0]], reverse=True)))
    print(f"{fn:10s} {len(done)} modules upgraded, {len(pm[':No'])} tech items total")
