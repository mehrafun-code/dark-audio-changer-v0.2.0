import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VERSION = (BASE_DIR / "VERSION").read_text().strip()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
VOICE_MALE = os.getenv("VOICE_MALE", "hi-IN-MadhurNeural")
VOICE_FEMALE = os.getenv("VOICE_FEMALE", "hi-IN-SwaraNeural")
TARGET_LANG = os.getenv("TARGET_LANG", "hi")
MAX_SPEEDUP = float(os.getenv("MAX_SPEEDUP", "1.5"))
