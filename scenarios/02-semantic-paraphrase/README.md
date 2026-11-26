# Paraphrase and verbatim copy

A verbatim copy pair, a pair that says the same thing in very different words, and an unrelated pair, among on-topic independent answers.

- Participants: 10
- Questions: 1 (text)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Labelled relations

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| S03, S07 | `verbatim_copy` | `copied` | Identical text. |
| S05, S08 | `paraphrase` | `copied` | Same meaning in almost entirely different words. |
| {S03, S07} x {S05, S08} | `paraphrase` | `copied` | The paraphrases restate the verbatim pair's text in different words. |
