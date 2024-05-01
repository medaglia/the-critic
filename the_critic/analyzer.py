import copy
import os
from typing import ClassVar

from openai import OpenAI

INITIAL_PARAMS = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "system",
            "content": (
                "Your are a 60-year-old man watching a movie with your grandchild."
                "You are cranky, ascerbic, and have a dry wit."
                "You hate this movie"
                "Keep your comments brief and 25 words or less."
            ),
        },
        {
            "role": "user",
            "content": [
                "These are frames from the movie. What do you think of it so far?",
            ],
        },
    ],
    "max_tokens": 60,
}

CONTENTS_LIMIT = 10


class Analyzer:
    client = None
    contents: ClassVar[list[str]] = []

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY", "OpenAI API key not set")
        )

    def store(self, content: str):
        self.contents.append(content)
        if len(self.contents) > CONTENTS_LIMIT:
            self.contents.pop(0)

    def build_params(self, base64Frames) -> dict:
        params = copy.deepcopy(INITIAL_PARAMS)

        prev_content = [
            {"role": "assistant", "content": content} for content in self.contents
        ]

        params["messages"] = (
            params["messages"][:1] + prev_content + params["messages"][1:]
        )

        params["messages"][-1]["content"].extend({"image": x} for x in base64Frames)
        return params

    def analyze(self, base64Frames) -> str:
        print("Analyzing frames...")
        params = self.build_params(base64Frames)
        result = self.client.chat.completions.create(**params)
        content: str = result.choices[0].message.content
        self.store(content)
        print(content)
        return content
