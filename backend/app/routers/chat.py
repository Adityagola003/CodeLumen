"""Chat router — POST /chat/"""

from fastapi import APIRouter

from ..schemas import ChatMessageRequest, ChatMessageResponse
from ..services.llm_analysis import LLMAnalysisError, llm_analysis_client

router = APIRouter()


@router.post(
    "/",
    response_model=ChatMessageResponse,
    summary="Chat with the configured LLM assistant about the code",
)
async def chat(req: ChatMessageRequest):
    if req.analysis_mode == "local" or not llm_analysis_client.enabled:
        return {
            "provider": "rule-based",
            "model": "codelumen-engine-v3",
            "mode": "rule-based",
            "reply": "LLM chat is not configured. Add LLM_API_KEY and LLM_BASE_URL to enable AI responses.",
        }

    try:
        reply = await llm_analysis_client.chat_reply(
            message=req.message,
            code=req.code,
            history=req.history,
            level=req.level,
        )
    except LLMAnalysisError as exc:
        return {
            "provider": llm_analysis_client.provider_name,
            "model": llm_analysis_client.model,
            "mode": "degraded",
            "reply": f"The LLM could not answer this request: {exc}",
        }

    return {
        "provider": llm_analysis_client.provider_name,
        "model": llm_analysis_client.model,
        "mode": "chat",
        "reply": reply,
    }