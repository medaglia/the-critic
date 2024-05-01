from .analyzer import Analyzer
from .capture import Capturer
from .text_to_speech import TextToSpeech

if __name__ == "__main__":
    analyzer = Analyzer()
    text_to_speech = TextToSpeech()
    capturer = Capturer(analyzer, text_to_speech, options={"write_image": True})
    capturer.capture()
