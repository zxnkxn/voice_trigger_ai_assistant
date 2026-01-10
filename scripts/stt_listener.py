import base64
import subprocess
from io import BytesIO

import requests
import speech_recognition as sr

from scripts.config_loader import load_config

# ------------------ Configuration ------------------

WAKE_WORD = "Маша"
SILENCE_TIMEOUT = 1.5

config = load_config()
YANDEX_API_KEY = config["API_KEYS"]["STT"]

YANDEX_STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

SAMPLE_RATE = 48000

# FastAPI server URL
SERVER_URL = "http://127.0.0.1:8000/dialog/voice"

TOY_ID = "test-toy-001"

# --------------------------------------------------

r = sr.Recognizer()
r.pause_threshold = SILENCE_TIMEOUT


def recognize_yandex(audio_data: sr.AudioData) -> str:
    """
    Send audio data to Yandex SpeechKit STT (Russian only) and return recognized text.
    """
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
    }

    params = {
        "lang": "ru-RU",
        "format": "lpcm",
        "sampleRateHertz": SAMPLE_RATE,
    }

    # Convert audio to the correct sample rate and width
    raw_data = audio_data.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)

    response = requests.post(
        YANDEX_STT_URL,
        headers=headers,
        params=params,
        data=raw_data,
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Yandex STT error {response.status_code}: {response.text}")

    result = response.json()
    return result.get("result", "")


def send_audio_to_server(audio_bytes: bytes, toy_id: str):
    """
    Send audio file to FastAPI /dialog/voice endpoint as multipart/form-data.
    """
    files = {
        "audio": ("audio.ogg", BytesIO(audio_bytes), "audio/ogg"),
    }
    data = {"toy_id": toy_id}

    try:
        response = requests.post(SERVER_URL, data=data, files=files, timeout=15)
        if response.status_code == 200:
            result = response.json()

            print("Recognized:", result["recognized_text"])
            print("Assistant:", result["assistant_text"])

            audio_bytes = base64.b64decode(result["audio_base64"])

            with open("response.ogg", "wb") as f:
                f.write(audio_bytes)

            subprocess.run(["ffplay", "-nodisp", "-autoexit", "response.ogg"])
        else:
            print("Server error:", response.status_code, response.text)
    except Exception as e:
        print("Error sending audio to server:", e)


def listen_and_send(wake_word=WAKE_WORD):
    """
    Listen continuously. If recognized phrase starts with wake_word, send it to the server.
    """
    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:
        r.adjust_for_ambient_noise(source)
        print(f"Listening... say something starting with '{wake_word}'")

        while True:
            try:
                audio = r.listen(source)
                text = recognize_yandex(audio).strip()

                if not text:
                    print("No speech recognized")
                    continue

                if text.lower().startswith(wake_word.lower()):
                    print(f"Wake word detected: {text}")
                    audio_bytes = audio.get_raw_data(
                        convert_rate=SAMPLE_RATE, convert_width=2
                    )
                    send_audio_to_server(audio_bytes, TOY_ID)
                else:
                    print("Text does not start with wake word, ignoring")

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    listen_and_send()
