# Lexical copy spectrum

Same-topic answers ranging from a verbatim copy, through a lightly edited copy and a partial overlap, to independent answers.

- Participants: 12
- Questions: 1 (text)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Known relations (ground truth)

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| S12, S10 | `verbatim_copy` | `copied` | Identical text. |
| S04, S11 | `verbatim_copy` | `copied` | Identical to each other (both carry the same edited text). |
| {S12, S10} x {S04, S11} | `light_edit_copy` | `copied` | The edited text is the original with a few words changed. |
| S03, S02 | `partial_overlap` | `partial` | Share an opening sentence inside otherwise different answers. |
