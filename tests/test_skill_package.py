"""Package integrity tests for the skills.sh skill layout."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "humanize-korean"


class SkillPackageTests(unittest.TestCase):
    def test_skill_references_orchestration_files(self) -> None:
        skill_md = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "subagent-orchestration.md",
            "subagent-roles.md",
            "strict-pipeline.md",
        ):
            self.assertIn(f"references/{name}", skill_md)
            self.assertTrue((SKILL_ROOT / "references" / name).is_file())

    def test_required_subagent_roles_are_documented(self) -> None:
        roles = (SKILL_ROOT / "references" / "subagent-roles.md").read_text(
            encoding="utf-8"
        )
        for role in (
            "humanize-monolith",
            "ai-tell-detector",
            "korean-style-rewriter",
            "content-fidelity-auditor",
            "naturalness-reviewer",
            "korean-ai-tell-taxonomist",
            "post-editese-metric-engineer",
            "quick-rules-integrator",
            "taxonomy-gap-analyzer",
            "translationese-research-distiller",
            "korean-translation-scholar",
            "humanize-web-architect",
        ):
            self.assertIn(f"### {role}", roles)

    def test_orchestration_defines_handoff_payloads_and_fallback(self) -> None:
        orchestration = (
            SKILL_ROOT / "references" / "subagent-orchestration.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Capability Probe",
            "Detector input",
            "Rewriter input",
            "Auditor input",
            "Reviewer input",
            "strict-pipeline.md",
        ):
            self.assertIn(phrase, orchestration)

    def test_skills_sh_config_lists_humanize_korean(self) -> None:
        config = json.loads((ROOT / "skills.sh.json").read_text(encoding="utf-8"))
        listed = [
            skill
            for group in config["groupings"]
            for skill in group.get("skills", [])
        ]
        self.assertIn("humanize-korean", listed)


if __name__ == "__main__":
    unittest.main()
