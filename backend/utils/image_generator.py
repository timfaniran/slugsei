import matplotlib.pyplot as plt
import io
import uuid
from google.cloud import storage

# Initialize GCS client
storage_client = storage.Client()
BUCKET_NAME = "slugsei-baseball-coach-images"  # Bucket name for storing analysis images

def generate_image(launch_angle, exit_velocity, chart_type):
    """
    Generate analysis images based on the provided chart type.

    Args:
        launch_angle (float): Launch angle for the player's swing.
        exit_velocity (float): Exit velocity for the player's swing.
        chart_type (str): Type of chart to generate ('barrel_zone', 'exit_velocity', 'launch_angle').

    Returns:
        io.BytesIO: A stream containing the generated image.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    
    if chart_type == "barrel_zone":
        ax.set_title("Barrel Zone")
        ax.set_xlabel("Launch Angle (degrees)")
        ax.set_ylabel("Exit Velocity (mph)")
        ax.plot([5, 25], [80, 110], label="Optimal Barrel Zone", color="blue", linewidth=2)
        ax.scatter([launch_angle], [exit_velocity], color="red", s=100, label="Your Swing")
        ax.legend()
    elif chart_type == "exit_velocity":
        ax.hist([50, 70, 90, 110, 130], bins=10, color="blue", alpha=0.7, label="Exit Velocity Distribution")
        ax.axvline(exit_velocity, color="red", linewidth=2, label="Your Exit Velocity")
        ax.legend()
        ax.set_title("Exit Velocity Distribution")
        ax.set_xlabel("Exit Velocity (mph)")
        ax.set_ylabel("Frequency")
    elif chart_type == "launch_angle":
        ax.hist([5, 15, 25, 35, 45], bins=10, color="orange", alpha=0.7, label="Launch Angle Distribution")
        ax.axvline(launch_angle, color="red", linewidth=2, label="Your Launch Angle")
        ax.legend()
        ax.set_title("Launch Angle Distribution")
        ax.set_xlabel("Launch Angle (degrees)")
        ax.set_ylabel("Frequency")
    else:
        raise ValueError("Invalid chart type")

    plt.grid(True)
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    plt.close()
    return image_stream

def upload_to_gcs(image_stream, chart_type, video_id):
    """
    Upload the generated image to Google Cloud Storage (GCS).

    Args:
        image_stream (io.BytesIO): The image stream to upload.
        chart_type (str): The type of chart for naming the file.
        video_id (str): The ID of the video being analyzed.

    Returns:
        str: The public URL of the uploaded image.
    """
    bucket = storage_client.bucket(BUCKET_NAME)
    blob_name = f"analysis_images/{video_id}/{chart_type}_{uuid.uuid4().hex}.png"
    blob = bucket.blob(blob_name)
    blob.upload_from_file(image_stream, content_type="image/png")
    # Remove blob.make_public() to avoid the error
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_name}"

def generate_and_upload_images(video_id, launch_angle, exit_velocity):
    """
    Generates and uploads analysis images for barrel zone, exit velocity, and launch angle.

    Args:
        video_id (str): ID of the video being analyzed.
        launch_angle (float): Launch angle for the player's swing.
        exit_velocity (float): Exit velocity for the player's swing.

    Returns:
        dict: URLs of the generated images.
    """
    images = {}

    # Generate and upload Barrel Zone Image
    barrel_zone_stream = generate_image(launch_angle, exit_velocity, "barrel_zone")
    images["barrel_zone"] = upload_to_gcs(barrel_zone_stream, "barrel_zone", video_id)

    # Generate and upload Exit Velocity Distribution Image
    exit_velocity_stream = generate_image(launch_angle, exit_velocity, "exit_velocity")
    images["exit_velocity"] = upload_to_gcs(exit_velocity_stream, "exit_velocity", video_id)

    # Generate and upload Launch Angle Distribution Image
    launch_angle_stream = generate_image(launch_angle, exit_velocity, "launch_angle")
    images["launch_angle"] = upload_to_gcs(launch_angle_stream, "launch_angle", video_id)

    return images