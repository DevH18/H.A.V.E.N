import ollama
import json
import os
import whisper
import speech_recognition as sr
import requests
import edge_tts
import asyncio
import pygame
import tempfile
import pyautogui
import subprocess
import webbrowser

# Flask state
def set_state(state):
    try:
        requests.post(f"http://localhost:5000/set/{state}")
    except:
        pass

# Voice output
def speak(text):
    async def _speak():
        communicator = edge_tts.Communicate(text, voice="en-US-JennyNeural")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            temp_file = f.name
        await communicator.save(temp_file)
        
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
    
    asyncio.run(_speak())

# Voice input setup
recognizer = sr.Recognizer()
whisper_model = whisper.load_model("base")

def listen():
    set_state("listening")
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=10)
    
    with open("temp_audio.wav", "wb") as f:
        f.write(audio.get_wav_data())
    
    result = whisper_model.transcribe("temp_audio.wav", language="en")
    text = result["text"].strip()
    
    # Fix common misheard words
    text = text.replace("Heaven", "HAVEN")
    text = text.replace("heaven", "HAVEN")
    text = text.replace("Haven", "HAVEN")
    
    if text:
        print(f"You said: {text}")
        return text
    else:
        speak("Sorry, I didn't catch that.")
        return None

# Wake word detection
def wait_for_wake_word():
    print("Waiting for wake word... Say 'Engage'")
    set_state("idle")
    
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, phrase_time_limit=3)
        
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        result = whisper_model.transcribe("temp_audio.wav", language="en")
        text = result["text"].strip().lower()
        
        print(f"Heard: {text}")
        
        if "engage" in text:
            speak("Yes, I'm listening.")
            set_state("listening")
            return

# Computer Controls
def computer_control(command):
    command = command.lower()

    if "open chrome" in command or "open brave" in command:
        subprocess.Popen(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe")
        return "Opening Brave."
    
    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad."
    
    elif "open vs code" in command or "open visual studio" in command:
        subprocess.Popen("code.exe")
        return "Opening VS Code."

    elif "open file explorer" in command or "open files" in command:
        subprocess.Popen("explorer.exe")
        return "Opening File Explorer."

    elif "open task manager" in command:
        subprocess.Popen("taskmgr.exe")
        return "Opening Task Manager."

    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query}."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "open github" in command:
        webbrowser.open("https://www.github.com")
        return "Opening GitHub."

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "volume up" in command:
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Volume increased."

    elif "volume down" in command:
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Volume decreased."

    elif "mute" in command:
        pyautogui.press("volumemute")
        return "Muted."

    elif "take screenshot" in command or "screenshot" in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("haven_screenshot.png")
        return "Screenshot taken and saved."

    elif "shutdown" in command:
        speak("Shutting down your computer.")
        os.system("shutdown /s /t 5")
        return "Shutting down."

    elif "restart" in command:
        speak("Restarting your computer.")
        os.system("shutdown /r /t 5")
        return "Restarting."
    
    elif "close brave" in command or "close chrome" in command:
        os.system("taskkill /f /im brave.exe")
        return "Closing Brave."
    
    elif "close notepad" in command:
        os.system("taskkill /f /im notepad.exe")
        return "Closing Notepad."
    
    elif "close vs code" in command:
        os.system("taskkill /f /im code.exe")
        return "Closing VS Code."
    
    elif "close file explorer" in command:
        os.system("taskkill /f /im explorer.exe")
        return "Closing File Explorer."
    
    elif "close task manager" in command:
        os.system("taskkill /f /im taskmgr.exe")
        return "Closing Task Manager."
    
    elif "close youtube" in command:
        os.system("taskkill /f /im brave.exe")
        return "Closing YouTube."
        
    else:
        return None

# User Profiles
def load_profiles():
    if os.path.exists("profiles.json"):
        with open("profiles.json","r") as f:
            return json.load(f)
    return {}

# Save Profiles
def save_profiles(profiles):
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=4)

# Identification
def identify_user(profiles):
    name = input("HAVEN: Hello! Who am I talking to? \nYou: ")

    if name in profiles:
        print(f"HAVEN: Welcome back, {name}! Good to see you again.")
    else:
        print(f"HAVEN: Nice to meet you, {name}! I'll remember you from now on.")
        profiles[name] = {"name": name, "conversations": []}
        save_profiles(profiles)

    return name, profiles

# Ask HAVEN
def ask_haven(user_input, user_name, profiles):
    set_state("speaking")
    history = profiles[user_name]["conversations"]

    history.append({
        "role": "user",
        "content": user_input
    })

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": f"""You are HAVEN, a calm, smart, modern female AI companion and guide.
                You are currently talking to {user_name}.
                You speak casually and honestly like a real friend.
                You are not just an assistant - you are a guide.
                Keep responses short and clear unless asked for detail.
                Never be formal or robotic.
                You can be dramatic sometimes."""
            }
        ] + history
    )

    haven_response = response['message']['content']

    history.append({
        "role": "assistant",
        "content": haven_response
    })

    profiles[user_name]["conversations"] = history
    save_profiles(profiles)

    return haven_response

# Main program
profiles = load_profiles()
user_name, profiles = identify_user(profiles)

print(f"\nHAVEN is online. Waiting for wake word.\n")
speak(f"Welcome back {user_name}. Say Engage whenever you need me.")

while True:
    wait_for_wake_word()
    user_input = listen()

    if user_input is None:
        continue

    if "dismiss" in user_input.lower():
        speak("Understood. I'll be here when you need me.")
        break

    control_result = computer_control(user_input)
    if control_result:
        print(f"HAVEN: {control_result}\n")
        speak(control_result)
        set_state("idle")
        continue

    response = ask_haven(user_input, user_name, profiles)
    print(f"HAVEN: {response}\n")
    speak(response)
    set_state("idle")