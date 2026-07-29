# Portfolio Markdown Validator

## 日本語概要

この検査は、プロフィールと6つの公開プロジェクトにある全Markdownを対象に、日本語概要、UTF-8、文字化けの兆候、日本語間の不要な半角空白、マージ競合記号、ローカルリンクを確認します。プロジェクトのルートREADMEだけは、主要セクションや代表結果などの構造も追加で検査します。

GitHub Actionsで毎日実行する方法とローカル実行の詳細は以下の英語本文を参照してください。

---

The validator applies one documentation contract across the public portfolio
without duplicating a workflow in every project repository.

## Scope

Every tracked or unignored Markdown file is checked for:

- valid UTF-8 decoding;
- common mojibake symptoms;
- unresolved merge-conflict markers;
- unnecessary ASCII spaces between Japanese characters;
- exactly one Japanese summary after the top-level title, except for the
  complete Japanese profile README;
- balanced code fences;
- working local files, images, and heading anchors;
- machine-specific absolute paths.

The root README of each project receives additional checks for its overview,
representative evidence, Quick Start, artifacts, evaluation boundaries,
reproducibility, development, compatibility, and license sections. These
project-level requirements are not imposed on changelogs, result reports,
research notes, or reference documents.

## Local Run

Run from a workspace that contains the profile and all six project
repositories:

```bash
python cab0a/tools/check_portfolio_markdown.py \
  --workspace . \
  --verbose
```

Use `--strict-git` after committing when every worktree is expected to be
clean. Repository names may be passed as positional arguments to check a
subset.

Exit code `0` means that no failures were found. Exit code `1` means that at
least one documentation contract failed. Invalid command-line arguments use
exit code `2`.

## Scheduled Verification

[`portfolio-markdown.yml`](../.github/workflows/portfolio-markdown.yml) checks
out this profile repository, clones the six public projects, and runs the same
script every day at 00:00 UTC. It also supports manual execution and runs when
the validator, workflow, or profile README changes.

The workflow uses Python's standard library only. It reads repository content
and does not modify files, settings, releases, or Social preview images.
Regression tests exercise the Japanese-spacing, mojibake, merge-marker, and
summary-structure checks before the portfolio scan runs.

## Boundaries

The validator does not decide whether a technical claim is scientifically
supported, request external URLs, execute project tests, reproduce numerical
experiments, or compare documented versions with package metadata. Those
checks remain part of each repository's test and release process.
