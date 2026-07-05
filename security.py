# H.A.V.E.N Security & Logging Module
import os
import logging
import datetime
from config import LOG_PATH

# ─────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────

def setup_logger():
    """Set up HAVEN's logging system."""
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("HAVEN")

# Initialize logger
logger = setup_logger()

# ─────────────────────────────────────────
# LOGGING FUNCTIONS
# ─────────────────────────────────────────

def log_info(message):
    """Log an info message."""
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)

def log_error(message):
    """Log an error message."""
    logger.error(message)

def log_startup():
    """Log HAVEN startup."""
    logger.info("=" * 50)
    logger.info("H.A.V.E.N SYSTEM STARTUP")
    logger.info(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

def log_user_login(user_name, success):
    """Log a login attempt."""
    if success:
        logger.info(f"[AUTH] Successful login: {user_name}")
    else:
        logger.warning(f"[AUTH] Failed login attempt: {user_name}")

def log_command(user_name, command, response):
    """Log a computer control command."""
    logger.info(f"[COMMAND] {user_name} → {command} → {response}")

def log_conversation(user_name, user_input, haven_response):
    """Log a conversation exchange."""
    logger.info(f"[CHAT] {user_name}: {user_input}")
    logger.info(f"[CHAT] HAVEN: {haven_response}")

def log_wake_word(detected_text):
    """Log wake word detection."""
    logger.info(f"[WAKE] Wake word detected in: '{detected_text}'")

def log_shutdown(user_name):
    """Log HAVEN shutdown."""
    logger.info(f"[SHUTDOWN] Session ended by {user_name}")
    logger.info("=" * 50)

# ─────────────────────────────────────────
# SECURITY CHECKS
# ─────────────────────────────────────────

def check_suspicious_command(command):
    """Flag potentially dangerous commands."""
    dangerous_keywords = [
        "format", "delete system", "rm -rf",
        "del /f /s /q c:", "system32"
    ]

    command_lower = command.lower()
    for keyword in dangerous_keywords:
        if keyword in command_lower:
            log_warning(f"[SECURITY] Suspicious command detected: {command}")
            return True
    return False