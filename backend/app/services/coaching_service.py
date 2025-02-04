import os
from google.cloud import firestore
from ..config import firestore_client

def generate_coaching_feedback(video_id: str):
    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    if not doc.exists():
        raise ValueError(f"No video found for ID: {video_id}")

    data = doc.to_dict()
    analysis = data.get("analysis_results")
    if not analysis:
        raise ValueError(f"No analysis results available for video ID: {video_id}")

    launch_angle = analysis["launch_angle"]
    exit_velocity = analysis["exit_velocity"]

    # Generate feedback based on thresholds
    if launch_angle < 10:
        feedback = "Your launch angle is too low. Try adjusting your swing to create a better upward trajectory."
    elif launch_angle > 40:
        feedback = "Your launch angle is too high, reducing exit velocity. Try a flatter swing."
    else:
        feedback = "Your launch angle is optimal. Keep working on consistency!"

    if exit_velocity < 50:
        feedback += " Also, focus on generating more power through your legs and core."

    return feedback
