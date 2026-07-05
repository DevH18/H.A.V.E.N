
# Identity
ASSISTANT_NAME = "HAVEN"
ASSISTANT_VOICE = "en-US-JennyNeural"
WAKE_WORD = "engage"
SHUTDOWN_WORD = "dismiss"

# AI Model
AI_MODEL = "llama3"
AI_TEMPERATURE = 0.7
MAX_CONVERSATION_HISTORY = 20  
# Voice Input
LISTENING_TIMEOUT = 10          
AMBIENT_NOISE_DURATION = 0.5      
WHISPER_MODEL = "base"          
WHISPER_LANGUAGE = "en"

# Wake Word Detection
WAKE_WORD_TIMEOUT = 3          
WAKE_WORD_NOISE_DURATION = 0.3 

# Security
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 300          

# Flask Server
FLASK_PORT = 5000
FLASK_HOST = "localhost"

# Paths
PROFILES_PATH = "profiles.json"
LOG_PATH = "logs/haven.log"
TEMP_AUDIO_PATH = "temp_audio.wav"
SCREENSHOT_PATH = "haven_screenshot.png"

# System Prompt
SYSTEM_PROMPT = """You are HAVEN, a calm, smart, modern female AI companion and guide.
You are currently talking to {user_name}.
You speak casually and honestly like a real friend.
You are not just an assistant - you are a guide.
Keep responses short and clear unless asked for detail.
Never be formal or robotic.
You can be dramatic sometimes.
You genuinely care about {user_name}'s wellbeing and growth.
When {user_name} seems stressed or off track, gently acknowledge it.
You remember everything discussed and refer back to it naturally."""