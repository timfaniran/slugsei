from fastapi import APIRouter, UploadFile, File, HTTPException
from ..config import get_videos_bucket, firestore_client, BUCKET_NAME
from uuid import uuid4
from google.cloud.firestore import SERVER_TIMESTAMP
from google.api_core.exceptions import GoogleAPICallError
from be.trackBall import track_baseball
from be.ballMotion import analyze_ball_motion
import os
from ..services.analysis_service import analyze_video

router = APIRouter()

ALLOWED_MIME_TYPES = {"video/mp4", "video/mov", "video/avi", "video/mkv"}

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only videos are allowed.")

    # Generate unique filename
    video_id = str(uuid4())
    extension = file.filename.split(".")[-1] if "." in file.filename else "mp4"  # Default to .mp4
    final_name = f"{video_id}.{extension}"

    try:
        # Get the GCS bucket
        bucket = get_videos_bucket()
        blob = bucket.blob(final_name)

        # Prevent overwriting existing videos
        if blob.exists():
            raise HTTPException(status_code=409, detail="A video with this ID already exists.")

        # Reset file pointer (important)
        file.file.seek(0)

        # Upload file to GCS
        blob.upload_from_file(file.file, content_type=file.content_type)

        # Save metadata in Firestore
        doc_ref = firestore_client.collection("videos").document(video_id)
        doc_ref.set({
            "video_id": video_id,
            "file_name": final_name,
            "bucket": BUCKET_NAME,
            "uploaded_at": SERVER_TIMESTAMP
        })

        video_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{final_name}"

        # Save the video locally for processing
        local_video_path = f"temp_videos/{final_name}"
        os.makedirs("temp_videos", exist_ok=True)
        with open(local_video_path, "wb") as local_file:
            local_file.write(file.file.read())

        # Process the video to analyze it
        analysis_results = analyze_video(video_id)
        if not analysis_results:
            raise HTTPException(status_code=500, detail="Error processing video for analysis.")

        return {
            "video_id": video_id,
            "status": "processed",
            "video_url": video_url,
            "launch_angle": analysis_results["launch_angle"],
            "exit_velocity": analysis_results["exit_velocity"]
        }

    except GoogleAPICallError as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")

@router.get("/video/{video_id}")
async def get_video(video_id: str):
    doc = firestore_client.collection("videos").document(video_id).get()
    if not doc.exists:
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
