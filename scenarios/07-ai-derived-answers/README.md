# AI-derived answers

Two AI-style reference answers, each with two near-verbatim copies and two paraphrases, plus nine independent answers.

- Participants: 19 (including 2 AI reference answers: S02, S16)
- Questions: 1 (text)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Labelled relations

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| {S16} x {S07, S18} | `ai_near_verbatim` | `copied` | Near-verbatim copy of the AI reference answer. |
| {S16} x {S13, S19} | `ai_paraphrase` | `copied` | Close paraphrase of the AI reference answer. |
| S07, S18, S13, S19 | `shared_ai_source` | `shared_source` | Both derive from the same AI answer; no evidence either copied the other. |
| {S02} x {S05, S08} | `ai_near_verbatim` | `copied` | Near-verbatim copy of the AI reference answer. |
| {S02} x {S06, S15} | `ai_paraphrase` | `copied` | Close paraphrase of the AI reference answer. |
| S05, S08, S06, S15 | `shared_ai_source` | `shared_source` | Both derive from the same AI answer; no evidence either copied the other. |
