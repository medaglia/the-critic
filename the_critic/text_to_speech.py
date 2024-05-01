import os

from elevenlabs import play
from elevenlabs.client import ElevenLabs

ELEVENLABS_VOICE = "Michael"


class TextToSpeech:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

    def say(self, text: str) -> None:
        if not text:
            return

        print(f"Speaking: {text}")

        # Substitute periods with explamation marks
        text = text.replace(".", "!")

        audio = self.client.generate(
            text=text, voice=ELEVENLABS_VOICE, model="eleven_monolingual_v1"
        )
        play(audio)
