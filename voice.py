# H.A.V.E.N Voice Module
import whisper
import speech_recognition as sr
import edge_tts
import asyncio
import pygame
import tempfile
import os
from config import (
    ASSISTANT_VOICE,
    WAKE_WORD,
    LISTENING_TIMEOUT,
    AMBIENT_NOISE_DURATION,
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
    WAKE_WORD_TIMEOUT,
    WAKE_WORD_NOISE_DURATION,
    TEMP_AUDIO_PATH
)

# Initialize
recognizer = sr.Recognizer()
recognizer.energy_threshold = 1500
recognizer.dynamic_energy_threshold = False
whisper_model = whisper.load_model(WHISPER_MODEL)

# ─────────────────────────────────────────
# VOICE OUTPUT
# ─────────────────────────────────────────

def speak(text):
    """Convert text to speech using Edge TTS."""
    try:
        async def _speak():
            communicator = edge_tts.Communicate(text, voice=ASSISTANT_VOICE)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                temp_file = f.name
            await communicator.save(temp_file)

            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()

            try:
                os.remove(temp_file)
            except:
                pass

        asyncio.run(_speak())

    except Exception as e:
        print(f"[VOICE ERROR] Could not speak: {e}")

# ─────────────────────────────────────────
# VOICE INPUT
# ─────────────────────────────────────────

def record_audio(timeout):
    """Record audio from microphone and save to file."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_DURATION)
            recognizer.energy_threshold = 1500
            recognizer.dynamic_energy_threshold = False
            audio = recognizer.listen(source, phrase_time_limit=timeout)

        with open(TEMP_AUDIO_PATH, "wb") as f:
            f.write(audio.get_wav_data())

        return True

    except Exception as e:
        print(f"[MIC ERROR] Could not record audio: {e}")
        return False

def transcribe_audio():
    """Transcribe recorded audio using Whisper."""
    try:
        result = whisper_model.transcribe(TEMP_AUDIO_PATH, language=WHISPER_LANGUAGE)
        text = result["text"].strip()

        # Fix common misheard words
        text = text.replace("Heaven", "HAVEN")
        text = text.replace("heaven", "HAVEN")
        text = text.replace("Haven", "HAVEN")

        return text

    except Exception as e:
        print(f"[WHISPER ERROR] Could not transcribe: {e}")
        return ""

def listen():
    """Listen to user and return transcribed text."""
    print("Listening...")

    if not record_audio(LISTENING_TIMEOUT):
        speak("Sorry, I had trouble with the microphone.")
        return None

    text = transcribe_audio()

    if text:
        print(f"You said: {text}")
        return text
    else:
        speak("Sorry, I didn't catch that.")
        return None

# ─────────────────────────────────────────
# WAKE WORD
# ─────────────────────────────────────────

def wait_for_wake_word():
    """Wait silently until wake word is detected."""
    print(f"Waiting for wake word... Say '{WAKE_WORD.capitalize()}'")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(
                    source, duration=WAKE_WORD_NOISE_DURATION
                )
                recognizer.energy_threshold = 1500
                recognizer.dynamic_energy_threshold = False
                audio = recognizer.listen(
                    source, phrase_time_limit=WAKE_WORD_TIMEOUT
                )

            with open(TEMP_AUDIO_PATH, "wb") as f:
                f.write(audio.get_wav_data())

            result = whisper_model.transcribe(
                TEMP_AUDIO_PATH, language=WHISPER_LANGUAGE
            )
            text = result["text"].strip().lower()

            print(f"Heard: {text}")

            if WAKE_WORD in text:
                speak("Yes, I'm listening.")
                return

        except Exception as e:
            print(f"[WAKE WORD ERROR] {e}")
            continue