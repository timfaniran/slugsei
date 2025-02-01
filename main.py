import os
import cv2
import mediapipe as mp
import pandas as pd
import glob
import urllib.request

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

# Folder paths
dataset_folder = "datasets"
video_save_folder = os.path.join(dataset_folder, "videos")
cropped_video_folder = os.path.join(dataset_folder, "cropped_videos")
pose_data_folder = os.path.join(dataset_folder, "pose_data")

# Ensure directories exist
os.makedirs(video_save_folder, exist_ok=True)
os.makedirs(cropped_video_folder, exist_ok=True)
os.makedirs(pose_data_folder, exist_ok=True)

# Get all CSV files
csv_files = glob.glob(os.path.join(dataset_folder, "*.csv"))

# Function to download videos
def download_video(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        return save_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

# Function to crop videos to the first 4 seconds using OpenCV
def crop_video(input_path, output_path, duration=4):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"Error opening video file: {input_path}")
        return None

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_frames = min(fps * duration, total_frames)  # Max frames for 4 sec

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 output

    # Create video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened() and frame_count < duration_frames:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    print(f"Cropped video saved: {output_path}")
    return output_path

# Function to analyze posture and save data
def analyze_posture(video_path, csv_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error opening video: {video_path}")
        return

    pose_data = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process frame with MediaPipe Pose
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                # Extract pose landmarks
                landmarks = results.pose_landmarks.landmark

                # Save x, y, z, visibility for each landmark
                frame_data = [video_path]  # Start with video path for reference
                for landmark in landmarks:
                    frame_data.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])

                pose_data.append(frame_data)

    cap.release()

    # Convert pose data to DataFrame
    column_names = ["video"] + [f"{name}_{coord}" for name in range(33) for coord in ["x", "y", "z", "visibility"]]
    df_pose = pd.DataFrame(pose_data, columns=column_names)

    # Save to CSV
    df_pose.to_csv(csv_path, index=False)
    print(f"Pose data saved: {csv_path}")

# Process each CSV file
for file in csv_files:
    print(f"Processing file: {file}")

    # Read CSV and extract video URLs
    df = pd.read_csv(file, usecols=["video"])

    # Loop through each video
    for idx, video_url in enumerate(df["video"]):
        video_filename = f"video_{idx}.mp4"
        video_path = os.path.join(video_save_folder, video_filename)
        cropped_video_path = os.path.join(cropped_video_folder, f"cropped_{video_filename}")
        pose_csv_path = os.path.join(pose_data_folder, f"pose_{idx}.csv")

        # Download video
        local_video_path = download_video(video_url, video_path)
        if not local_video_path:
            continue

        # Crop video to 4 seconds
        cropped_path = crop_video(local_video_path, cropped_video_path)
        if not cropped_path:
            continue

        # Analyze posture and save pose data
        analyze_posture(cropped_path, pose_csv_path)

    print("\n" + "="*50 + "\n")  # Separator for clarity
