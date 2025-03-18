from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

load_dotenv()

GPT_4O_MINI = "gpt-4o-mini"
GPT_4O = "gpt-4o"


llms = {
    GPT_4O_MINI: ChatOpenAI(model_name="gpt-4o-mini", temperature=0),
    GPT_4O: ChatOpenAI(model_name="gpt-4o", temperature=0, top_p=0),
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
        raise ValueError(f"LLM not found for ID: {llm}")
    return llms[llm].model_copy()
