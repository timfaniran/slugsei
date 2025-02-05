from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.analysis_service import analyze_video, analyze_video_background
from google.cloud import firestore

firestore_client = firestore.Client()

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
    

@router.get("/{video_id}")
def get_analysis(video_id: str):
    """Fetch analysis results."""
    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Video not found")

    data = doc.to_dict()
    analysis = data.get("analysis_results")

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not available yet")

    return {
        "video_id": video_id,
        "status": data.get("status", "unknown"),
        "analysis": analysis
    } 
