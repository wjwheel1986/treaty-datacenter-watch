"""Boundary tools: plain code (no AI). Given a point, report reservation/trust land,
treaty cession areas (merged by treaty), and distance to every nearby reservation."""
import json, math, os
from shapely.geometry import shape, Point
from shapely.ops import nearest_points
HERE = os.path.dirname(os.path.abspath(__file__))
_B = json.load(open(os.path.join(HERE, "..", "data", "boundaries_by_treaty.geojson")))
_F = [(f["properties"], shape(f["geometry"])) for f in _B["features"]]

def _miles(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(lon2-lon1)/2)**2
    return 2*r*math.asin(math.sqrt(a))

def check_boundaries(lat, lon):
    pt = Point(lon, lat)
    on, treaties, dists = None, [], {}
    for p, g in _F:
        if p["layer"] in ("reservation", "trust_land") and g.contains(pt):
            on = p["name"]
        if p["layer"] == "reservation":
            q = nearest_points(g, pt)[0]
            d = 0.0 if g.contains(pt) else _miles(lat, lon, q.y, q.x)
            dists[p["name"]] = round(min(d, dists.get(p["name"], 1e9)), 1)
        elif p["layer"] == "ceded" and g.contains(pt):
            treaties.append({k: p[k] for k in ("label", "year", "nation", "rights_kept", "treaty_link")})
    treaties.sort(key=lambda c: c["year"] or 9999)
    near = min(dists, key=dists.get)
    return {"on_reservation_or_trust": on, "cessions": treaties, "reservation_miles": dists,
            "nearest_reservation": near, "nearest_reservation_mi": dists[near]}

if __name__ == "__main__":
    import sys
    r = check_boundaries(float(sys.argv[1]), float(sys.argv[2]))
    r["reservation_miles"] = dict(sorted(r["reservation_miles"].items(), key=lambda x: x[1])[:5])
    print(json.dumps(r, indent=1))
