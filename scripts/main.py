import sys

from scripts.ai_responder import ask_ai
from scripts.stt_listener import listen_for_wake_word
from scripts.tts_synthesizer import synthesize_and_play


def main():
    print("Assistant started. Listening for wake word...")
    try:
        # Listen continuously for wake word
        for recognized_text in listen_for_wake_word():
            if recognized_text:
                print("Recognized:", recognized_text)

                # Get AI response
                ai_response = ask_ai(recognized_text)
                print("AI response:", ai_response)

                # Synthesize AI response to speech
                synthesize_and_play(ai_response)

    except KeyboardInterrupt:
        print("\nAssistant stopped by user")
        sys.exit(0)
    except Exception as e:
        print("Error in main loop:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
