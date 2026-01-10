import openai

from scripts.config_loader import load_config

# =========================
# Configuration
# =========================

config = load_config()
YANDEX_CLOUD_FOLDER = config["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = config["API_KEYS"]["AI"]

# Specify which model to use for the assistant
MODEL_NAME = "aliceai-llm/latest"  # Alice AI LLM

# YandexGPT 5 Pro - yandexgpt/latest
# YandexGPT 5.1 Pro - yandexgpt/rc
# Alice AI LLM - aliceai-llm/latest

# =========================
# OpenAI-compatible client
# =========================

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://llm.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER,
)

# =========================
# Main function
# =========================


def ask_ai(conversation_history: list) -> str:
    """
    Sends user input and returns a short response.
    Conversation history is automatically trimmed.
    """

    # Send request
    response = client.chat.completions.create(
        model=f"gpt://{YANDEX_CLOUD_FOLDER}/{MODEL_NAME}",
        messages=conversation_history,
        max_tokens=150,
        temperature=0.6,
        stream=False,
    )

    # Extract assistant reply
    assistant_message = response.choices[0].message.content

    return assistant_message
