# H.A.V.E.N - Main Program
# Built by Dev Harsha
# Inspired by Dev Harsha & Geetanjali

import ollama
import requests
from config import (
    ASSISTANT_NAME,
    AI_MODEL,
    SYSTEM_PROMPT,
    FLASK_PORT,
    FLASK_HOST,
    SHUTDOWN_WORD,
)
from voice import speak, listen, wait_for_wake_word
from memory import load_profiles, save_message, identify_user, get_history
from controls import computer_control
from security import (
    log_startup,
    log_user_login,
    log_command,
    log_conversation,
    log_wake_word,
    log_shutdown,
    check_suspicious_command,
    log_info,
    log_error
)

# ─────────────────────────────────────────
# FLASK STATE
# ─────────────────────────────────────────

def set_state(state):
    """Update HAVEN's visual state via Flask."""
    try:
        requests.post(f"http://{FLASK_HOST}:{FLASK_PORT}/set/{state}")
    except:
        pass

# ─────────────────────────────────────────
# AI RESPONSE
# ─────────────────────────────────────────

def ask_haven(user_input, user_name, profiles):
    """Send user input to Llama3 and get HAVEN's response."""
    set_state("speaking")

    try:
        history = get_history(profiles, user_name)

        response = ollama.chat(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(user_name=user_name)
                }
            ] + history + [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        haven_response = response['message']['content']

        # Save to memory
        profiles = save_message(profiles, user_name, "user", user_input)
        profiles = save_message(profiles, user_name, "assistant", haven_response)

        # Log conversation
        log_conversation(user_name, user_input, haven_response)

        return haven_response, profiles

    except Exception as e:
        log_error(f"AI response failed: {e}")
        return "I'm having trouble thinking right now. Please try again.", profiles

# ─────────────────────────────────────────
# MAIN PROGRAM
# ─────────────────────────────────────────

def main():
    # Startup
    log_startup()
    log_info(f"{ASSISTANT_NAME} is initializing...")

    # Load profiles and identify user
    profiles = load_profiles()
    user_name, profiles = identify_user(profiles)
    log_user_login(user_name, True)

    # Welcome
    print(f"\n{ASSISTANT_NAME} is online. Say '{ASSISTANT_NAME}' to wake her up.\n")
    speak(f"Welcome back {user_name}. I am online and ready. Say Engage whenever you need me.")
    set_state("idle")

    # ── Main Loop ──
    while True:
        try:
            # Wait for wake word
            set_state("idle")
            wait_for_wake_word()
            log_wake_word("engage")

            # Listen for command
            set_state("listening")
            user_input = listen()

            if user_input is None:
                log_info("No input detected, returning to idle.")
                continue

            # Check shutdown word
            if SHUTDOWN_WORD in user_input.lower():
                speak("Understood. Going to sleep. Call me whenever you need me.")
                log_shutdown(user_name)
                break

            # Check for suspicious commands
            if check_suspicious_command(user_input):
                speak("I'm sorry, I can't execute that command.")
                set_state("idle")
                continue

            # Check computer control
            control_response = computer_control(user_input)
            if control_response:
                print(f"{ASSISTANT_NAME}: {control_response}\n")
                speak(control_response)
                log_command(user_name, user_input, control_response)
                set_state("idle")
                continue

            # Send to AI
            haven_response, profiles = ask_haven(user_input, user_name, profiles)
            print(f"{ASSISTANT_NAME}: {haven_response}\n")
            speak(haven_response)
            set_state("idle")

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            log_shutdown(user_name)
            break

        except Exception as e:
            log_error(f"Unexpected error in main loop: {e}")
            speak("Something went wrong. I'm recovering.")
            set_state("idle")
            continue

if __name__ == "__main__":
    main()