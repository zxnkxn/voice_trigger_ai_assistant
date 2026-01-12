import base64
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, File, Form, UploadFile
from sqlalchemy.orm import Session

from config.config_loader import load_config
from server.ai_responder import ask_ai
from server.db.deps import get_db
from server.db.dialog_manager import get_dialog_history, save_message
from server.stt_processor import recognize_yandex
from server.tts_synthesizer import synthesize_speech_bytes

# Load system prompt from config
system_config = load_config("config/system_prompt_config.yml")
SYSTEM_PROMPT = system_config["SYSTEM_PROMPT"]

app = FastAPI(title="Voice Trigger AI Assistant API")


@app.post("/dialog/voice")
def stt_process(
    audio: UploadFile = File(...),
) -> Dict[str, Any]:
    """
    Stage 1: Speech-to-Text processing.
    Accepts voice input and converts it to text.
    """
    print(f"Received audio, filename={audio.filename}")

    # Read audio file into memory
    audio_bytes = audio.file.read()

    # Recognize text from audio bytes
    recognized_text = recognize_yandex(audio_bytes).strip()
    print("Recognized text:", recognized_text)

    if not recognized_text:
        recognized_text = None

    return {"recognized_text": recognized_text}


@app.post("/dialog/process")
def ai_process(
    toy_id: str = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Stage 2: AI processing.
    Takes recognized text and generates AI response.
    """
    print(f"Processing text from toy_id={toy_id}: {text}")

    # Save user message
    save_message(db, toy_id, role="user", text=text)

    # Get conversation history
    history = get_dialog_history(db, toy_id)
    history_messages = [{"role": msg.role, "content": msg.text} for msg in history]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history_messages

    # Get AI response
    assistant_text = ask_ai(messages)
    print("AI response:", assistant_text)

    # Save assistant message
    save_message(db, toy_id, role="assistant", text=assistant_text)

    return {"assistant_text": assistant_text}


@app.post("/dialog/speak")
def tts_process(
    text: Optional[str] = Form(None),
) -> Dict[str, Any]:
    """
    Stage 3: Text-to-Speech processing.
    Takes AI response text and converts it to audio.
    """
    print(f"Generating speech: {text}")

    if not text:
        audio_b64 = None
    else:
        # Synthesize speech
        audio_bytes = synthesize_speech_bytes(text)
        audio_b64 = base64.b64encode(audio_bytes).decode("ascii")

    return {"audio_base64": audio_b64}
