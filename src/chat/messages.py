class Message:
    def __init__(self, content: str, role: str):
        self.content = content
        self.role = role

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class SystemMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "system")


class HumanMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "user")


class AIMessage(Message):
    def __init__(self, content: str):
        super().__init__(content, "assistant")
