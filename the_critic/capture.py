import base64
import typing
from pathlib import Path
from time import time

import cv2
from cv2 import VideoCapture

from .analyzer import Analyzer
from .text_to_speech import TextToSpeech

QUIT_KEY = "q"
FRAME_WIDTH = 206  # Images will be resized to this width
CLIP_LENGTH = 5  # Number of frames to analyze at a time
FPS = 1  # frames to capture per second
VIDEO_READ_ERROR = "Unsuccessful video read"
WEBCAM_ERROR = "Cannot open webcam"
IMAGE_DIR = "images"


class CaptureException(Exception):
    def __init__(self, message):
        super().__init__(message)


def resize_frame(frame):
    width: int = frame.shape[1]
    height: int = frame.shape[0]

    if width <= FRAME_WIDTH:
        return frame

    ratio = FRAME_WIDTH / width
    new_height = int(height * ratio)
    return cv2.resize(frame, (FRAME_WIDTH, new_height), interpolation=cv2.INTER_AREA)


class CaptureOptions(typing.TypedDict):
    write_image: bool


class Capturer:
    options: typing.ClassVar[CaptureOptions] = {
        "write_image": False,
    }

    def __init__(
        self,
        analyzer: Analyzer,
        text_to_speech: TextToSpeech,
        options: CaptureOptions,
    ):
        self.analyzer = analyzer
        self.text_to_speech = text_to_speech
        self.options = dict(self.options, **options)
        self.storedFrames = []

    def capture(self):
        """Capture frames from the webcam."""

        next_capture_at: float = 0

        video: VideoCapture = cv2.VideoCapture(0)

        if not video.isOpened():
            raise OSError(WEBCAM_ERROR)

        print(f"Capturing frames. Hit '{QUIT_KEY}' to quit...")

        frame_no = 0

        while video.isOpened():

            # Hitting the quit key breaks the loop
            if cv2.pollKey() & 0xFF == ord(QUIT_KEY):
                print("Quitting via key press")
                break

            if time() * 1000 < next_capture_at:
                continue

            next_capture_at = time() * 1000 + 1000 / FPS

            try:
                frame = self.get_frame(video)
            except CaptureException as e:
                print(e)
                break

            # Skip the first frame as it's usually dark
            if frame_no > 0:
                self.process_frame(frame_no, frame)

            frame_no += 1

        video.release()

    def process_frame(self, frame_no: int, frame):

        self.storedFrames.append(frame)
        print(f"Added frame {frame_no}")

        if self.options["write_image"]:
            self.write_image(frame, frame_no)

        # Analyze the clip once it reaches the desired length
        if len(self.storedFrames) == CLIP_LENGTH:

            # Convert the frames to base64
            base64Frames = []

            for frame in self.storedFrames:
                _, buffer = cv2.imencode(".jpg", frame)
                base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

            content = self.analyzer.analyze(base64Frames)
            self.text_to_speech.say(content)
            self.storedFrames = []

    def get_frame(self, video):
        """Capture a frame from the webcam and return it."""
        success, frame = video.read()

        # Display the frame
        cv2.imshow("frame", frame)

        if not success:
            raise CaptureException(VIDEO_READ_ERROR)

        return resize_frame(frame)

    def write_image(self, frame, frame_no):
        image_path = Path(".") / IMAGE_DIR / f"test{frame_no:03d}.png"
        cv2.imwrite(str(image_path), frame)
