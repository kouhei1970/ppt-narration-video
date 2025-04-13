# PowerPoint スライド解析・ナレーション動画作成ツール

このツールは、PowerPointスライドの画像をGPT-4oで解析し、自動的にナレーションスクリプトを生成、VOICEVOXで音声化して動画として保存するPythonプログラムです。

## 機能

- PowerPointスライド画像（PNG）をGPT-4oで解析
- スライド内容に基づいた講義用ナレーションスクリプトを自動生成
- VOICEVOXを使用して自然な日本語音声を生成
- スライドと音声を組み合わせて動画を作成
- 複数のスライド動画を結合して一つの講義動画を作成

## インストール方法

### 必要条件

- Python 3.7以上
- pip (Pythonパッケージマネージャー)
- FFmpeg（音声・動画処理に必要）
- VOICEVOX（音声合成エンジン）
- OpenAI API キー（GPT-4oを使用するため）

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

### VOICEVOXのインストール

1. [VOICEVOX公式サイト](https://voicevox.hiroshiba.jp/)からVOICEVOXをダウンロードしてインストール
2. VOICEVOXエンジンを起動し、ポート50021でサービスが実行されていることを確認

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

## 使い方

### 準備

1. OpenAI APIキーを取得し、`ppt_narration.py`の`OPENAI_API_KEY`変数に設定します
2. VOICEVOXエンジンを起動します（デフォルトでは`http://localhost:50021`で動作）
3. PowerPointスライドをPNG形式で保存し、`slides`フォルダに配置します
   - ファイル名は「スライド1.png」、「スライド2.png」などの形式にしてください

### 実行方法

```bash
python ppt_narration.py
```

### フォルダ構成

プログラムは以下のフォルダを自動的に作成・使用します：

- `slides`: PowerPointスライド画像（PNG）を配置するフォルダ
- `audios`: 生成された音声ファイル（WAV）が保存されるフォルダ
- `videos`: 各スライドの動画ファイル（MP4）が保存されるフォルダ
- `scripts`: 生成されたナレーションスクリプトが保存されるフォルダ

最終的な動画ファイルは、デフォルトでは`lecture_video.mp4`という名前で保存されます。

## カスタマイズ

### VOICEVOX話者の変更

`ppt_narration.py`の`VOICEVOX_SPEAKER_ID`変数を変更することで、異なる話者の音声を使用できます。デフォルトでは`3`（ずんだもん）に設定されています。

```python
VOICEVOX_SPEAKER_ID = 3  # ← 好みの話者IDに変更
```

VOICEVOXの話者IDは以下のように対応しています（一部）：
- 1: 四国めたん（ノーマル）
- 2: 四国めたん（あまあま）
- 3: ずんだもん（ノーマル）
- 4: ずんだもん（あまあま）
- 8: 春日部つむぎ
- 10: 雨晴はう
- 11: 波音リツ
- 47: もち子さん

### GPTプロンプトの調整

ナレーションスクリプト生成のプロンプトは`ppt_narration.py`内の`prompt`変数で定義されています。必要に応じて調整することができます。

### 音声速度の調整

音声の速度は`generate_voice`関数内の`speedScale`パラメータで調整できます。デフォルトでは`1.1`（標準より10%速い）に設定されています。

```python
query["speedScale"] = 1.1  # ← デフォルトは1.0、これで10%早くなります
```

## ファイル命名規則

### スライド画像

スライド画像は「スライド」という接頭辞と番号を含む必要があります：

- `スライド1.png`
- `スライド2.png`
- ...
- `スライド10.png`

ファイルは自然順（natural sort）で並べられます。

## 処理の流れ

1. スライド画像の読み込み
2. GPT-4oによるスライド内容の解析
3. 講義用ナレーションスクリプトの生成（漢字含む整形文と読み上げ用のひらがな文）
4. VOICEVOXによる音声合成
5. スライド画像と音声を組み合わせた動画の作成
6. すべてのスライド動画の結合

## PowerPointスライドの準備方法

1. PowerPointでプレゼンテーションを作成します
2. 「ファイル」→「エクスポート」→「画像としてエクスポート」を選択
3. 形式としてPNGを選択し、すべてのスライドを保存
4. 保存したスライド画像のファイル名を「スライド1.png」、「スライド2.png」などに変更
5. すべてのスライド画像を`slides`フォルダに配置

## 注意事項

- OpenAI APIキーが必要です（GPT-4oを使用するため）
- VOICEVOXエンジンが起動していない場合、音声生成ができません
- FFmpegがインストールされていない場合、動画処理ができません
- 出力動画のフォーマットはMP4（H.264）です
- 大量のスライドや長いナレーションを処理する場合は、十分なメモリが必要です
- GPT-4oの使用にはAPIの利用料金が発生します

## トラブルシューティング

### よくある問題

1. **「requests module is not installed」というエラーが表示される**
   - `pip install requests` を実行してください

2. **「openai module is not installed」というエラーが表示される**
   - `pip install openai` を実行してください

3. **「natsort module is not installed」というエラーが表示される**
   - `pip install natsort` を実行してください

4. **「Pillow library is not installed」というエラーが表示される**
   - `pip install Pillow` を実行してください

5. **VOICEVOXに接続できない**
   - VOICEVOXエンジンが起動していることを確認してください
   - デフォルトでは`http://localhost:50021`で接続を試みます
   - VOICEVOXのポート設定を確認してください

6. **OpenAI APIエラーが発生する**
   - APIキーが正しく設定されているか確認してください
   - APIの利用制限や課金状況を確認してください

7. **FFmpegエラーが発生する**
   - FFmpegがインストールされていることを確認してください
   - コマンドラインで`ffmpeg -version`を実行して、正しくインストールされているか確認してください

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
