from pydub import AudioSegment


def wav_to_mp3(input_path: str, output_path: str):
    sound = AudioSegment.from_wav(input_path)
    sound.export(output_path, format="mp3", bitrate="320k")  # High-quality MP3


def mp3_to_wav(input_path: str, output_path: str):
    sound = AudioSegment.from_mp3(input_path)
    sound.export(
        output_path, format="wav", parameters=["-ar", "44100"]
    )  # CD-quality WAV


def m4a_to_mp3(input_path: str, output_path: str):
    sound = AudioSegment.from_file(input_path, format="m4a")
    sound.export(output_path, format="mp3", bitrate="320k")


def m4a_to_wav(input_path: str, output_path: str):
    sound = AudioSegment.from_file(input_path, format="m4a")
    sound.export(output_path, format="wav", parameters=["-ar", "44100"])
