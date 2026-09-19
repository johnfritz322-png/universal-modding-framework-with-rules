import hgsave, collections, math
S = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576\save.hg"
d,_ = hgsave.read(S)
objs = next(x for x in d["vLc"]["6f="]["F?0"]
            if (x.get("peI") or {}).get("DPp")=="PlayerShipBase" and x["CVX"]==7)["@ZJ"]
DECK, C = 3.1, 2.7
cell = lambda o: (round(o["wMC"][0]/C), round(o["wMC"][2]/C))
floor = {cell(o) for o in objs if o["r<7"]=="^L_FLOOR_Q"}

# a cell is blocked if a solid panel stands in it at body height
SOLID = ("STORAGEPANEL","BUILDFLATPANEL","BLDWALLUNIT","TECHPANEL","B_WALL",
         "BUILDWORKTOP","SERVERSTACK","BUILDHCABINET","SHELFPANEL","B_CARRIAGEWHEEL")
blocked = collections.Counter()
for o in objs:
    if DECK+0.3 < o["wMC"][1] < DECK+2.2 and any(s in o["r<7"].lstrip("^") for s in SOLID):
        blocked[cell(o)] += 1
walk = {c for c in floor if blocked.get(c,0)==0}

alk = [cell(o) for o in objs if "ALK" in o["r<7"]]
tp  = [cell(o) for o in objs if o["r<7"]=="^TELEPORTER"]
cok = [cell(o) for o in objs if "COK" in o["r<7"]]
hab = [cell(o) for o in objs if "HAB" in o["r<7"]]

start = next((a for a in alk if a in walk), None)
print(f"airlock cells {alk}  teleporter {tp}  cockpit {cok}  hab {hab}")
print(f"floor cells {len(floor)}  walkable {len(walk)}  blocked {len(floor)-len(walk)}")

seen, q = set(), [start] if start else []
if start: seen.add(start)
while q:
    c = q.pop()
    for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
        n=(c[0]+dx, c[1]+dz)
        if n in walk and n not in seen:
            seen.add(n); q.append(n)
print(f"\nreachable from the airlock: {len(seen)} of {len(walk)} walkable cells")
for name, cs in (("teleporter", tp), ("cockpit", cok), ("hab", hab)):
    for c in cs:
        state = "REACHABLE" if c in seen else ("blocked in place" if c in floor else "no floor there")
        print(f"   {name:11s} cell {c} -> {state}")

iso = sorted(walk - seen)
print(f"\nwalkable but CUT OFF from the airlock: {len(iso)} cells")
if iso:
    print("   ", [(round(c[0]*C,1), round(c[1]*C,1)) for c in iso][:20])
