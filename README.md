"# JENNIE-voice-assistant" 
# 🎙️ Jennie Voice Assistant (Flask Web App)

Jennie is a personal AI voice assistant built with **Python** and **Flask**.  
It can listen to your voice, understand your commands, and reply using text-to-speech — all through a simple web interface.

---

## 🚀 Features

- 🎧 **Speech-to-Text (STT)** — Converts your recorded voice into text using Google Speech Recognition.  
- 🗣️ **Text-to-Speech (TTS)** — Speaks out responses using `pyttsx3`.  
- 🌐 **Web-based Interface** — Easily accessible through your browser.  
- 🧠 **Smart Commands** — Supports basic actions like:
  - “Open YouTube”
  - “Open Google”
  - Simple greetings (“hello”, “hi”)
- ⚙️ **FFmpeg Integration** — Converts various audio formats (MP3, WAV, M4A, etc.) for recognition.

---

## 🧩 Tech Stack

- **Python 3**
- **Flask**
- **SpeechRecognition**
- **pyttsx3**
- **FFmpeg**
- **HTML/CSS/JS (for frontend)**

---

## 📁 Project Structure
Jennie-voice-assistant/
│
├── server.py # Flask backend
├── static/
│ ├── jennie.html # Frontend web page
│ ├── reply.wav # Generated voice replies
│ └── (other static files)
├── requirements.txt # Dependencies list
└── README.md # This file

## Dependcies
Flask==3.0.3
SpeechRecognition==3.10.0
pyttsx3==2.90
Werkzeug==3.0.3
ffmpeg-python==0.2.0
gunicorn==23.0.0

