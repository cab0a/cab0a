# Python R&Dエンジニア — 機械学習評価・コンピュータビジョン・点群処理

Pythonを中心に、コンピュータビジョン、機械学習評価、点群処理、監査可能な
データ処理に取り組んでいます。実験コードだけでなく、再実行できるCLI、
公開API、pytest、GitHub Actions、定量評価、検証可能な成果物、制約の説明まで
含めて実装しています。

このプロフィールは日本企業の採用担当者・技術面接官向けの案内です。
各プロジェクトのREADMEは、冒頭に日本語概要を置き、その後に英語の完全な
技術文書を掲載しています。

## 注目してほしい3プロジェクト

3D処理の定量評価、監査可能な実用CLI、機械学習の評価設計を短時間で確認できる
3件です。

### [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground)

既知の形状・変換・対応点・ラベルを使い、point-cloud registration、filtering、
normal estimation、downsamplingを定量評価する実験基盤です。追跡可能な
USGS 3DEP由来サンプルでも別途確認しています。

- **解決する問題:** 見た目では正しく見える点群処理結果でも、対応点、変換、
  幾何学的coverageが誤っている可能性があります。
- **主な技術:** Python、NumPy、SciPy、Matplotlib、XYZ/LAZ由来の点群データ。
- **評価・設計:** 7種類の実験、synthetic ground truth、制御したoverlapと
  outlier、手法別metrics、性質の異なる結果を単一scoreへ混合しないevidence index。
