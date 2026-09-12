import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()


# =========================================================
# API
# =========================================================

# 2. Retrieve key from st.secrets (Streamlit Cloud) OR os.getenv (Local .env)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file."
    )


# =========================================================
# GROQ MODELS
# =========================================================

# Fast speech recognition
STT_MODEL = "whisper-large-v3-turbo"

# Main conversation model
LLM_MODEL = "openai/gpt-oss-120b"


# Evaluation model
EVALUATION_MODEL = "openai/gpt-oss-120b"


# =========================================================
# KOKORO
# =========================================================

KOKORO_LANGUAGE = "a"

KOKORO_VOICE = "af_heart"

KOKORO_SAMPLE_RATE = 24000


# =========================================================
# TUTOR
# =========================================================

MAX_TEACHER_TOKENS = 180
