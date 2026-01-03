from fastapi import FastAPI, UploadFile
import shutil
import uuid

from app.speech_to_text import speech_to_text
from app.buyer_engine import get_buyer_response
from app.firebase_db import save_turn
from app.buyer_state import buyer_state

app = FastAPI()

@app.post("/talk")
async def talk(audio: UploadFile):
    session_id = str(uuid.uuid4())

    with open("input.wav", "wb") as f:
        shutil.copyfileobj(audio.file, f)

    user_text = speech_to_text("input.wav")
    buyer_text = get_buyer_response(user_text)

    save_turn(session_id, user_text, buyer_text, buyer_state)

    return {
        "user_text": user_text,
        "buyer_text": buyer_text,
        "buyer_state": buyer_state
    }
