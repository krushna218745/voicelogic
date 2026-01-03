import random
import os
import google.generativeai as genai
from app.buyer_state import buyer_state

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def update_state(user_text: str):
    text = user_text.lower()

    if any(word in text for word in ["maybe", "uh", "umm", "not sure"]):
        buyer_state["trust"] -= 10

    if len(text.split()) > 40:
        buyer_state["patience"] -= 10

    buyer_state["trust"] += random.randint(-5, 5)
    buyer_state["patience"] += random.randint(-5, 5)

    buyer_state["trust"] = max(0, min(100, buyer_state["trust"]))
    buyer_state["patience"] = max(0, min(100, buyer_state["patience"]))

def get_buyer_response(user_text: str) -> str:
    update_state(user_text)

    prompt = f"""
You are a real human buyer in a sales conversation.

Internal state (do NOT reveal):
- Trust: {buyer_state['trust']}
- Patience: {buyer_state['patience']}
- Emotion: {buyer_state['emotion']}

Rules:
- If patience is low, interrupt or be short
- If trust is low, challenge claims
- Behave naturally and unpredictably

Respond as the buyer.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()
