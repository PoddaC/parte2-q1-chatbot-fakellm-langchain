from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_chain

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, chain=Depends(get_chain)) -> ChatResponse:
    reply = await chain.ainvoke({"message": req.message})
    return ChatResponse(message=req.message, reply=reply)
