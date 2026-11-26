# Post-Exam Collusion Analysis Benchmark

Example exam answers, with the truth about who copied from whom, for testing methods that look for collusion and misconduct **after an exam has been taken**.

**Status: version 0.1.0, a first release.** The data is synthetic: no real students. Results from a detector are indications to review, never proof of misconduct.

## Background

Google Forms is a popular way to give an exam or a test. Each student's submitted answers arrive in a Google Sheet, one row per student, one column per question. That sheet is the raw material for checking whether the exam was taken honestly.

Some students cheat. Typical misconduct includes:

- copying from a classmate, word for word or with a few changes;
- sharing answers with others during the test, in person or by chatting outside the exam;
- searching Google, or asking an AI assistant, and pasting or rewording the result;
- using the same study guide or class notes and reproducing a shared passage.

A teacher cannot read every pair of answers in a class. So there is ongoing work, including software, on analysing the submitted answers automatically for signs of collusion and misconduct, and listing the cases worth a closer look.

## Question types

Google Forms assessments can have several different question types: multiple choice (MCQ), short answer, long answer and computer code. The best analysis strategy differs by type. For multiple choice, the useful signal is how many wrong answers two students share; for written answers it is how much of the wording or meaning they share; for code it is the program's structure once names are changed.

Tools such as the Academic Integrity Toolkit (AIT) try to work out each question's type by themselves. To be completely safe, this repository states it explicitly, so no method has to guess:

- **Where:** in `questions.json`, inside each scenario folder (`scenarios/<scenario>/questions.json`).
- **How:** every question has a `type` field with one of three values: `mcq` (multiple choice, which also carries `choices` and the `answer_key`), `text` (short and long written answers; both are `text`) and `code` (computer code).

```json
{ "id": "q1", "type": "mcq", "choices": ["A", "B", "C", "D"], "answer_key": "B", ... }
```

Questions are matched to students' answers by `id` (`q1`, `q2`, ...), as the keys of `answers` in `responses.jsonl`.

If you use the CSV export, the type is not in the CSV itself. Running `scripts/export_csv.py` with `--column-notes` writes a `<scenario>.column-notes.txt` file, in which each column is tagged in the AIT format, for example `<AIT-type=MCQ>B`, `<AIT-type=TEXT>` or `<AIT-type=CODE>`. These are the tags the add-on keeps as notes on the header cells in row 1 of the sheet. See "Getting the CSV files" below.

## The problem this repository addresses

To trust a detection method, you need to know how well it works. Does it find real copying? Does it wrongly flag students who only gave similar answers because they answered the same question honestly? Today there is no common set of examples to measure that, so methods are rarely tested against each other, and a method's authors usually test it on data they made themselves.

This repository is that common set. It contains exam answers made so that **the truth is known**: for every pair of students, whether their answers are independent, copied, or derived from a shared source, and how. Anyone can run a method on the data, compare its findings with the known truth, and report the result. Because the truth is public, the results can be checked, and different methods can be compared fairly.

## What it contains

Ten small scenarios, each a made-up class taking a short exam (8 to 20 students). Each scenario stands for a kind of misconduct, or for an innocent look-alike that a good method must not flag:

| What the student did | What shows up in the answers | Scenarios |
|---|---|---|
| Copied a classmate word for word | Identical text | 01, 02, 06, 10 |
| Copied and changed a few words | Almost identical text | 01, 10 |
| Copied and reworded it | Same meaning, different words | 02, 10 |
| Rearranged someone else's words | Same words in a different order | 03 |
| Shared multiple-choice answers, wrong ones included | Many matching wrong answers | 08, 10 |
| Copied a program and renamed the variables | Same program, different names | 09, 10 |
| Used an AI assistant | Close copies and paraphrases of one AI answer | 07 |
| Used the same web page, study guide or class notes | The same sentence in many answers | 05 |
| **Innocent look-alikes, not misconduct** | Common words, or an honest shared topic | 04, and the independent students in every scenario |

