from pydantic import BaseModel


class ViewConfig(BaseModel):
    you_color: str = "green"
    assistant_color: str = "cyan"
    system_message_label: str = "System"
    user_message_label: str = "User"
    assistant_message_lable: str = "Assistant"
    indent: int = 2
    save_chat_text: str = "Do you want to save this chat?"


class ChatConfig(BaseModel):
    model: str = "gpt-3.5-turbo"
    temperature: float = 1
    top_p: float = 1
    view: ViewConfig = ViewConfig()
