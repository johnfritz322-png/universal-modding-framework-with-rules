import hgsave, collections, math
S = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576\save.hg"
d,_ = hgsave.read(S)
objs = next(x for x in d["vLc"]["6f="]["F?0"]
            if (x.get("peI") or {}).get("DPp")=="PlayerShipBase" and x["CVX"]==7)["@ZJ"]
DECK = 3.1

# structure / skin / lighting / decals: part of the ship, never touch
STRUCTURE = ("STORAGEPANEL","BUILDFLATPANEL","WALLLIGHT","S_WALLLIGHT","DECAL","L_FLOOR",
             "TECHPANEL","HOLOFILES","BILLBOARD","CEILINGLIGHT","POSTER","WALLFAN",
             "B_","U_PARAGON","BLDWALLUNIT","ARCHIVE","BUILDSAVE","WEAPONRACK","DECAL_BLUESYS")
def is_structure(pid):
    body = pid.lstrip("^")
    return any(body.startswith(s) or s in body for s in STRUCTURE)

floor_cells = {(round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))
               for o in objs if o["r<7"] == "^L_FLOOR_Q"}

clutter = [o for o in objs
           if not is_structure(o["r<7"])
           and DECK + 0.2 < o["wMC"][1] < DECK + 2.6
           and (round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7)) in floor_cells]
print(f"free-standing objects standing on the deck: {len(clutter)}")
for k,v in collections.Counter(o["r<7"] for o in clutter).most_common(25):
    print(f"   {k.lstrip('^'):22s} {v}")

# open cells for amenities
occupied = collections.defaultdict(int)
for o in objs:
    if o["r<7"] == "^L_FLOOR_Q": continue
    if DECK + 0.2 < o["wMC"][1] < DECK + 3.0:
        occupied[(round(o["wMC"][0]/2.7), round(o["wMC"][2]/2.7))] += 1
free = sorted([c for c in floor_cells if occupied.get(c,0)==0], key=lambda c:(abs(c[0]), c[1]))
print(f"\ncompletely free deck cells available for amenities: {len(free)}")
print("   (x, z) ->", [(round(c[0]*2.7,1), round(c[1]*2.7,1)) for c in free])
