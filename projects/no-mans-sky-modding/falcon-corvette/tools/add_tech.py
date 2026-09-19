"""Fit the Falcon with the best ship technology in the save.

Every item is COPIED from a real instance already on one of the user's own ships,
so ids, amounts and structure are genuine - nothing is fabricated. Only the slot
index is changed. Slot 8 (Darth Fritz) is read from, never written."""
import os, sys, copy, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED = 7, 8

# in priority order - the list is trimmed to however many free slots exist
WANT = [
    # what the user asked for first
    ("^UT_LAUNCHCHARGE", "Launch System Recharger - auto-recharging lifters"),
    ("^HDRIVEBOOST1",    "Cadmium Drive - warp to red stars"),
    ("^HDRIVEBOOST2",    "Emeril Drive - warp to green stars"),
    ("^HDRIVEBOOST3",    "Indium Drive - warp to blue stars"),
    ("^UT_QUICKWARP",    "Emergency Warp Unit"),
    # flight
    ("^UT_LAUNCHER",     "Efficient Thrusters"),
    ("^UT_PULSESPEED",   "Photonix Core"),
    ("^UT_PULSEFUEL",    "Instability Drive"),
    ("^UT_SHIPDRIFT",    "Sublight Amplifier"),
    # defence and utility
    ("^UT_SHIPSHIELD",   "Ablative Armour"),
    ("^CARGOSHIELD",     "Cargo Shield"),
    ("^SHIP_TELEPORT",   "Teleport Receiver"),
    ("^SHIPSCAN_ECON",   "Economy Scanner"),
    ("^SHIPSCAN_COMBAT", "Conflict Scanner"),
    # S-class upgrade modules (tier 4), distinct seeds
    ("^UP_HYP4#02698",   "S-class Hyperdrive upgrade"),
    ("^UP_HYP4#68588",   "S-class Hyperdrive upgrade"),
    ("^UP_LAUN4#26628",  "S-class Launch Thruster upgrade"),
    ("^UP_LAUN4#92433",  "S-class Launch Thruster upgrade"),
    ("^UP_PULSE4#58155", "S-class Pulse Engine upgrade"),
    ("^UP_PULSE4#91414", "S-class Pulse Engine upgrade"),
    ("^UP_S_SHL4#48434", "S-class Shield upgrade"),
]

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    ships = d["vLc"]["6f="]["@Cs"]
    pm = ships[TARGET]["PMT"]
    before8 = len(ships[PROTECTED]["PMT"][":No"])

    # a library of real item instances from every ship in the save
    lib = {}
    for s in ships:
        for it in (s.get("PMT") or {}).get(":No") or []:
            if isinstance(it, dict) and it.get("b2n"):
                lib.setdefault(it["b2n"], it)

    occupied = {(it["3ZH"][">Qh"], it["3ZH"]["XJ>"]) for it in pm[":No"]}
    valid = [(s[">Qh"], s["XJ>"]) for s in pm["hl?"]]
    free = [c for c in valid if c not in occupied]
    present = {it["b2n"] for it in pm[":No"]}

    added = []
    for pid, label in WANT:
        if not free:
            break
        if pid in present:
            continue
        src = lib.get(pid)
        if src is None:
            print(f"   skip {label}: {pid} not owned anywhere in this save")
            continue
        x, y = free.pop(0)
        it = copy.deepcopy(src)
        it["3ZH"] = {">Qh": x, "XJ>": y}
        it["b76"] = True          # fully installed
        it["eVk"] = 0.0           # undamaged
        pm[":No"].append(it)
        present.add(pid)
        added.append((label, pid, x, y))

    assert len(ships[PROTECTED]["PMT"][":No"]) == before8, "slot 8 inventory changed!"
    assert pm.get("B@N", {}).get("1o6") == "S", "ship class is no longer S"
    occ2 = [(i["3ZH"][">Qh"], i["3ZH"]["XJ>"]) for i in pm[":No"]]
    assert len(occ2) == len(set(occ2)), "two items share a slot!"
    for i in pm[":No"]:
        assert (i["3ZH"][">Qh"], i["3ZH"]["XJ>"]) in valid, "item placed in an invalid slot"
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} tech {len(pm[':No'])-len(added)} -> {len(pm[':No'])} items, {len(free)} slots spare")
    if fn == "save.hg":
        for label, pid, x, y in added:
            print(f"      + {label:42s} {pid.lstrip('^'):18s} slot ({x},{y})")
