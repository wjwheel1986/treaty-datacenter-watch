"""Turn the project table (data/projects_input.json) into the public map (index.html).
Adds boundary results and which tribal nations each project may concern."""
import json, os, re, datetime
from shapely.geometry import shape
from geo import check_boundaries, _F
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = json.load(open(os.path.join(ROOT, "data", "projects_input.json")))
B = json.load(open(os.path.join(ROOT, "data", "boundaries.geojson")))
# which cession areas overlap each reservation (to link projects to nations)
res = [(p["name"], g) for p, g in _F if p["layer"] == "reservation"]
ced = {p["cession"]: g for p, g in _F if p["layer"] == "ceded"}
res_ces = {n: {c for c, cg in ced.items() if g.intersects(cg)} for n, g in res}
out = []
for p in P:
    b = check_boundaries(p["lat"], p["lon"])
    p.update(b)
    mine = {c["cession"] for c in b["cessions"]}
    p["relevant_nations"] = sorted({n for n, cs in res_ces.items() if cs & mine} |
                                   ({b["nearest_reservation"]} if b["nearest_reservation_mi"] <= 50 else set()))
    p["notices"].sort(key=lambda x: x["iso"], reverse=True)
    p["last_notice"] = p["notices"][0]["iso"]
    out.append(p)
html = open(os.path.join(ROOT, "site_template.html")).read()
html = (html.replace("__PROJECTS__", json.dumps(out))
            .replace("__BOUNDARIES__", json.dumps(B))
            .replace("__UPDATED__", datetime.date.today().isoformat())
            .replace("__REPO__", os.environ.get("REPO_URL", "#")))
open(os.path.join(ROOT, "index.html"), "w").write(html)
json.dump(out, open(os.path.join(ROOT, "data", "projects.json"), "w"), indent=1)
print(len(out), "projects ->", "index.html")
for p in out:
    print(f'{p["category"]:9} {p["name"][:38]:38} on={p["on_reservation_or_trust"]} ceded={[c["year"] for c in p["cessions"]]} near={p["nearest_reservation"]} {p["nearest_reservation_mi"]}mi')
