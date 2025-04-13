# PowerPoint ナレーション動画作成ツール

このツールは、PowerPointスライドの画像にナレーションを追加して動画として保存するためのPythonプログラムです。

## 機能

- PowerPointスライド画像（PNG/JPG）にナレーション音声を追加
- スライドとナレーションを組み合わせて動画を作成
- スライドごとに異なるナレーションを設定可能
- ナレーションがないスライドには設定した表示時間を適用

## インストール方法

### 必要条件

- Python 3.7以上
- pip (Pythonパッケージマネージャー)

### インストール手順

1. このリポジトリをクローンまたはダウンロードします：

```bash
git clone https://github.com/yourusername/ppt-narration-video.git
cd ppt-narration-video
```

2. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
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
  }
}
```

設定ファイルを使用するには：

```bash
python ppt_narration.py --slides ./slides --narration ./narration --output presentation.mp4 --config config.json
```

## 注意事項

- ナレーション音声ファイルが見つからないスライドには、デフォルトの表示時間が適用されます
- 出力動画のフォーマットはMP4（H.264）です
- 大量のスライドや長いナレーションを処理する場合は、十分なメモリが必要です

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
