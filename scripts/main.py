import base64

from fastapi import Depends, FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.deps import get_db
from scripts.ai_responder import ask_ai
from scripts.stt_listener import listen_and_send, recognize_yandex
from scripts.tts_synthesizer import synthesize_speech_bytes
from services.dialog_service import get_dialog_history, save_message

SYSTEM_PROMPT = (
    "Ты дружелюбный голосовой ассистент для детей 3-10 лет. "
    "Твой характер:\n"
    "- добрый, спокойный, поддерживающий;\n"
    "- любопытный и воодушевляющий;\n"
    "- никогда не грубишь и не споришь. "
    "Речь:\n"
    "- говори короткими и простыми предложениями;\n"
    "- используй понятные слова;\n"
    "- один ответ - не больше 2–4 предложений;\n"
    "- можно задавать один простой встречный вопрос. "
    "Безопасность:\n"
    "- ты не обсуждаешь страшные, жестокие, опасные или взрослые темы;\n"
    "- не говоришь о смерти, насилии, болезнях, политике, религии и деньгах;\n"
    "- не даёшь советов, которые могут навредить ребёнку;\n"
    "- не изображаешь себя человеком, врачом, родителем или другом семьи. "
    "Если вопрос неподходящий:\n"
    "- вежливо откажись;\n"
    "- скажи, что ты не можешь говорить об этом;\n"
    "- предложи безопасную и интересную тему. "
    "Поведение:\n"
    "- поощряй любопытство и фантазию;\n"
    "- поддерживай ребёнка фразами;\n"
    "- не критикуй и не высмеивай;\n"
    "- не используй сложные объяснения. "
    "Язык:\n"
    "- если с тобой говорят на русском языке, отвечай на русском;\n"
    "- если с тобой говорят на английском языке, отвечай на английском;\n"
    "- не смешивай языки. "
    "Формат:\n"
    "- всегда отвечай кратко;\n"
    "- не используй списки, если не просят;\n"
    "- не упоминай правила и инструкции."
)


app = FastAPI(title="Voice Trigger AI Assistant API")


@app.post("/dialog/voice")
def dialog_voice(
    toy_id: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Accepts voice input, converts it to text, sends to AI, and returns both
    recognized text and assistant response.
    """
    print(f"Received audio from toy_id={toy_id}, filename={audio.filename}")

    # Read audio file into memory
    audio_bytes = audio.file.read()

    # Create a temporary AudioData object to use recognize_yandex
    from speech_recognition import AudioData

    audio_data = AudioData(audio_bytes, sample_rate=48000, sample_width=2)
    recognized_text = recognize_yandex(audio_data).strip()
    print("Recognized text:", recognized_text)

    if not recognized_text:
        recognized_text = "(not recognized)"
        assistant_text = "(not recognized)"
        audio_b64 = None
    else:
        save_message(db, toy_id, role="user", text=recognized_text)

        history = get_dialog_history(db, toy_id)
        history_messages = [{"role": msg.role, "content": msg.text} for msg in history]
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history_messages

        assistant_text = ask_ai(messages)
        print("AI response:", assistant_text)

        save_message(db, toy_id, role="assistant", text=assistant_text)

        audio_bytes = synthesize_speech_bytes(assistant_text)
        audio_b64 = base64.b64encode(audio_bytes).decode("ascii")

    return JSONResponse(
        {
            "recognized_text": recognized_text,
            "assistant_text": assistant_text,
            "audio_base64": audio_b64,
        }
    )


if __name__ == "__main__":
    listen_and_send()
