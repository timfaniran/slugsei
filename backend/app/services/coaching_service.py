import os
import google.generativeai as genai
from google.cloud import firestore
from ..config import firestore_client

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_coaching_feedback(video_id: str):

    doc_ref = firestore_client.collection("videos").document(video_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise ValueError(f"No video found for ID: {video_id}")

    data = doc.to_dict()
    analysis = data.get("analysis_results")

    if not analysis:
        raise ValueError(f"No analysis results available for video ID: {video_id}")

    launch_angle = analysis.get("launch_angle")
    exit_velocity = analysis.get("exit_velocity")

    if launch_angle is None or exit_velocity is None:
        raise ValueError(f"Incomplete analysis data for video ID: {video_id}")

    prompt = f"""
    You are a professional baseball coach specializing in advanced swing mechanics and player development.
    You will provide **scientific and resource-backed feedback** based on reference materials like **MLB guidelines, biomechanics research, and professional coaching techniques**.

    ### Player Analysis:
    - **Launch Angle**: {launch_angle}° (Recommended: 10°-30° for line drives & home runs)
    - **Exit Velocity**: {exit_velocity} mph (Higher is better for power hitters)

    ### Your Task:
    Provide detailed feedback on **how to improve** using references from **biomechanics studies, pro player case studies, and scientific analysis**.
    
    #### **Feedback Format:**
    - **Reference Real-Life Players:** Compare to MLB players with similar metrics.
    - **Use Scientific Data:** Base swing adjustments on **sports science & biomechanics.**
    - **Actionable Drills:** Recommend specific **batting stance drills, weight training, and swing path corrections.**
    - **Performance Metrics:** Suggest **trackable goals** (e.g., increasing launch angle by X degrees, exit velocity improvement benchmarks).

    #### **Example Resources to Reference:**
    - **"The Science of Hitting" by Ted Williams**
    - **Statcast Data from MLB for Ideal Launch Angles**
    - **Biomechanics Studies from Driveline Baseball**
    - **Case Study: How Aaron Judge & Shohei Ohtani optimize their swing path**

    Structure your feedback as if giving **professional coaching advice to a serious player looking to improve.** Keep it **concise, structured, and reference-backed**.
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return {
            "video_id": video_id,
            "feedback": response.text   
        }

    except Exception as e:
        fallback_feedback = f"**Coaching Feedback**\n\n"
        
        if launch_angle < 10:
            fallback_feedback += "- Your launch angle is too low. Adjust your bat angle and follow through to generate better loft.\n"
        elif launch_angle > 40:
            fallback_feedback += "- Your launch angle is too high, which may reduce your exit velocity. Focus on a controlled, flatter swing.\n"
        else:
            fallback_feedback += "- Your launch angle is within the optimal range. Keep working on consistency.\n"

        if exit_velocity < 50:
            fallback_feedback += "- Your exit velocity is low. Focus on improving your bat speed and lower-body drive for more power.\n"
        else:
            fallback_feedback += "- Your exit velocity is strong! Maintain good mechanics to ensure consistent results.\n"

        fallback_feedback += "\n- **Track your metrics using tools like Rapsodo or Statcast and work on incremental improvements.**\n"

        return {
            "video_id": video_id,
            "feedback": fallback_feedback
        }