import time
import threading
import os
import wave
import pyaudio
import whisper
from pynput import keyboard
from AppKit import NSApplication, NSCursor

# Initialize a shared NSApplication instance to allow AppKit functions to work.
app = NSApplication.sharedApplication()

import sounddevice as sd

try:
    sd.check_input_settings()
    print("✅ Microphone access OK")
except Exception as e:
    import os
    os.system("""osascript -e 'display dialog "⚠️ Mic access denied for Whisper.\n\nGo to System Settings → Privacy & Security → Microphone and enable Python." buttons {"OK"}'""")
    os.system("""open "x-apple.systempreferences:com.apple.preference.security?Privacy_Microphone" """)
    raise e


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

recording = False
current_language = None
audio_frames = []
stop_recording_event = threading.Event()
last_key_times = {}
current_recording_thread = None
current_audio_filename = "temp_audio.wav"

p = pyaudio.PyAudio()
model = whisper.load_model("large")

def set_busy_cursor():
    try:
        NSCursor.closedHandCursor().set()  # Use a closed-hand cursor as an indicator.
    except Exception as e:
        print("Error setting busy cursor:", e)

def reset_cursor():
    try:
        NSCursor.arrowCursor().set()  # Revert to the default arrow cursor.
    except Exception as e:
        print("Error resetting cursor:", e)

def record_audio(filename):
    global audio_frames
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    audio_frames = []
    while not stop_recording_event.is_set():
        data = stream.read(CHUNK)
        audio_frames.append(data)
    stream.stop_stream()
    stream.close()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

def transcribe_and_type(audio_file, language):
    result = model.transcribe(audio_file, language=language)
    text = result["text"].strip()
    controller = keyboard.Controller()
    controller.type(text)

def start_recording_thread(language):
    global recording, current_language, current_recording_thread, stop_recording_event
    recording = True
    current_language = language
    stop_recording_event.clear()
    set_busy_cursor()
    current_recording_thread = threading.Thread(target=record_audio, args=(current_audio_filename,))
    current_recording_thread.start()
    print(f"Recording started for language: {language}")

def stop_recording():
    global recording, current_recording_thread, current_audio_filename
    if recording:
        stop_recording_event.set()
        current_recording_thread.join()
        print("Recording stopped. Transcribing...")
        transcribe_and_type(current_audio_filename, current_language)
        os.remove(current_audio_filename)
        reset_cursor()
        recording = False

def on_press(key):
    global last_key_times
    try:
        if key in [keyboard.Key.f1, keyboard.Key.f2, keyboard.Key.f3]:
            now = time.time()
            key_name = key.name
            if key_name in last_key_times and now - last_key_times[key_name] < 0.5:
                lang = "en" if key == keyboard.Key.f1 else "sk" if key == keyboard.Key.f2 else "ru"
                if not recording:
                    threading.Thread(target=start_recording_thread, args=(lang,)).start()
                last_key_times[key_name] = 0
            else:
                last_key_times[key_name] = now
        elif key == keyboard.Key.f12:
            if recording:
                stop_recording()
    except Exception:
        pass

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()