import tempfile
import cv2
import mediapipe as mp
from google.cloud import storage, firestore
from ..config import get_videos_bucket, firestore_client
from app.trackBall import track_baseball
from app.ballMotion import analyze_ball_motion
import threading
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

mp_pose = mp.solutions.pose


def analyze_video(video_id: str):
    try:
        # 1. Fetch video metadata from Firestore
        doc_ref = firestore_client.collection("videos").document(video_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise ValueError(f"No video found for ID: {video_id}")

        data = doc.to_dict()
        bucket_name = data.get("bucket")
        file_name = data.get("file_name")

        if not bucket_name or not file_name:
            raise ValueError(f"Invalid metadata for video ID: {video_id}")

        # 2. Download video to a temporary file
        bucket = get_videos_bucket(bucket_name)
        blob = bucket.blob(file_name)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            blob.download_to_filename(temp_video.name)
            local_video_path = temp_video.name

        # 3. Track baseball and analyze ball motion
        positions_file = track_baseball(local_video_path)

        if not positions_file:
            raise ValueError("Error processing video for ball tracking: No positions file generated.")

        # Read ball positions from the file
        ball_positions = []
        try:
            with open(positions_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        try:
                            x, y = float(parts[0]), float(parts[1])
                            ball_positions.append((x, y))
                        except ValueError:
                            print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            raise ValueError("Positions file not found after processing.")

        if not ball_positions:
            raise ValueError("No valid ball positions found in tracking output.")

        # 4. Analyze ball motion using the list of tuples
        launch_angle, exit_velocity = analyze_ball_motion(ball_positions)

        if launch_angle is None or exit_velocity is None:
            raise ValueError("Ball motion analysis failed.")

        analysis_results = {
            "launch_angle": launch_angle,
            "exit_velocity": exit_velocity
        }

        # 5. Save analysis results in Firestore
        doc_ref.update({"analysis_results": analysis_results, "status": "completed"})

        return analysis_results

    except Exception as e:
        doc_ref.update({"status": "failed"})
        raise ValueError(f"Error analyzing video: {str(e)}")
