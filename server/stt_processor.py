import requests

from config.config_loader import load_config

# Load API configuration
api_config = load_config("config/api_config.yml")
YANDEX_API_KEY = api_config["API_KEYS"]["STT"]

# Load server configuration for SAMPLE_RATE
server_config = load_config("config/server_config.yml")
SAMPLE_RATE = server_config["SAMPLE_RATE"]

YANDEX_STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"


def recognize_yandex(audio_bytes: bytes) -> str:
    """
    Send audio bytes to Yandex SpeechKit STT (Russian only) and return recognized text.
    This is a server-side version that works with raw audio bytes instead of AudioData objects.
    """
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
    }

    params = {
        "lang": "ru-RU",
        "format": "lpcm",
        "sampleRateHertz": SAMPLE_RATE,
    }

    response = requests.post(
        YANDEX_STT_URL,
        headers=headers,
        params=params,
        data=audio_bytes,
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Yandex STT error {response.status_code}: {response.text}")

    result = response.json()
    return result.get("result", "")
