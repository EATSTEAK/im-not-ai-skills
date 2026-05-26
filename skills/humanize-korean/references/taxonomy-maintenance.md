# Taxonomy And Metric Maintenance

Use this only when the user asks to update the taxonomy, add new AI-tell patterns, recalibrate metrics, or change the rulebook.

## Taxonomy Rules

- `ai-tell-taxonomy.md` is the SSOT for A-J pattern IDs.
- Preserve existing IDs. Append new IDs; do not renumber.
- Promote a new pattern only with at least two real examples from different texts, models, genres, or authors when possible.
- Keep severity conservative:
  - S1: decisive, remove whenever found.
  - S2: strong, remove when repeated or contextually unnatural.
  - S3: weak, use only with supporting evidence.
- Sync every promoted pattern with a rewrite recipe in `rewriting-playbook.md`.

## Maintenance Workflow

1. Collect examples and exact spans.
2. Compare against existing A-J taxonomy to avoid duplicates.
3. Decide: promote, merge into existing ID, hold, or reject.
4. Update `ai-tell-taxonomy.md` and `rewriting-playbook.md` together.
5. If the fast path needs the rule, add a compact version to `quick-rules.md`.
6. Add or update tests when the change touches `scripts/metrics.py` or `scripts/metrics_v2.py`.

## Post-Editese Metrics

`scripts/metrics_v2.py` implements Toral-style simplification, normalisation, and interference signals with Python standard library only. Do not add external Korean NLP dependencies such as konlpy, mecab, bareun, spaCy, or cloud APIs.

When updating metrics:

- Keep v1.6 metric function signatures backward compatible.
- Keep `compute_all` as a v2 superset alias.
- Store v1 baseline in `references/baseline.json`.
- Store v2 placeholder/calibration cells in `references/baseline_v2.json`.
- Preserve `_placeholder` and `calibration_due` flags until measured corpora replace them.

## Validation

Run:

```bash
python3 -m unittest tests.test_metrics tests.test_metrics_v2
```

If `pytest` is installed, it may also be used, but stdlib `unittest` is the default supported path.
