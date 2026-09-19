"""Restore slot 7's Corvette build from the last known-good backup.

Only the build (@ZJ) is copied. Everything else in the live save - progress,
inventory, position, and the ship technology fitted afterwards - is left alone."""
import os, copy, sys, hgsave

LIVE_DIR = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576"
GOOD = r"C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\outputs\NMS-Before-Amenities-20260918-223153\save.hg"
TARGET, PROTECTED = 7, 8

def psb(bases, slot):
    hits = [b for b in bases
            if (b.get("peI") or {}).get("DPp") == "PlayerShipBase" and b.get("CVX") == slot]
    if len(hits) != 1: sys.exit(f"slot {slot} lookup failed")
    return hits[0]

dg, _ = hgsave.read(GOOD)
good_objs = psb(dg["vLc"]["6f="]["F?0"], TARGET)["@ZJ"]
print(f"known-good build: {len(good_objs)} objects, "
      f"{sum(1 for o in good_objs if o['r<7']=='^U_PARAGON')} root")

for fn in ("save.hg", "save2.hg"):
    path = os.path.join(LIVE_DIR, fn)
    d, fmt = hgsave.read(path)
    bases = d["vLc"]["6f="]["F?0"]
    prot = psb(bases, PROTECTED); before8 = len(prot["@ZJ"])
    tgt = psb(bases, TARGET)
    before, ident = len(tgt["@ZJ"]), tgt.get("J=S")
    tech = len((d["vLc"]["6f="]["@Cs"][TARGET].get("PMT") or {}).get(":No") or [])

    tgt["@ZJ"] = copy.deepcopy(good_objs)

    assert sum(1 for o in tgt["@ZJ"] if o["r<7"] == "^U_PARAGON") == 1, "root count wrong"
    assert tgt.get("J=S") == ident, "slot 7 identity changed"
    assert len(prot["@ZJ"]) == before8 == 163, "slot 8 changed!"
    assert sum(1 for b in bases if (b.get("peI") or {}).get("DPp") == "PlayerShipBase") == 2
    tech_after = len((d["vLc"]["6f="]["@Cs"][TARGET].get("PMT") or {}).get(":No") or [])
    assert tech_after == tech, "ship technology was disturbed"
    hgsave.write(path, d, fmt)
    print(f"{fn:10s} slot7 {before} -> {len(tgt['@ZJ'])} objects | "
          f"tech {tech_after} kept | slot8 {before8} untouched")

print("\nverifying from disk:")
for fn in ("save.hg", "save2.hg"):
    d, _ = hgsave.read(os.path.join(LIVE_DIR, fn))
    b = psb(d["vLc"]["6f="]["F?0"], TARGET)
    tech = len(d["vLc"]["6f="]["@Cs"][TARGET]["PMT"][":No"])
    print(f"   {fn}: slot7 {len(b['@ZJ'])} objects, tech {tech} items")
