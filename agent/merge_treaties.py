"""Merge Royce cession pieces into one labeled area per treaty (year + nation group)."""
import json, os, re
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
B = json.load(open(os.path.join(ROOT, "data", "boundaries.geojson")))
def nation(h):
    h = h or ""
    if re.search(r"Chippewa", h): return "Ojibwe (Chippewa)"
    if re.search(r"Sioux|Medewa", h): return "Dakota (Sioux)" if "Yankton" not in h else "Yankton (Sioux)"
    if "Winnebago" in h: return "Ho-Chunk (Winnebago)"
    if "Menomin" in h: return "Menominee"
    if re.search(r"Iowa|Oto|Omaha|Sauk", h): return "Several nations"
    return h[:30] or "Unknown"
RIGHTS = {("1837", "Ojibwe (Chippewa)"), ("1842", "Ojibwe (Chippewa)"), ("1854", "Ojibwe (Chippewa)")}
groups = {}
keep = []
for f in B["features"]:
    p = f["properties"]
    if p["layer"] != "ceded":
        keep.append(f); continue
    key = (str(p["year"]), nation(p["historical_tribe"]))
    g = groups.setdefault(key, {"geoms": [], "cessions": [], "hist": set(), "treaty_link": p.get("treaty_link")})
    g["geoms"].append(shape(f["geometry"])); g["cessions"].append(p["cession"]); g["hist"].add(p["historical_tribe"] or "")
for (yr, nat), g in groups.items():
    geom = unary_union(g["geoms"]).buffer(0).simplify(0.004)
    label = f"{yr if yr!='None' else 'Undated'} treaty · {nat}"
    keep.append({"type": "Feature", "geometry": mapping(geom), "properties": {
        "layer": "ceded", "year": None if yr == "None" else int(yr), "nation": nat, "label": label,
        "rights_kept": (yr, nat) in RIGHTS, "cessions": sorted(g["cessions"]),
        "historical_tribe": "; ".join(sorted(h for h in g["hist"] if h))[:300], "treaty_link": g["treaty_link"],
        "source": "USDA Forest Service, Tribal Lands Ceded to the United States (Royce cessions), CC BY 4.0. Merged by treaty year and nation. APPROXIMATE."}})
json.dump({"type": "FeatureCollection", "features": keep}, open(os.path.join(ROOT, "data", "boundaries_by_treaty.geojson"), "w"))
print(len(groups), "treaty areas:", sorted(k[0]+" "+k[1] for k in groups))
