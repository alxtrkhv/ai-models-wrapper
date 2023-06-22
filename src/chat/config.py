from pydantic import BaseModel


class ViewConfig(BaseModel):
    you_color: str = "green"
    assistant_color: str = "cyan"
    system_message_label: str = "System"
    user_message_label: str = "User"
    assistant_message_lable: str = "Assistant"
    indent: int = 2
    save_chat_text: str = "Do you want to save this chat?"
    completion_spinner_text = "Waiting for response"


class ChatConfig(BaseModel):
    model: str = "gpt-3.5-turbo-16k-0613"
    view: ViewConfig = ViewConfig()
