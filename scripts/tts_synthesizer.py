import subprocess

import requests

from scripts.config_loader import load_config

# ------------------ Configuration ------------------

config = load_config()
API_KEY = config["API_KEYS"]["TTS"]
FOLDER_ID = config["YANDEX_CLOUD_FOLDER"]

OUTPUT_FILE = "speech.ogg"


# ------------------ Function to synthesize speech ------------------
def synthesize_speech(text):
    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
    }
    data = {
        "text": text,
        "lang": "ru-RU",
        "voice": "jane",  # Female voice
        "folderId": FOLDER_ID,
        "format": "oggopus",  # Compact streaming format
    }

    # Send request and write audio to file
    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError(
                f"Error synthesizing speech: code {resp.status_code}, message: {resp.text}"
            )
        with open(OUTPUT_FILE, "wb") as f:
            for chunk in resp.iter_content(chunk_size=None):
                f.write(chunk)
    print(f"Audio saved to {OUTPUT_FILE}")


# ------------------ Function to play audio ------------------
def play_audio():
    # Play audio using ffplay (part of ffmpeg)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", OUTPUT_FILE])


# Helper function for easier main.py integration
def synthesize_and_play(text):
    synthesize_speech(text)
    play_audio()


# Standalone test
if __name__ == "__main__":
    test_text = "Привет, как твои дела, дружок?"
    synthesize_and_play(test_text)
