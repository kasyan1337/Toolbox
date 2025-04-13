import argparse
import os
import re
import sys

import ffmpeg
import whisper


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"


def create_srt(segments):
    srt_content = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_content


def extract_audio(video_path, audio_path):
    (
        ffmpeg.input(video_path)
        .output(audio_path, ac=1, ar="16000")
        .overwrite_output()
        .run(quiet=True)
    )


def process_video_translate(
    video_path, output_dir, model, target_language, timestamps, temp_dir
):
    video_basename = os.path.splitext(os.path.basename(video_path))[0]
    temp_audio_path = os.path.join(temp_dir, video_basename + ".wav")
    print(f"Extracting audio from '{video_path}'...")
    extract_audio(video_path, temp_audio_path)
    if target_language.lower() == "en":
        print(f"Translating (to English) via Whisper for '{video_basename}'...")
        result = model.transcribe(temp_audio_path, task="translate")
        translated_text = result["text"]
        segments = result.get("segments")
    else:
        print(f"Transcribing original audio for '{video_basename}'...")
        result = model.transcribe(temp_audio_path)
        original_text = result["text"]
        segments = result.get("segments")
        print(f"Translating transcription to '{target_language}'...")
        try:
            from transformers import MarianMTModel, MarianTokenizer
        except ImportError:
            print(
                "Transformers package not found. Install it via 'pip install transformers'."
            )
            sys.exit(1)
        source_lang = result.get("language", "en").lower()
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_language}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        translation_model = MarianMTModel.from_pretrained(model_name)
        translated = translation_model.generate(
            **tokenizer(original_text, return_tensors="pt", padding=True)
        )
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    if timestamps and segments:
        if target_language.lower() == "en":
            srt_content = create_srt(result["segments"])
        else:
            srt_content = (
                "Timestamps not available for externally translated subtitles."
            )
        output_file = os.path.join(output_dir, video_basename + ".srt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)
        print(f"Translated subtitles with timestamps saved to '{output_file}'.")
    else:
        sentences = re.split(r"(?<=[.!?])\s+", translated_text)
        formatted_text = "\n".join(
            sentence.strip() for sentence in sentences if sentence.strip()
        )
        output_file = os.path.join(output_dir, video_basename + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        print(f"Translated subtitles saved to '{output_file}'.")
    os.remove(temp_audio_path)


def main():
    parser = argparse.ArgumentParser(
        description="Translate video subtitles using Whisper (and MarianMT for non-English)"
    )
    parser.add_argument(
        "--target_language",
        type=str,
        default="en",
        help="Target language code for translation (default: en). Note: Whisper's built-in translation supports only English. For other languages, MarianMT is used.",
    )
    parser.add_argument(
        "--timestamps",
        type=int,
        choices=[0, 1],
        default=0,
        help="Include timestamps if available; 1 for yes, 0 for no (default: 0)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="large",
        help="Whisper model size: tiny, base, small, medium, large",
    )
    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output_translated_whisper")
    temp_dir = os.path.join(base_dir, "temp")
    for folder in [input_dir, output_dir, temp_dir]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    video_extensions = (".mp4", ".mov", ".avi", ".mkv")
    video_files = [
        f for f in os.listdir(input_dir) if f.lower().endswith(video_extensions)
    ]
    if not video_files:
        print(f"No video files found in '{input_dir}'.")
        return
    print(f"Loading Whisper model ({args.model} model) ...")
    model = whisper.load_model(args.model)
    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        process_video_translate(
            video_path,
            output_dir,
            model,
            args.target_language,
            bool(args.timestamps),
            temp_dir,
        )


if __name__ == "__main__":
    main()
