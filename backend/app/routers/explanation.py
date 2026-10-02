"""Explanation router — POST /explanation/"""

from fastapi import APIRouter

from ..schemas import CodeRequest, ExplanationResponse
from ..services.code_assistant import enhanced_single_analysis

router = APIRouter()


@router.post(
    "/", response_model=ExplanationResponse, summary="Explain code in plain English"
)
async def explain(req: CodeRequest):
    return await enhanced_single_analysis(req.code, req.language, "explanation", req.analysis_mode)
