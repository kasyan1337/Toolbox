import os
import argparse
import subprocess


def burn_subtitles(video_path, subtitles_path, output_video_path, font=None, font_size=None):
    vf_option = f"subtitles='{subtitles_path}'"
    if font or font_size:
        style_args = []
        if font:
            style_args.append(f"FontName={font}")
        if font_size:
            style_args.append(f"FontSize={font_size}")
        style_string = ",".join(style_args)
        vf_option = f"subtitles='{subtitles_path}':force_style='{style_string}'"
    cmd = ["ffmpeg", "-i", video_path, "-vf", vf_option, "-c:a", "copy", output_video_path]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Burn subtitles from the output folder into videos from the input folder")
    parser.add_argument("--font", type=str, default=None, help="Optional font name for subtitles (e.g., Arial)")
    parser.add_argument("--font_size", type=str, default=None, help="Optional font size for subtitles (e.g., 24)")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    subtitles_dir = os.path.join(base_dir, "output")
    output_dir = os.path.join(base_dir, "output_burnt_subs")
    for folder in [input_dir, subtitles_dir, output_dir]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    video_extensions = (".mp4", ".mov", ".avi", ".mkv")
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(video_extensions)]

    if not video_files:
        print(f"No video files found in '{input_dir}'.")
        return

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        base_name = os.path.splitext(video_file)[0]
        subtitles_file = base_name + ".srt"
        subtitles_path = os.path.join(subtitles_dir, subtitles_file)
        if not os.path.exists(subtitles_path):
            print(f"Subtitles file '{subtitles_file}' not found in '{subtitles_dir}'. Skipping '{video_file}'.")
            continue
        output_video_path = os.path.join(output_dir, video_file)
        print(f"Burning subtitles for '{video_file}'...")
        burn_subtitles(video_path, subtitles_path, output_video_path, font=args.font, font_size=args.font_size)
        print(f"Output saved to '{output_video_path}'.")


if __name__ == "__main__":
    main()