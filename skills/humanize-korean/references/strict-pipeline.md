# Strict Pipeline

This is the sequential fallback and artifact contract for strict mode. Prefer
`subagent-orchestration.md` when the active client supports subagents, tasks, or
team workers. Use this file directly when subagents are unavailable.

Use strict mode when fast mode is too risky: long input, `--strict`, partial
redo, category-specific redo, or user-visible quality review.

## Artifacts

All paths are relative to the user's workspace run directory `_workspace/<run_id>/`.

- `01_input.txt`: original text.
- `02_detection.json`: span-level AI-tell findings.
- `03_rewrite.md`: rewritten text.
- `03_rewrite_diff.json`: edit map and change rate.
- `04_fidelity_audit.json`: meaning-preservation audit.
- `05_naturalness_review.json`: residual AI-tell and over-polish review.
- `final.md`: accepted final text.
- `summary.md`: concise metrics, grade, and highlights.

## Step 1: Detect

Read `ai-tell-taxonomy.md` and scan the input for A-J categories. Emit:

```json
{
  "meta": {
    "run_id": "YYYY-MM-DD-NNN",
    "estimated_genre": "칼럼",
    "detected_count": 0,
    "category_summary": {"A": 0, "B": 0, "C": 0}
  },
  "findings": [
    {
      "id": "f001",
      "category": "A-2",
      "category_label": "번역투: ~를 통해 남발",
      "severity": "S1",
      "scope": "span",
      "text_span": "데이터 분석을 통해",
      "start": 142,
      "end": 153,
      "reason": "기계적 경로 표현",
      "suggested_fix": "데이터를 분석해"
    }
  ]
}
```

Offsets must refer to the original string. For document-level rhythm or structure findings, set `scope: "document"` and omit offsets.

## Step 2: Rewrite

Read `rewriting-playbook.md`. Rewrite only detected spans unless the finding is document-level. Recommended order: D, A, I, G/A-10, H, F, B, C/J, E.

Emit:

```json
{
  "meta": {
    "char_count_before": 1820,
    "char_count_after": 1742,
    "change_rate": 0.18,
    "findings_resolved": 34,
    "findings_unresolved": 3,
    "over_polish_warning": false
  },
  "edits": [
    {
      "finding_id": "f001",
      "before": "데이터 분석을 통해 인사이트를 얻는다",
      "after": "데이터를 분석해 인사이트를 얻는다",
      "category": "A-2",
      "reason": "'통해' 남발 해소"
    }
  ],
  "unresolved_findings": []
}
```

## Step 3: Fidelity Audit

Compare `01_input.txt`, `03_rewrite.md`, and `03_rewrite_diff.json`. Audit these 13 invariants:

1. Proper nouns unchanged.
2. Numbers, units, dates, times, money, and percentages preserved.
3. Direct quotes unchanged.
4. Legal/regulatory clauses unchanged.
5. Formulas and symbolic notation unchanged.
6. Claim polarity unchanged.
7. Conclusion direction unchanged.
8. Causality unchanged.
9. Agent/patient unchanged after active/passive conversion.
10. Quantifiers and modality unchanged.
11. Sequence unchanged when meaningful.
12. No original information omitted.
13. No new information added.

Emit `audit_verdict: "full_pass" | "conditional_pass" | "fail"` plus flagged edits. If there is more than a 5% chance an edit changes meaning, mark it for rollback.

## Step 4: Naturalness Review

Re-scan the rewrite against the taxonomy. Check residual S1/S2 and over-polish signals:

- genre drift
- literary embellishment not present in source
- excessive colloquialization
- rhythm that feels forced
- replacement of core topic terms

Emit `verdict: "accept" | "accept_with_note" | "rewrite_round_2" | "rollback_and_rewrite" | "hold_and_report"` and `quality_level: "A" | "B" | "C" | "D"`.

When subagents are available, Step 3 and Step 4 may run in parallel after
`03_rewrite.md` and `03_rewrite_diff.json` exist. They must still write
independent artifacts before the primary agent performs final synthesis.

## Decision Matrix

- `full_pass` + `accept` or `accept_with_note`: finalize.
- `full_pass` + `rewrite_round_2`: rewrite only target findings.
- `conditional_pass`: rollback or repair flagged edits, then audit again.
- `fail`: redo from rewrite step.
- Any serious over-polish: rollback affected edits before trying again.
- Stop after three rewrite rounds and report `hold_and_report`.
