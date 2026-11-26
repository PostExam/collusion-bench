# Post-Exam Collusion Analysis Benchmark

Open, labelled exam-answer sets for testing methods that look for collusion **after an exam has been taken**. Nothing here is meant for use during an exam.

The aim is a shared test bed: anyone can run a method (S2 for multiple choice, word-overlap or meaning-level similarity for text, code comparison, or something new) on the same data and compare it against known ground truth.

**Status: version 0.1.0, a first release.** The data is synthetic. Results from a detector are indications to review, never proof of misconduct.

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
  labels.json       participants and the ground-truth relations between them
schemas/            JSON Schemas for the three files
scripts/            validate.py, export_csv.py, expand_labels.py
```

Everything is UTF-8 and uses LF line endings. JSON Lines keeps long answers, quotes and line breaks safe, and keeps pull-request diffs readable.

A question's `header` is the column heading as it appears in the Google Forms layout; for text and code questions it is the question itself (also in `prompt`).

Student names and emails are neutral (`Student 07`, `s07@example.edu`). The order of students is shuffled with a fixed seed so that the order gives nothing away. The original sample-data names, which reveal the design, appear only in `labels.json` under `source_name`.

## Ground truth

`labels.json` lists the participants and the relations between them. A pair that is not listed gets the scenario default: `independent` / `not_copied`. Run `python scripts/expand_labels.py scenarios/<scenario>` to get one row per pair.

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
| `mcq_copy` | Multiple-choice answers copied from a source student, wrong answers included. The label names the source. |
| `mcq_shared_source` | Two students who each copied the same third student. |
| `code_renamed` | The same program with identifiers renamed. |
| `code_reformatted` | The same program with new names and different comments and spacing. |
| `code_reordered` | The same logic with statements reordered. |
| `decoy_function_words` | A pair that looks alike only through shared common words. Not a copy. |
| `shared_text_source` | Two submissions each derived from the same third student's text. |
| `independent` | Independent answers (the default for every pair not listed). |

A relation may carry `questions` (the questions it applies to) and `source` (who copied whom, for multiple choice). A pair may have several relations, each for different questions, as in the mixed-exam scenario; a relation without `questions` applies to every question. Labels describe how the data was constructed, not anyone's intent.

## Using the data

```python
import json
with open("scenarios/08-mcq-answer-copying/responses.jsonl", encoding="utf-8") as f:
    students = [json.loads(line) for line in f]
print(students[0]["answers"]["q1"])
```

To load a scenario into a spreadsheet, export it to CSV in the layout of a Google Forms response sheet:

```
python scripts/export_csv.py scenarios out/
```

Add `--column-notes` to also write, for each scenario, a text file naming every question column's type and the multiple-choice answer key. The tag format in it is that of the Academic Integrity Toolkit add-on, which stores question types as notes on the header cells; other tools can ignore the file.

## Checking your changes

```
pip install jsonschema
python scripts/validate.py
```

The same check runs automatically on every push and pull request.

## Evaluating a method

This release contains data and labels only. A scoring script and baseline results are planned. Until then, report per scenario, at a stated false-positive rate: how many of the labelled `copied` pairs a method finds, and how it ranks them. Say how the method was run, including every setting. Do not tune a method on the labels of a scenario and then report that scenario as a test.

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

See [CITATION.cff](CITATION.cff), or use the "Cite this repository" button on GitHub.
