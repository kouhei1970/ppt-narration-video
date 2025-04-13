import os
import requests
import json
import wave
import base64
from glob import glob
import subprocess
from openai import OpenAI
from PIL import Image
from natsort import natsorted

# === 設定 ===
SLIDE_IMG_DIR = "slides"
AUDIO_DIR = "audios"
VIDEO_DIR = "videos"
SCRIPT_DIR = "scripts"
FINAL_VIDEO = "lecture_video.mp4"
VOICEVOX_SPEAKER_ID = 3
OPENAI_API_KEY = "sk-**************"

client = OpenAI(api_key=OPENAI_API_KEY)

# === フォルダ作成 ===
for folder in [SLIDE_IMG_DIR, AUDIO_DIR, VIDEO_DIR, SCRIPT_DIR]:
    os.makedirs(folder, exist_ok=True)

# === VOICEVOX音声生成 ===
def generate_voice(text, filename, speaker_id=VOICEVOX_SPEAKER_ID):
    base_url = "http://localhost:50021"
    query = requests.post(f"{base_url}/audio_query", params={"text": text, "speaker": speaker_id}).json()
    query["speedScale"] = 1.1  # ← デフォルトは1.0、これで30%早くなります
    synthesis = requests.post(
        f"{base_url}/synthesis",
        params={"speaker": speaker_id},
        data=json.dumps(query),
        headers={"Content-Type": "application/json"}
    )
    with open(filename, "wb") as f:
        f.write(synthesis.content)

# === .wavの長さ取得 ===
def get_wav_duration(wav_path):
    with wave.open(wav_path, 'rb') as wf:
        return wf.getnframes() / float(wf.getframerate())

def append_silence_to_audio(input_wav, output_wav, silence_duration=1.0):
    temp_output = output_wav + ".temp.wav"
    silence = "anullsrc=r=44100:cl=stereo"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_wav,
        "-f", "lavfi", "-t", str(silence_duration), "-i", silence,
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
        "-map", "[out]",
        temp_output
    ], check=True)
    os.replace(temp_output, output_wav)  # ← 上書き

# === スライド画像 + 音声 → 動画 ===
def create_slide_video(image_file, audio_file, output_file):
    duration = get_wav_duration(audio_file)
    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1",
        "-t", f"{duration:.2f}",
        "-i", image_file,
        "-i", audio_file,
        "-c:v", "libx264",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_file
    ], check=True)

# === メイン処理 ===
slide_images = natsorted(glob(f"{SLIDE_IMG_DIR}/スライド*.png"))
for i, img_path in enumerate(slide_images, 1):
    print(f"▶ Slide {i} - GPT画像解析＆スクリプト生成中...")

    with open(img_path, "rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    instruction = "Slide1に該当するため、挨拶と導入を含めてください。" if i == 1 else "すでに講義が始まっている前提で、挨拶や導入は不要です。"

    prompt = (
        "この画像は大学講義のスライドです。以下の要件で講義用ナレーションスクリプトを作成してください：\n"
        f"・{instruction}\n"
        "・あいさつは視聴者がいつの時間視聴するかわからないので、あいさつは不要です。\n"
        "・まず整形文（漢字含む自然な講義文）を生成し、その後にVOICEVOXで正しく読み上げられるように平仮名の『読み用』文も出力してください。\n"
        "・読み用には句読点や自然な区切りを含め、熟語の誤読を避けてください（例：「解析手法」は『かいせきしゅほう』）。\n"
        "・スライド内に含まれるメールアドレスや内線番号などの個人連絡情報は読み上げないでください。\n"
        "・人の名前に敬称は不要です。\n"
        "・長い数式の読み上げはせず、このようになりますと説明すれば良いです。\n"
        "・TeX形式の数式が含まれる場合は、それを日本語の自然な読み方に直してください。例えば、\frac{1}{2}mv^2 は『2分の1、エム、ブイの2乗』といった形にしてください。\n"
        "・TeX形式において分数と微分は区別して読み上げてください。\n"
        "出力形式：\n整形文:\n[漢字含む文]\n\n読み用:\n[すべてひらがな]\n"
    )

    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.4
    )
    content = response.choices[0].message.content.strip()

    lines = content.splitlines()
    kanji_lines = []
    yomi_lines = []
    mode = None
    for line in lines:
        if line.strip().startswith("整形文"):
            mode = "kanji"
        elif line.strip().startswith("読み用"):
            mode = "yomi"
        elif mode == "kanji":
            kanji_lines.append(line)
        elif mode == "yomi":
            yomi_lines.append(line)

    kanji_script = "\n".join(kanji_lines).strip()
    yomi_script = "\n".join(yomi_lines).strip()

    # スクリプト保存
    with open(f"{SCRIPT_DIR}/slide{i:03}_kanji.txt", "w", encoding="utf-8") as f:
        f.write(kanji_script)
    with open(f"{SCRIPT_DIR}/slide{i:03}_yomi.txt", "w", encoding="utf-8") as f:
        f.write(yomi_script)

    # 音声生成
    audio_path = f"{AUDIO_DIR}/slide{i:03}.wav"
    print(f"🔊 VOICEVOX 音声生成中（slide{i:03}.wav）")
    generate_voice(yomi_script, audio_path)
    append_silence_to_audio(audio_path, audio_path, silence_duration=1.0)

    # 動画生成
    video_path = f"{VIDEO_DIR}/slide{i:03}.mp4"
    print(f"🎬 スライド動画生成中（slide{i:03}.mp4）")
    create_slide_video(img_path, audio_path, video_path)

# === 全スライド動画の結合 ===
print("📦 lecture_video.mp4 に結合中...")
with open("video_list.txt", "w") as f:
    for file in sorted(glob(f"{VIDEO_DIR}/slide*.mp4")):
        f.write(f"file '{file}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "video_list.txt",
    "-c", "copy", FINAL_VIDEO
], check=True)

print(f"✅ 講義動画の完成！ファイル名: {FINAL_VIDEO}")
