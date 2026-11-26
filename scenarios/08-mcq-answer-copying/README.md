# Multiple-choice answer copying

A 30-question four-choice test taken by 20 students, with one copying pair and one copying group of three.

- Participants: 20
- Questions: 30 (mcq)
- Files: `responses.jsonl`, `questions.json`, `labels.json`

## Known relations (ground truth)

Every pair not listed below is `independent` / `not_copied`.

| Participants | Relation | Ground truth | Note |
|---|---|---|---|
| S15, S09 | `mcq_copy` | `copied` | B copied A's answers, wrong ones included (generator copy rate 0.9). (source: S15) |
| S17, S16 | `mcq_copy` | `copied` | Ring_2 copied Ring_1's answers (generator copy rate 0.85). (source: S17) |
| S17, S05 | `mcq_copy` | `copied` | Ring_3 copied Ring_1's answers (generator copy rate 0.85). (source: S17) |
| S16, S05 | `mcq_shared_source` | `shared_source` | Both copied Ring_1; no evidence of copying each other. |

The answer key for each question is in `questions.json`.
