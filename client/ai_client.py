import requests

from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")
SERVER_URL = client_config["SERVER_URL"]
TOY_ID = client_config["TOY_ID"]
REQUEST_TIMEOUT = client_config["REQUEST_TIMEOUT"]


def send_text_to_ai(recognized_text: str) -> dict:
    """
    Send recognized text to the AI processing endpoint and return the response.

    Args:
        recognized_text (str): Text recognized from speech

    Returns:
        dict: Response from the AI processing endpoint
    """
    try:
        process_data = {"toy_id": TOY_ID, "text": recognized_text}

        ai_response = requests.post(
            f"{SERVER_URL}/dialog/process", data=process_data, timeout=REQUEST_TIMEOUT
        )

        if ai_response.status_code != 200:
            print("AI processing error:", ai_response.status_code, ai_response.text)
            return None

        return ai_response.json()

    except Exception as e:
        print("Error in AI request:", e)
        return None
