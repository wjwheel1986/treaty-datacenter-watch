"""Turn the project table (data/projects_input.json) into the public map (index.html)."""
import json, os, datetime
from geo import check_boundaries, _F
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = json.load(open(os.path.join(ROOT, "data", "projects_input.json")))
B = json.load(open(os.path.join(ROOT, "data", "boundaries_by_treaty.geojson")))
# notices that may describe the same physical site (reviewed by hand; see README)
SITE = {"hermantown-dc": "Hermantown", "harmony-group": "Hermantown", "hermantown-auar": "Hermantown", "stlouis-230": "Hermantown",
        "project-skyway": "Pine Island", "skyway-345": "Pine Island"}
res = [(p["name"], g) for p, g in _F if p["layer"] == "reservation"]
ced = [(p["label"], g) for p, g in _F if p["layer"] == "ceded"]
res_treaties = {n: {lab for lab, cg in ced if g.intersects(cg)} for n, g in res}
out = []
for p in P:
    b = check_boundaries(p["lat"], p["lon"]); p.update(b)
    mine = {c["label"] for c in b["cessions"]}
    p["near_nations"] = sorted(n for n, d in b["reservation_miles"].items() if d <= 50)
    p["treaty_nations"] = sorted(n for n, ts in res_treaties.items() if ts & mine and n not in p["near_nations"])
    p["site"] = SITE.get(p["id"])
    p["same_site_as"] = [q["name"] for q in P if q is not p and SITE.get(q["id"]) and SITE.get(q["id"]) == p["site"]]
    p["notices"].sort(key=lambda x: x["iso"], reverse=True)
    p["last_notice"] = p["notices"][0]["iso"]
    out.append(p)
html = open(os.path.join(ROOT, "site_template.html")).read()
html = (html.replace("__PROJECTS__", json.dumps(out)).replace("__BOUNDARIES__", json.dumps(B))
            .replace("__UPDATED__", datetime.date.today().isoformat())
            .replace("__REPO__", os.environ.get("REPO_URL", "https://github.com/wjwheel1986/treaty-datacenter-watch")))
open(os.path.join(ROOT, "index.html"), "w").write(html)
json.dump(out, open(os.path.join(ROOT, "data", "projects.json"), "w"), indent=1)
print(len(out), "projects")
for p in out:
    print(f'{p["id"]:22} {[c["label"] for c in p["cessions"]]} near={p["near_nations"][:3]} treatyN={len(p["treaty_nations"])} site={p["site"]}')
