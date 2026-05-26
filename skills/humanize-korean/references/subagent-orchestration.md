# Subagent Orchestration

This file describes the optional multi-agent path. Use it only when the active
client exposes a subagent, task, worker, or team capability. If no such tool is
available, use `strict-pipeline.md` as the sequential fallback.

## Capability Probe

Before spawning workers, check the current client/tooling:

- If the client can run isolated subagents or tasks, use the role prompts in
  `subagent-roles.md`.
- If the client supports parallel workers, run the fidelity auditor and
  naturalness reviewer in parallel after the rewrite is complete.
- If the client has no subagent capability, do not simulate tool calls or invent
  workers. Follow `strict-pipeline.md` in the primary agent.

The primary agent always owns orchestration, final synthesis, user-facing
responses, and decisions about retry/hold. Subagents produce artifacts and
recommendations only.

## Fast Mode With Subagents

Use fast mode for normal inputs under 8,000 Korean characters unless the user
asks for strict mode or a targeted redo.

1. Create `_workspace/<run_id>/01_input.txt`.
2. Optionally run `scripts/prepare_monolith_input.py` and pass
   `01_input_with_metrics.txt` to the worker.
3. Spawn one `humanize-monolith` worker with:

```json
{
  "run_id": "YYYY-MM-DD-NNN",
  "input_path": "_workspace/<run_id>/01_input.txt",
  "combined_input_path": "_workspace/<run_id>/01_input_with_metrics.txt",
  "quick_rules_path": "references/quick-rules.md",
  "genre_hint": "칼럼 | 리포트 | 블로그 | 공적 | null"
}
```

4. The worker writes `final.md` and a summary block or `summary.md`.
5. The primary agent verifies the artifact exists, extracts the status, and
   returns the result.

## Strict Mode With Subagents

Use strict mode for `--strict`, long input, category redo, paragraph redo, or
second-pass requests.

1. Spawn `ai-tell-detector`.
2. Spawn `korean-style-rewriter` after detection is complete.
3. Spawn `content-fidelity-auditor` and `naturalness-reviewer` after rewrite is
   complete. Run them in parallel when the client supports parallel workers.
4. The primary agent reads both review artifacts, applies the decision matrix in
   `strict-pipeline.md`, and either finalizes or asks the rewriter for a targeted
   retry. Stop after three rewrite rounds.

## Handoff Payloads

Detector input:

```json
{
  "run_id": "YYYY-MM-DD-NNN",
  "input_text": "...",
  "genre_hint": "칼럼 | 리포트 | 블로그 | 공적 | null",
  "options": {
    "min_severity": "S1 | S2 | S3",
    "include_document_level": true
  },
  "taxonomy_path": "references/ai-tell-taxonomy.md"
}
```

Rewriter input:

```json
{
  "run_id": "YYYY-MM-DD-NNN",
  "input_path": "_workspace/<run_id>/01_input.txt",
  "detection_path": "_workspace/<run_id>/02_detection.json",
  "playbook_path": "references/rewriting-playbook.md",
  "target_filter": {
    "categories": ["A", "D"],
    "finding_ids": ["f001"],
    "paragraph_range": null
  }
}
```

Auditor input:

```json
{
  "run_id": "YYYY-MM-DD-NNN",
  "input_path": "_workspace/<run_id>/01_input.txt",
  "rewrite_path": "_workspace/<run_id>/03_rewrite.md",
  "diff_path": "_workspace/<run_id>/03_rewrite_diff.json"
}
```

Reviewer input:

```json
{
  "run_id": "YYYY-MM-DD-NNN",
  "original_detection_path": "_workspace/<run_id>/02_detection.json",
  "rewrite_path": "_workspace/<run_id>/03_rewrite.md",
  "taxonomy_path": "references/ai-tell-taxonomy.md",
  "genre_hint": "칼럼 | 리포트 | 블로그 | 공적 | null"
}
```

Synthesis input, read by the primary agent only:

```json
{
  "fidelity_audit_path": "_workspace/<run_id>/04_fidelity_audit.json",
  "naturalness_review_path": "_workspace/<run_id>/05_naturalness_review.json",
  "rewrite_path": "_workspace/<run_id>/03_rewrite.md",
  "diff_path": "_workspace/<run_id>/03_rewrite_diff.json"
}
```

## Retry Rules

- Category redo: pass only matching categories or finding IDs in
  `target_filter`; do not rework unrelated text.
- Paragraph redo: create a new run for that paragraph unless the user explicitly
  wants the original run rewritten in place.
- Second pass: use the previous `final.md` as input and preserve the original
  run's audit artifacts when comparing changes.
- Rollback: if auditor flags an edit, ask the rewriter to repair that edit only.

## Artifact Rule

Workers must write the same artifact names used by the sequential pipeline:
`02_detection.json`, `03_rewrite.md`, `03_rewrite_diff.json`,
`04_fidelity_audit.json`, `05_naturalness_review.json`, `final.md`, and
`summary.md`.
