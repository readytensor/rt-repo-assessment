from dotenv import load_dotenv
from chat.openai import ChatOpenAI
from chat.base import BaseChatModel

load_dotenv()

GPT_4O_MINI = ChatOpenAI(model="gpt-4o-mini", temperature=0)
GPT_4O = ChatOpenAI(model="gpt-4o", temperature=0)
GPT_4_1_MINI = ChatOpenAI(model="gpt-4.1-mini", temperature=0)


llms = {
    "gpt-4o-mini": GPT_4O_MINI,
    "gpt-4o": GPT_4O,
    "gpt-4.1-mini": GPT_4_1_MINI,
}


def get_llm(llm: str) -> BaseChatModel:
    """
    Retrieves a language model instance based on the provided identifier.

    Args:
        llm (str): The identifier for the language model to retrieve.
            Should be one of the keys in the `llms` dictionary.

    Returns:
        BaseChatModel: A copy of the requested language model instance.

    Raises:
        ValueError: If the provided identifier is not found in the `llms` dictionary.
    """
    if llm not in llms:
        raise ValueError(f"Invalid model: {llm}. Available models: {llms.keys()}")
    return llms[llm]
