from client.ai_client import send_text_to_ai
from client.audio_listener import listen_for_speech
from client.audio_player import play_audio
from client.stt_client import send_audio_to_stt
from client.tts_client import send_text_to_tts
from client.wake_word_checker import check_wake_word
from config.config_loader import load_config

# Load client configuration
client_config = load_config("config/client_config.yml")
WAKE_WORD = client_config["WAKE_WORD"]


def main():
    """
    Main function that coordinates the voice assistant workflow.
    """
    while True:
        # Listen for speech and get raw audio data
        audio_bytes = listen_for_speech()
        if audio_bytes is None:
            continue

        # Send audio to STT service
        stt_result = send_audio_to_stt(audio_bytes)
        if stt_result is None:
            continue

        recognized_text = stt_result["recognized_text"]
        print("Recognized:", recognized_text)

        if not recognized_text:
            print("No speech recognized")
            continue

        # Check for wake word
        if not check_wake_word(recognized_text):
            print("Text does not start with wake word, ignoring")
            continue

        # Process with AI
        ai_result = send_text_to_ai(recognized_text)
        if ai_result is None:
            continue

        assistant_text = ai_result["assistant_text"]
        print("Assistant:", assistant_text)

        if not assistant_text:
            print("No response from assistant")
            continue

        # Convert to speech
        tts_result = send_text_to_tts(assistant_text)
        if tts_result is None:
            continue

        # Play the response
        audio_base64 = tts_result["audio_base64"]
        if audio_base64:
            play_audio(audio_base64)
        else:
            print("No audio to play")


if __name__ == "__main__":
    main()
