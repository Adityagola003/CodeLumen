"""Suggestions router — POST /suggestions/"""

from fastapi import APIRouter

from ..schemas import CodeRequest, SuggestionsResponse
from ..services.code_assistant import enhanced_single_analysis

router = APIRouter()


@router.post(
    "/", response_model=SuggestionsResponse, summary="Get improvement suggestions"
)
async def suggest(req: CodeRequest):
    return await enhanced_single_analysis(req.code, req.language, "suggestions", req.analysis_mode)
