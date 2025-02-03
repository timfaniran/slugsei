# app/services/analysis_service.py
import tempfile
import cv2
import mediapipe as mp
from google.cloud import storage, firestore
from ..config import get_videos_bucket, firestore_client

mp_pose = mp.solutions.pose

def analyze_video(video_id: str):
    # 1. Fetch video metadata from Firestore
    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError(f"No video found for ID: {video_id}")

    data = doc.to_dict()
    bucket_name = data["bucket"]
    file_name = data["file_name"]

    # 2. Download video to a temp file
    bucket = get_videos_bucket(bucket_name)
    blob = bucket.blob(file_name)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
        blob.download_to_filename(temp_video.name)
        local_video_path = temp_video.name

    # 3. Extract pose and compute metrics
    analysis_results = run_pose_estimation(local_video_path)

    # 4. Save analysis results in Firestore
    doc_ref.update({"analysis_results": analysis_results})

    return analysis_results


def run_pose_estimation(video_path: str):
    pose = mp_pose.Pose(static_image_mode=False, 
                        model_complexity=2,
                        enable_segmentation=False,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(video_path)
    results = []
    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Optionally downsample for speed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_result = pose.process(frame_rgb)

        if pose_result.pose_landmarks:
            # Example: track joint angles, etc.
            landmarks = pose_result.pose_landmarks.landmark
            # Calculate metrics (e.g., angles, velocity, etc.)
            # For MVP, we might store just a few key points
            # ...
            results.append({
                "frame": frame_count,
                "landmarks": [ { "x": lm.x, "y": lm.y, "z": lm.z } for lm in landmarks ]
            })

        frame_count += 1

    cap.release()
    pose.close()

    # A placeholder summary: perhaps average angles or velocity
    summary_metrics = {"frame_count": frame_count, "key_frames_analyzed": len(results)}
    return summary_metrics
