import hgsave, collections, math
S = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576\save.hg"
d,_ = hgsave.read(S)
objs = next(x for x in d["vLc"]["6f="]["F?0"]
            if (x.get("peI") or {}).get("DPp")=="PlayerShipBase" and x["CVX"]==7)["@ZJ"]
mag = lambda v: math.dist((0,0,0), v)

floors = [o for o in objs if o["r<7"] in ("^L_FLOOR_Q","^M_FLOOR","^C_FLOOR","^B_FLOOR")]
fy = collections.Counter(round(o["wMC"][1],1) for o in floors)
print(f"floor pieces: {len(floors)}   heights: {fy.most_common(5)}")
fxs=[o['wMC'][0] for o in floors]; fzs=[o['wMC'][2] for o in floors]
print(f"floor extent: X {min(fxs):.1f}..{max(fxs):.1f}   Z {min(fzs):.1f}..{max(fzs):.1f}")

DECK = fy.most_common(1)[0][0]
print(f"\ndeck height = {DECK}")

# what sits in the walking band above the deck
band = [o for o in objs if DECK + 0.3 < o["wMC"][1] < DECK + 2.6]
print(f"\nobjects at walking height ({DECK+0.3:.1f} to {DECK+2.6:.1f}): {len(band)}")
for k,v in collections.Counter(o["r<7"] for o in band).most_common(18):
    print(f"   {k.lstrip('^'):22s} {v}")

# occupancy grid of the deck, to find open floor
cells = {}
for o in floors:
    cells[(round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))] = True
obst = collections.defaultdict(int)
for o in band:
    if o["r<7"].startswith("^L_FLOOR"): continue
    obst[(round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))] += 1

print(f"\ndeck cells with floor: {len(cells)}")
open_cells = [c for c in cells if obst.get(c,0)==0]
print(f"open (no obstruction at walking height): {len(open_cells)}")
print(f"obstructed: {len(cells)-len(open_cells)}")

print("\ndeck map  (. = open floor, digits = obstacles in that cell, A = airlock)")
alk = {(round(o['wMC'][0]/2.7), round(o['wMC'][2]/2.7)) for o in objs if 'ALK' in o['r<7']}
cok = {(round(o['wMC'][0]/2.7), round(o['wMC'][2]/2.7)) for o in objs if 'COK' in o['r<7']}
gx = sorted({c[0] for c in cells}); gz = sorted({c[1] for c in cells})
for z in range(max(gz), min(gz)-1, -1):
    row = f"{z*2.7:6.1f} "
    for x in range(min(gx), max(gx)+1):
        c=(x,z)
        if c in cok: row += "C"
        elif c in alk: row += "A"
        elif c not in cells: row += " "
        elif obst.get(c,0)==0: row += "."
        else: row += str(min(9,obst[c]))
    print(row)
print("       " + "".join("^" if x==0 else " " for x in range(min(gx), max(gx)+1)) + "  (^ = centreline, up = ship front)")
