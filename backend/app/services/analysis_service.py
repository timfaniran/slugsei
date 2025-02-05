import tempfile
import cv2
import mediapipe as mp
from google.cloud import storage, firestore
from ..config import get_videos_bucket, firestore_client
from .advancedTracker import BaseballTracker
import threading
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

mp_pose = mp.solutions.pose

def analyze_video(video_id: str):
    try:
        doc_ref = firestore_client.collection("videos").document(video_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise ValueError(f"No video found for ID: {video_id}")

        data = doc.to_dict()
        bucket_name = data.get("bucket")
        file_name = data.get("file_name")

        if not bucket_name or not file_name:
            raise ValueError(f"Invalid metadata for video ID: {video_id}")

        bucket = get_videos_bucket(bucket_name)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            blob.download_to_filename(temp_video.name)
            local_video_path = temp_video.name

        # Track baseball and analyze ball motion using advancedTracker
        tracker = BaseballTracker(local_video_path)
        results, _ = tracker.track_baseball()
        launch_angle = results['launch_angle']
        exit_velocity = results['exit_velocity']
        if launch_angle is None or exit_velocity is None:
            raise ValueError("Error analyzing ball motion.")

        analysis_results = {
            "launch_angle": launch_angle,
            "exit_velocity": exit_velocity
        }

        doc_ref.update({"analysis_results": analysis_results, "status": "completed"})

        return analysis_results

    except Exception as e:
        doc_ref.update({"status": "failed"})
        raise ValueError(f"Error analyzing video: {str(e)}")

def analyze_video_background(video_id: str):
    thread = threading.Thread(target=analyze_video, args=(video_id,))
    thread.start()
    return thread

