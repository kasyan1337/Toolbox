# tests/test_conversions.py

import os
import unittest

from main import convert_file


class TestFileConversions(unittest.TestCase):
    input_dir = "input_test"
    output_dir = "output_test"

    def setUp(self):
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Remove generated files after each test
        for file in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def check_conversion(self, input_file, conversion_type, expected_extension, **kwargs):
        output_file = os.path.join(self.output_dir, f"{os.path.splitext(input_file)[0]}.{expected_extension}")
        convert_file(input_file, self.output_dir, conversion_type, **kwargs)
        self.assertTrue(os.path.exists(output_file), f"{conversion_type} failed to create {output_file}")

    def test_pdf_to_docx(self):
        self.check_conversion("test.pdf", "pdf_to_docx", "docx")

    def test_docx_to_pdf(self):
        self.check_conversion("test.docx", "docx_to_pdf", "pdf")

    def test_heic_to_jpg(self):
        self.check_conversion("IMG_7440.HEIC", "heic_to_jpg", "jpg")

    def test_jpg_to_png(self):
        self.check_conversion("github.jpeg", "jpg_to_png", "png", transparent_color=(255, 255, 255))

    def test_png_to_jpg(self):
        self.check_conversion("github.png", "png_to_jpg", "jpg")

    def test_mov_to_mp4(self):
        self.check_conversion("poizzi.mov", "mov_to_mp4", "mp4")

    def test_mp4_to_mov(self):
        self.check_conversion("poizzi.mp4", "mp4_to_mov", "mov")

    def test_wav_to_mp3(self):
        self.check_conversion("recording.wav", "wav_to_mp3", "mp3")

    def test_mp3_to_wav(self):
        self.check_conversion("recording.mp3", "mp3_to_wav", "wav")


if __name__ == "__main__":
    unittest.main()
