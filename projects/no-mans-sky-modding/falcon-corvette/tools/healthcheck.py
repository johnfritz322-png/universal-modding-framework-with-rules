import hgsave, math, collections, json
S = r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576\save.hg"
d, _ = hgsave.read(S)
bases = d["vLc"]["6f="]["F?0"]
b7 = next(x for x in bases if (x.get("peI") or {}).get("DPp")=="PlayerShipBase" and x["CVX"]==7)
objs = b7["@ZJ"]
mag = lambda v: math.dist((0,0,0), v)
issues = []

# 1. degenerate / malformed transforms
for o in objs:
    if any(not math.isfinite(c) for c in o["wMC"]+o["wJ0"]+o["aNu"]):
        issues.append(("NON-FINITE", o["r<7"], o["wMC"]))
    if mag(o["wJ0"]) < 1e-6 or mag(o["aNu"]) < 1e-6:
        issues.append(("ZERO VECTOR", o["r<7"], o["wMC"]))
    else:
        u, a = o["wJ0"], o["aNu"]
        dot = sum(x*y for x,y in zip(u,a))/(mag(u)*mag(a))
        if abs(dot) > 0.05:
            issues.append(("UP/AT NOT PERPENDICULAR", o["r<7"], round(dot,3)))
    if abs(mag(o["aNu"]) - 1.0) > 0.02:
        issues.append(("AT NOT UNIT", o["r<7"], round(mag(o["aNu"]),3)))

# 2. strays far from the hull
xs=[o["wMC"][0] for o in objs]; ys=[o["wMC"][1] for o in objs]; zs=[o["wMC"][2] for o in objs]
cx, cz = (min(xs)+max(xs))/2, (min(zs)+max(zs))/2
far = [o for o in objs if math.hypot(o["wMC"][0]-cx, o["wMC"][2]-cz) > 40 or o["wMC"][1] < -2 or o["wMC"][1] > 20]
print(f"objects: {len(objs)}")
print(f"envelope: X {min(xs):.1f}..{max(xs):.1f}  Y {min(ys):.1f}..{max(ys):.1f}  Z {min(zs):.1f}..{max(zs):.1f}")
print(f"strays far outside the hull: {len(far)}")
for o in far[:8]: print("   ", o["r<7"], [round(v,1) for v in o["wMC"]])

# 3. functional parts present?
need = {"cockpit": ["COK"], "landing gear": ["LND"], "airlock": ["ALK"],
        "hab": ["HAB"], "generator": ["GEN"], "turret": ["TUR"]}
print("\nfunctional parts:")
for label, keys in need.items():
    hits = [o["r<7"] for o in objs if any(k in o["r<7"] for k in keys)]
    print(f"   {label:14s} {len(hits)}  {sorted(set(hits))}")

# 4. structural (capped at 100) vs decoration (uncapped)
struct = [o for o in objs if o["r<7"].startswith("^B_") or o["r<7"]=="^U_PARAGON"]
print(f"\nstructural/^B_ count: {len(struct)}  (game cap is 100)")

# 5. parts unknown to this save's other builds (possible PS5-only)
known = set()
for b in bases:
    if b is b7: continue
    for o in b.get("@ZJ") or []: known.add(o["r<7"])
exp = json.load(open(r"C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\outputs\NMS-Corvette-Exports-20260918\Corvette-1-Original.json"))["objects"]
for e in exp: known.add(e["ObjectID"])
novel = collections.Counter(o["r<7"] for o in objs if o["r<7"] not in known)
print(f"\npart types not seen in any of your other builds: {len(novel)}")
for k,v in novel.most_common(12): print(f"   {k.lstrip('^'):22s} {v}")

print(f"\nmalformed-transform issues: {len(issues)}")
for i in issues[:10]: print("   ", i)
