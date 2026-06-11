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
    - macOS: `brew install imagemagick` 推奨
    - Linux: `sudo apt install imagemagick`
  - `OpenSSL`: RSA鍵生成用

## 主要なワークフロー

### 1. 初期セットアップ (Wi-Fi 接続)
macOS環境ではBluetooth（BLE）のセキュリティ制限により、PythonスクリプトからのWi-Fiプロビジョニングが失敗する場合があります。その場合、以下の回避策を推奨します。

- **Matter経由でのセットアップ**: 
  - 本デバイスはMatterに対応しているため、公式アプリやスクリプトが失敗する場合でも、スマートホーム（iOSの「ホーム」アプリ等）からMatterデバイスとして追加することで、Wi-Fiネットワークへの接続が可能です。
- **モバイルアプリでのセットアップ**:
  - 公式の「SMARTWIZ+ art」アプリや「EspBlufi」アプリを使用してWi-Fi設定のみ完了させます。

### 2. ローカル登録 (HTTP)
Wi-Fi接続後、デバイスのIPアドレスを特定し、以下のコマンドで登録を行います。
```bash
# IPアドレスを直接指定して登録
uv run examples/device_register.py <デバイスのIPアドレス>
```
**注意**: この操作により、独自のRSA公開鍵が登録され、公式アプリ/クラウドとの連携が解除されます。

### 3. 画像表示
- **自動変換とアップロード (推奨)**:
  ```bash
  # 画像ファイルを指定して自動転送（JPG/PNG/GIF対応）
  # 内部でSpectra 6形式への変換、自動回転（縦長画像の場合）、device_idの解決、アップロード、表示更新を一括で行います
  mise run upload <画像ファイルのパス>
  ```
- **手動操作**:
  - `convert_image.py` で一般画像を `.s6` 形式に変換。
  - `display_local_image.py` でデバイスに送信。

### 技術的な詳細
- **暗号化 (AES-CBC)**: 
  - 画像転送時の暗号化には、デバイス固有の `device_id`（32文字の16進数）が必要です。
  - 本プロジェクトのスクリプトは、IPアドレス指定時でも自動的にデバイスから `device_id` を取得し、適切なIV（初期化ベクトル）を生成するように改善されています。
- **ImageMagick**:
  - ImageMagick v7 (`magick` コマンド) を優先的に使用します。

## ハードウェアと運用の制約
- **ディスプレイ特性**: 6色E-Ink。更新には約30秒かかり、画面が点滅（フラッシング）します。
- **電力管理**: 
  - 常時給電（USB-C）が推奨。
  - バッテリー駆動時は1時間ごとに1回（約1分40秒間）しかWi-Fiが有効になりません。物理ボタンの短押しで強制的に起動可能です。
- **書き換え頻度**: パネルの寿命保護のため、更新間隔は15分〜30分以上を推奨します。

## 開発ガイドライン
- 新しい自動化スクリプトを作成する際は、`examples/epd_util.py` の共通ユーティリティを活用してください。
- 詳細なAPI仕様は `doc/SMARTWIZ+art_APIDeveloperGuide.pdf` を参照してください。
