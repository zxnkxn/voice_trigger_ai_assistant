import requests
import speech_recognition as sr

from scripts.config_loader import load_config

# ------------------ Configuration ------------------

WAKE_WORD = "Маша"
SILENCE_TIMEOUT = 1.5

config = load_config()
YANDEX_API_KEY = config["API_KEYS"]["STT"]

YANDEX_STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

SAMPLE_RATE = 48000  # fixed sample rate for Yandex STT

# --------------------------------------------------

r = sr.Recognizer()
r.pause_threshold = SILENCE_TIMEOUT


def recognize_yandex(audio_data: sr.AudioData) -> str:
    """
    Send audio data to Yandex SpeechKit STT (Russian only) and return recognized text.
    """
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
    }

    params = {
        "lang": "ru-RU",
        "format": "lpcm",
        "sampleRateHertz": SAMPLE_RATE,
    }

    # Convert audio to the correct sample rate and width
    raw_data = audio_data.get_raw_data(convert_rate=SAMPLE_RATE, convert_width=2)

    response = requests.post(
        YANDEX_STT_URL,
        headers=headers,
        params=params,
        data=raw_data,
        timeout=10,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Yandex STT error {response.status_code}: {response.text}")

    result = response.json()
    return result.get("result", "")


def listen_for_wake_word(wake_word=WAKE_WORD):
    """
    Listen continuously and print recognized text if it starts with the wake word.
    """
    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:
        r.adjust_for_ambient_noise(source)
        print(f"Listening... say something starting with '{wake_word}'")

        while True:
            try:
                audio = r.listen(source)
                text = recognize_yandex(audio).strip()

                if not text:
                    print("No speech recognized")
                    continue

                if text.lower().startswith(wake_word.lower()):
                    yield (text)
                else:
                    print("Text does not start with wake word, ignoring")

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    for t in listen_for_wake_word():
        print("Recognized:", t)
