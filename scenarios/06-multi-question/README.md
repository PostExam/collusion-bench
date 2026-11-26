# Multi-question survey

Four questions. Three pairs each match closely on a different subset of the questions, plus four independent students.

- Participants: 10
- Questions: 4 (text)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Labelled relations

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| S09, S05 | `verbatim_copy` | `copied` | Share a long passage on question 1 only. (questions: q1) |
| S04, S08 | `verbatim_copy` | `copied` | Share a long passage on question 2 only. (questions: q2) |
| S01, S10 | `light_edit_copy` | `copied` | Near-identical on questions 1 and 2. (questions: q1, q2) |
