import os
import sys
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AGNES_API_KEY = os.getenv("AGNES_API_KEY")

if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found in .env")
    sys.exit(1)
if not AGNES_API_KEY:
    print("ERROR: AGNES_API_KEY not found in .env")
    sys.exit(1)

GROQ_BASE_URL = "https://api.groq.com"
AGNES_BASE_URL = "https://apihub.agnes-ai.com/v1"

QWEN_MODEL = "qwen/qwen3.6-27b"
AGNES_MODEL = "agnes-2.0-flash"

OUTPUT_DIR = "output"
AUDIO_DIR = f"{OUTPUT_DIR}/audio"
METADATA_DIR = f"{OUTPUT_DIR}/metadata"
SOCIAL_DIR = f"{OUTPUT_DIR}/social"
