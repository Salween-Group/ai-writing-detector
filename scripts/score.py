#!/usr/bin/env python3
"""
score.py - turn detected AI-writing patterns into the 0-100 score.

Detection stays with the model: deciding that a sentence really is significance
inflation, and not a human writing with conviction, is judgement. The arithmetic
that follows is not, and doing it by hand gives a different answer on different
runs of the same text - which is the one thing a scoring tool cannot afford.

It reads the penalty table and the category caps OUT OF SKILL.md rather than
carrying its own copy, so the numbers can never disagree with the documented ones.
Edit a penalty in SKILL.md and this follows; no second place to update.

Usage:
    python scripts/score.py findings.json [--skill SKILL.md] [--json out.json]
    python scripts/score.py --self-test

findings.json:
    {
      "banned_words":   12,           # total occurrences, -5 each
      "originality":    -5,           # optional, 0 or -5
      "findings": [
        {"id": "1",  "occurrences": 3},
        {"id": "27", "occurrences": 1, "category": "language & grammar"},
        {"id": "L2", "occurrences": 2}
      ]
    }

`category` is required only for patterns #25-39, where SKILL.md says the violation
counts toward content patterns OR language & grammar "whichever is more relevant" -
a judgement the model makes and this script will not guess. Everything else is
derived from the caps table.

Exit 0 on a clean run, 1 on a malformed findings file.
"""
import argparse
import json
import os
import re
import sys

BANNED_EACH = -5
STACK_MULTIPLE = 2          # repeats of one pattern cap at 2x its base penalty
SEVERITY_THRESHOLD = 150    # raw deductions above this add the extra penalty
SEVERITY_EXTRA = -10
AMBIGUOUS = range(25, 40)   # SKILL.md: content OR language, model decides
AMBIGUOUS_CHOICES = ("content patterns", "language & grammar")


def load_rules(skill_md):
    """Parse penalties and category caps out of SKILL.md."""
    t = open(skill_md, encoding="utf-8").read()

    penalties = {}
    for pid, _name, pts in re.findall(
            r"(?m)^\*\*([0-9]+|[LES][0-9]+)\.\s*([^*]+?)\*\*\s*\((-?\d+)[^)]*\)", t):
        penalties[pid] = int(pts)

    caps, covers = {}, {}
    for name, what, cap in re.findall(
            r"(?m)^\|\s*\*\*([^*]+)\*\*\s*\|([^|]*)\|\s*(-\d+)\s*\|", t):
        key = name.strip().lower()
        caps[key] = int(cap)
        covers[key] = what.strip()

    # category for a numbered pattern, from the caps table's "what it covers"
    ranges = {}
    for key, what in covers.items():
        for lo, hi in re.findall(r"#(\d+)-(\d+)", what):
            for n in range(int(lo), int(hi) + 1):
                ranges.setdefault(n, key)
    return penalties, caps, ranges


def category_for(pid, ranges, supplied):
    if pid[0] in "LES":
        return "channel-specific patterns"
    n = int(pid)
    if n in AMBIGUOUS:
        if supplied and supplied.lower() in AMBIGUOUS_CHOICES:
            return supplied.lower()
        # SKILL.md leaves this to judgement; default to the stricter-capped
        # bucket and say so, rather than silently picking.
        return "content patterns"
    return ranges.get(n)


def score(data, penalties, caps, ranges):
    per_cat, raw, notes, rows = {}, 0, [], []

    banned = int(data.get("banned_words", 0) or 0)
    if banned:
        d = banned * BANNED_EACH          # negative
        raw += -d                          # raw is a positive magnitude
        per_cat["banned vocabulary"] = per_cat.get("banned vocabulary", 0) + d
        rows.append(("banned vocabulary", f"{banned} occurrence(s)", d))

    for f in data.get("findings", []):
        pid = str(f.get("id", "")).strip().lstrip("#")
        occ = max(1, int(f.get("occurrences", 1) or 1))
        if pid not in penalties:
            raise ValueError(f"unknown pattern id {pid!r} - not found in SKILL.md")
        base = penalties[pid]
        stacked = max(base * occ, base * STACK_MULTIPLE)   # negatives: max() is the floor
        cat = category_for(pid, ranges, f.get("category"))
        if cat is None:
            raise ValueError(f"no category for pattern #{pid} - check the caps table")
        if pid.isdigit() and int(pid) in AMBIGUOUS and not f.get("category"):
            notes.append(f"#{pid} had no category supplied; counted as content patterns "
                         "(SKILL.md leaves #25-39 to judgement)")
        per_cat[cat] = per_cat.get(cat, 0) + stacked
        raw += -stacked
        rows.append((cat, f"#{pid} x{occ}", stacked))

    orig = int(data.get("originality", 0) or 0)
    if orig:
        per_cat["originality"] = per_cat.get("originality", 0) + orig
        raw += -orig

    capped, hit = {}, []
    for cat, total in per_cat.items():
        cap = caps.get(cat)
        if cap is None:
            raise ValueError(f"no cap defined for category {cat!r}")
        # <= not <: a category landing exactly on its cap has reached it, and
        # SKILL.md says to mark reached categories in the summary table.
        if total <= cap:
            capped[cat] = cap
            hit.append(cat)
        else:
            capped[cat] = total

    deductions = sum(capped.values())
    severity = SEVERITY_EXTRA if raw > SEVERITY_THRESHOLD else 0
    final = max(0, 100 + deductions + severity)
    return {"score": final, "raw_deductions": raw, "capped_total": deductions,
            "severity_penalty": severity, "by_category": capped,
            "caps_reached": sorted(hit), "rows": rows, "notes": notes}


