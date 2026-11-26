#!/usr/bin/env python3
"""Validate every scenario in the repository.

    pip install jsonschema
    python scripts/validate.py

Checks, per scenario folder under scenarios/:
  * responses.jsonl, questions.json and labels.json exist, are UTF-8 and match schemas/
  * participant ids are unique and identical in responses and labels
  * every answer belongs to a declared question; multiple-choice answers are valid choices
  * every id used in labels exists; no pair is labelled twice for the same question; a 'source' belongs to its pair
  * 'questions' named in a label exist
Exit status is 0 when everything passes, 1 otherwise.
"""
import json
import os
import sys

try:
    import jsonschema
except ImportError:
    sys.exit("This script needs the 'jsonschema' package: pip install jsonschema")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from expand_labels import expand  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_scenario(folder, schemas):
    errors = []
    name = os.path.basename(folder)

    def err(msg):
        errors.append("%s: %s" % (name, msg))

    paths = {k: os.path.join(folder, k) for k in ("responses.jsonl", "questions.json", "labels.json")}
    for p in paths.values():
        if not os.path.exists(p):
            err("missing file %s" % os.path.basename(p))
    if errors:
        return errors
    try:
        questions = load_json(paths["questions.json"])
        labels = load_json(paths["labels.json"])
        with open(paths["responses.jsonl"], encoding="utf-8") as f:
            responses = [json.loads(line) for line in f if line.strip()]
    except (ValueError, UnicodeDecodeError) as e:
        return ["%s: cannot read a file: %s" % (name, e)]

    for doc, schema, label in ((questions, "questions", "questions.json"), (labels, "labels", "labels.json")):
        for e in jsonschema.Draft202012Validator(schemas[schema]).iter_errors(doc):
            err("%s: %s (at %s)" % (label, e.message, "/".join(map(str, e.absolute_path))))
    for i, r in enumerate(responses, 1):
        for e in jsonschema.Draft202012Validator(schemas["responses"]).iter_errors(r):
            err("responses.jsonl line %d: %s" % (i, e.message))
    if errors:
        return errors

    if questions.get("scenario") != name or labels.get("scenario") != name:
        err("'scenario' in questions.json and labels.json must equal the folder name")
    qmap = {q["id"]: q for q in questions["questions"]}
    if len(qmap) != len(questions["questions"]):
        err("duplicate question ids")
    ids = [r["id"] for r in responses]
    if len(set(ids)) != len(ids):
        err("duplicate ids in responses.jsonl")
    pids = [p["id"] for p in labels["participants"]]
    if len(set(pids)) != len(pids):
        err("duplicate ids in labels.json participants")
    if set(ids) != set(pids):
        err("participants in labels.json differ from ids in responses.jsonl")
    for r in responses:
        for qid, ans in r["answers"].items():
            q = qmap.get(qid)
            if q is None:
                err("%s answers unknown question %s" % (r["id"], qid))
            elif q["type"] == "mcq" and ans not in q["choices"]:
                err("%s: answer %r to %s is not one of %s" % (r["id"], ans, qid, q["choices"]))
    for q in qmap.values():
        if q["type"] == "mcq" and q["answer_key"] not in q["choices"]:
            err("%s: answer_key not among choices" % q["id"])
    known = set(pids)
    for entry in labels["relations"]:
        members = entry.get("members", []) + [m for g in entry.get("between", []) for m in g]
        for m in members:
            if m not in known:
                err("label refers to unknown participant %s" % m)
        for qid in entry.get("questions", []):
            if qid not in qmap:
                err("label refers to unknown question %s" % qid)
    if errors:
        return errors
    try:
        rows = expand(labels)
    except ValueError as e:
        return ["%s: %s" % (name, e)]
    for row in rows:
        if row["source"] and row["source"] not in (row["a"], row["b"]):
            err("source %s is not part of pair %s-%s" % (row["source"], row["a"], row["b"]))
    return errors


def main():
    schemas = {k: load_json(os.path.join(ROOT, "schemas", k + ".schema.json")) for k in ("responses", "questions", "labels")}
    base = os.path.join(ROOT, "scenarios")
    folders = sorted(os.path.join(base, d) for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))
    errors = []
    for f in folders:
        errors.extend(check_scenario(f, schemas))
    for e in errors:
        print("ERROR", e)
    print("%d scenario(s) checked, %d problem(s)" % (len(folders), len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