The list of scenarios, with the exact pairs involved, is below.

## What it does not contain

The data holds the answers only. It does not hold how the students produced them: no timing, no keystrokes, no browser or chat records. A Google search, an AI assistant, or a chat message appears here only through its **effect**, similar answers. So the benchmark tests whether a method can **reveal misconduct from the surrounding data, the answers themselves**, not whether it can observe the act. It also cannot say whether similar answers are cheating: a shared source, for example, may be innocent. The truth recorded here describes how the data was built.

## What you can do with it

- **Developers** of a detection method (S2 for multiple choice, word-overlap or meaning-level similarity for text, code comparison, or a new idea): run it on the scenarios and measure how many of the known cases it finds and how many innocent pairs it flags.
- **Teachers and institutions** evaluating a tool: try it on data where you know the right answer before trusting it on a real class.
- **Researchers**: cite a fixed, versioned dataset, reproduce each other's results and extend it with new scenarios by pull request.

A first run takes a few minutes: pick a scenario folder, read its `README.md` to see what is in it and which pairs are related, run your method on `responses.jsonl` (or on a CSV export, see below), then compare its findings with the known relations.

## Disclosure

The first scenarios were taken from the sample data of the Academic Integrity Toolkit, a Google Sheets add-on made by Agentic Planet, Inc. The maintainer is that product's developer. The benchmark is meant to be useful to every method, including competitors, and results for other methods are welcome.

## Scenarios

| Scenario | What it contains | Participants | Questions |
|---|---|---|---|
| [01-lexical-copy-spectrum](scenarios/01-lexical-copy-spectrum) | Same-topic answers ranging from a verbatim copy, through a lightly edited copy and a partial overlap, to independent answers. | 12 | 1 |
| [02-semantic-paraphrase](scenarios/02-semantic-paraphrase) | A verbatim copy pair, a pair that says the same thing in very different words, and an unrelated pair, among on-topic independent answers. | 10 | 1 |
| [03-word-order-reshuffle](scenarios/03-word-order-reshuffle) | A pair that reuses nearly the same words rearranged into different sentences, among independent answers. | 9 | 1 |
| [04-function-word-decoy](scenarios/04-function-word-decoy) | A pair that looks similar only because both are full of common function words. They are not copies. | 9 | 1 |
| [05-shared-class-template](scenarios/05-shared-class-template) | Six students who each include the same sentence from a shared source inside otherwise original answers, plus two controls. | 8 | 1 |
| [06-multi-question](scenarios/06-multi-question) | Four questions. Three pairs each match closely on a different subset of the questions, plus four independent students. | 10 | 4 |
| [07-ai-derived-answers](scenarios/07-ai-derived-answers) | Two AI-style reference answers, each with two near-verbatim copies and two paraphrases, plus nine independent answers. | 19 | 1 |
| [08-mcq-answer-copying](scenarios/08-mcq-answer-copying) | A 30-question four-choice test taken by 20 students, with one copying pair and one copying group of three. | 20 | 30 |
| [09-code-renamed-variables](scenarios/09-code-renamed-variables) | Twelve Python answers to one task: one program, a renamed copy, a renamed and reformatted copy, a reordered copy, and eight independent solutions. | 12 | 1 |
| [10-mixed-exam](scenarios/10-mixed-exam) | Fourteen questions (ten multiple choice, two text, two code) answered by 11 students. One pair copies everything, one student rewords the first student's text answers, eight are independent. | 11 | 14 |

Each scenario folder has its own README listing exactly which pairs are related and how.

## Files and format

```
scenarios/<scenario>/
  responses.jsonl   one JSON object per student: id, name, email, timestamp, answers
  questions.json    each question: id, header, type (text | mcq | code), plus choices and answer_key for mcq
  labels.json       the ground truth: which students' answers are related, and how
schemas/            JSON Schemas for the three files
scripts/            validate.py, export_csv.py, expand_labels.py, scenario_tables.py
```

