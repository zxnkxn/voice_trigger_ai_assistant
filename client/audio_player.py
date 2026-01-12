import base64
import subprocess


def play_audio(audio_base64: str) -> None:
    """
    Play audio from base64 encoded string.

    Args:
        audio_base64 (str): Base64 encoded audio data
    """
    try:
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)

            with open("response.ogg", "wb") as f:
                f.write(audio_bytes)

            subprocess.run(["ffplay", "-nodisp", "-autoexit", "response.ogg"])

    except Exception as e:
        print("Error playing audio:", e)
