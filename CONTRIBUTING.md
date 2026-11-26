# Contributing

Thank you for helping. Contributions are pull requests against `main`.

## What is welcome

- **New scenarios**: another kind of copying, another question type, a larger class, another language.
- **Corrections**: a wrong ground-truth entry, a typo, an answer that is not what its ground truth says.
- **Script improvements**: for `validate.py`, `export_csv.py`, `scenario_tables.py` and `expand_labels.py`.

## Rules for data

- **No real student data.** Contribute synthetic data, or data from volunteers who agreed in writing that it may be published under CC BY 4.0, with any required ethics approval, and no names or identifying content.
- **Record the truth you built.** Every relation must follow from how you made the data. If you generated text with an AI tool, say which one in the scenario README.
- **Maintainers review the ground truth.** The ground truth (which answers are related, and how) is the value of this benchmark, so it is checked more closely than the rest.
- **Use the existing vocabulary** for `relation` and `ground_truth` (see the README). If you need a new relation, propose it in an issue first.
- **Keep it small and plain.** One scenario per folder, named `NN-short-description`.

## A new scenario

Create `scenarios/NN-short-description/` with:

1. `responses.jsonl`: one student per line. Ids are `S01`, `S02`, and so on. Use neutral names and `@example.edu` emails. Shuffle the order so that the order gives nothing away.
2. `questions.json`: every question with `id` (`q1`, `q2`, ...), `header`, and `type`. Multiple choice also needs `choices` and `answer_key`; code needs `language`.
3. `labels.json`: the ground truth. It lists the participants, with `source_name` for how you identify them in your own notes, and the relations between them.
4. `README.md`: what the scenario tests and which pairs are related.

Then run:

```
pip install jsonschema
python scripts/validate.py
python scripts/scenario_tables.py scenarios/
```

and fix everything it reports before opening the pull request.

## Licensing

By contributing you agree that your data is released under CC BY 4.0 and your code under the MIT license, the same as the rest of the repository.

## Conduct

Be courteous and assume good faith. Disagreements about a ground-truth entry are settled by looking at how the data was built.
