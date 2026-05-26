---
name: humanize-korean
description: Korean AI-text humanizer for removing AI 티 from Korean writing without changing meaning. Use for 한글 윤문, AI 티 제거, 번역투 제거, ChatGPT/GPT 문체 제거, 사람이 쓴 것처럼 다듬기, Korean translationese cleanup, Korean humanizer, and 2차 윤문 requests.
license: MIT
metadata:
  version: "2.0.0"
  source: "EATSTEAK/im-not-ai-skills"
---

# Humanize Korean

AI가 쓴 듯한 한글 문장을 자연스러운 한국어로 윤문한다. 사실, 주장, 수치, 고유명사, 직접 인용은 보존하고 문체, 리듬, 조사, 어미, 구조만 손본다.

## Core Contract

1. Preserve meaning exactly. Do not add, delete, soften, strengthen, or fact-check claims unless the user explicitly asks.
2. Edit only AI-tell spans you can ground in `references/quick-rules.md` or `references/ai-tell-taxonomy.md`.
3. Keep the source genre and register. A report stays a report; a formal column stays formal.
4. Do not edit numbers, units, dates, proper nouns, legal clauses, formulas, or text inside direct quotes.
5. Keep change rate below 30% when possible. Stop and report if a safe rewrite would exceed 50%.

## Default Workflow

Use fast mode unless the user asks for strict/정밀 mode, requests partial rework, or the input is over 8,000 Korean characters.

1. Identify the user's text or file path. If the input is not Korean prose, say this skill only handles Korean text.
2. Create a run directory under the user's current workspace: `_workspace/YYYY-MM-DD-NNN/`.
3. For fast mode, use `references/subagent-orchestration.md` when the client supports subagents; otherwise read `references/quick-rules.md`, scan S1/S2 patterns, rewrite locally, then self-check.
4. For strict mode or redo requests, read `references/subagent-orchestration.md` first. If subagents are unavailable, follow the sequential fallback in `references/strict-pipeline.md`.
5. Write the final output to `_workspace/<run_id>/final.md`.
6. Return a concise status with change rate, grade, top categories fixed, and the final text unless the user asked for files only.

## Optional Metric Shim

When shell execution is available, run the bundled metric preprocessor before rewriting. It is advisory evidence, not an automatic verdict.

```bash
python3 scripts/prepare_monolith_input.py \
  --workspace-root "$PWD" \
  --text "<Korean text>" \
  --genre essay
```

If the user already created `_workspace/<run_id>/01_input.txt`, run:

```bash
python3 scripts/prepare_monolith_input.py \
  --workspace-root "$PWD" \
  --run-dir "_workspace/<run_id>" \
  --genre essay
```

Read the generated `01_input_with_metrics.txt` as the fast-mode input. If the script degrades or is unavailable, continue with text-only rewriting.

## Modes

Fast mode:
- Read `references/quick-rules.md`.
- Detect high-confidence patterns in memory.
- Rewrite D 관용구, A 번역투, I 형식명사, G hedging, H 접속사, F 수식, B 영어 용어, C/J 구조 장식, then E 리듬.
- Self-check the six core constraints before finalizing.

Strict mode:
- Use when the user says `--strict`, "정밀 모드", "5인 파이프라인", asks for a second pass, asks to target one category/paragraph, or provides long input.
- Prefer the optional subagent path in `references/subagent-orchestration.md` when available: detector -> rewriter -> auditor/reviewer -> primary synthesis.
- If subagents are unavailable, follow `references/strict-pipeline.md` for the same detector, rewriter, fidelity audit, and naturalness review contracts.

Maintenance mode:
- Use `references/taxonomy-maintenance.md` only when the user asks to add, audit, or recalibrate taxonomy rules or post-editese metrics.

## References

- `references/quick-rules.md`: fast-mode S1/S2 rules and self-check list.
- `references/ai-tell-taxonomy.md`: full A-J taxonomy.
- `references/rewriting-playbook.md`: category rewrite recipes and do-not rules.
- `references/subagent-orchestration.md`: optional subagent routing, handoff payloads, and fallback rules.
- `references/subagent-roles.md`: portable role prompts for subagent-capable clients.
- `references/strict-pipeline.md`: strict workflow and JSON output contracts.
- `references/scholarship.md`: Korean translationese and post-editese source notes.
- `references/taxonomy-maintenance.md`: rule and metric maintenance workflow.
- `references/web-service-spec.md`: optional web product architecture.

## Output Standard

Use this summary shape:

```text
완료. 변경률 X% / 등급 A|B|C|D / 자체검증 N/6 통과

핵심 수정:
- A-2 번역투: N -> M
- D 관용구: N -> M

윤문본:
...
```

Grade A means no S1 remains, S2 is at most 2, meaning is preserved, and the text reads natural for the genre. Grade B is acceptable with minor residual S2. Grade C needs another pass. Grade D should be held for human review.
