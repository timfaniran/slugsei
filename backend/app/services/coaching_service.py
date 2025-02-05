import os
import google.generativeai as genai
from google.cloud import firestore
from ..config import firestore_client

def generate_coaching_feedback(video_id: str):
    """
    Generates AI-powered coaching feedback based on video analysis.
    If Gemini API fails, fallback to a hardcoded feedback mechanism.
    """

    # Fetch analysis results from Firestore
    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise ValueError(f"No video found for ID: {video_id}")

    data = doc.to_dict()
    analysis = data.get("analysis_results")

    if not analysis:
        raise ValueError(f"No analysis results available for video ID: {video_id}")

    # Extract launch angle and exit velocity
    launch_angle = analysis.get("launch_angle")
    exit_velocity = analysis.get("exit_velocity")

    if launch_angle is None or exit_velocity is None:
        raise ValueError(f"Incomplete analysis data for video ID: {video_id}")

    # Create prompt for AI feedback with direct user display context
    prompt = f"""
    You are providing direct baseball coaching feedback for a player.
    Your response will be shown directly to the user, so structure it in a clear and engaging way.
    
    Based on these statistics:
    - **Launch Angle**: {launch_angle} degrees
    - **Exit Velocity**: {exit_velocity} mph

    Provide **detailed feedback**, including:
    - **Launch Angle Analysis**
    - **Exit Velocity Analysis**
    - **Swing Mechanics Adjustments**
    - **Stance Corrections**
    - **Strength Training Recommendations**
    - **Additional Tips**

    Format the response using **bullet points** for readability.
    """

    try:
        # Send request to Gemini API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return {
            "video_id": video_id,
            "feedback": response.text  # Directly show response to user
        }

    except Exception as e:
        # Fallback Hardcoded Feedback in Case of Gemini API Failure
        fallback_feedback = f"**Coaching Feedback**\n\n"
        
        if launch_angle < 10:
            fallback_feedback += "- Your launch angle is too low. Adjust your swing to generate better loft and trajectory.\n"
        elif launch_angle > 40:
            fallback_feedback += "- Your launch angle is too high, which may reduce your exit velocity. Try a more controlled, flatter swing.\n"
        else:
            fallback_feedback += "- Your launch angle is within the optimal range. Keep working on maintaining consistency.\n"

        if exit_velocity < 50:
            fallback_feedback += "- Your exit velocity is low. Focus on improving your leg drive and bat speed to generate more power.\n"
        else:
            fallback_feedback += "- Your exit velocity is strong! Maintain good mechanics to ensure consistent results.\n"

        fallback_feedback += "\n- **Practice regularly and seek feedback from coaches to fine-tune your mechanics.**\n"
        
        return {
            "video_id": video_id,
            "feedback": fallback_feedback
        }