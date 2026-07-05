# H.A.V.E.N Computer Control Module
import os
import subprocess
import webbrowser
import pyautogui
import datetime
from config import SCREENSHOT_PATH

# ─────────────────────────────────────────
# APPLICATION CONTROL
# ─────────────────────────────────────────

APPS = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "notepad": "notepad.exe",
    "vs code": "code.exe",
    "visual studio": "code.exe",
    "file explorer": "explorer.exe",
    "files": "explorer.exe",
    "task manager": "taskmgr.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}

APP_PROCESS_NAMES = {
    "brave": "brave.exe",
    "chrome": "brave.exe",
    "notepad": "notepad.exe",
    "vs code": "code.exe",
    "visual studio": "code.exe",
    "file explorer": "explorer.exe",
    "files": "explorer.exe",
    "task manager": "taskmgr.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "google": "https://www.google.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://www.stackoverflow.com",
    "chatgpt": "https://www.chat.openai.com",
}

# ─────────────────────────────────────────
# MAIN CONTROL FUNCTION
# ─────────────────────────────────────────

def computer_control(command):
    """Process a computer control command and return response."""
    command = command.lower().strip()

    # ── Open Applications ──
    if command.startswith("open"):
        app_name = command.replace("open", "").strip()

        # Check websites first
        for site, url in WEBSITES.items():
            if site in app_name:
                webbrowser.open(url)
                return f"Opening {site.capitalize()}."

        # Check applications
        for app, path in APPS.items():
            if app in app_name:
                try:
                    subprocess.Popen(path)
                    return f"Opening {app.capitalize()}."
                except Exception as e:
                    return f"Sorry, I couldn't open {app}. Make sure it's installed."

        return None

    # ── Close Applications ──
    elif command.startswith("close"):
        app_name = command.replace("close", "").strip()
        
        for app, process in APP_PROCESS_NAMES.items():
            if app in app_name:
                try:
                    subprocess.Popen(
                        f"taskkill /f /im {process}",
                        shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                        )
                    return f"Closing {app.capitalize()}."
                except Exception as e:
                    return f"Couldn't close {app}: {e}"
                
                return None
            
    # ── Web Search ──
    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query}."
        return "What would you like me to search for?"

    # ── Volume Control ──
    elif "volume up" in command:
        steps = 5
        for _ in range(steps):
            pyautogui.press("volumeup")
        return "Volume increased."

    elif "volume down" in command:
        steps = 5
        for _ in range(steps):
            pyautogui.press("volumedown")
        return "Volume decreased."

    elif "mute" in command or "unmute" in command:
        pyautogui.press("volumemute")
        return "Toggled mute."

    # ── Screenshot ──
    elif "screenshot" in command or "take screenshot" in command:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"haven_screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            return f"Screenshot saved as {path}."
        except Exception as e:
            return f"Couldn't take screenshot: {e}"

    # ── Time and Date ──
    elif "what time" in command or "current time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"It's {now}."

    elif "what date" in command or "today's date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today is {today}."

    # ── System Control ──
    elif "shutdown" in command or "shut down" in command:
        os.system("shutdown /s /t 5")
        return "Shutting down in 5 seconds."

    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Restarting in 5 seconds."

    elif "sleep" in command and "computer" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting computer to sleep."

    # ── No match ──
    else:
        return None