- **確認先:** [Quick Startと評価結果](https://github.com/cab0a/pointcloud-playground#quick-start)

<a href="https://github.com/cab0a/pointcloud-playground/tree/main/results/joint_sensitivity/synthetic"><img src="https://raw.githubusercontent.com/cab0a/pointcloud-playground/main/results/joint_sensitivity/synthetic/comparison.png" width="560" alt="Overlapとoutlierのjoint sensitivity"></a>

### [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit)

UTF-8 CSVの構造を検査し、確認可能なschema候補を作成し、明示的なrulesに
基づいてcleaningするPython CLIです。row-levelとfile-levelの監査証跡を
生成します。

- **解決する問題:** notebook内の前処理だけでは、変更された値、除外された行、
  出力を再生成できる条件が見えにくくなります。
- **主な技術:** Python標準ライブラリ、typed package API、JSON schema、
  決定論的なCSV/JSON、文書化されたCLI exit code。
- **評価・設計:** inspection、schema suggestion、rule-driven cleaningを分離。
  mapping coverageはdata-quality scoreではなくexact-match rateとして報告します。
- **確認先:** [30秒で試せる手順と成果物](https://github.com/cab0a/data-cleaning-toolkit#quick-start)

```text
Input rows: 7        Output rows: 3
Invalid rows: 3      Duplicate rows removed: 1
Clean CSV: results/demo_clean.csv
Audit JSON: results/demo_cleaning_report.json
```

### [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench)

checksumで固定した公開データと共通splitを使い、3種類のclassifierを比較する
評価プロジェクトです。holdout、fold-level metrics、row-level predictions、
ablation、calibration、validation robustness、class-imbalance sensitivityを
成果物として保存します。

- **解決する問題:** 単一のmodel scoreだけでは、baselineとの差、splitの影響、
  leakage、確率品質、誤分類の内容を判断できません。
- **主な技術:** Python、pandas、scikit-learn pipelines、NumPy、Matplotlib。
- **評価・設計:** 6種類の実験から固定方針で25件の代表比較を生成。
  preprocessingは各training partition内でfitし、shuffled-label negative controlと
  split-integrity checksを含みます。v1.0ではCLI、Python API、27個の成果物名、
  15種類のCSV列順、5種類のJSONトップレベルキーを1.x interfaceとして固定しています。
- **確認先:** [評価方法と結果](https://github.com/cab0a/ml-evaluation-workbench#evaluation-methodology)

<a href="https://github.com/cab0a/ml-evaluation-workbench/tree/main/results"><img src="https://raw.githubusercontent.com/cab0a/ml-evaluation-workbench/main/results/feature_ablation_scores.png" width="560" alt="Feature ablationのmacro F1"></a>

## リポジトリ一覧

| 役割 | リポジトリ | 解決する問題・主な技術・確認できる成果物 |
| --- | --- | --- |
| 監査可能なデータ処理 | [data-cleaning-toolkit](https://github.com/cab0a/data-cleaning-toolkit) | Python標準ライブラリによるrule-drivenなCSV normalizationとvalidation。cleaned data、versioned audit JSON、checksum、exit codeを出力します。 |
| 画像データセット監査 | [image-dataset-inspector](https://github.com/cab0a/image-dataset-inspector) | JPEG/PNGを再帰的に検査するOpenCV CLI。decode error、画像サイズ、brightness、contrast、Laplacian varianceを安定したCSVへ記録します。 |
| 3D・点群処理 | [pointcloud-playground](https://github.com/cab0a/pointcloud-playground) | registration、normal estimation、filtering、downsamplingを既知の幾何条件と公開lidarサンプルで評価し、CSV metricsと比較図を生成します。 |
| コンピュータビジョン実験 | [vision-playground](https://github.com/cab0a/vision-playground) | thresholding、denoising、edge detection、classical segmentationをsynthetic maskとラベル付き公開データで比較。165件のmethod-condition evaluationとchecksum検証済み成果物を含みます。 |
| 機械学習評価 | [ml-evaluation-workbench](https://github.com/cab0a/ml-evaluation-workbench) | 3種類のclassifierを共通holdout・cross-validation splitで比較。6種類の実験、25件の代表比較、fold-level score、row-level prediction、安定化された成果物contractを含みます。 |
| 研究記録 | [research-notes](https://github.com/cab0a/research-notes) | 画像処理のresearch question、source review、controlled fixture、実験コード、結果、考察、limitationsを接続。cross-platform JPEG decoder contractも検証しています。 |

画像関連の3件は役割を分けています。`image-dataset-inspector` は実験前の入力監査、
`vision-playground` は宣言した条件下でのalgorithm comparison、`research-notes` は
research questionとsourceから実験、解釈、主張できる範囲までの記録です。

## 複数リポジトリで確認できる設計原則

- **制御された評価:** synthetic ground truth、既知の変換、注入したラベル、
  固定した公開データrevision、共通foldにより比較条件を確認できます。
- **再現可能なworkflow:** installable packageとCLIから、committed inputと設定を使って
  CSV、JSON、Markdown、figureを再生成できます。
- **監査可能な成果物:** row-level prediction、fold-level metrics、cleaning issue、
  provenance manifest、checksumを保存し、最終summaryだけでなく途中の根拠も確認できます。
- **主張範囲の明示:** controlled experimentの結果と、external validity、
  semantic quality、deployment readinessを区別してlimitationsを記録しています。
- **互換性の文書化:** 安定版では、CLI command、public Python name、主要な
  output filename・schema、release boundaryをinterfaceとして明示しています。
- **notebook以外の検証:** pytestとGitHub Actionsで対応Python versionを検証。
  一部ではdistributionのbuild、wheel install、成果物の再生成、committed referenceとの
  比較までCIで実行しています。

## 採用担当者・技術面接官向けの確認順

- **3D geometryと定量的なrecovery error**:
  [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground)
- **CLI、API、validation、監査設計**:
  [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit)
- **model comparisonと評価diagnostics**:
  [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench)
- **input inspection、algorithm experiment、research recordの違い**:
  [Image Dataset Inspector](https://github.com/cab0a/image-dataset-inspector)、
  [Vision Playground](https://github.com/cab0a/vision-playground)、
  [Research Notes](https://github.com/cab0a/research-notes)

各リポジトリのコードは、open-source software、公開データ、生成したfixtureを使って
独立に作成しています。licenseとデータ・成果物に別条件がある場合は、各リポジトリで
明示しています。
