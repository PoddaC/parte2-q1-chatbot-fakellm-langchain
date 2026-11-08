import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.fake import FakeListLLM

from app.services.chat_service import build_chain
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("Olá!", "Olá! Sou um chatbot"),
        ("Qual é o seu nome?", "FakeBot"),
        ("Qual o horário de atendimento?", "segunda a sexta"),
        ("Quanto é o preço?", "R$ 29,90"),
    ],
)
def test_predefined_answers(msg, expected):
    r = client.post("/chat", json={"message": msg})
    assert r.status_code == 200
    assert expected in r.json()["reply"]


def test_fallback():
    r = client.post("/chat", json={"message": "xyzzy"})
    assert "não entendi" in r.json()["reply"]


def test_deterministic():
    a = client.post("/chat", json={"message": "preço"}).json()["reply"]
    b = client.post("/chat", json={"message": "preço"}).json()["reply"]
    assert a == b


def test_empty_message_rejected():
    assert client.post("/chat", json={"message": ""}).status_code == 422


def test_chain_accepts_langchain_builtin_fake():
    chain = build_chain(FakeListLLM(responses=["resposta fixa"]))
    assert chain.invoke({"message": "qualquer"}) == "resposta fixa"
