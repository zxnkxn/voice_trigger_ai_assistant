from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")
WAKE_WORD = client_config["WAKE_WORD"]


def check_wake_word(text: str) -> bool:
    """
    Check if the given text starts with the wake word.

    Args:
        text (str): The text to check

    Returns:
        bool: True if text starts with wake word, False otherwise
    """
    if not text:
        return False

    return text.lower().startswith(WAKE_WORD.lower())
