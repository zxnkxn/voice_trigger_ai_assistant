import openai

from scripts.config_loader import load_config

# =========================
# Configuration
# =========================

config = load_config()
YANDEX_CLOUD_FOLDER = config["YANDEX_CLOUD_FOLDER"]
YANDEX_CLOUD_API_KEY = config["API_KEYS"]["AI"]

# Maximum number of messages to keep in conversation history
MAX_HISTORY_MESSAGES = 8

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
# System prompt
# =========================

SYSTEM_PROMPT = (
    "Ты дружелюбный голосовой ассистент для детей. "
    "Ты говоришь короткими, простыми и доброжелательными предложениями. "
    "Ты не обсуждаешь запрещённые, страшные, жестокие или взрослые темы. "
    "Если вопрос неподходящий, ты вежливо отказываешься и предлагаешь безопасную тему. "
    "Если с тобой говорят на русском языке, ты отвечаешь на русском языке. "
    "Если с тобой говорят на английском языке, ты отвечаешь на английском языке. "
    "Всегда отвечай кратко."
)

# =========================
# Conversation history
# =========================

# This list will store the dialogue context
conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# =========================
# Main function
# =========================


def ask_ai(user_text: str) -> str:
    """
    Sends user input and returns a short response.
    Conversation history is automatically trimmed.
    """

    global conversation_history

    # Add user message to history
    conversation_history.append({"role": "user", "content": user_text})

    # Trim history to keep only the last N messages (+ system prompt)
    if len(conversation_history) > MAX_HISTORY_MESSAGES + 1:
        conversation_history = [conversation_history[0]] + conversation_history[
            -MAX_HISTORY_MESSAGES:
        ]

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

    # Add assistant reply to history
    conversation_history.append({"role": "assistant", "content": assistant_message})

    return assistant_message


# =========================
# Entry point (for testing)
# =========================

if __name__ == "__main__":
    # Hardcoded prompt for debugging
    test_prompt = "Маша, расскажи короткую сказку про доброго кота"

    answer = ask_ai(test_prompt)

    print("Assistant response:")
    print(answer)
