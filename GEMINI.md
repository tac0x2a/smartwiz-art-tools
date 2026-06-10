# SMARTWIZ+ art: Local Developer API Tools - Project Instructions

このファイルには、本リポジトリを利用した開発における重要なガイドラインと技術的要約が記載されています。

## プロジェクト概要
SMARTWIZ+ art（6色E-Inkディスプレイ）を、クラウドを介さずローカルネットワーク（BLEおよびHTTP）から直接制御するための開発者向けツールキットです。

## 開発環境のセットアップ (uv & mise)
本プロジェクトでは、Pythonのバージョン管理に **mise**、パッケージ管理に **uv** を使用しています。

### クイックスタート
1. **mise のインストール**: [mise documentation](https://mise.jdx.dev/) を参照してください。
2. **依存関係のセットアップ**:
   ```bash
   mise install
   uv sync
   ```
3. **スクリプトの実行**:
   ```bash
   uv run examples/scan_art_device.py
   ```

### 技術スタックと依存関係
- **Language**: Python 3.12+ (managed by `mise`)
- **Package Manager**: `uv`
- **Dependencies** (managed via `pyproject.toml`):
  - `bleak`, `requests`, `cryptography`, `Pillow`
  - `pyBlufi` (Git dependency)
- **External Tools**:
  - `ImageMagick`: Spectra 6形式（.s6）へのディザリング変換に必須
  - `OpenSSL`: RSA鍵生成用

## 主要なワークフロー
1. **初期セットアップ (BLE)**:
   - `scan_art_device.py` でデバイスを検出。
   - `connect_wifi.py` でWi-Fi情報を送信。
2. **ローカル登録 (HTTP)**:
   - `device_register.py` でRSA公開鍵を交換。
   - **注意**: この操作により公式アプリ/クラウドとの連携が解除されます。
3. **画像表示**:
   - `convert_image.py` で一般画像を `.s6` 形式に変換。
   - `display_local_image.py` でデバイスに送信。

## ハードウェアと運用の制約
- **ディスプレイ特性**: 6色E-Ink。更新には約30秒かかり、画面が点滅（フラッシング）します。
- **電力管理**: 
  - 常時給電（USB-C）が推奨。
  - バッテリー駆動時は1時間ごとに1回（約1分40秒間）しかWi-Fiが有効になりません。物理ボタンの短押しで強制的に起動可能です。
- **書き換え頻度**: パネルの寿命保護のため、更新間隔は15分〜30分以上を推奨します。

## 開発ガイドライン
- 新しい自動化スクリプトを作成する際は、`examples/epd_util.py` の共通ユーティリティを活用してください。
- 詳細なAPI仕様は `doc/SMARTWIZ+art_APIDeveloperGuide.pdf` を参照してください。
