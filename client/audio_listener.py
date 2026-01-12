import speech_recognition as sr

from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")

SILENCE_TIMEOUT = client_config["SILENCE_TIMEOUT"]
SAMPLE_RATE = client_config["SAMPLE_RATE"]
CONVERT_WIDTH = client_config["CONVERT_WIDTH"]


r = sr.Recognizer()
r.pause_threshold = SILENCE_TIMEOUT


def listen_for_speech():
    """
    Listen for speech and return the raw audio data.
    """
    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:
        r.adjust_for_ambient_noise(source)
        print("Listening... say something")

        try:
            audio = r.listen(source)
            # Convert audio to raw bytes directly
            raw_data = audio.get_raw_data(
                convert_rate=SAMPLE_RATE, convert_width=CONVERT_WIDTH
            )
            return raw_data
        except Exception as e:
            print("Error:", e)
            return None
