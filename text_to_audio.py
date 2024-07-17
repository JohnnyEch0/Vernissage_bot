from openai import audio
from pathlib import Path


def main(response, voice, counter):
    """
    This function streams the response to an audio file
    """
    AUDIO_STREAMING_PATH = Path(__file__).parent / f"data/speech{counter}.mp3"
    response_audio = audio.speech.create(
            model="tts-1-hd",
            voice= voice,
            input=f"{response}",
            )
    response_audio.stream_to_file(AUDIO_STREAMING_PATH)

if __name__ == "__main__":
    introduction = "Welcome to our exhibition by John Dustem. I am now handing the panel talk over to Melina and Steven, both experts in their own right and shining examples of the art scenes bright future."
    main(introduction, "shimmer", 10)