BANDS = [(90, "Human-sounding. Clean."), (70, "Minor AI tells. Quick fixes needed."),
         (50, "Obvious AI patterns. Significant rewrite needed."),
         (30, "Heavy AI patterns. Major rewrite."),
         (0, "Reads like raw ChatGPT output. Full rewrite.")]


def band(s):
    return next(label for lo, label in BANDS if s >= lo)


def self_test(skill_md):
    """Prove the documented worked examples still come out right."""
    pen, caps, ranges = load_rules(skill_md)
    cases = [
        ("clean text", {"findings": []}, 100),
        ("one -10 pattern once", {"findings": [{"id": "1", "occurrences": 1}]}, 90),
        ("stacking caps at 2x", {"findings": [{"id": "1", "occurrences": 5}]}, 80),
        ("banned cap at -15", {"banned_words": 10}, 85),
        ("every cap saturated + severity",
         {"banned_words": 25,
          "findings": [{"id": str(i), "occurrences": 5} for i in range(1, 25)],
          "originality": -5}, 0),
    ]
    ok = True
    for name, data, expect in cases:
        got = score(data, pen, caps, ranges)["score"]
        flag = "ok " if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"  {flag} {name:34} expected {expect:>3}  got {got:>3}")
    # SKILL.md states the worst case as the sum of the caps alone: 100 - 105 = -5.
    # Check the caps in the table still add up to that, so a future cap edit that
    # silently changes the floor is caught here rather than in a client report.
    caps_only = sum(caps.values())
    documented = -105
    if caps_only != documented:
        print(f"  FAIL caps now sum to {caps_only}, but SKILL.md's worst case is "
              f"stated as 100 {documented:+d} = {100 + documented} - update the prose")
        ok = False
    else:
        print(f"  ok  caps sum to {caps_only}: 100 {caps_only:+d} = {100 + caps_only}, "
              f"floored to 0 (matches SKILL.md)")
    print(f"  ... with the severity override a saturated text reaches "
          f"{100 + caps_only + SEVERITY_EXTRA}, also floored to 0")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings", nargs="?")
    ap.add_argument("--skill", default=None)
    ap.add_argument("--json")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    skill = a.skill or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    os.pardir, "SKILL.md")
    if not os.path.isfile(skill):
        print(f"cannot find SKILL.md at {skill} - pass --skill")
        return 1

    if a.self_test:
        print("score.py self-test (rules read from SKILL.md):")
        return 0 if self_test(skill) else 1

    if not a.findings:
        print(__doc__)
        return 1

    pen, caps, ranges = load_rules(skill)
    try:
        data = json.load(open(a.findings, encoding="utf-8"))
        r = score(data, pen, caps, ranges)
    except (ValueError, json.JSONDecodeError) as e:
        print(f"findings file rejected: {e}")
        return 1

    print(f"AI Writing Score: {r['score']}/100  - {band(r['score'])}")
    print(f"  raw deductions {r['raw_deductions']}, after caps {r['capped_total']}"
          + (f", severity {r['severity_penalty']}" if r["severity_penalty"] else ""))
    for cat in sorted(r["by_category"]):
        mark = "  (CAP REACHED)" if cat in r["caps_reached"] else ""
        print(f"    {cat:28} {r['by_category'][cat]:>4}{mark}")
    for n in r["notes"]:
        print(f"  note: {n}")
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
