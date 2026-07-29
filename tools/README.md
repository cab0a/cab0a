# Portfolio Markdown Validator

## 日本語概要

この検査は、プロフィールと7つの公開プロジェクトにある全Markdownを対象に、日本語概要、README以外の英語概要、UTF-8、文字化けの兆候、日本語間の不要な半角空白、マージ競合記号、ステータスバッジ、ローカルリンクを確認します。Markdownの変更時には対象リポジトリを即時検査し、毎日1回はポートフォリオ全体を検査します。プロジェクトのルートREADMEだけは、主要セクションや代表結果などの構造も追加で検査します。

GitHub Actionsで毎日実行する方法とローカル実行の詳細は以下の英語本文を参照してください。

---

The validator applies one documentation contract across the public portfolio.
Its implementation remains in the profile repository; lightweight project
workflows call that shared implementation instead of copying validation code.

## Scope

Every tracked or unignored Markdown file is checked for:

- valid UTF-8 decoding;
- common mojibake symptoms;
- unresolved merge-conflict markers;
- status or build badge URLs;
- unnecessary ASCII spaces between Japanese characters;
- exactly one Japanese summary after the top-level title, except for the
  complete Japanese profile README;
- exactly one `English Summary` immediately after the Japanese separator in
  every Markdown file not named `README.md`;
- balanced code fences;
- working local files, images, and heading anchors;
- machine-specific absolute paths.

The preregistered Markdown files listed in
`few-shot-anomaly-poc/artifacts/v0.1/freeze/pre-evaluation-freeze.json` keep
their original English-only bytes. The validator exempts them from summary
headings only while each file still matches its recorded SHA-256; all common
text and link checks still apply.

The root README of each project receives additional checks for its overview,
representative evidence, Quick Start, artifacts, evaluation boundaries,
reproducibility, development, compatibility, and license sections. These
project-level requirements are not imposed on changelogs, result reports,
research notes, or reference documents.

Each project is also checked for the lightweight Markdown workflow, its push
and pull-request path filters, and its invocation of the shared validator.

## Local Run

Run from a workspace that contains the profile and all seven project
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
out this profile repository, clones the seven public projects, and runs the same
script every day at 00:00 UTC. It also supports manual execution and runs when
the validator, workflow, or profile README changes.

The workflow uses Python's standard library only. It reads repository content
and does not modify files, settings, releases, or Social preview images.
Regression tests exercise the Japanese-spacing, mojibake, merge-marker, and
summary-structure checks before the portfolio scan runs.

## Immediate Project Verification

Each public project contains a `Markdown` workflow that delegates to
[`project-markdown.yml`](../.github/workflows/project-markdown.yml). A push or
pull request that adds, changes, or removes a Markdown file scans only the
affected repository. Manual execution is also available.

Changes that do not touch Markdown or the workflow file do not start this
additional job. The existing project CI remains responsible for package tests
and artifact reproduction.

## Boundaries

The validator does not decide whether a technical claim is scientifically
supported, request external URLs, execute project tests, reproduce numerical
experiments, or compare documented versions with package metadata. Those
checks remain part of each repository's test and release process.
