---
name: data-center-watch
description: Weekly agent that reads Minnesota's EQB Monitor, finds data center proposals (including ones not labeled as data centers), checks them against reservation and treaty cession boundaries, updates the public map, and writes a short alert. Use when asked to "run Data Center Watch" or to check a new EQB Monitor.
---

# Treaty-Territory Data Center Watch: agent instructions

## Goal
For each new weekly EQB Monitor, find every data center proposal (and power lines built for one), record where it is relative to reservations, trust land and treaty cession areas, note the review stage and any comment deadline, update the map, and tell tribal staff what is new. Stop when every entry in the new Monitor has been decided.

## Hard rules
- Public data only. Never add cultural, sacred, or harvest sites. Never guess tribal positions.
- Every record must carry the source link and a quote copied from **the same entry**. Read ONE entry at a time; never take a location, deadline or step from a neighboring entry. (Known failure: the Oct 27, 2026 Monitor lists Harmony Group Data Center, Hermantown, right above a Calumet mining EAW with a Nov 26 deadline. Those fields do not belong to Harmony Group.)
- Treaty cession boundaries are approximate. Say so. Tribes, not maps, are the authority.
- "Tribal consultation noted" is `unknown` unless the notice says otherwise.
- When unsure, use the `possible` category with a reason. Do not drop it, and do not call it confirmed.

## Tools
1. **Get the Monitor.** The archive is at https://www.eqb.state.mn.us/eqb-monitor-archive-2026. Open the newest issue (a content.govdelivery.com link). Save its text as `{"vol","id","url","text"}` in a JSON list.
2. **Split into entries:** `python3 agent/parse_eqb.py <bulletins.json> <entries.json>` (plain code, one entry per project).
3. **Decide each entry (your judgment).** Categories:
   - `confirmed`: the entry says data center / datacenter.
   - `possible`: signals without the words. Examples: "technology park" or "technology campus," code-named LLCs (e.g., "Project ___, LLC" or an LLC named only for a county), very large single-user buildings (1M+ sq ft) with no tenant named, or the same city as a known data center.
   - `related`: transmission lines, substations or power plants the notice ties to a data center, a named tech company, or "the customer's facility."
   - `not`: everything else. EQB board-meeting announcements that mention data centers are `not` (they are not projects).
   Write one line of reasoning for every non-`not` decision.
4. **Locate:** use the city/township and county from the entry's own Location line. Use the city center and mark `location_precision: "city center (approx.)"`.
5. **Check boundaries:** `python3 agent/geo.py <lat> <lon>` returns reservation/trust land, cession areas (treaty year), and nearest reservation in miles.
6. **Match existing records** in `data/projects_input.json` (same name, or same city + same RGU + same process). If it matches, append the notice to that project's `notices` and update the step and deadline. If not, add a new project.
7. **Publish:** `python3 agent/build_site.py` rebuilds `index.html`.
8. **Alert:** write `alerts/<date>.md` that lists new or updated projects. Put first any with an open comment period that are within 10 miles of a reservation or inside a treaty cession area, with the deadline and source link.

## Loop
```
get newest Monitor -> split into entries
for each entry:
    decide category (+reason, +quote)          # AI judgment
    if not 'not': locate -> check_boundaries    # plain code
                  match existing -> add/update
when all entries decided: build site -> write alert -> stop
```
If a step fails (page will not load, location unclear), record the entry as `possible` with the problem in the reason and keep going. A human reviews `possible` items.

## Evaluation
`python3 eval/run_eval.py <predictions.json>` compares decisions to the hand-checked answer key in `eval/gold.json` and reports caught, missed, false alarms, and field errors.
