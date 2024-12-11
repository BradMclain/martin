import argparse
from pathlib import Path
import subprocess
from glob import glob

parser = argparse.ArgumentParser(
    prog="martin",
    description="batch convert mp4 to webp using ffmpeg"
)
parser.add_argument('--fps', default=25, required=False)
parser.add_argument('--width', default=None, required=False)
args = parser.parse_args()

def run():
    ffmpeg_path = Path(".", "ffmpeg-2024-12-09", "bin", "ffmpeg")
    ffprobe_path = Path(".", "ffmpeg-2024-12-09", "bin", "ffprobe")

    in_path = Path(".", "in")
    in_path.mkdir(parents=True, exist_ok=True)

    out_path = Path(".", "out")
    out_path.mkdir(parents=True, exist_ok=True)

    convered = 0

    videos = [p for p in in_path.rglob('*') if p.suffix in [".mp4", ".gif", ".mov"]]
    for video in videos:

        name, _ = video.name.split(".")

        size = subprocess.run([
            ffprobe_path,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            video
        ], capture_output = True, text=True).stdout
        i_width, i_height = size.strip().split("x")

        o_width = i_width
        o_height = i_height
        if args.width is not None:
            width = int(args.width)
            i_width = float(i_width)
            i_height = float(i_height)
            
            aspect = float(i_width) / float(i_height)
            
            o_width = width
            o_height = int(o_width / aspect)

        webp_path = Path(out_path, f"{name}.webp")
        subprocess.run([
            ffmpeg_path,
            "-i", video,
            "-vcodec", "libwebp",
            "-filter:v", f"fps=fps={args.fps}",
            "-lossless", "1",
            "-loop", "0",
            "-preset", "default",
            "-an",
            "-fps_mode", "passthrough",
            "-s", f"{o_width}:{o_height}",
            "-y", # overwrite
            webp_path
        ])

        convered += 1

    print(f"\nconverted {convered} videos to webp!")

if __name__ == "__main__":
    run()