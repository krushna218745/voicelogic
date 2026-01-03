from fastapi import FastAPI, UploadFile
import shutil

from buyer_engine import get_buyer_response
from speech_to_text import speech_to_text
from firebase_db import save_turn
from buyer_state import buyer_state

# ✅ STEP 1: Define app FIRST
app = FastAPI()

# ✅ STEP 2: Then use decorators
@app.post("/talk")
async def talk(audio: UploadFile):
    with open("input.wav", "wb") as f:
        shutil.copyfileobj(audio.file, f)

    user_text = speech_to_text("input.wav")
    buyer_text = get_buyer_response(user_text)

    save_turn("demo-session", user_text, buyer_text, buyer_state)

    return {
        "user_text": user_text,
        "buyer_text": buyer_text,
        "buyer_state": buyer_state
    }
