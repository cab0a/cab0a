# Research and Development Engineer

I build small, reproducible systems for technical investigation and proof-of-concept development using Python.

My work focuses on machine learning, computer vision, image processing, 3D and point-cloud data, data processing, and automation. The emphasis is not only on implementation, but also on selecting an appropriate method, evaluating its behavior, identifying failure conditions, and documenting the result.

## Engineering Workflow

`Research → Method Selection → Prototype → Evaluation → Improvement → Documentation`

This workflow is used to move from an open technical question to a reviewable implementation and evidence-based conclusion.

## Technical Focus

- **Python Development:** command-line tools, data processing, automation, testing, and maintainable package structure
- **Machine Learning and Computer Vision:** reproducible experiments, image processing, object detection, and method comparison
- **3D and Point-Cloud Processing:** public-data experiments, geometric processing, analysis, and quantitative evaluation
- **Technical Investigation:** literature review, method selection, prototype development, and feasibility testing
- **Evaluation:** metrics, parameter sensitivity, error analysis, benchmarking, and reproducibility

## Featured Projects

### [Image Dataset Inspector](https://github.com/cab0a/image-dataset-inspector)

A Python and OpenCV CLI that recursively inspects JPEG and PNG datasets, records unreadable files without stopping the scan, and exports dimensions, file size, brightness, contrast, and Laplacian-based blur metrics to CSV.

- Stable sample release: [`v0.1.2`](https://github.com/cab0a/image-dataset-inspector/releases/tag/v0.1.2)
- Includes generated demo images, checksum-verified public samples, unit tests, and CI
- Demonstrates input validation and dataset inspection before downstream vision experiments

### [Research Notes](https://github.com/cab0a/research-notes)

Reproducible technical investigations that connect source review and method
selection to controlled experiments, evaluation, interpretation, and explicit
limitations.

- Current release: [`v0.11.0`](https://github.com/cab0a/research-notes/releases/tag/v0.11.0)
- Fixes ten synthetic baseline, progressive, restart-marker, grayscale, RGB, and CMYK streams and compares OpenCV, Pillow, and FFmpeg decoder paths across five GitHub-hosted platform profiles
- Records 150 successful stream and array-interface contracts, 75 pixel-exact matched syntax comparisons, and an FFmpeg 4:2:0 cross-platform hash split isolated to the macOS arm64 profile
- Includes fixture and runtime manifests, committed cross-platform CSV reports and figures, 42 tests, and a full CI matrix without treating code-value differences as perceptual quality thresholds

### [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit)

A deterministic Python CLI for inspecting UTF-8 CSV files, drafting reviewable
schema rules, and applying explicit value mapping, normalization, column-level,
cross-column, and conditional-presence validation, and deduplication with
machine-readable audit evidence.

- Stable release: [`v1.0.0`](https://github.com/cab0a/data-cleaning-toolkit/releases/tag/v1.0.0)
- Separates structural inspection, conservative schema suggestion, and reviewed schema-driven cleaning
- Defines stable 1.x boundaries for its typed public Python API, CLI contract, and cleaning-report version 1
- Maps reviewed aliases with exact rules and records row-level audit evidence for each applied mapping
- Summarizes per-column and overall exact mapping coverage while keeping the result distinct from a data-quality score
- Supports raw, redacted, and disabled unmatched-value summaries with deterministic ordering and explicit disclosure boundaries
- Validates named equality and ordering relationships between normalized columns
- Enforces named one-to-one presence dependencies after normalization and records the trigger and target in each failure
- Includes controlled type, value-mapping, mapping-coverage, unmatched-frequency, privacy-mode, cross-column, conditional-presence, public API, and reproducibility evaluations, 16 checksum-verified reference artifacts, 94 tests, and CI for Python 3.10 through 3.14

### [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench)

A reproducible machine-learning evaluation project that compares controlled classifier baselines on a pinned public dataset.

- Current release: [`v0.3.0`](https://github.com/cab0a/ml-evaluation-workbench/releases/tag/v0.3.0)
- Compares a majority-class dummy, logistic regression, and fixed 5-nearest-neighbors classifier on the same holdout and five stratified folds
- Fits preprocessing inside every training partition and keeps KNN parameters fixed rather than selecting them from evaluation scores
- Reports holdout and fold-level metrics, variability summaries, paired differences, row-level predictions, and comparison figures
- Records KNN macro F1 of 0.949 ± 0.018 versus 0.928 ± 0.041 for logistic regression, while documenting a fold where KNN trails
- Includes CC0 dataset provenance, six SHA-256-verified reference artifacts, 23 tests, and CI for Python 3.10 through 3.14

### [Vision Playground](https://github.com/cab0a/vision-playground)

A reproducible collection of OpenCV experiments covering thresholding, parameter sensitivity, denoising, edge detection, and classical segmentation.

- Stable release: [`v1.0.0`](https://github.com/cab0a/vision-playground/releases/tag/v1.0.0)
- Five registered experiments and 165 method-condition evaluations
- Includes synthetic ground truth, a labeled public-data subset, CSV metrics, visual comparisons, tests, CI, and SHA-256 result verification
- Documents assumptions, failure conditions, valid interpretations, and limitations

### [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground)

A stable, reproducible point-cloud experiment suite covering voxel downsampling, statistical outlier filtering, local PCA normal estimation, controlled rigid registration, partial-overlap registration, joint overlap-and-outlier sensitivity, and cross-experiment evidence review on synthetic data and a traceable public USGS 3DEP lidar sample.

- Current release: [`v1.0.0`](https://github.com/cab0a/pointcloud-playground/releases/tag/v1.0.0)
- Evaluates 48 joint sensitivity conditions per dataset across four overlap levels, four controlled outlier rates, and three correspondence-retention policies
- Uses known transforms, overlap membership, exact generating pairs, and outlier labels to report correspondence composition, precision and recall, outlier rejection, residuals, transform error, and recovery
- Demonstrates a controlled effective-valid-pair boundary while keeping experimental findings separate from production parameter recommendations
- Consolidates fourteen result sets spanning seven experiments and two datasets into a shared review schema without combining incompatible metrics into one score
- Defines a stable 1.x contract for the top-level Python API, existing CLI, primary output filenames, and CSV schemas
- Supports non-destructive reference regeneration and verifies two inputs, fifteen CSV reports, one generated Markdown summary, and fifteen figures
- Includes 68 tests plus sdist, wheel, installation, and CLI checks in CI for Python 3.10 through 3.14
- Documents API, reproducibility, evidence, limitation, changelog, and stable-release review boundaries

## Planned Public Projects

| Project | Scope |
| --- | --- |
| `research-to-poc` | Case studies documenting the path from research to prototype and evaluation |

All public work is based on independently created code, open-source software, public datasets, and public research.
