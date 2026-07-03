import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("Available voices:")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name}")

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)
engine.say("Hello Dev, I am HAVEN.")
engine.runAndWait()