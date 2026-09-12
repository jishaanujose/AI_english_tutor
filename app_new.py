import streamlit as st
import hashlib
from audio_recorder_streamlit import audio_recorder
from pathlib import Path
import base64
import uuid
from tutor import (
    start_session,
    get_teacher_response
)

from groq_client import (
    transcribe_audio
)

from kokoro_tts import (
    text_to_speech
)

from evaluator import (
    evaluate_conversation
)

TEACHER_IMAGE = Path("teacher_img.png")
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

base64_image = image_to_base64("teacher_img.png")

import mimetypes

TEACHER_IMAGE = Path("teacher_img.png")


def get_image_data_uri(path: Path) -> str:
    """Reads an image file and returns a complete, formatted Base64 Data URI."""
    if not path.exists():
        # Fallback SVG avatar if file is missing (prevents white broken box)
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="#4A90E2"/><text x="50%" y="55%" dominant-baseline="middle" text-anchor="middle" font-size="40" fill="white">👩‍🏫</text></svg>"""
        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

    # Auto-detect mime type (png, jpeg, webp, etc.)
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/png"

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


# Generate complete data URI
image_data_uri = get_image_data_uri(TEACHER_IMAGE)
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI English Speaking Tutor",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
        text-align: center;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
        text-align: center;
    }

    /* Central teacher area */
    .conversation-stage {
        width: 100%;
        min-height: 220px;
        background-color: #000000;
        border-radius: 24px;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        padding: 50px;
        margin: 25px 0;
        box-sizing: border-box;
    }

    .teacher-label {
        color: #aaaaaa;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .teacher-question {
        color: white;
        font-size: 32px;
        font-weight: 500;
        line-height: 1.4;
        text-align: center;
        max-width: 800px;
    }
    
    .student-area {
        text-align: center;
        margin-top: 25px;
    }
    .teacher-avatar {
        width: 256px;
        height: 256px;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }
    .score {
        font-size: 32px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "call_active": False,
    "conversation": [],
    "teacher_audio": None,
    "last_student_text": "",
    "evaluation": None,
    "session_count": 0,
    "audio_played": False,

    # Remember the last audio recording that was processed
    "processed_audio_hash": None
}


for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🎓 AI English Speaking Tutor'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Have a natural conversation with your personal '
    'English teacher.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🎯 Speaking Coach")

    st.write(
        """
        Your teacher will:

        • Listen to what you say

        • Ask follow-up questions

        • Keep the conversation natural

        • Adapt questions to your answers

        • Evaluate your English after the call
        """
    )


    st.divider()


    st.subheader("Session")

    st.write(
        f"Sessions completed: "
        f"{st.session_state.session_count}"
    )


# =========================================================
# START CALL
# =========================================================

if not st.session_state.call_active:

    st.subheader(
        "Ready to practice?"
    )


    st.write(
        "Start a conversation and speak naturally."
    )


    if st.button(
        "📞 Start Call",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Your teacher is preparing..."
            ):

                teacher_text, conversation = (
                    start_session()
                )


                teacher_audio = (
                    text_to_speech(
                        teacher_text
                    )
                )


            st.session_state.conversation = (
                conversation
            )

            st.session_state.teacher_audio = (
                teacher_audio
            )
            st.session_state.audio_played = False
            st.session_state.call_active = True

            st.session_state.evaluation = None

            st.session_state.last_student_text = ""

            st.rerun()


        except Exception as e:

            st.error(
                f"Could not start session: {e}"
            )


# =========================================================
# ACTIVE CALL
# =========================================================

if st.session_state.call_active:

    # -----------------------------------------------------
    # Call status
    # -----------------------------------------------------

    st.success(
        "🟢 Call is active"
    )


    # -----------------------------------------------------
    # Teacher
    # -----------------------------------------------------

    st.subheader(
        "👩‍🏫 Teacher"
    )


    teacher_messages = [

        x for x in
        st.session_state.conversation

        if x["role"] == "assistant"

    ]


    if teacher_messages:

        latest_teacher = (
            teacher_messages[-1]["content"]
        )

        st.markdown(
            f"""
            <div class="conversation-stage">
                <img 
                    src="data:image/jpeg;base64,{base64_image}" 
                    class="teacher-avatar" 
                    alt="Teacher"
                />
                <div class="teacher-question">
                    {latest_teacher}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # Audio
    # -----------------------------------------------------

    # if st.session_state.teacher_audio:
    #     col1, col2, col3 = st.columns([1, 2, 1])
    #
    #     with col2:
    #         st.audio(
    #             st.session_state.teacher_audio,
    #             format="audio/wav"
    #         )
    # if st.session_state.teacher_audio and not st.session_state.get("audio_played", False):
    #     audio_b64 = base64.b64encode(st.session_state.teacher_audio).decode()
    #     unique_id = uuid.uuid4().hex

    #     autoplay_html = f"""
    #         <html>
    #             <body>
    #                 <audio id="aud_{unique_id}" autoplay>
    #                     <source src="data:audio/wav;base64,{audio_b64}" type="audio/wav">
    #                 </audio>
    #                 <script>
    #                     var audio = document.getElementById("aud_{unique_id}");
    #                     if (audio) {{
    #                         audio.play().catch(function(e) {{ console.log(e); }});
    #                     }}
    #                 </script>
    #             </body>
    #         </html>
    #     """

    #     st.components.v1.html(autoplay_html, height=0, width=0)

        # Mark as played so subsequent reruns ignore it
        # st.session_state.audio_played = True
    if st.session_state.teacher_audio and not st.session_state.get("audio_played", False):
        audio_b64 = base64.b64encode(st.session_state.teacher_audio).decode()
        unique_id = uuid.uuid4().hex
    
        autoplay_html = f"""
            <html>
                <body style="margin:0; padding:0;">
                    <audio id="aud_{unique_id}" controls autoplay style="width:100%;">
                        <source src="data:audio/wav;base64,{audio_b64}" type="audio/wav">
                    </audio>
                    <script>
                        var audio = document.getElementById("aud_{unique_id}");
                        if (audio) {{
                            audio.play().catch(function(e) {{
                                console.log("Autoplay prevented on mobile device:", e);
                            }});
                        }}
                    </script>
                </body>
            </html>
        """

        # Render as a small visible player block (e.g., height 50px)
        st.components.v1.html(autoplay_html, height=50)
        st.session_state.audio_played = True

    st.divider()


    # =====================================================
    # STUDENT RECORDING
    # =====================================================

    # st.markdown(
    #     """
    #     <div class="student-area">
    #         <h3>🎤 Your turn</h3>
    #         <p>Speak your answer when you're ready.</p>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    audio_bytes = audio_recorder(
        text="Record answer",
        recording_color="#ff4b4b",
        neutral_color="#777777",
        icon_name="microphone",
        icon_size="2x"
    )

    # =====================================================
    # PROCESS ONLY A NEW RECORDING
    # =====================================================

    if audio_bytes:

        # Create a unique ID for this recording
        audio_hash = hashlib.md5(audio_bytes).hexdigest()

        # Only process if this is a NEW recording
        if audio_hash != st.session_state.processed_audio_hash:

            try:

                # ---------------------------------------------
                # Remember this recording immediately
                # ---------------------------------------------

                st.session_state.processed_audio_hash = audio_hash

                # ---------------------------------------------
                # STT
                # ---------------------------------------------

                with st.spinner(
                        "Understanding what you said..."
                ):

                    student_text = transcribe_audio(
                        audio_bytes
                    )

                if not student_text:
                    st.warning(
                        "I couldn't understand the recording. "
                        "Please try again."
                    )

                    st.stop()

                # # ---------------------------------------------
                # # CLEAR OLD AUDIO HERE TO PREVENT REPLAY
                # # ---------------------------------------------
                # st.session_state.teacher_audio = None

                # ---------------------------------------------
                # Save student response
                # ---------------------------------------------

                st.session_state.last_student_text = (
                    student_text
                )
                st.session_state.audio_played = False
                st.session_state.conversation.append(
                    {
                        "role": "user",
                        "content": student_text
                    }
                )

                # ---------------------------------------------
                # LLM
                # ---------------------------------------------

                with st.spinner(
                        "Teacher is thinking..."
                ):

                    teacher_text = get_teacher_response(
                        st.session_state.conversation
                    )

                # ---------------------------------------------
                # Save teacher response
                # ---------------------------------------------

                st.session_state.conversation.append(
                    {
                        "role": "assistant",
                        "content": teacher_text
                    }
                )

                # ---------------------------------------------
                # Kokoro TTS
                # ---------------------------------------------

                with st.spinner(
                        "Teacher is speaking..."
                ):

                    teacher_audio = text_to_speech(
                        teacher_text
                    )

                st.session_state.teacher_audio = (
                    teacher_audio
                )

                # ---------------------------------------------
                # Rerun to display teacher response
                # ---------------------------------------------

                st.rerun()


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


    # =====================================================
    # END CALL
    # =====================================================

    st.divider()


    if st.button(
        "🔴 End Call",
        type="secondary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Evaluating your conversation..."
            ):

                evaluation = (
                    evaluate_conversation(
                        st.session_state.conversation
                    )
                )


            st.session_state.evaluation = (
                evaluation
            )

            st.session_state.call_active = False

            st.session_state.session_count += 1

            st.rerun()


        except Exception as e:

            st.error(
                f"Evaluation failed: {e}"
            )


