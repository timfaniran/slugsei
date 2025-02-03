# app/routers/analysis.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.analysis_service import analyze_video

router = APIRouter()

class AnalysisRequest(BaseModel):
    video_id: str

@router.post("/process")
def process_video(request: AnalysisRequest):
    try:
        result = analyze_video(request.video_id)
        return {"video_id": request.video_id, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
