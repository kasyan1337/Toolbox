import glob
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.audio_converter import wav_to_mp3, mp3_to_wav, m4a_to_mp3, m4a_to_wav
from src.image_converter import heic_to_jpg, jpg_to_png, png_to_jpg
from src.pdf_converter import pdf_to_docx, docx_to_pdf
from src.video_converter import (
    mov_to_mp4,
    mp4_to_mov,
    video_to_gif,
    gif_to_video,
    live_photo_to_gif,
    live_photo_to_video,
)


def get_file_stats(file_path):
    file_stats = os.stat(file_path)
    file_size = file_stats.st_size / 1024  # Size in KB
    return file_size


def batch_convert_files(
    input_folder: str,
    output_folder: str,
    conversion_type: str,
    file_extension: str,
    **kwargs,
):
    files = glob.glob(os.path.join(input_folder, f"*.{file_extension}"))
    for input_file in files:
        input_filename = os.path.basename(input_file)
        convert_file(input_filename, output_folder, conversion_type, **kwargs)


def convert_file(input_file: str, output_folder: str, conversion_type: str, **kwargs):
    input_path = os.path.join("input", input_file)
    output_path = os.path.join(output_folder, f"{os.path.splitext(input_file)[0]}")

    conversions = {
        "pdf_to_docx": lambda: pdf_to_docx(input_path, f"{output_path}.docx"),
        "docx_to_pdf": lambda: docx_to_pdf(input_path, f"{output_path}.pdf"),
        "heic_to_jpg": lambda: heic_to_jpg(input_path, f"{output_path}.jpg"),
        "jpg_to_png": lambda: jpg_to_png(
            input_path,
            f"{output_path}.png",
            transparent_color=kwargs.get("transparent_color"),
        ),
        "png_to_jpg": lambda: png_to_jpg(input_path, f"{output_path}.jpg"),
        "mov_to_mp4": lambda: mov_to_mp4(input_path, f"{output_path}.mp4"),
        "mp4_to_mov": lambda: mp4_to_mov(input_path, f"{output_path}.mov"),
        "wav_to_mp3": lambda: wav_to_mp3(input_path, f"{output_path}.mp3"),
        "mp3_to_wav": lambda: mp3_to_wav(input_path, f"{output_path}.wav"),
        "m4a_to_mp3": lambda: m4a_to_mp3(input_path, f"{output_path}.mp3"),
        "m4a_to_wav": lambda: m4a_to_wav(input_path, f"{output_path}.wav"),
        "video_to_gif": lambda: video_to_gif(input_path, f"{output_path}.gif"),
        "gif_to_video": lambda: gif_to_video(input_path, f"{output_path}.mp4"),
        "live_photo_to_gif": lambda: live_photo_to_gif(
            input_path, f"{output_path}.gif"
        ),
        "live_photo_to_video": lambda: live_photo_to_video(
            input_path, f"{output_path}.mp4"
        ),
    }

    if conversion_type in conversions:
        original_size = get_file_stats(input_path)
        conversions[conversion_type]()
        new_size = get_file_stats(f"{output_path}.{conversion_type.split('_')[-1]}")

        print(f"Conversion {conversion_type} completed.")
        print(f"Original size: {original_size:.2f} KB")
        print(f"New size: {new_size:.2f} KB")
        print(f"Size change: {((new_size - original_size) / original_size) * 100:.2f}%")

        # Additional detailed stats can be added here
    else:
        print(f"Conversion type {conversion_type} not supported.")


if __name__ == "__main__":
    # convert_file("test.pdf", "output", "pdf_to_docx")
    # convert_file("test.docx", "output", "docx_to_pdf")
    # convert_file("IMG_7440.HEIC", "output", "heic_to_jpg")
    convert_file(
        "github.jpeg", "output", "jpg_to_png", transparent_color=(255, 255, 255)
    )
    # convert_file("github.png", "output", "png_to_jpg")
    # convert_file("poizzi.mov", "output", "mov_to_mp4")
    # convert_file("poizzi.mp4", "output", "mp4_to_mov")
    # convert_file("recording.wav", "output", "wav_to_mp3")
    # convert_file("recording.mp3", "output", "mp3_to_wav")

    # convert_file("IMG_2144.mov", "output", "mov_to_mp4")
    # batch_convert_files("input", "output", "jpg_to_png", "jpeg")
