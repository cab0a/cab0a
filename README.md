# Python R&D Engineer — Evaluation, Computer Vision, and Point Clouds

## 日本語概要

- Pythonを中心に、コンピュータビジョン、機械学習評価、点群処理、監査可能なデータ処理に取り組んでいます。
- 再現可能なCLI、定量評価、テスト、CI、生成物の検証、明示的な制約説明を重視しています。
- 代表3件は、3D評価の `pointcloud-playground`、実用CLIの `data-cleaning-toolkit`、ML評価設計の `ml-evaluation-workbench` です。
- 画像関連では、入力監査・アルゴリズム比較・研究記録を別リポジトリに分けています。詳細は英語本文を参照してください。

---

I build Python systems for computer-vision experiments, machine-learning
evaluation, point-cloud processing, and auditable data preparation. The work
below is designed to be reviewed through runnable CLIs, committed artifacts,
tests, CI, quantitative comparisons, and explicit claim boundaries.

## Featured Projects

These three repositories provide the shortest review path across 3D research,
an audit-oriented command-line tool, and machine-learning evaluation design.

### [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground)

Evaluates point-cloud methods against controlled geometry and a traceable USGS
3DEP sample, so registration, filtering, normal estimation, and downsampling
can be judged from known transforms, labels, residuals, and recovery error.

- **Problem:** method output can look plausible even when correspondences or
  transforms are wrong.
- **Technology:** Python, NumPy, SciPy, Matplotlib, XYZ/LAZ-derived point data.
- **Evaluation design:** seven experiments, synthetic ground truth, controlled
  overlap and outliers, method-specific metrics, and a shared evidence index
  that does not combine incompatible results into one score.
- **Review:** [Quick Start and results](https://github.com/cab0a/pointcloud-playground#quick-start)

<a href="https://github.com/cab0a/pointcloud-playground/tree/main/results/joint_sensitivity/synthetic"><img src="https://raw.githubusercontent.com/cab0a/pointcloud-playground/main/results/joint_sensitivity/synthetic/comparison.png" width="560" alt="Joint overlap and outlier sensitivity"></a>

### [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit)

Inspects UTF-8 CSV files, drafts reviewable schema candidates, and applies
explicit cleaning rules while preserving row-level and file-level audit
evidence.

- **Problem:** notebook cleanup often hides which values changed, which rows
  were rejected, and whether the output can be regenerated.
- **Technology:** Python standard library, typed package API, JSON schemas,
  deterministic CSV/JSON output, CLI exit codes.
- **Design:** inspection, schema suggestion, and rule-driven cleaning remain
  separate; mapping coverage is reported as an exact-match rate rather than a
  data-quality score.
- **Review:** [30-second workflow and committed artifacts](https://github.com/cab0a/data-cleaning-toolkit#quick-start)

```text
Input rows: 7        Output rows: 3
Invalid rows: 3      Duplicate rows removed: 1
Clean CSV: results/demo_clean.csv
Audit JSON: results/demo_cleaning_report.json
```

### [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench)

Compares fixed classifier baselines on a checksum-pinned public dataset and
exports holdout, fold-level, ablation, prediction, and leakage-diagnostic
evidence.

- **Problem:** a single model score is difficult to interpret without a
  baseline, shared splits, leakage-aware preprocessing, and inspectable errors.
- **Technology:** Python, pandas, scikit-learn pipelines, NumPy, Matplotlib.
- **Evaluation design:** deterministic holdout, shared stratified folds,
  majority-class baseline, feature ablation, split-integrity checks, and a
  shuffled-training-label negative control.
- **Review:** [evaluation methodology and results](https://github.com/cab0a/ml-evaluation-workbench#evaluation-methodology)

<a href="https://github.com/cab0a/ml-evaluation-workbench/tree/main/results"><img src="https://raw.githubusercontent.com/cab0a/ml-evaluation-workbench/main/results/feature_ablation_scores.png" width="560" alt="Feature-ablation macro F1"></a>

## Repository Categories

| Role | Repository | Problem, technology, and reviewable evidence |
| --- | --- | --- |
| Audit-oriented data tools | [data-cleaning-toolkit](https://github.com/cab0a/data-cleaning-toolkit) | Rule-driven CSV normalization and validation using the standard library; emits cleaned data, versioned audit JSON, checksums, and documented exit codes. |
| Audit-oriented data tools | [image-dataset-inspector](https://github.com/cab0a/image-dataset-inspector) | OpenCV CLI for recursive JPEG/PNG inspection; records unreadable files, dimensions, brightness, contrast, and Laplacian variance in a stable CSV inventory. |
| 3D controlled experiments | [pointcloud-playground](https://github.com/cab0a/pointcloud-playground) | NumPy/SciPy experiments for registration, normals, filtering, and downsampling; evaluates known geometry and a public lidar sample with CSV metrics and comparison figures. |
| Computer-vision controlled experiments | [vision-playground](https://github.com/cab0a/vision-playground) | Compares thresholding, denoising, edge detection, and classical segmentation using synthetic masks, a labeled public subset, 165 method-condition evaluations, and checksum-verified numeric artifacts. |
| Machine-learning evaluation | [ml-evaluation-workbench](https://github.com/cab0a/ml-evaluation-workbench) | Evaluates three fixed classifiers with shared holdout and cross-validation splits; exports per-fold scores, row-level predictions, ablations, and leakage diagnostics. |
| Research record | [research-notes](https://github.com/cab0a/research-notes) | Connects focused image-processing questions to source review, controlled fixtures, experiment code, results, interpretation, and limitations; includes cross-platform JPEG decoder contracts. |

The three image-focused repositories serve different purposes:
`image-dataset-inspector` audits inputs before analysis, `vision-playground`
compares algorithms under declared controls, and `research-notes` preserves the
longer chain from question and sources through experiments and bounded
conclusions.

## Engineering Principles Demonstrated in the Repositories

- **Controlled evidence:** synthetic ground truth, known transforms, injected
  labels, fixed public-data revisions, and shared folds make comparisons
  inspectable.
- **Reproducible workflows:** installable packages and CLIs regenerate CSV,
  JSON, Markdown, and figures from committed inputs and configurations.
- **Audit-friendly artifacts:** row-level predictions, fold-level metrics,
  cleaning issues, provenance manifests, and checksums expose intermediate
  evidence rather than only final summaries.
- **Explicit claim boundaries:** README limitations distinguish controlled
  behavior from external validity, semantic quality, or deployment claims.
- **Compatibility as a documented interface:** stable repositories record
  supported CLI commands, public Python names, output filenames or schemas,
  and release boundaries.
- **Verification beyond notebooks:** pytest suites and GitHub Actions exercise
  supported Python versions; selected workflows also rebuild distributions,
  install wheels, regenerate artifacts, and compare them with committed
  references.

## Review Paths

- For **3D geometry and quantitative recovery**, start with
  [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground).
- For **CLI, API, validation, and audit design**, start with
  [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit).
- For **model comparison and evaluation diagnostics**, start with
  [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench).
- For the distinction between **input inspection**, **algorithm experiments**,
  and **research records**, compare
  [Image Dataset Inspector](https://github.com/cab0a/image-dataset-inspector),
  [Vision Playground](https://github.com/cab0a/vision-playground), and
  [Research Notes](https://github.com/cab0a/research-notes).

Repository code is independently written using open-source software, public
datasets, and generated fixtures. Each project documents its license and any
separate data or artifact terms.
