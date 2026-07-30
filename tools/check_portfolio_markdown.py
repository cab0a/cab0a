#!/usr/bin/env python3
"""Validate Markdown contracts across the public GitHub portfolio."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_WORKSPACE = Path(__file__).resolve().parents[2]
PROFILE_REPOSITORY = "cab0a"
PROJECT_REPOSITORIES = (
    "few-shot-anomaly-poc",
    "pointcloud-playground",
    "data-cleaning-toolkit",
    "ml-evaluation-workbench",
    "vision-playground",
    "image-dataset-inspector",
    "research-notes",
)
ALL_REPOSITORIES = (PROFILE_REPOSITORY, *PROJECT_REPOSITORIES)
FEATURED_REPOSITORIES = {
    "few-shot-anomaly-poc",
    "pointcloud-playground",
    "research-notes",
}

INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
JAPANESE_CHAR_CLASS = r"\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff"
JAPANESE_CHAR_RE = re.compile(f"[{JAPANESE_CHAR_CLASS}]")
JAPANESE_INTERNAL_SPACE_RE = re.compile(
    f"[{JAPANESE_CHAR_CLASS}] [{JAPANESE_CHAR_CLASS}]"
)
CONFLICT_MARKER_RE = re.compile(
    r"^(?:<<<<<<<(?: .*)?|=======|>>>>>>>(?: .*)?)$", re.MULTILINE
)
STATUS_BADGE_RE = re.compile(
    r"(?:badge\.svg|https?://(?:img\.)?shields\.io/)",
    re.IGNORECASE,
)
MOJIBAKE_PATTERNS = (
    (
        "Unicode replacement character",
        re.compile("\ufffd"),
    ),
    (
        "common Japanese encoding corruption",
        re.compile(
            r"(?:縺|繧|繝|譁|蜿|荳|莠)"
            r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]{1,2}"
        ),
    ),
    (
        "common UTF-8 decoded as a Western encoding",
        re.compile(r"(?:Ã[\x80-\xff]|Â[\x80-\xff]|â(?:€™|€œ|€|™))"),
    ),
)
AUDIENCE_PATTERNS = (
    re.compile(r"\b(?:intended|designed)\s+for\b", re.IGNORECASE),
    re.compile(r"\buseful\s+for\b", re.IGNORECASE),
    re.compile(
        r"\bfor\s+(?:researchers|engineers|reviewers|teams|users|practitioners)\b",
        re.IGNORECASE,
    ),
    re.compile(r"(?:担当者|利用者|研究者|エンジニア|レビュー担当者)向け"),
    re.compile(r"(?:担当者|利用者|研究者|エンジニア|レビュー担当者)に役立"),
)
MACHINE_PATH_PATTERNS = (
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    re.compile(r"\\\\wsl\.localhost\\", re.IGNORECASE),
    re.compile(r"file://", re.IGNORECASE),
)
REQUIRED_EXACT_HEADINGS = (
    "Overview",
    "Key Features",
    "Quick Start",
    "Generated Artifacts",
    "Reproducibility",
    "Development and Testing",
    "License",
)
IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
    "output",
    "regenerated-results",
}
FEW_SHOT_FREEZE_RECORD = Path(
    "artifacts/v0.1/freeze/pre-evaluation-freeze.json"
)


@dataclass(frozen=True)
class Finding:
    level: str
    repository: str
    location: str
    message: str


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check Japanese summaries, encoding symptoms, merge markers, "
            "local links, README structure, and optional Git cleanliness."
        )
    )
    parser.add_argument(
        "repositories",
        nargs="*",
        choices=ALL_REPOSITORIES,
        help="Repository names to check. The default is all eight repositories.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help=(
            "Directory containing all repository directories. "
            f"Default: {DEFAULT_WORKSPACE}"
        ),
    )
    parser.add_argument(
        "--strict-git",
        action="store_true",
        help="Treat an uncommitted worktree as a failure instead of a warning.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the Markdown count and branch status for each repository.",
    )
    return parser.parse_args()


def markdown_files(repository_path: Path) -> list[Path]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            "*.md",
        ],
        cwd=repository_path,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode == 0:
        return sorted(
            repository_path / relative_path
            for relative_path in completed.stdout.split("\0")
            if relative_path
        )

    files: list[Path] = []
    for path in repository_path.rglob("*.md"):
        relative_parts = path.relative_to(repository_path).parts
        if any(part in IGNORED_DIRECTORIES for part in relative_parts):
            continue
        files.append(path)
    return sorted(files)


def verified_summary_exemptions(
    repository: str,
    repository_path: Path,
    findings: list[Finding],
) -> set[Path]:
    """Return immutable historical Markdown whose recorded bytes still match."""
    if repository != "few-shot-anomaly-poc":
        return set()

    record_path = repository_path / FEW_SHOT_FREEZE_RECORD
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        frozen_files = record["frozen_files"]
    except (FileNotFoundError, UnicodeDecodeError, json.JSONDecodeError, KeyError) as error:
        findings.append(
            Finding(
                "FAIL",
                repository,
                str(FEW_SHOT_FREEZE_RECORD),
                f"could not read the pre-evaluation freeze record: {error}",
            )
        )
        return set()

    exemptions: set[Path] = set()
    for item in frozen_files:
        if not isinstance(item, dict):
            continue
        relative_path = item.get("relative_path")
        expected_sha256 = item.get("sha256")
        if (
            not isinstance(relative_path, str)
            or not relative_path.endswith(".md")
            or not isinstance(expected_sha256, str)
        ):
            continue
        markdown_path = repository_path / relative_path
        try:
            observed_sha256 = hashlib.sha256(markdown_path.read_bytes()).hexdigest()
        except OSError as error:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    relative_path,
                    f"could not verify frozen Markdown: {error}",
                )
            )
            continue
        if observed_sha256 != expected_sha256:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    relative_path,
                    "frozen Markdown no longer matches its pre-evaluation SHA-256",
                )
            )
            continue
        exemptions.add(markdown_path.resolve())
    return exemptions


def read_markdown(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    findings: list[Finding],
) -> str | None:
    location = str(markdown_path.relative_to(repository_path))
    try:
        return markdown_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"file is not valid UTF-8: {error}",
            )
        )
    except OSError as error:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"file could not be read: {error}",
            )
        )
    return None


def strip_heading_markup(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").replace("_", "")
    return text.strip().rstrip("#").strip()


def github_slug(text: str) -> str:
    normalized = strip_heading_markup(text).lower()
    kept: list[str] = []
    for character in normalized:
        category = unicodedata.category(character)
        if category.startswith(("L", "N")) or character in {" ", "-", "_"}:
            kept.append(character)
    return re.sub(r"\s+", "-", "".join(kept).strip())


def heading_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = github_slug(match.group(2))
        count = counts.get(base, 0)
        slug = base if count == 0 else f"{base}-{count}"
        counts[base] = count + 1
        slugs.add(slug)
    return slugs


def clean_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif re.search(r"\s+[\"']", target):
        target = re.split(r"\s+[\"']", target, maxsplit=1)[0]
    return unquote(target)


def is_external_target(target: str) -> bool:
    scheme = urlparse(target).scheme.lower()
    return scheme in {"http", "https", "mailto", "tel", "data"}


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_common_text_quality(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    location = str(markdown_path.relative_to(repository_path))

    conflict_match = CONFLICT_MARKER_RE.search(text)
    if conflict_match:
        findings.append(
            Finding(
                "FAIL",
                repository,
                f"{location}:{line_number(text, conflict_match.start())}",
                f"unresolved merge-conflict marker: {conflict_match.group(0)!r}",
            )
        )

    badge_match = STATUS_BADGE_RE.search(text)
    if badge_match:
        findings.append(
            Finding(
                "FAIL",
                repository,
                f"{location}:{line_number(text, badge_match.start())}",
                "status badges are not used in portfolio Markdown",
            )
        )

    for label, pattern in MOJIBAKE_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    f"{location}:{line_number(text, match.start())}",
                    f"{label}: {match.group(0)!r}",
                )
            )

    for match in JAPANESE_INTERNAL_SPACE_RE.finditer(text):
        findings.append(
            Finding(
                "FAIL",
                repository,
                f"{location}:{line_number(text, match.start())}",
                f"unnecessary ASCII space between Japanese characters: {match.group(0)!r}",
            )
        )


def check_fences(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    fences = [
        line for line in text.splitlines() if re.match(r"^\s*(?:```|~~~)", line)
    ]
    if len(fences) % 2:
        findings.append(
            Finding(
                "FAIL",
                repository,
                str(markdown_path.relative_to(repository_path)),
                f"unbalanced fenced code blocks ({len(fences)} fence lines)",
            )
        )


def check_machine_paths(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    location = str(markdown_path.relative_to(repository_path))
    for pattern in MACHINE_PATH_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    f"{location}:{line_number(text, match.start())}",
                    f"machine-specific path or file URI found: {match.group(0)!r}",
                )
            )


def check_local_links(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    location = str(markdown_path.relative_to(repository_path))
    raw_targets = [match.group(1) for match in INLINE_LINK_RE.finditer(text)]
    raw_targets.extend(match.group(1) for match in HTML_LINK_RE.finditer(text))
    source_slugs = heading_slugs(text)

    for raw_target in raw_targets:
        target = clean_link_target(raw_target)
        if not target or is_external_target(target):
            continue

        if target.startswith("#"):
            anchor = target[1:]
            if anchor and anchor not in source_slugs:
                findings.append(
                    Finding(
                        "FAIL",
                        repository,
                        location,
                        f"missing local heading anchor: #{anchor}",
                    )
                )
            continue

        path_text, separator, anchor = target.partition("#")
        target_path = (markdown_path.parent / path_text).resolve()
        if not target_path.exists():
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    location,
                    f"missing local target: {target}",
                )
            )
            continue

        if separator and anchor and target_path.suffix.lower() == ".md":
            try:
                target_text = target_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if anchor not in heading_slugs(target_text):
                findings.append(
                    Finding(
                        "FAIL",
                        repository,
                        location,
                        f"missing heading anchor in {path_text}: #{anchor}",
                    )
                )


def is_prose(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and not re.match(
        r"^(?:[-*+] |\d+\. |>|#{1,6} |```|~~~|\|)", stripped
    )


def check_japanese_summary(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
    *,
    root_readme: bool,
) -> None:
    location = str(markdown_path.relative_to(repository_path))
    lines = text.splitlines()
    positions = [index for index, line in enumerate(lines) if line == "## 日本語概要"]

    if positions != [2]:
        display_positions = ", ".join(str(index + 1) for index in positions) or "none"
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "`## 日本語概要` must appear exactly once on line 3; "
                f"found {display_positions}",
            )
        )
        return

    try:
        rule_index = lines.index("---", positions[0] + 1)
    except ValueError:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "Japanese summary is not followed by a horizontal rule",
            )
        )
        return

    summary_lines = lines[positions[0] + 1 : rule_index]
    summary_text = "\n".join(summary_lines)
    character_count = len(re.sub(r"\s+", "", summary_text))
    minimum = 180 if root_readme else 70
    maximum = 450
    if not minimum <= character_count <= maximum:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"Japanese summary length is {character_count}; "
                f"expected {minimum}–{maximum} characters",
            )
        )

    if not JAPANESE_CHAR_RE.search(summary_text):
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "Japanese summary does not contain Japanese text",
            )
        )
    if "英語本文" not in summary_text:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "Japanese summary must point to the canonical English text",
            )
        )

    for offset in range(len(summary_lines) - 1):
        if is_prose(summary_lines[offset]) and is_prose(summary_lines[offset + 1]):
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    f"{location}:{positions[0] + 2 + offset}",
                    "Japanese prose appears hard-wrapped across physical lines",
                )
            )


def check_english_summary(
    repository: str,
    repository_path: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    location = str(markdown_path.relative_to(repository_path))
    lines = text.splitlines()
    positions = [
        index for index, line in enumerate(lines) if line == "## English Summary"
    ]

    if len(positions) != 1:
        display_positions = ", ".join(str(index + 1) for index in positions) or "none"
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "`## English Summary` must appear exactly once in non-README "
                f"Markdown; found {display_positions}",
            )
        )
        return

    try:
        japanese_position = lines.index("## 日本語概要")
        rule_index = lines.index("---", japanese_position + 1)
    except ValueError:
        return

    first_content_index = rule_index + 1
    while (
        first_content_index < len(lines)
        and not lines[first_content_index].strip()
    ):
        first_content_index += 1

    if positions[0] != first_content_index:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "`## English Summary` must be the first English section after "
                "the Japanese summary separator",
            )
        )

    section_end = len(lines)
    for index in range(positions[0] + 1, len(lines)):
        if lines[index].startswith("## "):
            section_end = index
            break

    summary_text = "\n".join(lines[positions[0] + 1 : section_end])
    word_count = len(re.findall(r"\b[A-Za-z][A-Za-z0-9'-]*\b", summary_text))
    if not 12 <= word_count <= 120:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"English summary contains {word_count} words; expected 12–120",
            )
        )


def check_project_readme(
    repository: str, text: str, findings: list[Finding]
) -> None:
    headings = [
        strip_heading_markup(match.group(2))
        for line in text.splitlines()
        if (match := HEADING_RE.match(line))
    ]
    heading_set = set(headings)
    for heading in REQUIRED_EXACT_HEADINGS:
        if heading not in heading_set:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    "README.md",
                    f"missing required section: {heading}",
                )
            )

    if not any(heading.startswith("Representative") for heading in headings):
        findings.append(
            Finding(
                "FAIL",
                repository,
                "README.md",
                "missing representative result or comparison section",
            )
        )
    if not any(
        "Evaluation" in heading or "Claim Boundaries" in heading
        for heading in headings
    ):
        findings.append(
            Finding(
                "FAIL",
                repository,
                "README.md",
                "missing evaluation design or claim-boundary section",
            )
        )
    if not any(heading.startswith("Compatibility") for heading in headings):
        findings.append(
            Finding(
                "FAIL",
                repository,
                "README.md",
                "missing compatibility section",
            )
        )
    if not (
        any("Limitations" in heading or "Boundaries" in heading for heading in headings)
        or "docs/limitations.md" in text
    ):
        findings.append(
            Finding(
                "FAIL",
                repository,
                "README.md",
                "limitations or claim boundaries are not discoverable",
            )
        )

    for pattern in AUDIENCE_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    "README.md",
                    f"audience-targeting wording found: {match.group(0)!r}",
                )
            )


def check_profile(text: str, findings: list[Finding]) -> None:
    lines = text.splitlines()
    if any(line == "## 日本語概要" for line in lines):
        findings.append(
            Finding(
                "FAIL",
                PROFILE_REPOSITORY,
                "README.md",
                "profile README must remain canonical Japanese without `## 日本語概要`",
            )
        )

    japanese_count = len(JAPANESE_CHAR_RE.findall(text))
    if japanese_count < 500:
        findings.append(
            Finding(
                "FAIL",
                PROFILE_REPOSITORY,
                "README.md",
                f"profile contains only {japanese_count} Japanese characters; "
                "the complete Japanese profile may have been shortened",
            )
        )

    for repository in PROJECT_REPOSITORIES:
        url = f"https://github.com/cab0a/{repository}"
        if url not in text:
            findings.append(
                Finding(
                    "FAIL",
                    PROFILE_REPOSITORY,
                    "README.md",
                    f"profile does not link to {repository}",
                )
            )

    featured_match = re.search(
        r"^## 代表プロジェクト\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        re.MULTILINE,
    )
    if not featured_match:
        findings.append(
            Finding(
                "FAIL",
                PROFILE_REPOSITORY,
                "README.md",
                "missing `## 代表プロジェクト` section",
            )
        )
    else:
        featured_links = {
            repository
            for repository in PROJECT_REPOSITORIES
            if f"https://github.com/cab0a/{repository}" in featured_match.group(1)
        }
        if featured_links != FEATURED_REPOSITORIES:
            findings.append(
                Finding(
                    "FAIL",
                    PROFILE_REPOSITORY,
                    "README.md",
                    "Featured Projects must contain exactly few-shot-anomaly-poc, "
                    "pointcloud-playground, and research-notes",
                )
            )

    banned_profile_phrases = (
        "採用担当者・技術面接官向け",
        "採用担当者・技術面接官向けの確認順",
        "READMEの言語",
    )
    for phrase in banned_profile_phrases:
        if phrase in text:
            findings.append(
                Finding(
                    "FAIL",
                    PROFILE_REPOSITORY,
                    "README.md",
                    f"unwanted profile meta-explanation found: {phrase!r}",
                )
            )


def check_profile_remote_anchors(
    workspace: Path, text: str, findings: list[Finding]
) -> None:
    pattern = re.compile(
        r"https://github\.com/cab0a/"
        r"(?P<repository>[A-Za-z0-9._-]+)"
        r"(?:/[A-Za-z0-9._/-]+)?"
        r"#(?P<anchor>[A-Za-z0-9._-]+)"
    )
    for match in pattern.finditer(text):
        repository = match.group("repository")
        if repository not in PROJECT_REPOSITORIES:
            continue
        target_readme = workspace / repository / "README.md"
        try:
            target_text = target_readme.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if match.group("anchor") not in heading_slugs(target_text):
            findings.append(
                Finding(
                    "FAIL",
                    PROFILE_REPOSITORY,
                    "README.md",
                    f"broken profile anchor: {repository}#{match.group('anchor')}",
                )
            )


def check_local_agents(
    repository: str,
    repository_path: Path,
    findings: list[Finding],
) -> None:
    agents_path = repository_path / "AGENTS.md"
    agents_tracked = (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", "AGENTS.md"],
            cwd=repository_path,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).returncode
        == 0
    )
    if agents_tracked:
        findings.append(
            Finding(
                "FAIL",
                repository,
                "AGENTS.md",
                "local AGENTS.md must not be tracked or committed",
            )
        )
    elif agents_path.exists():
        agents_ignored = (
            subprocess.run(
                ["git", "check-ignore", "--quiet", "--", "AGENTS.md"],
                cwd=repository_path,
                check=False,
            ).returncode
            == 0
        )
        if not agents_ignored:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    "AGENTS.md",
                    "local AGENTS.md exists but is not excluded from Git",
                )
            )


def check_markdown_workflow(
    repository: str,
    repository_path: Path,
    findings: list[Finding],
) -> None:
    workflow_path = repository_path / ".github" / "workflows" / "markdown.yml"
    location = ".github/workflows/markdown.yml"
    try:
        workflow_text = workflow_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                "shared Markdown validation workflow is missing",
            )
        )
        return
    except UnicodeDecodeError as error:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"workflow is not valid UTF-8: {error}",
            )
        )
        return
    except OSError as error:
        findings.append(
            Finding(
                "FAIL",
                repository,
                location,
                f"workflow could not be read: {error}",
            )
        )
        return

    required_fragments = {
        "push trigger": "  push:",
        "pull-request trigger": "  pull_request:",
        "manual trigger": "  workflow_dispatch:",
        "Markdown path filter": '"**/*.md"',
        "shared workflow reference": (
            "uses: cab0a/cab0a/.github/workflows/"
            "project-markdown.yml@main"
        ),
    }
    for requirement, fragment in required_fragments.items():
        if fragment not in workflow_text:
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    location,
                    f"{requirement} is missing",
                )
            )


def git_status(repository_path: Path) -> tuple[bool, str]:
    completed = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=repository_path,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode:
        return False, completed.stderr.strip() or "git status failed"
    lines = completed.stdout.splitlines()
    dirty_lines = [line for line in lines if not line.startswith("##")]
    branch_line = lines[0] if lines else "branch unknown"
    return not dirty_lines, branch_line


def check_repository(
    workspace: Path,
    repository: str,
    strict_git: bool,
) -> tuple[list[Finding], int, str]:
    findings: list[Finding] = []
    repository_path = workspace / repository
    root_readme = repository_path / "README.md"

    if not repository_path.is_dir():
        return [
            Finding("FAIL", repository, ".", "repository directory is missing")
        ], 0, "repository missing"
    if not root_readme.is_file():
        return [
            Finding("FAIL", repository, "README.md", "root README is missing")
        ], 0, "README missing"

    check_local_agents(repository, repository_path, findings)
    if repository in PROJECT_REPOSITORIES:
        check_markdown_workflow(repository, repository_path, findings)

    files = markdown_files(repository_path)
    summary_exemptions = verified_summary_exemptions(
        repository,
        repository_path,
        findings,
    )
    texts: dict[Path, str] = {}
    for markdown_path in files:
        markdown_text = read_markdown(
            repository, repository_path, markdown_path, findings
        )
        if markdown_text is None:
            continue
        texts[markdown_path] = markdown_text

        lines = markdown_text.splitlines()
        top_level_headings = [
            line for line in lines if re.match(r"^# ", line)
        ]
        if (
            not lines
            or not lines[0].startswith("# ")
            or len(top_level_headings) != 1
        ):
            findings.append(
                Finding(
                    "FAIL",
                    repository,
                    str(markdown_path.relative_to(repository_path)),
                    "Markdown must start with exactly one top-level heading",
                )
            )

        is_profile_readme = (
            repository == PROFILE_REPOSITORY and markdown_path == root_readme
        )
        if not is_profile_readme and markdown_path.resolve() not in summary_exemptions:
            check_japanese_summary(
                repository,
                repository_path,
                markdown_path,
                markdown_text,
                findings,
                root_readme=(
                    repository in PROJECT_REPOSITORIES
                    and markdown_path == root_readme
                ),
            )
            if markdown_path.name != "README.md":
                check_english_summary(
                    repository,
                    repository_path,
                    markdown_path,
                    markdown_text,
                    findings,
                )

        check_common_text_quality(
            repository, repository_path, markdown_path, markdown_text, findings
        )
        check_fences(
            repository, repository_path, markdown_path, markdown_text, findings
        )
        check_machine_paths(
            repository, repository_path, markdown_path, markdown_text, findings
        )
        check_local_links(
            repository, repository_path, markdown_path, markdown_text, findings
        )

    root_text = texts.get(root_readme)
    if root_text is not None:
        if repository == PROFILE_REPOSITORY:
            check_profile(root_text, findings)
            check_profile_remote_anchors(workspace, root_text, findings)
        else:
            check_project_readme(repository, root_text, findings)

    clean, branch_status = git_status(repository_path)
    if not clean:
        findings.append(
            Finding(
                "FAIL" if strict_git else "WARN",
                repository,
                ".git",
                "worktree contains uncommitted changes",
            )
        )
    return findings, len(files), branch_status


def main() -> int:
    arguments = parse_arguments()
    workspace = arguments.workspace.resolve()
    repositories = tuple(arguments.repositories) or ALL_REPOSITORIES
    all_findings: list[Finding] = []
    results: dict[str, tuple[int, str]] = {}

    for repository in repositories:
        findings, file_count, branch_status = check_repository(
            workspace, repository, arguments.strict_git
        )
        all_findings.extend(findings)
        results[repository] = (file_count, branch_status)

    for repository in repositories:
        repository_findings = [
            finding for finding in all_findings if finding.repository == repository
        ]
        failures = [
            finding for finding in repository_findings if finding.level == "FAIL"
        ]
        warnings = [
            finding for finding in repository_findings if finding.level == "WARN"
        ]
        if failures:
            status = "FAIL"
        elif warnings:
            status = "WARN"
        else:
            status = "PASS"

        file_count, branch_status = results[repository]
        detail = (
            f" ({file_count} Markdown files; {branch_status})"
            if arguments.verbose
            else ""
        )
        print(f"{status:4} {repository}{detail}")
        for finding in repository_findings:
            print(f"     {finding.level}: {finding.location}: {finding.message}")

    failure_count = sum(
        finding.level == "FAIL" for finding in all_findings
    )
    warning_count = sum(
        finding.level == "WARN" for finding in all_findings
    )
    print(
        f"\nSUMMARY repositories={len(repositories)} "
        f"failures={failure_count} warnings={warning_count}"
    )
    return 1 if failure_count else 0


if __name__ == "__main__":
    sys.exit(main())
