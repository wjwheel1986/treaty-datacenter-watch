"""Score agent decisions against the hand-checked answer key.
Usage: python3 eval/run_eval.py predictions.json [label]"""
import json, sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
gold = json.load(open(os.path.join(HERE, os.environ.get("GOLD", "gold.json"))))
pred = {p["key"]: p for p in json.load(open(sys.argv[1]))}
label = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
flag = lambda c: c in ("confirmed", "possible", "related")
tp = [k for k, g in gold.items() if flag(g) and flag(pred.get(k, {}).get("category", "not"))]
fn = [k for k, g in gold.items() if flag(g) and not flag(pred.get(k, {}).get("category", "not"))]
fp = [k for k, g in gold.items() if not flag(g) and flag(pred.get(k, {}).get("category", "not"))]
exact = sum(1 for k, g in gold.items() if pred.get(k, {}).get("category", "not") == g)
def by(cat):
    ks = [k for k, g in gold.items() if g == cat]
    return f"{sum(1 for k in ks if flag(pred.get(k,{}).get('category','not')))}/{len(ks)}"
# field check: the known trap (Harmony Group must not inherit Calumet / Nov 26 fields)
trap = [p for k, p in pred.items() if k.startswith("50-43|Harmony")]
trap_ok = bool(trap) and "calumet" not in json.dumps(trap[0]).lower() and "november 26" not in json.dumps(trap[0]).lower()
r = {"label": label, "entries": len(gold), "flagged_correctly": len(tp), "missed": len(fn), "false_alarms": len(fp),
     "recall": round(len(tp) / max(1, len(tp) + len(fn)), 2), "precision": round(len(tp) / max(1, len(tp) + len(fp)), 2),
     "exact_category_match": f"{exact}/{len(gold)}", "confirmed_caught": by("confirmed"), "possible_caught": by("possible"),
     "related_caught": by("related"), "harmony_calumet_trap_passed": trap_ok,
     "missed_items": fn, "false_alarm_items": fp}
print(json.dumps(r, indent=1))
