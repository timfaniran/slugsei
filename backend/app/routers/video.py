from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from ..config import get_videos_bucket, firestore_client, BUCKET_NAME
from uuid import uuid4
from google.cloud.firestore import SERVER_TIMESTAMP
from google.api_core.exceptions import GoogleAPICallError 
from ..services.analysis_service import analyze_video_background
import os

router = APIRouter()

ALLOWED_MIME_TYPES = {"video/mp4", "video/mov", "video/avi", "video/mkv", "application/octet-stream"}

@router.post("/upload")
async def upload_video(file: UploadFile = File(...), background_tasks: BackgroundTasks):
    print(f"Detected MIME type: {file.content_type}") 

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only videos are allowed.")

    actual_content_type = file.content_type
    if file.content_type == "application/octet-stream":
        actual_content_type = "video/mp4"  

    video_id = str(uuid4())
    extension = file.filename.split(".")[-1] if "." in file.filename else "mp4"  
    final_name = f"{video_id}.{extension}"

    try:
        bucket = get_videos_bucket()
        blob = bucket.blob(final_name)

        if (blob.exists()):
            raise HTTPException(status_code=409, detail="A video with this ID already exists.")

        file.file.seek(0)

        blob.upload_from_file(file.file, content_type=actual_content_type)

        # Firestore metadata
        doc_ref = firestore_client.collection("videos").document(video_id)
        doc_ref.set({
            "video_id": video_id,
            "file_name": final_name,
            "bucket": BUCKET_NAME,
            "uploaded_at": SERVER_TIMESTAMP
        })

        video_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{final_name}"

        # Locally
        local_video_path = f"temp_videos/{final_name}"
        os.makedirs("temp_videos", exist_ok=True)
        with open(local_video_path, "wb") as local_file:
            local_file.write(file.file.read())
 
        background_tasks.add_task(analyze_video_background, video_id)

        return {
            "video_id": video_id,
            "status": "processing",
            "video_url": video_url
        }

    except GoogleAPICallError as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")

@router.get("/video/{video_id}")
async def get_video(video_id: str):
    doc = firestore_client.collection("videos").document(video_id).get()
    if not doc.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    video_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{doc.get('file_name')}"
    return {
        "video_id": video_id,
        "file_name": doc.get("file_name"),
        "bucket": BUCKET_NAME,
        "uploaded_at": doc.get("uploaded_at"),
        "video_url": video_url 
    }

@router.get("/videos")
async def list_videos():
    docs = firestore_client.collection("videos").stream()
    videos = [{"video_id": doc.id, **doc.to_dict()} for doc in docs]
    
    if not videos:
        return {"message": "No videos found.", "videos": []}
    
    return {"videos": videos}
