import json

from groq_client import evaluate_with_groq


EVALUATION_PROMPT = """
You are an expert English speaking teacher.

Evaluate the student's English based on the complete
conversation below.

Evaluate:

1. Grammar
2. Vocabulary
3. Fluency
4. Sentence formation
5. Communication
6. Confidence

Score every category from 1 to 10.

Important:

Do NOT judge the teacher.

Only evaluate the student's English.

Do not penalize the student simply for using simple
sentences.

Identify meaningful mistakes rather than every tiny issue.

Return ONLY valid JSON using exactly this structure:

{
    "overall_score": 0,
    "grammar": 0,
    "vocabulary": 0,
    "fluency": 0,
    "sentence_formation": 0,
    "communication": 0,
    "confidence": 0,

    "strengths": [],

    "mistakes": [
        {
            "said": "",
            "correct": "",
            "explanation": ""
        }
    ],

    "vocabulary_improvements": [
        {
            "simple_word": "",
            "better_word": "",
            "example": ""
        }
    ],

    "recommendations": [],

    "next_session_focus": ""
}
"""


def evaluate_conversation(
    conversation
):

    transcript = ""


    for message in conversation:

        if message["role"] == "assistant":

            role = "Teacher"

        else:

            role = "Student"


        transcript += (
            f"{role}: "
            f"{message['content']}\n\n"
        )


    messages = [
        {
            "role": "system",
            "content": EVALUATION_PROMPT
        },
        {
            "role": "user",
            "content": (
                "Evaluate this conversation:\n\n"
                + transcript
            )
        }
    ]


    raw_result = evaluate_with_groq(
        messages
    )


    try:

        return json.loads(
            raw_result
        )

    except json.JSONDecodeError:

        return {
            "error": "Could not parse evaluation",
            "raw": raw_result
        }