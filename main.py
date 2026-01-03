@app.post("/talk")
async def talk(audio: UploadFile):
    # STT
    user_text = speech_to_text("input.wav")

    # AI
    buyer_text = get_buyer_response(user_text)

    # Save
    save_turn("demo-session", user_text, buyer_text, buyer_state)

    return {
        "user_text": user_text,
        "buyer_text": buyer_text,
        "buyer_state": buyer_state
    }
