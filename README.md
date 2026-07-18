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

### [Vision Playground](https://github.com/cab0a/vision-playground)

A reproducible collection of OpenCV experiments covering thresholding, parameter sensitivity, denoising, edge detection, and classical segmentation.

- Stable release: [`v1.0.0`](https://github.com/cab0a/vision-playground/releases/tag/v1.0.0)
- Five registered experiments and 165 method-condition evaluations
- Includes synthetic ground truth, a labeled public-data subset, CSV metrics, visual comparisons, tests, CI, and SHA-256 result verification
- Documents assumptions, failure conditions, valid interpretations, and limitations

### [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground)

A reproducible point-cloud experiment that evaluates centroid-based voxel downsampling on controlled synthetic data and a traceable public USGS 3DEP lidar sample.

- Initial release: [`v0.1.0`](https://github.com/cab0a/pointcloud-playground/releases/tag/v0.1.0)
- Reports point retention, nearest-neighbor spacing, and coverage RMSE across multiple voxel sizes
- Includes deterministic data generation, source checksums, CSV metrics, comparison plots, a CLI, tests, and CI for Python 3.10 through 3.14
- Documents the relationship between point reduction and geometric coverage without prescribing a universal parameter choice

## Planned Public Projects

| Project | Scope |
| --- | --- |
| `data-cleaning-toolkit` | Utilities for validating, cleaning, and transforming tabular data |
| `research-notes` | Notes on papers, methods, and technical investigations |
| `research-to-poc` | Case studies documenting the path from research to prototype and evaluation |

All public work is based on independently created code, open-source software, public datasets, and public research.
