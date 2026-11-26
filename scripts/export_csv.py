#!/usr/bin/env python3
"""Export scenarios to CSV in the layout of a Google Forms response sheet.

    python scripts/export_csv.py scenarios out/                # every scenario
    python scripts/export_csv.py scenarios/08-mcq-answer-copying out/

Columns: Timestamp, Email, Name, then one column per question (its 'header').
The JSONL files stay the source of truth: never edit the CSVs by hand.

Optional: --column-notes also writes <scenario>.column-notes.txt, listing for every
question column its type (text / mcq / code) and, for multiple choice, the answer key,
for tools that want the question types entered as notes on the header cells. The tag
format used there belongs to the Academic Integrity Toolkit add-on (see README).
"""
import csv
import json
import os
import sys


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def export_scenario(folder, out_dir, column_notes=False):
    name = os.path.basename(os.path.normpath(folder))
    responses = load_jsonl(os.path.join(folder, "responses.jsonl"))
    with open(os.path.join(folder, "questions.json"), encoding="utf-8") as f:
        questions = json.load(f)["questions"]
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, name + ".csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Timestamp", "Email", "Name"] + [q["header"] for q in questions])
        for r in responses:
            w.writerow([r["timestamp"], r["email"], r["name"]] + [r["answers"].get(q["id"], "") for q in questions])
    if column_notes:
        with open(os.path.join(out_dir, name + ".column-notes.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("Name: <AIT-role=name><AIT-type=TEXT>\n")
            f.write("Timestamp, Email: <AIT-type=TEXT><AIT-disabled>\n")
            for q in questions:
                tag = "<AIT-type=%s>" % q["type"].upper()
                if q["type"] == "mcq":
                    tag += q["answer_key"]
                f.write("%s: %s\n" % (q["header"], tag))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    src, out_dir = args
    column_notes = "--column-notes" in argv
    if os.path.exists(os.path.join(src, "responses.jsonl")):
        folders = [src]
    else:
        folders = sorted(os.path.join(src, d) for d in os.listdir(src)
                         if os.path.exists(os.path.join(src, d, "responses.jsonl")))
    for folder in folders:
        export_scenario(folder, out_dir, column_notes)
        print("exported", folder)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
