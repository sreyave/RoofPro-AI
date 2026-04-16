from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_input, context=None):

    try:
        # ======================
        # 🧠 SAFE FALLBACK
        # ======================
        if not context:
            return (
                "I'm not completely sure about that 🤔\n\n"
                "But I can help you with:\n\n"
                "🏠 1 · Our Services\n"
                "🚨 2 · Emergency Repair Guide\n"
                "📐 3 · Get a Roof Estimate\n"
                "👤 4 · Contact a Human\n\n"
                "Please choose an option 😊"
            )

        # ======================
        # 🤖 NORMAL AI CALL (NO STREAM)
        # ======================
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful and professional roofing assistant.\n\n"
                        "Use ONLY the provided context.\n"
                        "Do not guess.\n"
                        "Keep answers short and clear.\n"
                    )
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {user_input}"
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return "Sorry, something went wrong. Please try again."
