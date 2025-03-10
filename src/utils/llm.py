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
    if llm not in llms:
        raise ValueError(f"LLM not found for ID: {llm}")
    return llms[llm]
