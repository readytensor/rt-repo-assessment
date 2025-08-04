class Document:
    def __init__(self, content: str, metadata: dict = {}):
        self.content = content
        self.metadata = metadata

    def __str__(self):
        return self.content
