import speech_recognition as sr

recognizer = sr.Recognizer()

print("Available microphones:")
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic}")

print("\nTesting microphone...")
print("Speak now — say anything!")

with sr.Microphone() as source:
    print(f"Energy threshold before calibration: {recognizer.energy_threshold}")
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print(f"Energy threshold after calibration: {recognizer.energy_threshold}")
    audio = recognizer.listen(source, phrase_time_limit=5)
    print("Got audio!")

with open("debug_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())

print("Audio saved — check debug_audio.wav")