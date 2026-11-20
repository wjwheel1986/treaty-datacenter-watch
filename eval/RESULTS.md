# Evaluation results

## Test set
- **26 past EQB Monitor issues, 152 entries** (June 2025 to Nov 17, 2026):
  - every issue that contains a known data center, possible data center, or related power line
  - three "trap" issues
  - four randomly chosen ordinary issues
- **Answer key (`gold.json`):** hand-checked labels for each entry.
  - 8 confirmed data center notices
  - 15 possible (data centers described as "technology park," "industrial," or code-named LLCs)
  - 2 related power lines
  - 127 not data centers
- **Trap cases:**
  - Oct 27, 2026: Harmony Group Data Center (Hermantown, petition) is listed directly above a Calumet mining EAW with a Nov 26 deadline. The agent must not attach those fields to Harmony Group. An earlier web search made exactly this mistake.
  - EQB board-meeting announcements that mention data centers but are not projects.

## Results

| | Keyword search (no AI) | Agent, run 1 |
|---|---|---|
| Confirmed data centers caught | 8/8 | 8/8 |
| Possible data centers caught | **0/16** | **16/16** |
| Related power lines caught | 0/2 | 2/2 |
| Recall (share of real items flagged) | 0.31 | **1.00** |
| False alarms | 0 | 4 |
| Precision (share of flags that were right) | 1.00 | 0.87 |
| Harmony/Calumet trap passed | yes | yes |

Scored against the adjudicated key (see below). Against the original key the agent had recall 1.00, precision 0.83 and 5 "false alarms," because one of them was not actually false.

**Run the scoring yourself:** `GOLD=gold_adjudicated.json python3 eval/run_eval.py eval/pred_agent_run1.json`

## What we learned
1. **Keyword search is not enough.** About two-thirds of the relevant notices never say "data center." They say "technology park," "technology center," "light industrial," or use code-named LLCs ("Project Deacon, LLC," "MNLCO Dakota County Two, LLC"). Power lines are filed for "the customer's facility."
2. **The agent found something the answer key missed.** It flagged **Project Skyway** (Pine Island): about 482 acres of "Technology Center," and the destination of a 345 kV line co-applied by a Google subsidiary. After review, the answer key was corrected (`gold_adjudicated.json`). This is the main reason to have an AI read every entry.
3. **The 4 remaining false alarms come from one rule.** All four (Monticello Industrial ×2, Inver Grove Heights Northwest Expansion ×2) were flagged only because they share a city with a known data center project. The agent itself named these as the most likely false alarms. Next step: tighten that rule so a shared city alone is not enough.
4. **Field mixing was avoided** by reading one entry at a time. The Harmony Group record kept Hermantown and no Nov 26 deadline.

## Limits of this test
- The agent's rules were written by someone who had already seen these notices, so this is closer to a training-set check than a true blind test. The real test is the next Monitors (Nov 24 onward).
- Two runs only. More runs would be better.
- Locations are city centers, so distances are approximate. Hermantown comes out at 10.5 miles from the Fond du Lac Reservation, right at the 10-mile alert threshold.
- Boundary results were spot-checked by hand for Hermantown (inside the 1854 cession, near Fond du Lac), not for every project.

## Run 2 (consistency)
A second, independent agent run (same instructions, same test set):
- Caught all 26 real items again. Recall 1.00, precision 0.84, 5 false alarms. Harmony/Calumet trap passed.
- **Agreed with run 1 on 151 of 152 entries.** The one difference was Summit Lake Project (solar and battery storage in the same townships as the Nobles County data center), which run 2 flagged under the same-city rule.
- Same conclusion: the agent is consistent, and its false alarms come from the same-city rule.

`GOLD=gold_adjudicated.json python3 eval/run_eval.py eval/pred_agent_run2.json`
