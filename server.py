import os
import tempfile
import base64
import subprocess
import datetime
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import speech_recognition as sr
import pyttsx3

app = Flask(__name__, static_folder="static", static_url_path="/static")
ALLOWED_EXT = {"wav", "webm", "mp3", "m4a", "ogg"}

# --- TTS ---
def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

# --- Greeting ---
def wishMe():
    now = datetime.datetime.now()
    day = now.strftime("%A, %B %d")
    greeting = f"Hello there, Jennie here. Today is {day}. How can I help you?"
    speak(greeting)

# --- STT ---
def transcribe_wav(wav_path):
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="en-in")
    except Exception as e:
        print("Transcription error:", e)
        return ""

# --- Convert to wav ---
def convert_to_wav(in_path, out_path):
    cmd = ["ffmpeg", "-y", "-i", in_path, "-ar", "16000", "-ac", "1", out_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print("ffmpeg conversion failed:", e)
        return False

# --- Save TTS file ---
def text_to_speech_save(text, out_path):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    return out_path

# --- Jennie logic ---
def process_text_with_jennie(input_text):
    txt = (input_text or "").lower()
    reply = "I did not understand that. Can you repeat?"
    open_url = None

    if 'open youtube' in txt:
        reply = "Opening YouTube."
        open_url = "https://youtube.com"
    elif 'open google' in txt:
        reply = "Opening Google."
        open_url = "https://google.com"
    elif 'hello' in txt or 'hi' in txt:
        reply = "Hello! How can I help you?"
    elif txt.strip() == "":
        reply = "Sorry, I didn't hear anything."
    else:
        reply = "You said: " + input_text

    static_dir = os.path.join(os.getcwd(), "static")
    os.makedirs(static_dir, exist_ok=True)
    audio_path = os.path.join(static_dir, "reply.wav")
    try:
        text_to_speech_save(reply, audio_path)
    except Exception as e:
        print("TTS error:", e)
        audio_path = None

    return reply, audio_path, open_url

# --- Serve HTML ---
@app.route("/")
def index():
    return send_from_directory("static", "jennie.html")

# --- Greeting API ---
@app.route("/api/greet", methods=["POST"])
def api_greet():
    wishMe()
    return jsonify({"status": "greeted"})

# --- Voice API ---
@app.route("/api/voice", methods=["POST"])
def api_voice():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    f = request.files["audio"]
    filename = secure_filename(f.filename) or "upload"
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXT):
        return jsonify({"error": "Unsupported file type"}), 400

    tmp_dir = tempfile.gettempdir()
    in_path = os.path.join(tmp_dir, filename)
    f.save(in_path)

    ext = filename.rsplit(".", 1)[-1].lower()
    wav_path = in_path if ext == "wav" else os.path.join(tmp_dir, filename + ".wav")
    if ext != "wav":
        if not convert_to_wav(in_path, wav_path):
            return jsonify({"error": "Failed to convert audio"}), 500

    transcript = transcribe_wav(wav_path)
    reply_text, audio_path, open_url = process_text_with_jennie(transcript)

    audio_b64 = None
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f2:
            audio_b64 = base64.b64encode(f2.read()).decode("utf-8")

    return jsonify({
        "text": reply_text,
        "audio_base64": audio_b64,
        "open_url": open_url
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
