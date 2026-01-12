import openai

from config.config_loader import load_config

api_config = load_config("config/api_config.yml")
YANDEX_CLOUD_FOLDER = api_config["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = api_config["API_KEYS"]["AI"]

server_config = load_config("config/server_config.yml")
MAX_TOKENS = server_config["MAX_TOKENS"]
TEMPERATURE = server_config["TEMPERATURE"]
STREAM = server_config["STREAM"]

# Specify which model to use for the assistant
MODEL_NAME = "aliceai-llm/latest"  # Alice AI LLM

# YandexGPT 5 Pro - yandexgpt/latest
# YandexGPT 5.1 Pro - yandexgpt/rc
# Alice AI LLM - aliceai-llm/latest

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://llm.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER,
)


def ask_ai(conversation_history: list) -> str:
    """
    Sends user input and returns a short response.
    Conversation history is automatically trimmed.
    """

    # Send request
    response = client.chat.completions.create(
        model=f"gpt://{YANDEX_CLOUD_FOLDER}/{MODEL_NAME}",
        messages=conversation_history,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        stream=STREAM,
    )

    # Extract assistant reply
    assistant_message = response.choices[0].message.content

    return assistant_message
