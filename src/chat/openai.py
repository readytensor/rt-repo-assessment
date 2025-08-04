from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List
from chat.base import BaseChatModel
from chat.messages import Message, HumanMessage


load_dotenv()


class ChatOpenAI(OpenAI, BaseChatModel):
    def __init__(self, model: str, temperature: float = 0):
        super().__init__()
        self.model = model
        self.temperature = temperature

    def invoke(
        self,
        message: Optional[str] = None,
        messages: List[Message] = None,
        response_format: Optional[BaseModel] = None,
    ):
        if message is not None and messages is not None:
            raise ValueError("Cannot provide both message and messages")
        elif message is not None:
            messages = [HumanMessage(message)]
        elif messages is None:
            raise ValueError("Must provide either message or messages")

        messages_dicts = [message.to_dict() for message in messages]
        if response_format:
            return (
                super()
                .chat.completions.parse(
                    model=self.model,
                    messages=messages_dicts,
                    response_format=response_format,
                    temperature=self.temperature,
                )
                .choices[0]
                .message.parsed
            )
        else:
            return (
                super()
                .chat.completions.create(
                    model=self.model,
                    messages=messages_dicts,
                    temperature=self.temperature,
                )
                .choices[0]
                .message.content
            )
