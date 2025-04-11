import os
import sys
import argparse
import re
import whisper
import ffmpeg


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"


def create_srt(segments):
    srt_content = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_content


def extract_audio(video_path, audio_path):
    (ffmpeg.input(video_path)
     .output(audio_path, ac=1, ar='16000')
     .overwrite_output()
     .run(quiet=True))


def process_video(video_path, output_dir, model, language, timestamps, temp_dir):
    video_basename = os.path.splitext(os.path.basename(video_path))[0]
    temp_audio_path = os.path.join(temp_dir, video_basename + ".wav")
    print(f"Extracting audio from '{video_path}'...")
    extract_audio(video_path, temp_audio_path)
    print(f"Running Whisper transcription on '{video_basename}'...")
    result = model.transcribe(temp_audio_path, language=language)
    if timestamps:
        srt_content = create_srt(result['segments'])
        output_file = os.path.join(output_dir, video_basename + ".srt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)
        print(f"Subtitles with timestamps saved to '{output_file}'.")
    else:
        text = result["text"]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        formatted_text = "\n".join(sentence.strip() for sentence in sentences if sentence.strip())
        output_file = os.path.join(output_dir, video_basename + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        print(f"Subtitles saved to '{output_file}'.")
    os.remove(temp_audio_path)


def main():
    parser = argparse.ArgumentParser(description="Video Subtitle Generator using Whisper")
    parser.add_argument("--language", type=str, default="en", help="Language code for transcription (default: en)")
    parser.add_argument("--timestamps", type=int, choices=[0, 1], default=0,
                        help="Include timestamps: 1 for yes, 0 for no (default: 0)")
    parser.add_argument("--model", type=str, default="large", help="Model size: tiny, base, small, medium, large")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    temp_dir = os.path.join(base_dir, "temp")
    summaries_dir = os.path.join(base_dir, "summaries")

    # Create necessary directories if they do not exist.
    for folder in [input_dir, output_dir, temp_dir, summaries_dir]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    video_extensions = (".mp4", ".mov", ".avi", ".mkv")
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(video_extensions)]
    if not video_files:
        print(f"No video files found in '{input_dir}'.")
        sys.exit(0)

    print(f"Loading Whisper model: ({args.model}) ...")
    model = whisper.load_model(args.model)
    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        process_video(video_path, output_dir, model, args.language, bool(args.timestamps), temp_dir)

    # At the end, generate a summary file that combines all the output subtitle files.
    summary_ext = ".srt" if args.timestamps else ".txt"
    summary_filename = "summary" + summary_ext
    summary_filepath = os.path.join(summaries_dir, summary_filename)

    summary_contents = []
    # Iterate over all output files with the chosen extension.
    for filename in sorted(os.listdir(output_dir)):
        if filename.lower().endswith(summary_ext):
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            header = f"Filename: {filename}\n{'-' * 40}\n"
            summary_contents.append(header + content + "\n\n")

    if summary_contents:
        with open(summary_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(summary_contents))
        print(f"Summary file created at '{summary_filepath}'.")
    else:
        print("No output subtitle files found for summarization.")


if __name__ == "__main__":
    main()