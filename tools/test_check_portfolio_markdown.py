"""Regression tests for the portfolio Markdown validator."""

from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import unittest

from check_portfolio_markdown import (
    FEATURED_REPOSITORIES,
    Finding,
    PROJECT_REPOSITORIES,
    check_common_text_quality,
    check_english_summary,
    check_japanese_summary,
    check_markdown_workflow,
    verified_summary_exemptions,
)


REPOSITORY = "example"
REPOSITORY_PATH = Path("/workspace/example")
MARKDOWN_PATH = REPOSITORY_PATH / "docs" / "example.md"


class PortfolioInventoryTests(unittest.TestCase):
    def test_seven_projects_are_validated(self) -> None:
        self.assertEqual(len(PROJECT_REPOSITORIES), 7)
        self.assertIn("few-shot-anomaly-poc", PROJECT_REPOSITORIES)

    def test_featured_projects_match_profile_selection(self) -> None:
        self.assertEqual(
            FEATURED_REPOSITORIES,
            {
                "few-shot-anomaly-poc",
                "pointcloud-playground",
                "data-cleaning-toolkit",
            },
        )


class FrozenMarkdownExemptionTests(unittest.TestCase):
    def _repository(self, root: Path, content: str) -> Path:
        repository = root / "few-shot-anomaly-poc"
        document = repository / "docs/evaluation-plan.md"
        document.parent.mkdir(parents=True)
        document.write_text(content, encoding="utf-8")
        record = repository / "artifacts/v0.1/freeze/pre-evaluation-freeze.json"
        record.parent.mkdir(parents=True)
        record.write_text(
            json.dumps(
                {
                    "frozen_files": [
                        {
                            "relative_path": "docs/evaluation-plan.md",
                            "sha256": hashlib.sha256(document.read_bytes()).hexdigest(),
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        return repository

    def test_accepts_exact_frozen_markdown_without_summary(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = self._repository(
                Path(temporary_directory),
                "# Evaluation Plan\n\nOriginal preregistered text.\n",
            )
            findings: list[Finding] = []

            exemptions = verified_summary_exemptions(
                "few-shot-anomaly-poc",
                repository,
                findings,
            )

            self.assertEqual(
                exemptions,
                {(repository / "docs/evaluation-plan.md").resolve()},
            )
            self.assertEqual(findings, [])

    def test_rejects_changed_frozen_markdown(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = self._repository(
                Path(temporary_directory),
                "# Evaluation Plan\n\nOriginal preregistered text.\n",
            )
            document = repository / "docs/evaluation-plan.md"
            document.write_text(
                "# Evaluation Plan\n\nChanged after the freeze.\n",
                encoding="utf-8",
            )
            findings: list[Finding] = []

            exemptions = verified_summary_exemptions(
                "few-shot-anomaly-poc",
                repository,
                findings,
            )

            self.assertEqual(exemptions, set())
            self.assertTrue(
                any("pre-evaluation SHA-256" in finding.message for finding in findings)
            )


class CommonTextQualityTests(unittest.TestCase):
    def findings_for(self, text: str) -> list[Finding]:
        findings: list[Finding] = []
        check_common_text_quality(
            REPOSITORY,
            REPOSITORY_PATH,
            MARKDOWN_PATH,
            text,
            findings,
        )
        return findings

    def test_accepts_clean_japanese(self) -> None:
        self.assertEqual(self.findings_for("文字化けのない日本語です。"), [])

    def test_rejects_japanese_internal_ascii_space(self) -> None:
        findings = self.findings_for("日本語 の不要な空白")
        self.assertTrue(
            any("ASCII space" in finding.message for finding in findings)
        )

    def test_rejects_merge_conflict_marker(self) -> None:
        findings = self.findings_for("before\n<<<<<<< HEAD\nafter\n")
        self.assertTrue(
            any("merge-conflict marker" in finding.message for finding in findings)
        )

    def test_rejects_status_badge(self) -> None:
        text = (
            "[![CI](https://github.com/example/project/actions/workflows/"
            "ci.yml/badge.svg)](https://github.com/example/project/actions)\n"
        )
        findings = self.findings_for(text)
        self.assertTrue(
            any(
                "status badges are not used" in finding.message
                for finding in findings
            )
        )

    def test_rejects_replacement_character(self) -> None:
        findings = self.findings_for("broken \ufffd text")
        self.assertTrue(
            any("replacement character" in finding.message for finding in findings)
        )

    def test_rejects_common_japanese_mojibake(self) -> None:
        findings = self.findings_for("縺薙")
        self.assertTrue(
            any("encoding corruption" in finding.message for finding in findings)
        )


class JapaneseSummaryTests(unittest.TestCase):
    def findings_for(self, text: str) -> list[Finding]:
        findings: list[Finding] = []
        check_japanese_summary(
            REPOSITORY,
            REPOSITORY_PATH,
            MARKDOWN_PATH,
            text,
            findings,
            root_readme=False,
        )
        return findings

    def test_accepts_summary_after_title(self) -> None:
        text = (
            "# Example\n\n"
            "## 日本語概要\n\n"
            "本書は固定入力と評価結果を対応付け、再現条件と制約を記録します。"
            "生成した成果物と検証方法も明示します。"
            "数値、手順、適用範囲の詳細は以下の英語本文を参照してください。\n\n"
            "---\n\n"
            "English text.\n"
        )
        self.assertEqual(self.findings_for(text), [])

    def test_rejects_missing_summary(self) -> None:
        findings = self.findings_for("# Example\n\nEnglish text.\n")
        self.assertTrue(
            any("must appear exactly once" in finding.message for finding in findings)
        )

    def test_rejects_hard_wrapped_summary(self) -> None:
        text = (
            "# Example\n\n"
            "## 日本語概要\n\n"
            "本書は固定入力と評価結果を対応付けます。\n"
            "再現条件と制約の詳細は以下の英語本文を参照してください。\n\n"
            "---\n\n"
            "English text.\n"
        )
        findings = self.findings_for(text)
        self.assertTrue(
            any("hard-wrapped" in finding.message for finding in findings)
        )


class EnglishSummaryTests(unittest.TestCase):
    def findings_for(self, text: str) -> list[Finding]:
        findings: list[Finding] = []
        check_english_summary(
            REPOSITORY,
            REPOSITORY_PATH,
            MARKDOWN_PATH,
            text,
            findings,
        )
        return findings

    def test_accepts_first_section_after_separator(self) -> None:
        text = (
            "# Example\n\n"
            "## 日本語概要\n\n"
            "概要の詳細は以下の英語本文を参照してください。\n\n"
            "---\n\n"
            "## English Summary\n\n"
            "This summary explains the document purpose, evidence, boundaries, "
            "and verification method in concise technical English.\n\n"
            "## Details\n"
        )
        self.assertEqual(self.findings_for(text), [])

    def test_rejects_missing_english_summary(self) -> None:
        text = (
            "# Example\n\n"
            "## 日本語概要\n\n"
            "概要の詳細は以下の英語本文を参照してください。\n\n"
            "---\n\n"
            "English text.\n"
        )
        findings = self.findings_for(text)
        self.assertTrue(
            any("must appear exactly once" in finding.message for finding in findings)
        )

    def test_rejects_late_english_summary(self) -> None:
        text = (
            "# Example\n\n"
            "## 日本語概要\n\n"
            "概要の詳細は以下の英語本文を参照してください。\n\n"
            "---\n\n"
            "## Details\n\n"
            "## English Summary\n\n"
            "This summary explains the document purpose, evidence, boundaries, "
            "and verification method in concise technical English.\n"
        )
        findings = self.findings_for(text)
        self.assertTrue(
            any("first English section" in finding.message for finding in findings)
        )


class MarkdownWorkflowTests(unittest.TestCase):
    VALID_WORKFLOW = """\
name: Markdown
on:
  push:
    paths:
      - "**/*.md"
  pull_request:
  workflow_dispatch:
jobs:
  validate:
    uses: cab0a/cab0a/.github/workflows/project-markdown.yml@main
"""

    def findings_for(self, workflow: str | None) -> list[Finding]:
        with TemporaryDirectory() as temporary_directory:
            repository_path = Path(temporary_directory)
            if workflow is not None:
                workflow_path = (
                    repository_path / ".github" / "workflows" / "markdown.yml"
                )
                workflow_path.parent.mkdir(parents=True)
                workflow_path.write_text(workflow, encoding="utf-8")
            findings: list[Finding] = []
            check_markdown_workflow(
                REPOSITORY,
                repository_path,
                findings,
            )
            return findings

    def test_accepts_shared_validator_workflow(self) -> None:
        self.assertEqual(self.findings_for(self.VALID_WORKFLOW), [])

    def test_rejects_missing_workflow(self) -> None:
        findings = self.findings_for(None)
        self.assertTrue(
            any("workflow is missing" in finding.message for finding in findings)
        )

    def test_rejects_workflow_without_markdown_trigger(self) -> None:
        workflow = self.VALID_WORKFLOW.replace('      - "**/*.md"\n', "")
        findings = self.findings_for(workflow)
        self.assertTrue(
            any(
                "Markdown path filter is missing" in finding.message
                for finding in findings
            )
        )


if __name__ == "__main__":
    unittest.main()
