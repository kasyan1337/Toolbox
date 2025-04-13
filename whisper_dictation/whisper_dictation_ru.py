import time
import threading
import os
import wave
import pyaudio
import whisper
from pynput import keyboard
from AppKit import NSApplication, NSCursor
import signal
import sys

# Initialize the macOS application (needed for AppKit interactions)
app = NSApplication.sharedApplication()

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Global state and threading primitives
recording = False
audio_frames = []
stop_recording_event = threading.Event()
current_audio_filename = "temp_audio.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Load Whisper model in background (if needed)
model = whisper.load_model("large")
# Alternatively, load asynchronously as previously shown if startup delay is an issue.

current_recording_thread = None


def set_busy_cursor():
    try:
        NSCursor.closedHandCursor().set()
    except Exception as e:
        print("Error setting busy cursor:", e)


def reset_cursor():
    try:
        NSCursor.arrowCursor().set()
    except Exception as e:
        print("Error resetting cursor:", e)


def record_audio(filename):
    global audio_frames
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)
    except Exception as e:
        print("Error opening audio stream:", e)
        return
    audio_frames = []
    print("Recording audio...")
    while not stop_recording_event.is_set():
        try:
            data = stream.read(CHUNK)
            audio_frames.append(data)
        except Exception as e:
            print("Error reading audio stream:", e)
            break
    stream.stop_stream()
    stream.close()
    try:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_frames))
        wf.close()
    except Exception as e:
        print("Error writing audio file:", e)


def transcribe_and_type(audio_file, language):
    print("Transcribing audio...")
    try:
        result = model.transcribe(audio_file, language=language)
        text = result.get("text", "").strip()
        print("Transcribed text:", text)
    except Exception as e:
        print("Error during transcription:", e)
        text = ""
    if text:
        try:
            controller = keyboard.Controller()
            controller.type(text)
            # Delay to allow keystrokes to be processed
            time.sleep(0.5)
        except Exception as e:
            print("Error typing out the transcription:", e)


def start_recording(language):
    global recording, current_recording_thread
    recording = True
    stop_recording_event.clear()
    set_busy_cursor()
    current_recording_thread = threading.Thread(target=record_audio, args=(current_audio_filename,))
    current_recording_thread.start()
    print(f"Recording started in {language}...")


def stop_recording(language):
    global recording, current_recording_thread
    if recording:
        print("Stopping recording...")
        stop_recording_event.set()
        current_recording_thread.join()
        print("Recording stopped. Beginning transcription...")
        transcribe_and_type(current_audio_filename, language)
        try:
            os.remove(current_audio_filename)
        except Exception as e:
            print("Error removing temporary file:", e)
        reset_cursor()
        recording = False


def signal_handler(sig, frame):
    print("\nSignal received. Initiating shutdown process...")
    stop_recording("en")
    sys.exit(0)


if __name__ == "__main__":
    language = "ru" # Default language
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Application started: Recording automatically in English.")
    start_recording(language)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught. Stopping recording...")
        stop_recording(language)