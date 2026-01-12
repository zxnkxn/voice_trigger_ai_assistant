import requests

from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")
SERVER_URL = client_config["SERVER_URL"]
REQUEST_TIMEOUT = client_config["REQUEST_TIMEOUT"]


def send_text_to_tts(assistant_text: str) -> dict:
    """
    Send assistant text to the TTS endpoint and return the response.

    Args:
        assistant_text (str): Text from the AI assistant

    Returns:
        dict: Response from the TTS endpoint
    """
    try:
        tts_data = {"text": assistant_text}

        tts_response = requests.post(
            f"{SERVER_URL}/dialog/speak", data=tts_data, timeout=REQUEST_TIMEOUT
        )

        if tts_response.status_code != 200:
            print("TTS error:", tts_response.status_code, tts_response.text)
            return None

        return tts_response.json()

    except Exception as e:
        print("Error in TTS request:", e)
        return None
