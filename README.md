# Python R&Dエンジニア

機械学習評価、コンピュータビジョン、点群・3Dデータ処理を中心に、再現可能な実験基盤と監査可能なPythonツールを実装しています。

- **主な領域:** 機械学習評価、画像処理、点群・3Dデータ処理、データ品質確認
- **開発経験:** 技術調査、要件定義、設計、実装、レビュー、テスト、評価、導入、保守
- **公開成果物:** CLI、公開API、pytest、GitHub Actions、CSV・JSON、評価図、監査レポート

## 代表プロジェクト

| プロジェクト | 解決する問題と技術的な証拠 |
| --- | --- |
| [Few-Shot Anomaly PoC](https://github.com/cab0a/few-shot-anomaly-poc) | <strong>少数例の異常検知を採否判定まで検証。</strong>正常画像20枚以内・CPU実行・異常ラベルを学習に使わない条件で2手法を比較し、事前固定した誤検知率・再現率・処理時間の基準により両手法を却下しました。ラベル開示前のスコア、誤検知・見逃し、処理時間、判定根拠をCSV・JSONで保存しています。 |
| [Point Cloud Playground](https://github.com/cab0a/pointcloud-playground) | <strong>点群処理を既知の真値で評価。</strong>NumPy・SciPyによる7種類の実験で重なり率と外れ値率を制御し、変換誤差、対応点精度、幾何学的被覆をCSVと比較図へ出力します。 |
| [Research Notes](https://github.com/cab0a/research-notes) | <strong>研究課題を再現可能な証拠へ接続。</strong>17件の研究で文献調査、統制実験、結果、考察、制約を記録しています。最新のv0.17.0では、JPEG metadata admissionの10種類のresource上限を24個の合成fixtureで評価し、5環境の120観測からdecision、reason code、work counter、fixture hashの安定性を確認しています。 |

| 異常検知の固定基準評価 | 点群の同時感度分析 |
| --- | --- |
| <a href="https://github.com/cab0a/few-shot-anomaly-poc/tree/main/docs/assets"><img src="https://raw.githubusercontent.com/cab0a/few-shot-anomaly-poc/main/docs/assets/v0.1-gate-summary.svg" width="400" alt="異常検知二手法の固定基準に対する評価結果"></a> | <a href="https://github.com/cab0a/pointcloud-playground/tree/main/results/joint_sensitivity/synthetic"><img src="https://raw.githubusercontent.com/cab0a/pointcloud-playground/main/results/joint_sensitivity/synthetic/comparison.png" width="400" alt="重なり率と外れ値率の同時感度"></a> |

## その他の公開プロジェクト

- **データ整形 — [Data Cleaning Toolkit](https://github.com/cab0a/data-cleaning-toolkit):** Python標準ライブラリ、型付きPython API、JSONスキーマ、文書化した終了コードを備え、行単位の変更理由を監査JSONへ記録し、同じ入力から同じ内容のCSV・JSONを生成します。
- **モデル評価 — [ML Evaluation Workbench](https://github.com/cab0a/ml-evaluation-workbench):** 共通のデータ分割で3種類の分類器を比較し、6種類の実験と25件の代表比較から分割ごとの評価指標、行単位の予測、誤分類、評価図を生成します。
- **入力監査 — [Image Dataset Inspector](https://github.com/cab0a/image-dataset-inspector):** JPEG・PNGを再帰的に検査し、読み込みエラー、画像サイズ、明るさ、コントラスト、ラプラシアン分散をCSVへ記録します。
- **手法比較 — [Vision Playground](https://github.com/cab0a/vision-playground):** 二値化、ノイズ除去、輪郭検出、古典的な画像分割を、正解データ付きの合成画像と公開画像で165件の手法・条件評価にかけます。

## 非公開プロジェクト

機密性のある運用データや継続中の検証条件を含むため、以下の個人開発は非公開にしています。

- **時系列データ評価・運用基盤:** 原データ・整形済みデータ・特徴量の分離、DuckDB、品質ゲート、入れ子型の時系列交差検証、確率校正、データリーク防止、CLI、定期実行、稼働監視を実装しています。
- **仮説検証・意思決定研究ラボ:** 仮説、データ、成功・停止条件、実験、採否判断を接続し、情報源、固定スナップショット、データ仕様、検証条件、CSV・GeoJSON・レポート・運用手順書を管理しています。
- **業務台帳・ワークフロー自動化:** Excel VBAで外部データ取込、既存入力を保持する台帳更新、業務ルールに基づく一覧作成、帳票出力、状態管理、処理ログ、管理者・利用者向け文書を実装しています。

## 共通する設計

- **再現性:** コミット済みの入力と設定から、CLIで数値成果物と図を再生成
- **定量評価:** 既知の真値、共通のデータ分割、制御したテストデータを使って条件間を比較
- **監査可能性:** 行・分割・条件単位の結果と、入力・設定・判断根拠を保存
- **制約の明示:** 統制実験の結果と外部への一般化可能性を区別
- **継続的な検証:** pytestとGitHub Actionsで対応Pythonバージョンと主要インターフェースを確認
