import io

import numpy as np
import soundfile as sf

from kokoro import KPipeline

from config import (
    KOKORO_LANGUAGE,
    KOKORO_VOICE,
    KOKORO_SAMPLE_RATE,
)


# =========================================================
# LOAD KOKORO ONCE
# =========================================================

print("Loading Kokoro TTS model...")

pipeline = KPipeline(
    lang_code=KOKORO_LANGUAGE
)

print("Kokoro TTS loaded.")


# =========================================================
# TEXT → SPEECH
# =========================================================

def text_to_speech(
    text: str,
    voice: str = KOKORO_VOICE
) -> bytes:

    if not text:
        return b""


    audio_chunks = []


    # Kokoro returns a generator
    generator = pipeline(
        text,
        voice=voice
    )


    for _, _, audio in generator:

        if hasattr(audio, "numpy"):

            audio = audio.numpy()

        else:

            audio = np.asarray(audio)


        audio_chunks.append(
            audio
        )


    if not audio_chunks:

        return b""


    # Join chunks
    audio = np.concatenate(
        audio_chunks
    )


    # -----------------------------------------------------
    # Convert to WAV in memory
    # -----------------------------------------------------

    buffer = io.BytesIO()


    sf.write(
        buffer,
        audio,
        KOKORO_SAMPLE_RATE,
        format="WAV"
    )


    return buffer.getvalue()