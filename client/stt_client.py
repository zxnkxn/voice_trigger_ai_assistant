from io import BytesIO

import requests

from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")
SERVER_URL = client_config["SERVER_URL"]
REQUEST_TIMEOUT = client_config["REQUEST_TIMEOUT"]


def send_audio_to_stt(audio_bytes: bytes) -> dict:
    """
    Send audio bytes to the STT endpoint and return the response.

    Args:
        audio_bytes (bytes): Raw audio bytes

    Returns:
        dict: Response from the STT endpoint
    """
    try:
        # Send audio to server for STT processing
        files = {
            "audio": ("audio.ogg", BytesIO(audio_bytes), "audio/ogg"),
        }

        stt_response = requests.post(
            f"{SERVER_URL}/dialog/voice", files=files, timeout=REQUEST_TIMEOUT
        )

        if stt_response.status_code != 200:
            print("STT error:", stt_response.status_code, stt_response.text)
            return None

        return stt_response.json()

    except Exception as e:
        print("Error in STT request:", e)
        return None
