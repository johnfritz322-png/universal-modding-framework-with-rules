"""Add working amenities to the delivered Falcon and clear floor clutter.

Conservative by design: the creator's hull, lighting, decals and furniture are
untouched. Only loose debris standing in walkways is removed, and amenities go
into deck cells that are already completely empty."""
import os, sys, copy, json, collections, hgsave

SAVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
TARGET, PROTECTED, DECK = 7, 8, 3.1

# amenity -> (part id, deck cell x, cell z, facing)
PLACE = [
    ("Teleporter",      "^TELEPORTER",     0.0,  2.7, (0.0, 0.0, 1.0)),
    ("Trade terminal",  "^BUILDTERMINAL",  2.7,  2.7, (0.0, 0.0, 1.0)),
    ("Mission table",   "^MAPTABLE",      -2.7,  2.7, (0.0, 0.0, 1.0)),
    ("Health station",  "^HEALTHSTATION",  5.4, -2.7, (-1.0, 0.0, 0.0)),
    ("Hazard station",  "^SHIELDSTATION", -5.4, -2.7, (1.0, 0.0, 0.0)),
    ("Room scanner",    "^FRE_ROOM_SCAN",  2.7,  0.0, (0.0, 0.0, 1.0)),
]
CLUTTER = {"^S_CEMENTBAG", "^S_CRATE0", "^S_TRAY0", "^S_CANISTER1"}

def base(bases, slot):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == slot]
    if len(hits) != 1:
        sys.exit(f"expected 1 PlayerShipBase in slot {slot}")
    return hits[0]

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(SAVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    before8 = len(base(bases, PROTECTED)["@ZJ"])
    tgt = base(bases, TARGET)
    objs, ident = tgt["@ZJ"], tgt.get("J=S")
    before = len(objs)

    # part templates from anywhere in this save (nothing invented)
    pool = {o["r<7"]: o for o in objs}
    for b in bases:
        for o in b.get("@ZJ") or []:
            pool.setdefault(o["r<7"], o)
    exp = json.load(open(r"C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\outputs\NMS-Corvette-Exports-20260918\Corvette-1-Original.json"))["objects"]
    for e in exp:
        pool.setdefault(e["ObjectID"], {"b1:": e["Timestamp"], "r<7": e["ObjectID"],
                                        "CVX": e["UserData"], "wMC": e["Position"],
                                        "wJ0": e["Up"], "aNu": e["At"]})

    # 1. clear loose debris standing on the deck
    floor_cells = {(round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))
                   for o in objs if o["r<7"] == "^L_FLOOR_Q"}
    kept, removed = [], collections.Counter()
    for o in objs:
        on_deck = DECK + 0.2 < o["wMC"][1] < DECK + 2.6
        cell = (round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))
        if o["r<7"] in CLUTTER and on_deck and cell in floor_cells:
            removed[o["r<7"]] += 1
            continue
        kept.append(o)

    # 2. add amenities
    added = []
    for label, pid, x, z, at in PLACE:
        if pid not in pool:
            print(f"   skip {label}: {pid} not available in this save")
            continue
        it = copy.deepcopy(pool[pid])
        it["wMC"] = [float(x), DECK, float(z)]
        it["wJ0"] = [0.0, 1.0, 0.0]
        it["aNu"] = [float(v) for v in at]
        kept.append(it)
        added.append(label)

    tgt["@ZJ"] = kept
    assert sum(1 for o in kept if o["r<7"] == "^U_PARAGON") == 1, "root count wrong"
    assert len(base(bases, PROTECTED)["@ZJ"]) == before8 == 163, "slot 8 changed!"
    assert tgt.get("J=S") == ident, "slot 7 identity changed"
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} {before} -> {len(kept)} parts | removed {sum(removed.values())} debris | added {len(added)}")
    if fn == "save.hg":
        print("   debris cleared:", dict(removed))
        print("   amenities added:", ", ".join(added))
