"""Boundary tools: plain code (no AI). Given a point, report reservation/trust land,
treaty cession areas, and distance to the nearest reservation."""
import json, math, os
from shapely.geometry import shape, Point
HERE = os.path.dirname(os.path.abspath(__file__))
_B = json.load(open(os.path.join(HERE, "..", "data", "boundaries.geojson")))
_F = [(f["properties"], shape(f["geometry"])) for f in _B["features"]]

def _miles(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.asin(math.sqrt(a))

def check_boundaries(lat, lon):
    pt = Point(lon, lat)
    on, ceded, best = None, [], (None, 1e9)
    for p, g in _F:
        if p["layer"] in ("reservation", "trust_land"):
            if g.contains(pt):
                on = p["name"]
            if p["layer"] == "reservation":
                # nearest point on the boundary, measured in miles
                from shapely.ops import nearest_points
                q = nearest_points(g, pt)[0]
                d = 0 if g.contains(pt) else _miles(lat, lon, q.y, q.x)
                if d < best[1]:
                    best = (p["name"], d)
        elif p["layer"] == "ceded" and g.contains(pt):
            ceded.append({k: p[k] for k in ("cession", "year", "historical_tribe", "present_day_tribes", "treaty_link")})
    ceded.sort(key=lambda c: c["year"] or 9999)
    return {"on_reservation_or_trust": on, "cessions": ceded,
            "nearest_reservation": best[0], "nearest_reservation_mi": round(best[1], 1)}

if __name__ == "__main__":
    import sys
    print(json.dumps(check_boundaries(float(sys.argv[1]), float(sys.argv[2])), indent=1))
