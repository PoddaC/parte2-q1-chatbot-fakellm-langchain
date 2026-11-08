from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.services.fake_llm import ANSWER_MARKER, QUESTION_MARKER, RuleBasedFakeLLM

PROMPT = PromptTemplate.from_template(
    "Você é um assistente prestativo.\n" + QUESTION_MARKER + " {message}\n" + ANSWER_MARKER
)


def build_chain(llm=None):
    """prompt -> LLM -> parser. Trocar o Fake LLM por um LLM real não altera o resto da aplicação."""
    return PROMPT | (llm or RuleBasedFakeLLM()) | StrOutputParser()


@lru_cache(maxsize=1)
def get_chain():
    return build_chain()
