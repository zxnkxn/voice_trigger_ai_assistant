import requests

from scripts.config_loader import load_config

config = load_config()
API_KEY = config["API_KEYS"]["TTS"]
FOLDER_ID = config["YANDEX_CLOUD_FOLDER"]


def synthesize_speech_bytes(text: str) -> bytes:
    """
    Synthesize speech and return audio as bytes (ogg/opus).
    """
    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
    }
    data = {
        "text": text,
        "lang": "ru-RU",
        "voice": "jane",
        "folderId": FOLDER_ID,
        "format": "oggopus",
    }

    response = requests.post(url, headers=headers, data=data, stream=True)

    if response.status_code != 200:
        raise RuntimeError(f"TTS error {response.status_code}: {response.text}")

    return response.content
