# Contributor Notes

This repository packages `humanize-korean` as a skills.sh-compatible Agent Skill.

Canonical skill path:

```text
skills/humanize-korean/
```

Keep runtime skill logic inside that directory:

- `SKILL.md` for activation and workflow instructions.
- `references/` for taxonomy, playbooks, baselines, and maintenance guidance.
- `scripts/` for reusable Python helpers.

Root `assets/` and social-preview scripts are repository marketing assets, not runtime skill dependencies.

Run the supported local checks before publishing:

```bash
python3 -m unittest tests.test_metrics tests.test_metrics_v2
python3 skills/humanize-korean/scripts/prepare_monolith_input.py \
  --workspace-root /tmp/humanize-skill-smoke \
  --text "결론적으로 이는 시사하는 바가 크다." \
  --genre essay
```
