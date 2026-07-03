import speech_recognition as sr
import whisper

recognizer = sr.Recognizer()
whisper_model = whisper.load_model("base")

print("Say something...")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
    audio = recognizer.listen(source, phrase_time_limit=5)

with open("test_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())

result = whisper_model.transcribe("test_audio.wav", language="en")
print(f"You said: {result['text']}")