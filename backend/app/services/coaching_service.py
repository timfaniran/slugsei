import os
from google.cloud import firestore
from ..config import firestore_client

def generate_coaching_feedback(video_id: str):
    # 1. Retrieve analysis from Firestore
    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError(f"No video found for ID: {video_id}")
    data = doc.to_dict()

    analysis = data.get("analysis_results")
    if not analysis:
        raise ValueError(f"No analysis results for video ID: {video_id}")

    # 2. Formulate prompt with analysis data
    prompt = f"""
    The user has a baseball swing video with the following analysis: {analysis}.
    Provide feedback focusing on angles and posture to improve batting form.
    Also, highlight any major issues or tips.
    """

    # 3. Call LLM
    response = f"This is a stubbed response interpreting {analysis}. (Replace with LLM API call)"

    return response
