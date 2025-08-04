from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel
from chat.messages import Message


class BaseChatModel(ABC):
    @abstractmethod
    def invoke(
        self,
        messages: List[Message],
        response_format: Optional[BaseModel] = None,
    ):
        pass