Everything is UTF-8 and uses LF line endings. JSON Lines keeps long answers, quotes and line breaks safe, and keeps pull-request diffs readable.

A question's `header` is the column heading as it appears in the Google Forms layout; for text and code questions it is the question itself (also in `prompt`).

Each scenario's `README.md` starts with **The data at a glance**: a table that looks exactly like the Google Sheet would look with the scenario loaded: one row per student, one column per question. The tables are generated by `scripts/scenario_tables.py` and should not be edited by hand.

Student names and emails are neutral (`Student 07`, `s07@example.edu`). The order of students is shuffled with a fixed seed so that the order gives nothing away. The original sample-data names, which reveal the design, appear only in `labels.json` under `source_name`.

## Ground truth

The ground truth is the set of known facts about which students' answers are related and how. We know them because we built the data that way. It is stored in `labels.json`, which lists the participants and the relations between them. A pair that is not listed gets the scenario default: `independent` / `not_copied`. Run `python scripts/expand_labels.py scenarios/<scenario>` to get one row per pair.

Ground truth, per pair:

| Value | Meaning |
|---|---|
| `copied` | One answer was derived from the other, or both from one copied text. |
| `partial` | A shared passage inside otherwise different answers; whether it is misconduct is a judgement. |
| `shared_source` | Both derive from a common outside source (class template, AI answer, a third student). No evidence either copied the other. |
| `not_copied` | No copying. |

Relation, per pair:

| Relation | Meaning |
|---|---|
| `verbatim_copy` | The answers are identical text. |
| `light_edit_copy` | One text is the other with a few words changed. |
| `partial_overlap` | A passage is shared inside otherwise different answers. |
| `paraphrase` | The same meaning restated in almost entirely different words. |
| `reordered_words` | Nearly the same words rearranged into different sentences. |
| `shared_template_sentence` | One identical sentence from a shared source reused inside otherwise original answers. |
| `ai_near_verbatim` | A near-verbatim copy of an AI-style reference answer (the pair includes the reference). |
| `ai_paraphrase` | A close paraphrase of an AI-style reference answer (the pair includes the reference). |
| `shared_ai_source` | Two submissions derived from the same AI-style answer. |
| `mcq_copy` | Multiple-choice answers copied from a source student, wrong answers included. The entry names the source. |
| `mcq_shared_source` | Two students who each copied the same third student. |
| `code_renamed` | The same program with identifiers renamed. |
| `code_reformatted` | The same program with new names and different comments and spacing. |
| `code_reordered` | The same logic with statements reordered. |
| `decoy_function_words` | A pair that looks alike only through shared common words. Not a copy. |
| `shared_text_source` | Two submissions each derived from the same third student's text. |
| `independent` | Independent answers (the default for every pair not listed). |

A relation may carry `questions` (the questions it applies to) and `source` (who copied whom, for multiple choice). A pair may have several relations, each for different questions, as in the mixed-exam scenario; a relation without `questions` applies to every question. The ground truth describes how the data was constructed, not anyone's intent.

## Using the data

```python
import json
with open("scenarios/08-mcq-answer-copying/responses.jsonl", encoding="utf-8") as f:
    students = [json.loads(line) for line in f]
print(students[0]["answers"]["q1"])
```

## Getting the CSV files

### Why the data is not stored as CSV

Google Forms collects answers in a Google Sheet, so a spreadsheet is the natural form for exam data, and CSV is the usual way to move a sheet around. But CSV is a poor format to keep and maintain a dataset in:

