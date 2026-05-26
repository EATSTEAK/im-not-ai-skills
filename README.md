<p align="center">
  <img src="assets/social-preview.png" alt="Humanize Korean — 한글 AI 티 제거기" width="820">
</p>

# Humanize Korean

[![skills.sh](https://skills.sh/b/EATSTEAK/im-not-ai-skills)](https://skills.sh/EATSTEAK/im-not-ai-skills)

AI(ChatGPT, Claude, Gemini 등)가 쓴 듯한 한글 글에서 **AI 티**를 줄이는 Agent Skill입니다. 사실, 주장, 수치, 고유명사, 직접 인용은 보존하고 번역투, 기계적 병렬, 과한 접속사, AI 관용구, 피동태 남용, 리듬 균일성 같은 문체 신호만 다룹니다.

## Install

```bash
npx skills add EATSTEAK/im-not-ai-skills
```

설치 후 에이전트에게 자연어로 요청하면 됩니다.

```text
이 AI 글 자연스럽게 윤문해줘:

[한글 초안]
```

잘 걸리는 표현:

- AI 티 없애줘
- 한글 윤문
- 번역투 제거
- ChatGPT/GPT 문체 제거
- 사람이 쓴 것처럼 다듬어줘
- 2차 윤문해줘

## What It Does

- **Fast mode**: `quick-rules.md` 중심으로 S1/S2 핵심 패턴을 빠르게 탐지하고 윤문합니다.
- **Strict mode**: 긴 글, `--strict`, 2차 윤문, 특정 카테고리/문단 재작업 요청에 대해 detector, rewriter, fidelity audit, naturalness review 절차를 순차 실행합니다.
- **Metric shim**: Python 표준 라이브러리만 사용해 쉼표, 결산 어휘, safe-balance 표현, post-editese interference 지표를 계산해 근거 보조로 사용합니다.

## Skill Structure

```text
skills/
  humanize-korean/
    SKILL.md
    references/
      quick-rules.md
      ai-tell-taxonomy.md
      rewriting-playbook.md
      scholarship.md
      strict-pipeline.md
      taxonomy-maintenance.md
      web-service-spec.md
      baseline.json
      baseline_v2.json
    scripts/
      metrics.py
      metrics_v2.py
      prepare_monolith_input.py
skills.sh.json
```

## Local Verification

The default test path uses stdlib `unittest`; `pytest` is not required.

```bash
python3 -m unittest tests.test_metrics tests.test_metrics_v2
```

Script smoke test:

```bash
python3 skills/humanize-korean/scripts/prepare_monolith_input.py \
  --workspace-root /tmp/humanize-skill-smoke \
  --text "결론적으로 이는 시사하는 바가 크다." \
  --genre essay
```

Structure check:

```bash
test -f skills/humanize-korean/SKILL.md
test -f skills.sh.json
test ! -d .claude
```

## Core Rules

1. 의미 불변: 사실, 주장, 수치, 고유명사, 직접 인용 보존.
2. 근거 기반: taxonomy나 quick rules에 걸린 구간만 수술적으로 수정.
3. 장르 유지: 리포트를 에세이로, 칼럼을 문학으로 바꾸지 않음.
4. 과윤문 금지: 변경률 30% 초과는 경고, 50% 초과는 중단 또는 사람 검토.

## License

MIT
