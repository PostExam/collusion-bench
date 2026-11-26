#!/usr/bin/env python3
"""Expand a scenario's labels.json into one row per pair of participants.

Usage:
    python scripts/expand_labels.py scenarios/01-lexical-copy-spectrum            # JSON Lines
    python scripts/expand_labels.py scenarios/01-lexical-copy-spectrum --csv      # CSV

Every pair of participants gets at least one row (several if the pair is labelled separately
for different questions). Pairs not mentioned in labels.json receive the scenario's default
(normally: independent / not_copied).
"""
import csv
import itertools
import json
import os
import sys


def _pairs_of(entry):
    """Yield (a, b) pairs described by one relation entry."""
    if "members" in entry:
        for a, b in itertools.combinations(entry["members"], 2):
            yield a, b
    elif "between" in entry:
        g1, g2 = entry["between"]
        for a in g1:
            for b in g2:
                if a != b:
                    yield a, b
    else:
        raise ValueError("a relation needs 'members' or 'between': %r" % (entry,))


def expand(labels):
    """Return a list of dicts: a, b, relation, ground_truth, source, questions, note.

    A pair may appear in several entries if each entry names different 'questions';
    an entry without 'questions' applies to every question and cannot be combined
    with another entry for the same pair.
    """
    ids = sorted(p["id"] for p in labels["participants"])
    default = labels["default"]
    assigned = {}
    for entry in labels["relations"]:
        for a, b in _pairs_of(entry):
            key = tuple(sorted((a, b)))
            assigned.setdefault(key, []).append(entry)
    for key, entries in assigned.items():
        if len(entries) > 1:
            seen = set()
            for e in entries:
                qs = e.get("questions")
                if not qs or seen & set(qs):
                    raise ValueError("pair %s-%s is labelled more than once for the same question(s)" % key)
                seen |= set(qs)
    rows = []
    for a, b in itertools.combinations(ids, 2):
        entries = assigned.get((a, b))
        if not entries:
            rows.append(dict(a=a, b=b, relation=default["relation"], ground_truth=default["ground_truth"],
                             source="", questions="", note=""))
            continue
        for entry in entries:
            rows.append(dict(a=a, b=b, relation=entry["relation"], ground_truth=entry["ground_truth"],
                             source=entry.get("source", ""), questions=" ".join(entry.get("questions", [])),
                             note=entry.get("note", "")))
    return rows


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    folder = argv[1]
    with open(os.path.join(folder, "labels.json"), encoding="utf-8") as f:
        labels = json.load(f)
    rows = expand(labels)
    if "--csv" in argv:
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    else:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
