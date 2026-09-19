import hgsave, collections, math
S = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576\save.hg"
d,_ = hgsave.read(S)
objs = next(x for x in d["vLc"]["6f="]["F?0"]
            if (x.get("peI") or {}).get("DPp")=="PlayerShipBase" and x["CVX"]==7)["@ZJ"]
DECK, BODY_LO, BODY_HI = 3.1, 3.35, 5.35      # stop below the ceiling (starts 5.4)
floors = [o["wMC"] for o in objs if o["r<7"] == "^L_FLOOR_Q"]

def floor_near(x, z, r=2.0):
    return any(math.hypot(f[0]-x, f[2]-z) <= r for f in floors)

def is_partition(o):
    """floor on BOTH sides => it's an internal wall. floor on one side => hull."""
    x, y, z = o["wMC"]
    for dx, dz in ((2.6,0), (0,2.6)):
        if floor_near(x+dx, z+dz) and floor_near(x-dx, z-dz):
            return True
    return False

WALLISH = ("STORAGEPANEL","BUILDFLATPANEL","BLDWALLUNIT","TECHPANEL","BUILDSIDEPANEL",
           "WALLSCREEN","BOXEDSCREEN","BUILDHCABINET","SHELFPANEL","SERVERSTACK",
           "SERVERBOX","BUILDWORKTOP","B_WALL","M_WALL","C_WALL","B_CHEV_WALL")
band = [o for o in objs if BODY_LO < o["wMC"][1] < BODY_HI
        and any(w in o["r<7"].lstrip("^") for w in WALLISH)]
part = [o for o in band if is_partition(o)]
hull = [o for o in band if not is_partition(o)]
print(f"wall-type panels in the walking band ({BODY_LO}-{BODY_HI}): {len(band)}")
print(f"   internal partitions (floor both sides) : {len(part)}")
print(f"   outer hull (floor one side only)       : {len(hull)}  <- keep")
print("\npartitions by part:")
for k,v in collections.Counter(o["r<7"] for o in part).most_common(10):
    print(f"   {k.lstrip('^'):20s} {v}")

# fittings that would be orphaned
FIT = ("WALLLIGHT","S_WALLLIGHT","WALLHANGING","DECAL","POSTER","HOLO_SMALL",
       "CEILINGLIGHT","WALLFAN","BILLBOARD")
orph = [o for o in objs if BODY_LO < o["wMC"][1] < BODY_HI
        and any(f in o["r<7"].lstrip("^") for f in FIT) and is_partition(o)]
print(f"\nfittings that would be left floating: {len(orph)}")
print("   ", collections.Counter(o['r<7'].lstrip('^') for o in orph).most_common(6))

# usable items and where they sit
USABLE = ("TELEPORTER","BUILDTERMINAL","MAPTABLE","HEALTHSTATION","SHIELDSTATION",
          "FRE_ROOM_SCAN","BUILDSAVE","ARCHIVE","WEAPONRACK","REFINER","APPEARANCE",
          "BUILDCHAIR","BUILDBED","BUILDSIMPLEDESK","MEDTUBE","BUILDTERMINAL")
print("\nUSABLE ITEMS and their heights (deck is 3.1, standing height ~3.23):")
for o in objs:
    body = o["r<7"].lstrip("^")
    if any(u in body for u in USABLE):
        off = o["wMC"][1] - DECK
        tag = "on deck" if 0.05 < off < 0.35 else ("SUNK" if off <= 0.05 else "OFF-FLOOR")
        print(f"   {body:18s} y={o['wMC'][1]:5.2f}  ({tag})  pos {[round(v,1) for v in o['wMC']]}")
