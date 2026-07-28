# Python R&Dエンジニア

機械学習評価、コンピュータビジョン、点群・3Dデータ処理を中心に、
再現可能な実験基盤と監査可能なPythonツールを実装しています。

- **主な領域:** 機械学習評価、画像処理、点群・3Dデータ処理、データ品質確認
- **開発経験:** 技術調査、要件定義、設計、実装、レビュー、テスト、評価、
  導入、保守
- **公開成果物:** CLI、公開API、pytest、GitHub Actions、CSV・JSON、評価図、
  checksum、監査レポート

## 代表プロジェクト

| プロジェクト | 解決する問題と技術的な証拠 |
| --- | --- |
| [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground#quick-start) | **点群処理を既知の真値で評価。** NumPy・SciPyによる7種類の実験でoverlapとoutlierを制御し、変換誤差、対応点、幾何学的coverageをCSVと比較図へ出力します。 |
| [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit#quick-start) | **変更内容を追跡できるCSV cleaning。** Python標準ライブラリ、typed API、JSON schema、文書化したexit codeを備え、row単位の変更理由、checksum、決定論的なCSV・JSONを出力します。デモでは7行から3行を出力し、無効3行と重複1行を記録します。 |
| [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench#evaluation-methodology) | **モデル評価の根拠を保存。** 共通splitで3種類の分類器を比較し、6種類の実験と25件の代表比較からfold-level metrics、row-level predictions、誤分類、評価図、SHA-256 manifestを生成します。CLI、Python API、主要schemaはv1.0で固定しています。 |

| Point-cloud joint sensitivity | ML feature ablation |
| --- | --- |
| <a href="https://github.com/cab0a/pointcloud-playground/tree/main/results/joint_sensitivity/synthetic"><img src="https://raw.githubusercontent.com/cab0a/pointcloud-playground/main/results/joint_sensitivity/synthetic/comparison.png" width="400" alt="Overlapとoutlierのjoint sensitivity"></a> | <a href="https://github.com/cab0a/ml-evaluation-workbench/tree/main/results"><img src="https://raw.githubusercontent.com/cab0a/ml-evaluation-workbench/main/results/feature_ablation_scores.png" width="400" alt="Feature ablationのmacro F1"></a> |

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

## 非公開プロジェクト

機密性のある運用データや継続中の検証条件を含むため、
以下の個人開発は非公開にしています。

- **時系列データ評価・運用基盤:** raw・cleaned・featuresの分離、DuckDB、
  品質ゲート、nested walk-forward、確率校正、データリーク防止、
  CLI、定期実行、稼働監視を実装しています。
- **仮説検証・意思決定研究ラボ:** 仮説、データ、成功・停止条件、実験、
  採否判断を接続し、情報源、固定snapshot、schema、scenario、
  CSV・GeoJSON・レポート・runbookを管理しています。
- **業務台帳・ワークフロー自動化:** Excel VBAで外部データ取込、
  既存入力を保持する台帳更新、業務ルールに基づく一覧作成、帳票出力、
  状態管理、処理ログ、管理者・利用者向け文書を実装しています。

## 共通する設計

- **再現性:** commit済みの入力と設定から、CLIで数値成果物と図を再生成
- **定量評価:** 既知の真値、共通split、制御したfixtureを使って条件間を比較
- **監査可能性:** row・fold・条件単位の結果とprovenance・checksumを保存
- **制約の明示:** controlled experimentの結果と外部への一般化可能性を区別
- **継続的な検証:** pytestとGitHub Actionsで対応Pythonバージョンと主要interfaceを確認
