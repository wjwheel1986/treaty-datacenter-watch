# Data Center Watch for Tribal Nations (Minnesota pilot)

*Minnesota data center proposals near reservations and in treaty cession areas.*

**Live map:** https://wjwheel1986.github.io/treaty-datacenter-watch/

An early-warning tool that finds data center proposals in Minnesota's weekly environmental review bulletin (the [EQB Monitor](https://www.eqb.state.mn.us/eqb-monitor)), checks each one against reservation, trust land and treaty cession boundaries, and shows the review stage and comment deadline with a link to the official notice.

Built for tribal environmental and natural resource staff, and useful to local advocates and reporters, so they don't have to wait for a developer or a local government to tell them a project is coming.

## Why
- Data center proposals are moving fast in Minnesota. Most project information comes from developers.
- Cities and counties often run the environmental review and are not required to consult tribes. State agencies that must consult usually come in later.
- Treaty cession areas matter, not just reservations. Off-reservation projects can affect treaty-reserved rights to hunt, fish, gather and harvest wild rice.
- Every project must be announced in the EQB Monitor, but data center notices are buried among mines, roads and feedlots. Many never say "data center" and use terms like "technology park" or code-named LLCs instead.

## How to use the map
1. Open the live map. Each dot is a project:
   - red: on or within 10 miles of a reservation or trust land
   - orange: inside a treaty cession area
   - blue: other
2. Use **"Show projects that may concern a tribal nation"** to filter to projects within 50 miles of that nation's reservation, or inside a treaty cession area that also covers part of it.
3. Use **Filter** for open comment periods, confirmed vs. possible data centers, or related power lines.
4. Click a project card for its notice history, a quote from each notice, and links to the official EQB Monitor issue.

## What's in this repo
| Path | What it is |
|---|---|
| `index.html` | The public site (one self-contained page). |
| `classic.html` | The earlier version of the site, kept as a backup. |
| `data/projects.json` | One record per project, with boundary results and notice history. |
| `data/boundaries.geojson` | Reservations and off-reservation trust land (U.S. Census TIGERweb), plus treaty cession areas (USDA Forest Service, Royce cessions), clipped to Minnesota and nearby areas. |
| `data/boundaries_by_treaty.geojson` | Same boundaries, with cession pieces merged into one area per treaty (year and nation), flagged where Ojibwe bands kept treaty rights (1837, 1842, 1854). The map uses this file. |
| `img/hero.jpg` | Lake Superior, by Courtney Celley, U.S. Fish and Wildlife Service (public domain). |
| `agent/SKILL.md` | **The agent:** goal, rules, tools and loop that Claude follows each week. |
| `agent/parse_eqb.py` | Tool: splits a Monitor issue into one entry per project. |
| `agent/geo.py` | Tool: boundary check for a point (on reservation? which treaty cession? miles to nearest reservation). |
| `agent/build_site.py` | Tool: rebuilds the map from the project table. |
| `agent/merge_treaties.py` | Merges cession pieces by treaty for the map. |
| `agent/merge_treaties.py` | Merges cession pieces by treaty for the map. |
| `eval/` | Answer key, test bulletins, predictions, scoring script and results. |

## How the agent works
An agent is an AI that uses tools in a loop to reach a goal. Here the AI does the reading and judging, and plain code does the geography:

```
get newest Monitor -> split into entries (code)
for each entry:
    decide: confirmed / possible / related / not, with reason + quote   (AI)
    if flagged: locate -> check boundaries (code) -> match existing record -> add/update
when every entry is decided: rebuild map (code) -> write weekly alert -> stop
```

To run it, open this repo in Claude (Claude Code or Cowork) and say "run Data Center Watch on the newest EQB Monitor." The skill file has the full instructions. No API key is needed.

## Evaluation
See [`eval/RESULTS.md`](eval/RESULTS.md). Short version: a keyword search for "data center" found every notice that used those words but **missed all 17 notices for possible data centers and their power lines**. The agent was tested on 26 past Monitor issues (153 entries) against a hand-checked answer key.

## Limits (please read)
- **Early warning, not an authority.** Treaty cession areas come from 1890s maps (Royce) digitized by the U.S. Forest Service and are approximate. Tribal nations, not this map, define their territories and treaty rights. What rights were kept differs by treaty.
- None of the projects tracked so far sits on reservation or trust land. Almost all of Minnesota lies inside some treaty cession area, so distance to a reservation and reserved-rights areas are the more telling measures.
- Treaty rights and tribal interests are not limited to the lines shown. Being inside or near a boundary doesn't establish legal impact.
- Project locations are city, township or county centers, not parcels.
- "Possible" projects are flagged from wording signals and need a human to confirm.
- "Tribal consultation noted: unknown" means the public notice doesn't say. That gap is itself worth asking about.
- Public data only. The tool never maps cultural, sacred or harvest sites, and it holds no tribal data. Any future tribal data would follow the CARE principles for Indigenous data governance and the tribe's own consent.
- Minnesota only for now. The data covers EQB Monitor issues from June 2025 to Nov 17, 2026.

## Data and credits
- Minnesota Environmental Quality Board, EQB Monitor (public notices)
- U.S. Census Bureau, TIGERweb AIANNH (federal reservations, off-reservation trust lands)
- USDA Forest Service, *Tribal Lands Ceded to the United States* (Royce cessions), CC BY 4.0
- Map tiles © OpenStreetMap contributors; map library Leaflet

Built by Jake Wheeler with Claude (Anthropic) for DPI-681M, Harvard Kennedy School, Fall 2026.
