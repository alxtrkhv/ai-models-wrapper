from ..config import read_config
from ..openai.api import get_api


def single_completion(prompt: str):
    api = get_api()

    if api is None:
        return

    config = read_config().chat

    completion = api.ChatCompletion.create(
        n=1,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return completion
