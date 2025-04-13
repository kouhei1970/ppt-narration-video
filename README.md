# PowerPoint ナレーション動画作成ツール

このツールは、PowerPointスライドの画像にナレーションを追加して動画として保存するためのPythonプログラムです。

## 機能

- PowerPointスライド画像（PNG/JPG）にナレーション音声を追加
- スライドとナレーションを組み合わせて動画を作成
- スライドごとに異なるナレーションを設定可能
- ナレーションがないスライドには設定した表示時間を適用
- 設定ファイルによる詳細なカスタマイズが可能

## インストール方法

### 必要条件

- Python 3.7以上
- pip (Pythonパッケージマネージャー)
- FFmpeg（音声・動画処理に必要）

### FFmpegのインストール

#### Windows
1. [FFmpeg公式サイト](https://ffmpeg.org/download.html)からWindows用のビルドをダウンロード
2. ダウンロードしたファイルを解凍し、任意のフォルダに配置
3. 環境変数のPATHにFFmpegの`bin`フォルダのパスを追加

#### macOS
Homebrewを使用してインストール:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Pythonパッケージのインストール

1. このリポジトリをクローンまたはダウンロードします：

```bash
git clone https://github.com/yourusername/ppt-narration-video.git
cd ppt-narration-video
```

2. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

3. または、パッケージとしてインストールすることもできます：

```bash
pip install .
```

## 使い方

### 基本的な使い方

```bash
python ppt_narration.py --slides スライド画像のディレクトリ --narration ナレーション音声のディレクトリ --output 出力動画ファイル
```

### 例

```bash
python ppt_narration.py --slides ./slides --narration ./narration --output presentation.mp4
```

### 詳細なオプション

```
usage: ppt_narration.py [-h] --slides SLIDES --narration NARRATION --output OUTPUT [--duration DURATION] [--fps FPS] [--audio-format AUDIO_FORMAT] [--config CONFIG]

Create a video from PowerPoint slides with narration.

options:
  -h, --help            ヘルプメッセージを表示して終了
  --slides SLIDES, -s SLIDES
                        スライド画像（PNGまたはJPG）が含まれるディレクトリ
  --narration NARRATION, -n NARRATION
                        ナレーション音声ファイルが含まれるディレクトリ
  --output OUTPUT, -o OUTPUT
                        出力動画ファイルのパス
  --duration DURATION, -d DURATION
                        ナレーションがないスライドのデフォルト表示時間（秒）
  --fps FPS             出力動画のフレームレート（FPS）
  --audio-format AUDIO_FORMAT
                        音声ファイルのフォーマット（デフォルト: mp3）
  --config CONFIG, -c CONFIG
                        JSON設定ファイルへのパス
```

## ファイル命名規則

### スライド画像

スライド画像は数字順に並べられます。例：

- `slide1.png`
- `slide2.png`
- ...
- `slide10.png`

### ナレーション音声

ナレーション音声ファイルは、対応するスライドの名前または番号を含む必要があります。例：

- `narration_slide1.mp3` または `narration_1.mp3`
- `narration_slide2.mp3` または `narration_2.mp3`
- ...

## 設定ファイル（オプション）

JSON形式の設定ファイルを使用して、詳細な設定を行うことができます。例：

```json
{
  "slide_settings": {
    "slide1": {
      "duration": 10.0
    },
    "slide3": {
      "duration": 8.0
    }
  },
  "output_settings": {
    "fps": 30,
    "resolution": [1920, 1080]
  }
}
```

設定ファイルを使用するには：

```bash
python ppt_narration.py --slides ./slides --narration ./narration --output presentation.mp4 --config config.json
```

サンプル設定ファイル`example_config.json`がリポジトリに含まれています。

## 使用例

リポジトリには`example.py`というサンプルスクリプトが含まれています。このスクリプトは`PPTNarrationVideo`クラスの使い方を示しています：

```python
from ppt_narration import PPTNarrationVideo

# 例としてのパラメータ
slides_dir = "./example/slides"
narration_dir = "./example/narration"
output_path = "./example/presentation.mp4"

# PPTNarrationVideoオブジェクトを作成して実行
ppt_video = PPTNarrationVideo(
    slides_dir=slides_dir,
    narration_dir=narration_dir,
    output_path=output_path,
    slide_duration=5.0,
    fps=24,
    audio_format="mp3"
)

# 動画を作成
ppt_video.create_video()
```

## 準備手順

### PowerPointスライドの準備

1. PowerPointでプレゼンテーションを作成します
2. 「ファイル」→「エクスポート」→「画像としてエクスポート」を選択
3. 形式としてPNGまたはJPGを選択し、すべてのスライドを保存
4. 保存したスライド画像を`slides`フォルダに配置

### ナレーションの準備

1. 各スライドに対応するナレーションを録音します
   - Windowsの「ボイスレコーダー」
   - macOSの「QuickTime Player」
   - スマートフォンの録音アプリなど
2. 録音したファイルをMP3形式に変換（必要な場合）
3. ファイル名をスライドと対応するように命名（例：`narration_slide1.mp3`）
4. すべてのナレーションファイルを`narration`フォルダに配置

## 注意事項

- ナレーション音声ファイルが見つからないスライドには、デフォルトの表示時間が適用されます
- 出力動画のフォーマットはMP4（H.264）です
- 大量のスライドや長いナレーションを処理する場合は、十分なメモリが必要です
- FFmpegがインストールされていない場合、音声処理ができません

## トラブルシューティング

### よくある問題

1. **「Pillow library is not installed」というエラーが表示される**
   - `pip install Pillow` を実行してください

2. **「MoviePy library is not installed」というエラーが表示される**
   - `pip install moviepy` を実行してください

3. **「Pydub library is not installed」というエラーが表示される**
   - `pip install pydub` を実行してください

4. **音声が再生されない**
   - FFmpegがインストールされていることを確認してください。インストールされていない場合は、[FFmpegの公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストールしてください。

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
