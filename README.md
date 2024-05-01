# The Critic

Nowadays, generative AI can produce high-quality videos given basic text prompts. This means that in the near future, we will find ourselves overwhelmed with AI-generated videos and films. Given that our attention spans are already maxed out, it will be impossible to keep up with the influx of content. We're drinking from the firehose.

To address this issue, I have developed 'The Critic', an AI-powered application designed to both watch films and provide critique on your behalf. All you need to do is point your webcam at the screen and listen to the app's analysis of the movie's strengths and weaknesses. It seems only fitting to have AI analyze its own creations ;-)

## Installation

Use Python 3.12 and [Poetry](https://python-poetry.org/).

Create an .env file by copying the example env file:
```shell
cp example.env .env file
```

Sign up to [Elevenlabs](https://elevenlabs.io/) and [OpenAI](https://openai.com/) and add your API keys to the .env file.

Initialize
```shell
poetry init
```

Run
```shell
poetry run python -m the_critic.main
```
