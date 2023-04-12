from rich.console import Console
from rich.padding import Padding

from typer import prompt, confirm


system_message_request = "Setup (system message)"
user_message_request = "Prompt"


def system_message_prompt():
    return prompt(system_message_request, default="")


def user_message_prompt():
    return prompt(user_message_request, default="")


console = Console()

you_color = "green"
you_prompt = f"[{you_color}]Prompt:[/{you_color}]"

gpt_color = "cyan"
gpt_prompt = f"[{gpt_color}]Reply:[/{gpt_color}]"

indent = 2


def completion_output(completion, prompt):
    usage = completion.usage
    content = completion.choices[0].message.content

    console.print(Padding(you_prompt, (1, 0, 0, 0)))
    console.print(Padding(prompt, (0, 0, 1, indent)))

    console.print(gpt_prompt)
    console.print(Padding(content, (0, 0, 1, indent)))

    console.print(
        Padding(
            f"{usage.prompt_tokens}/{usage.completion_tokens}/{usage.total_tokens}",
            (1, 0),
        )
    )


save_chat_text = "Do you want to save this chat?"


def save_prompt() -> bool:
    return confirm(save_chat_text, default=True)
