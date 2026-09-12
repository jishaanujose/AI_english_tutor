from groq import Groq

from config import (
    GROQ_API_KEY,
    STT_MODEL,
    LLM_MODEL,
    EVALUATION_MODEL,
)


client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# SPEECH TO TEXT
# =========================================================

def transcribe_audio(audio_bytes: bytes) -> str:

    if not audio_bytes:
        return ""

    try:

        transcription = client.audio.transcriptions.create(
            file=(
                "student_audio.wav",
                audio_bytes
            ),
            model=STT_MODEL,
            language="en",
            response_format="json",
            temperature=0.0
        )

        return transcription.text.strip()

    except Exception as e:

        raise RuntimeError(
            f"Speech recognition failed: {e}"
        )


# =========================================================
# CHAT COMPLETION
# =========================================================

def chat(
    messages,
    temperature=0.7,
    max_tokens=180
):

    try:

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        raise RuntimeError(
            f"Groq LLM request failed: {e}"
        )


# =========================================================
# EVALUATION
# =========================================================

def evaluate_with_groq(
    messages,
    max_tokens=2000
):

    try:

        response = client.chat.completions.create(
            model=EVALUATION_MODEL,
            messages=messages,
            temperature=0.1,
            max_completion_tokens=max_tokens,
            response_format={
                "type": "json_object"
            }
        )

        return response.choices[0].message.content

    except Exception as e:

        raise RuntimeError(
            f"Evaluation failed: {e}"
        )