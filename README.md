# H.A.V.E.N
### Personal AI Companion & Guide

HAVEN is a locally-running personal AI assistant built with Python.
Inspired by and named after **Dev Harsha** and **Geetanjali**.

---

## What HAVEN Can Do

- 🎙️ Listens to your voice (Whisper - fully offline)
- 🧠 Thinks and responds intelligently (Llama3 via Ollama)
- 🔊 Speaks back naturally (Microsoft Edge TTS)
- 💾 Remembers all conversations (local JSON memory)
- 👤 Recognises different users
- 🖥️ Controls your computer (open/close apps, search, volume, screenshot)
- 🌐 Neural network visual UI that reacts to her states
- 🔒 Completely private — no cloud, no Google, no data sent anywhere

---

## Wake Word
Say **"Engage"** to activate HAVEN.
Say **"Dismiss"** to put her to sleep.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Brain | Llama3 (via Ollama) |
| Voice Input | OpenAI Whisper |
| Voice Output | Microsoft Edge TTS |
| Memory | Local JSON |
| UI | HTML/CSS/JavaScript |
| Backend Bridge | Flask |
| Computer Control | PyAutoGUI + Subprocess |

---

## Requirements

- Python 3.11+
- Ollama installed with Llama3 model
- FFmpeg installed
- Microphone

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DevH18/H.A.V.E.N.git
cd H.A.V.E.N
```

2. Install dependencies:
```bash
pip install ollama whisper speechrecognition pyaudio edge-tts pygame pyautogui flask flask-cors requests openai-whisper
```

3. Install and run Ollama with Llama3:
```bash
ollama pull llama3
```

4. Run the Flask server:
```bash
python server.py
```

5. Run HAVEN:
```bash
python haven.py
```

6. Open `haven_ui.html` in your browser.

---

## Project Roadmap

- [x] Voice input and output
- [x] AI brain (Llama3)
- [x] Memory system
- [x] Wake word detection
- [x] Computer control
- [x] Neural network UI
- [ ] News updates
- [ ] Face recognition
- [ ] Eye tracking (IR)
- [ ] Arc Reactor UI
- [ ] Waveform UI
- [ ] Humanoid Silhouette UI

---

## Built By
**Dev Harsha Thantipudi** — CSE - Artificial Intelligence & Machine Learning Student, NRI Institute of Technology, Vijayawada