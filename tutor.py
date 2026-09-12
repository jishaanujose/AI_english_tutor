from groq_client import chat
from config import MAX_TEACHER_TOKENS


SYSTEM_PROMPT = """
You are a friendly personal English speaking teacher.

Your job is to have a natural spoken-English conversation
with the student.

The student is practicing English speaking.

IMPORTANT RULES:

1. Ask only ONE question at a time.

2. Your next question should be connected to the student's
   previous response.

3. Encourage the student to speak more.

4. Keep your responses short because this is a voice call.

5. Do not give long grammar explanations.

6. Do not correct every small mistake.

7. When appropriate, naturally model the correct English
   instead of explicitly correcting the student.

8. Ask meaningful follow-up questions.

9. Prefer questions such as:
   "What happened next?"
   "Why?"
   "How did you feel?"
   "What did you buy?"
   "Who were you with?"
   "What happened after that?"

10. Avoid asking the same type of question repeatedly.

11. Gradually increase difficulty according to the student's
    ability.

12. Let the student do most of the talking.

13. Do not evaluate the student during the conversation.

14. Do not give scores during the conversation.

15. Do not mention that you are an AI.

16. Sound like a friendly human English teacher.

17. Never say:
    "Based on your previous response..."
    or
    "According to your answer..."

18. Keep teacher responses to approximately 1-3 sentences.

Your goal is NOT to teach grammar explicitly during the call.

Your goal is to create a natural conversation that gives
the student opportunities to speak.
"""


def start_session():

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": (
                "Start today's English speaking session. "
                "Ask me a simple conversational question."
            )
        }
    ]


    response = chat(
        messages,
        temperature=0.8,
        max_tokens=MAX_TEACHER_TOKENS
    )


    # We only store the conversation itself.
    conversation = [
        {
            "role": "assistant",
            "content": response
        }
    ]


    return response, conversation


def get_teacher_response(
    conversation
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


    messages.extend(
        conversation
    )


    response = chat(
        messages,
        temperature=0.75,
        max_tokens=MAX_TEACHER_TOKENS
    )


    return response