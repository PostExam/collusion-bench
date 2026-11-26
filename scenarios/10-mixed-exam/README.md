# Mixed exam: every question type

Fourteen questions (ten multiple choice, two text, two code) answered by 11 students. One pair copies everything, one student rewords the first student's text answers, eight are independent.

- Participants: 11
- Questions: 14 (code, mcq, text)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Known relations (ground truth)

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| S03, S08 | `mcq_copy` | `copied` | Copier_B repeats Copier_A's multiple-choice answers, wrong ones included. (source: S03) (questions: q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) |
| S03, S08 | `light_edit_copy` | `copied` | Near-identical text answers (a few words added or changed). (questions: q11, q12) |
| S03, S08 | `code_renamed` | `copied` | Same programs with every name changed. (questions: q13, q14) |
| S03, S01 | `paraphrase` | `copied` | Reworded_C rewords Copier_A's text answers. (questions: q11, q12) |
| S08, S01 | `shared_text_source` | `shared_source` | Both derive from Copier_A's text answers (Copier_B near-verbatim, Reworded_C reworded). (questions: q11, q12) |
