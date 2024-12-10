import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(
    prog="martin",
    description="batch convert mp4 to webp using ffmpeg"
)
parser.add_argument('--fps', default=25, required=False)
args = parser.parse_args()

def run():
    ffmpeg_path = Path(".", "ffmpeg-2024-12-09", "bin", "ffmpeg")
    ffprobe_path = Path(".", "ffmpeg-2024-12-09", "bin", "ffprobe")

    in_path = Path(".", "in")
    in_path.mkdir(parents=True, exist_ok=True)

    out_path = Path(".", "out")
    out_path.mkdir(parents=True, exist_ok=True)

    convered = 0

    videos = Path(".", "in").rglob('*.mp4')
    for video in videos:

        size = subprocess.run([
            ffprobe_path,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            video
        ], capture_output = True, text=True).stdout
        width, height = size.strip().split("x")

        webp_path = Path(out_path, f"{video.name.replace(".mp4", "")}.webp")
        return_code = subprocess.run([
            ffmpeg_path,
            "-i", video,
            "-vcodec", "libwebp",
            "-filter:v", f"fps=fps={args.fps}",
            "-lossless", "1",
            "-loop", "0",
            "-preset", "default",
            "-an",
            "-vsync", "0",
            "-s", f"{width}:{height}",
            "-y", # overwrite
            webp_path
        ])

        print(return_code)

        convered += 1

    print(f"\nconverted {convered} videos to webp!")

if __name__ == "__main__":
    run()