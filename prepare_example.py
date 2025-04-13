
"""
Example script to prepare sample slides and narration for demonstration.
This is for demonstration purposes only and not required for the main functionality.
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_sample_slide(output_path, slide_number, width=1280, height=720, bg_color=(255, 255, 255)):
    """Create a sample slide with a number and text."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font_path = None
        system_fonts = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
            '/System/Library/Fonts/Helvetica.ttc',  # macOS
            'C:\\Windows\\Fonts\\Arial.ttf'  # Windows
        ]
        for path in system_fonts:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            title_font = ImageFont.truetype(font_path, 60)
            content_font = ImageFont.truetype(font_path, 40)
        else:
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
    except Exception as e:
        print(f"Error loading font: {e}")
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
    
    title = f"サンプルスライド {slide_number}"
    draw.text((width//2, height//4), title, fill=(0, 0, 0), font=title_font, anchor="mm")
    
    content = f"このスライドはサンプルです。\nナレーション付き動画のデモンストレーション用です。"
    draw.text((width//2, height//2), content, fill=(0, 0, 128), font=content_font, anchor="mm", align="center")
    
    img.save(output_path)
    print(f"Created sample slide: {output_path}")

def create_sample_audio(output_path, duration=5, sample_rate=44100):
    """
    Create a sample audio file with a beep sound.
    This is just a placeholder - in a real scenario, you would use actual narration recordings.
    """
    try:
        import scipy.io.wavfile as wavfile
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        note = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        
        fade_duration = 0.1  # seconds
        fade_samples = int(fade_duration * sample_rate)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        note[:fade_samples] *= fade_in
        note[-fade_samples:] *= fade_out
        
        audio = (note * 32767).astype(np.int16)
        
        wavfile.write(output_path, sample_rate, audio)
        print(f"Created sample audio: {output_path}")
        
        try:
            from pydub import AudioSegment
            wav_audio = AudioSegment.from_wav(output_path)
            mp3_path = output_path.replace('.wav', '.mp3')
            wav_audio.export(mp3_path, format="mp3")
            print(f"Converted to MP3: {mp3_path}")
            
            os.remove(output_path)
            return mp3_path
        except Exception as e:
            print(f"Could not convert to MP3: {e}")
            return output_path
            
    except ImportError:
        print("Error: scipy is not installed. Cannot create sample audio.")
        print("Please install it using 'pip install scipy'")
        return None

def main():
    """Create sample slides and narration files for demonstration."""
    example_dir = Path("./example")
    slides_dir = example_dir / "slides"
    narration_dir = example_dir / "narration"
    
    slides_dir.mkdir(parents=True, exist_ok=True)
    narration_dir.mkdir(parents=True, exist_ok=True)
    
    num_slides = 3
    for i in range(1, num_slides + 1):
        slide_path = slides_dir / f"slide{i}.png"
        create_sample_slide(slide_path, i)
        
        narration_path = narration_dir / f"narration_slide{i}.wav"
        create_sample_audio(narration_path, duration=3 + i)  # Varying durations
    
    print("\nSample files created successfully!")
    print(f"Slides directory: {slides_dir.absolute()}")
    print(f"Narration directory: {narration_dir.absolute()}")
    print("\nYou can now run the example script:")
    print("python example.py")

if __name__ == "__main__":
    main()
