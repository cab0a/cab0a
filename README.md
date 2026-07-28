# Python R&Dエンジニア

CAD・設計支援ツール開発を起点に、現在はMMS画像・点群を用いた
3D都市モデルの自動作成・更新に関する要素技術開発に取り組んでいます。
公開リポジトリでは、再現性、定量評価、監査可能性を、
synthetic dataとpublic dataで確認できる形にしています。

- **AI・3D R&D:** 7種の都市設備を対象に、MMS画像と点群を用いた
  検出・分類、3次元位置・形状推定、LOD3自動モデリングを開発
- **CAD・設計支援:** CATIA・SOLIDWORKSの設計経験を基に、
  CATVBA・C#・Excel VBAで業務を自動化し、年間約1,000時間の工数削減に貢献
- **開発経験:** 技術調査、要件定義、設計、実装、レビュー、テスト、評価、
  導入、保守
- **公開成果物:** CLI、公開API、pytest、GitHub Actions、CSV・JSON、評価図、
  checksum、監査レポート

## 代表プロジェクト

### [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground) — 点群処理を既知の真値で評価

位置合わせ、外れ値除去、法線推定、downsamplingを、既知の変換・対応点・
ラベルを使って評価する実験基盤です。

- **実装:** NumPy・SciPyによる7種類の実験と、追跡可能なUSGS 3DEP由来サンプル
- **評価:** overlapとoutlierを制御し、変換誤差、対応点、幾何学的coverageを測定
- **成果物:** 条件別CSV metrics、比較図、再生成用CLI

[Quick Startと評価結果](https://github.com/cab0a/pointcloud-playground#quick-start)

<a href="https://github.com/cab0a/pointcloud-playground/tree/main/results/joint_sensitivity/synthetic"><img src="https://raw.githubusercontent.com/cab0a/pointcloud-playground/main/results/joint_sensitivity/synthetic/comparison.png" width="560" alt="Overlapとoutlierのjoint sensitivity"></a>

### [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit) — 変更内容を追跡できるCSV cleaning

CSVの構造確認、schema候補の作成、明示的なrulesによるcleaningを分離した
Python CLIです。

- **実装:** Python標準ライブラリ、typed API、JSON schema、文書化されたexit code
- **監査:** 変更・除外理由をrow単位で記録し、決定論的なCSV・JSONとchecksumを出力

```text
Input rows: 7        Output rows: 3
Invalid rows: 3      Duplicate rows removed: 1
Clean CSV: results/demo_clean.csv
Audit JSON: results/demo_cleaning_report.json
```

[Quick Startと成果物](https://github.com/cab0a/data-cleaning-toolkit#quick-start)

### [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench) — モデル評価の根拠を残す

固定した公開データと共通splitを使い、3種類の分類器を同じ条件で比較する
評価プロジェクトです。

- **評価:** baseline、feature ablation、calibration、validation robustness、
  class-imbalance sensitivityを含む6種類の実験と25件の代表比較
- **成果物:** fold-level metrics、row-level predictions、誤分類、評価図、SHA-256 manifest
- **互換性:** v1.0でCLI、Python API、主要な成果物名とschemaを1.x interfaceとして固定

[評価方法と結果](https://github.com/cab0a/ml-evaluation-workbench#evaluation-methodology)

<a href="https://github.com/cab0a/ml-evaluation-workbench/tree/main/results"><img src="https://raw.githubusercontent.com/cab0a/ml-evaluation-workbench/main/results/feature_ablation_scores.png" width="560" alt="Feature ablationのmacro F1"></a>

## 画像処理リポジトリの役割

- **入力監査 — [Image Dataset Inspector](https://github.com/cab0a/image-dataset-inspector):**
  JPEG・PNGを再帰的に検査し、decode error、画像サイズ、brightness、contrast、
  Laplacian varianceをCSVへ記録します。
- **手法比較 — [Vision Playground](https://github.com/cab0a/vision-playground):**
  thresholding、denoising、edge detection、classical segmentationを、
  synthetic ground truthと公開データで165件のmethod-condition評価にかけます。
- **研究記録 — [Research Notes](https://github.com/cab0a/research-notes):**
  research question、source、仮説、実験、結果、考察、limitationsを接続し、
  cross-platformのJPEG decoder contractも検証しています。

## 共通する設計

- **再現性:** commit済みの入力と設定から、CLIで数値成果物と図を再生成
- **定量評価:** 既知の真値、共通split、制御したfixtureを使って条件間を比較
- **監査可能性:** row・fold・条件単位の結果とprovenance・checksumを保存
- **制約の明示:** controlled experimentの結果と外部への一般化可能性を区別
- **継続的な検証:** pytestとGitHub Actionsで対応Pythonバージョンと主要interfaceを確認