- **Long answers break it.** Written and code answers contain commas, quotation marks and line breaks. CSV needs all of these escaped, a single stray quote can shift every following column, and different programs read the same file differently.
- **It is hard to compare changes.** The whole row is one line, so when one answer changes, the review shows the entire row as changed and the edit is hard to spot. Data in this repository is changed by pull request, so readable changes matter.
- **It cannot describe itself.** There is no place in a CSV for the question types, the multiple-choice answer key or the known relations between students, and everything is plain text with no structure.

So the repository keeps the data as JSON Lines (one student per line, one named field per answer), which is the source of truth. It copes with any text and gives clean, reviewable changes.

### CSV for Google Sheets

Even so, a Google Forms response sheet is where this data is meant to be used, so the repository also provides the same data **as CSV in the layout of a Google Forms response sheet**: columns Timestamp, Email and Name, then one column per question. The CSV files are generated from the JSON Lines files by a small script, never edited by hand. To use one, open a Google Sheet and choose **File → Import → Upload**, or open the CSV in Excel or any spreadsheet program. Your analysis tool then sees what it would see for a real Google Forms exam.

There are two ways to get the CSV files:

1. **From GitHub, without installing anything.** Open the **Actions** tab, click the latest **validate** run, and on its **Summary** page scroll to **Artifacts**. Download `csv-exports`: a zip with one CSV per scenario. You need to be signed in to GitHub, and GitHub deletes artifacts after a retention period, so treat this as a convenience.
2. **On your own computer.** With Python 3 installed, in the repository folder run:

```
python scripts/export_csv.py scenarios out/
```

Add `--column-notes` to also write, for each scenario, a text file naming every question column's type and the multiple-choice answer key. The tag format in it is that of the Academic Integrity Toolkit add-on, which stores question types as notes on the header cells; other tools can ignore the file.

Never edit the CSVs by hand: change the JSONL files and export again.

## Checking your changes

Every scenario is checked automatically. The check (`scripts/validate.py`, started by `.github/workflows/validate.yml`) runs on every push and every pull request, and reports on the commit or pull request:

- a **green tick** means all scenarios passed: the files are valid, their ids match, every answer belongs to a declared question, multiple-choice answers are valid letters, and every ground-truth entry points to a student that exists;
- a **red cross** means a problem. Click it, open the **validate** job, and read the step **Run python scripts/validate.py** for the exact lines.

You can also run it yourself before opening a pull request:

```
pip install jsonschema
python scripts/validate.py
```

It should end with `N scenario(s) checked, 0 problem(s)`.

## Evaluating a method

This release contains data and ground truth only. A scoring script and baseline results are planned. Until then, report per scenario, at a stated false-positive rate: how many of the pairs whose ground truth is `copied` a method finds, and how it ranks them. Say how the method was run, including every setting. Do not tune a method on the labels of a scenario and then report that scenario as a test.

## Limitations

- Synthetic data: no real students, and small classes (8 to 20). Real answers are messier.
- One short answer per question (a few sentences, a short program, or a letter). Long essays are not covered.
- English only. Texts were written for the sample data, so some copy designs are easier than real life.
- Independent answers on the same topic share vocabulary by design. That is the honest baseline, not an error.
- `partial` and `shared_source` pairs are judgements. Different reviewers may disagree about whether they are misconduct.
- The multiple-choice class was generated from a seeded model of student ability and wrong-answer popularity. It is a plausible class, not a measured one.

## Provenance

The answers were written for the Academic Integrity Toolkit's sample data. Scenario 07's reference answers were written to resemble the output of two AI chat assistants (a Gemini-style and a Claude-style answer); the Claude-style answer was produced by Claude. The multiple-choice class is generated by a seeded script. No real student work is included.

## Contributing

New scenarios and corrections are welcome as pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

- Data (everything under `scenarios/`): [CC BY 4.0](LICENSE-DATA)
- Code (`scripts/`): [MIT](LICENSE)

## Citation

See [CITATION.cff](CITATION.cff), or use the "Cite this repository" button on GitHub. Please also state the version of the benchmark you used (shown in `CITATION.cff` and on the Releases page).