# =========================================================
# TRANSCRIPT
# =========================================================

if (
    st.session_state.conversation
    and not st.session_state.call_active
):

    st.divider()

    st.header(
        "💬 Conversation Transcript"
    )


    for message in st.session_state.conversation:

        if message["role"] == "assistant":

            st.markdown(
                f"""
                <div class="teacher-box">
                <strong>👩‍🏫 Teacher</strong><br><br>
                {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="student-box">
                <strong>🧑 You</strong><br><br>
                {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# EVALUATION
# =========================================================

if st.session_state.evaluation:

    evaluation = (
        st.session_state.evaluation
    )


    st.divider()

    st.header(
        "📊 Your Speaking Evaluation"
    )


    if "error" in evaluation:

        st.error(
            evaluation["error"]
        )

        st.code(
            evaluation.get(
                "raw",
                ""
            )
        )

        st.stop()


    # -----------------------------------------------------
    # Overall
    # -----------------------------------------------------

    overall = evaluation.get(
        "overall_score",
        0
    )


    st.metric(
        "Overall Score",
        f"{overall}/10"
    )


    # -----------------------------------------------------
    # Individual scores
    # -----------------------------------------------------

    cols = st.columns(3)


    scores = [

        (
            "Grammar",
            evaluation.get(
                "grammar",
                0
            )
        ),

        (
            "Vocabulary",
            evaluation.get(
                "vocabulary",
                0
            )
        ),

        (
            "Fluency",
            evaluation.get(
                "fluency",
                0
            )
        ),

        (
            "Sentence Formation",
            evaluation.get(
                "sentence_formation",
                0
            )
        ),

        (
            "Communication",
            evaluation.get(
                "communication",
                0
            )
        ),

        (
            "Confidence",
            evaluation.get(
                "confidence",
                0
            )
        )
    ]


    for index, (name, score) in enumerate(scores):

        with cols[index % 3]:

            st.metric(
                name,
                f"{score}/10"
            )


    # =====================================================
    # STRENGTHS
    # =====================================================

    st.subheader(
        "💪 Your strengths"
    )


    strengths = evaluation.get(
        "strengths",
        []
    )


    for strength in strengths:

        st.write(
            f"✅ {strength}"
        )


    # =====================================================
    # MISTAKES
    # =====================================================

    st.subheader(
        "✏️ Important corrections"
    )


    mistakes = evaluation.get(
        "mistakes",
        []
    )


    if not mistakes:

        st.success(
            "No major grammar mistakes detected."
        )


    for mistake in mistakes:

        st.error(
            f"You said: "
            f"**{mistake.get('said', '')}**"
        )


        st.success(
            f"Better: "
            f"**{mistake.get('correct', '')}**"
        )


        st.write(
            mistake.get(
                "explanation",
                ""
            )
        )


    # =====================================================
    # VOCABULARY
    # =====================================================

    st.subheader(
        "📚 Vocabulary improvements"
    )


    vocabulary = evaluation.get(
        "vocabulary_improvements",
        []
    )


    for item in vocabulary:

        st.write(
            f"**{item.get('simple_word', '')}** "
            f"→ "
            f"**{item.get('better_word', '')}**"
        )


        st.caption(
            item.get(
                "example",
                ""
            )
        )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    st.subheader(
        "🎯 Recommendations"
    )


    recommendations = evaluation.get(
        "recommendations",
        []
    )


    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )


    # =====================================================
    # NEXT SESSION
    # =====================================================

    st.subheader(
        "📌 Next session focus"
    )


    st.info(
        evaluation.get(
            "next_session_focus",
            "Continue practicing spoken English."
        )
    )


    # =====================================================
    # NEW CALL
    # =====================================================

    st.divider()


    if st.button(
        "📞 Start Another Session",
        type="primary",
        use_container_width=True
    ):

        st.session_state.conversation = []

        st.session_state.teacher_audio = None

        st.session_state.evaluation = None

        st.session_state.last_student_text = ""

        st.session_state.processed_audio_hash = None

        st.rerun()
