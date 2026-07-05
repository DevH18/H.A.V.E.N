# H.A.V.E.N Memory Module
import json
import os
import hashlib
import time
from config import (
    PROFILES_PATH,
    MAX_CONVERSATION_HISTORY,
    MAX_LOGIN_ATTEMPTS,
    LOCKOUT_DURATION
)

# ─────────────────────────────────────────
# HASHING
# ─────────────────────────────────────────

def hash_pin(pin):
    """Hash a PIN using SHA-256."""
    salt = "HAVEN_SECURE_SALT_2026"
    return hashlib.sha256((pin + salt).encode()).hexdigest()

# ─────────────────────────────────────────
# PROFILE MANAGEMENT
# ─────────────────────────────────────────

def load_profiles():
    """Load all user profiles from disk."""
    try:
        if os.path.exists(PROFILES_PATH):
            with open(PROFILES_PATH, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"[MEMORY ERROR] Could not load profiles: {e}")
        return {}

def save_profiles(profiles):
    """Save all user profiles to disk."""
    try:
        with open(PROFILES_PATH, "w") as f:
            json.dump(profiles, f, indent=4)
    except Exception as e:
        print(f"[MEMORY ERROR] Could not save profiles: {e}")

# ─────────────────────────────────────────
# CONVERSATION HISTORY
# ─────────────────────────────────────────

def get_history(profiles, user_name):
    """Get conversation history for a user."""
    return profiles[user_name].get("conversations", [])

def save_message(profiles, user_name, role, content):
    """Save a single message to conversation history."""
    profiles[user_name]["conversations"].append({
        "role": role,
        "content": content
    })

    # Trim history to max allowed
    history = profiles[user_name]["conversations"]
    if len(history) > MAX_CONVERSATION_HISTORY * 2:
        profiles[user_name]["conversations"] = history[-(MAX_CONVERSATION_HISTORY * 2):]

    save_profiles(profiles)
    return profiles

# ─────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────

def is_locked_out(profiles, user_name):
    """Check if a user is currently locked out."""
    lockout_until = profiles[user_name].get("lockout_until", 0)
    if time.time() < lockout_until:
        remaining = int(lockout_until - time.time())
        minutes = remaining // 60
        seconds = remaining % 60
        print(f"[SECURITY] Profile locked. Try again in {minutes}m {seconds}s.")
        return True
    return False

def record_failed_attempt(profiles, user_name):
    """Record a failed login attempt."""
    attempts = profiles[user_name].get("failed_attempts", 0) + 1
    profiles[user_name]["failed_attempts"] = attempts

    if attempts >= MAX_LOGIN_ATTEMPTS:
        profiles[user_name]["lockout_until"] = time.time() + LOCKOUT_DURATION
        profiles[user_name]["failed_attempts"] = 0
        save_profiles(profiles)
        print(f"[SECURITY] Too many failed attempts. Profile locked for {LOCKOUT_DURATION // 60} minutes.")
        return True

    save_profiles(profiles)
    return False

def reset_failed_attempts(profiles, user_name):
    """Reset failed attempts after successful login."""
    profiles[user_name]["failed_attempts"] = 0
    profiles[user_name]["lockout_until"] = 0
    save_profiles(profiles)

# ─────────────────────────────────────────
# USER IDENTIFICATION
# ─────────────────────────────────────────

def identify_user(profiles):
    """Identify and authenticate the user."""
    name = input("HAVEN: Hello! Who am I talking to?\nYou: ").strip()

    if not name:
        print("HAVEN: I didn't catch your name. Please restart.")
        exit()

    if name in profiles:
        # Check lockout
        if is_locked_out(profiles, name):
            print("HAVEN: This profile is temporarily locked due to too many failed attempts.")
            exit()

        # Existing user — authenticate
        attempts = 0
        while attempts < MAX_LOGIN_ATTEMPTS:
            pin = input("HAVEN: Please enter your PIN:\nYou: ").strip()

            if hash_pin(pin) == profiles[name]["pin"]:
                reset_failed_attempts(profiles, name)
                print(f"HAVEN: Welcome back, {name}! Good to see you again.")
                return name, profiles
            else:
                attempts += 1
                remaining = MAX_LOGIN_ATTEMPTS - attempts
                locked = record_failed_attempt(profiles, name)

                if locked:
                    print("HAVEN: Profile locked due to too many failed attempts.")
                    exit()
                elif remaining > 0:
                    print(f"HAVEN: Wrong PIN. {remaining} attempt(s) remaining.")

        print("HAVEN: Access denied.")
        exit()

    else:
        # New user — register
        print(f"HAVEN: Nice to meet you, {name}! Let's set up your profile.")
        print("HAVEN: Please set a PIN for your profile:")

        while True:
            pin = input("You: ").strip()
            confirm = input("HAVEN: Confirm your PIN:\nYou: ").strip()

            if pin == confirm:
                profiles[name] = {
                    "name": name,
                    "pin": hash_pin(pin),
                    "conversations": [],
                    "failed_attempts": 0,
                    "lockout_until": 0
                }
                save_profiles(profiles)
                print(f"HAVEN: Profile created successfully! Welcome, {name}.")
                return name, profiles
            else:
                print("HAVEN: PINs don't match. Please try again.")