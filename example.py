
"""
Example script demonstrating how to use the PPTNarrationVideo class.
"""

from ppt_narration import PPTNarrationVideo

def main():
    """Example usage of the PPTNarrationVideo class."""
    slides_dir = "./example/slides"
    narration_dir = "./example/narration"
    output_path = "./example/presentation.mp4"
    
    ppt_video = PPTNarrationVideo(
        slides_dir=slides_dir,
        narration_dir=narration_dir,
        output_path=output_path,
        slide_duration=5.0,
        fps=24,
        audio_format="mp3"
    )
    
    ppt_video.create_video()


if __name__ == "__main__":
    main()
