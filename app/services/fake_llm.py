"""Fake LLM baseado em regras: responde a perguntas pré-definidas sem rede, sem custo e de forma determinística."""
from typing import Any, Dict, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

QUESTION_MARKER = "Pergunta do usuário:"
ANSWER_MARKER = "Resposta:"

DEFAULT_RULES: Dict[str, str] = {
    "olá": "Olá! Sou um chatbot de demonstração. Como posso ajudar?",
    "ola": "Olá! Sou um chatbot de demonstração. Como posso ajudar?",
    "seu nome": "Eu me chamo FakeBot e rodo sobre um Fake LLM do LangChain.",
    "horário": "Atendemos de segunda a sexta, das 9h às 18h.",
    "preço": "O plano básico custa R$ 29,90 por mês.",
    "ajuda": "Posso responder sobre horário, preço e sobre o meu nome.",
    "tchau": "Até logo! 👋",
}
FALLBACK = "Desculpe, não entendi. Tente perguntar sobre horário, preço ou digite 'ajuda'."


class RuleBasedFakeLLM(LLM):
    """Procura palavras-chave na pergunta do usuário e devolve a resposta pré-definida."""

    rules: Dict[str, str] = DEFAULT_RULES
    fallback: str = FALLBACK

    @property
    def _llm_type(self) -> str:
        return "rule-based-fake-llm"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        # Considera só o trecho da pergunta, ignorando instruções do template.
        question = prompt.split(QUESTION_MARKER)[-1].split(ANSWER_MARKER)[0].lower()
        for keyword, answer in self.rules.items():
            if keyword in question:
                return answer
        return self.fallback
