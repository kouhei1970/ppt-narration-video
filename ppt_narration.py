
"""
PowerPoint Narration Video Creator
This script adds narration to PowerPoint slide images and converts them to video.
"""

import os
import sys
import argparse
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import subprocess
import tempfile
import shutil

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is not installed. Please install it using 'pip install Pillow'")
    sys.exit(1)

try:
    import moviepy.editor as mpy
except ImportError:
    print("Error: MoviePy library is not installed. Please install it using 'pip install moviepy'")
    sys.exit(1)

try:
    import pydub
except ImportError:
    print("Error: Pydub library is not installed. Please install it using 'pip install pydub'")
    sys.exit(1)


class PPTNarrationVideo:
    """Class to handle the creation of narrated videos from PowerPoint slides."""
    
    def __init__(self, 
                 slides_dir: str, 
                 narration_dir: str, 
                 output_path: str,
                 slide_duration: float = 5.0,
                 fps: int = 24,
                 audio_format: str = "mp3",
                 config_file: Optional[str] = None):
        """
        Initialize the PPTNarrationVideo object.
        
        Args:
            slides_dir: Directory containing slide images
            narration_dir: Directory containing narration audio files
            output_path: Path where the output video will be saved
            slide_duration: Default duration for slides without narration (seconds)
            fps: Frames per second for the output video
            audio_format: Format of the audio files
            config_file: Optional path to a JSON configuration file
        """
        self.slides_dir = Path(slides_dir)
        self.narration_dir = Path(narration_dir)
        self.output_path = Path(output_path)
        self.slide_duration = slide_duration
        self.fps = fps
        self.audio_format = audio_format
        self.config = {}
        
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config_file:
            self._load_config(config_file)
    
    def _load_config(self, config_file: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to the JSON configuration file
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"Loaded configuration from {config_file}")
        except Exception as e:
            print(f"Error loading configuration file: {e}")
    
    def _get_sorted_files(self, directory: Path, extension: str) -> List[Path]:
        """
        Get a sorted list of files with the given extension from the directory.
        
        Args:
            directory: Directory to search for files
            extension: File extension to filter by
            
        Returns:
            Sorted list of file paths
        """
        files = list(directory.glob(f"*.{extension}"))
        return sorted(files, key=lambda x: int(''.join(filter(str.isdigit, x.stem))) if any(c.isdigit() for c in x.stem) else x.stem)
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """
        Get the duration of an audio file in seconds.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration of the audio in seconds
        """
        try:
            audio = pydub.AudioSegment.from_file(str(audio_path))
            return len(audio) / 1000.0  # Convert milliseconds to seconds
        except Exception as e:
            print(f"Error getting duration for {audio_path}: {e}")
            return self.slide_duration
    
    def create_video(self) -> None:
        """Create a video from slides with narration."""
        slide_files = self._get_sorted_files(self.slides_dir, "png") or self._get_sorted_files(self.slides_dir, "jpg")
        narration_files = self._get_sorted_files(self.narration_dir, self.audio_format)
        
        if not slide_files:
            print(f"Error: No slide images found in {self.slides_dir}")
            return
        
        print(f"Found {len(slide_files)} slides and {len(narration_files)} narration files")
        
        clips = []
        for i, slide_path in enumerate(slide_files):
            narration_path = None
            slide_name = slide_path.stem
            
            for narr_path in narration_files:
                if slide_name in narr_path.stem or str(i+1) in narr_path.stem:
                    narration_path = narr_path
                    break
            
            duration = self.slide_duration
            if narration_path:
                duration = max(self._get_audio_duration(narration_path), self.slide_duration)
                print(f"Slide {i+1}: Using narration {narration_path.name} with duration {duration:.2f}s")
            else:
                print(f"Slide {i+1}: No narration found, using default duration {duration:.2f}s")
            
            img_clip = mpy.ImageClip(str(slide_path), duration=duration)
            
            if narration_path:
                audio_clip = mpy.AudioFileClip(str(narration_path))
                img_clip = img_clip.set_audio(audio_clip)
            
            clips.append(img_clip)
        
        final_clip = mpy.concatenate_videoclips(clips, method="compose")
        
        print(f"Creating video at {self.output_path}...")
        final_clip.write_videofile(
            str(self.output_path),
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=tempfile.NamedTemporaryFile(suffix='.m4a').name,
            remove_temp=True
        )
        print(f"Video created successfully: {self.output_path}")


def main():
    """Main function to parse arguments and create the video."""
    parser = argparse.ArgumentParser(description='Create a video from PowerPoint slides with narration.')
    parser.add_argument('--slides', '-s', required=True, help='Directory containing slide images (PNG or JPG)')
    parser.add_argument('--narration', '-n', required=True, help='Directory containing narration audio files')
    parser.add_argument('--output', '-o', required=True, help='Output video file path')
    parser.add_argument('--duration', '-d', type=float, default=5.0, help='Default duration for slides without narration (seconds)')
    parser.add_argument('--fps', type=int, default=24, help='Frames per second for the output video')
    parser.add_argument('--audio-format', default='mp3', help='Format of the audio files')
    parser.add_argument('--config', '-c', help='Path to a JSON configuration file')
    
    args = parser.parse_args()
    
    ppt_video = PPTNarrationVideo(
        slides_dir=args.slides,
        narration_dir=args.narration,
        output_path=args.output,
        slide_duration=args.duration,
        fps=args.fps,
        audio_format=args.audio_format,
        config_file=args.config
    )
    
    ppt_video.create_video()


if __name__ == "__main__":
    main()
