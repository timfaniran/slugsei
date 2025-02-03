import os
from google.cloud import storage, firestore
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "slugsei-baseball-coach-videos"

GCP_PROJECT_ID = os.getenv("GCP_PROJECT")
if not GCP_PROJECT_ID:
    raise ValueError("Missing GCP_PROJECT environment variable.")

# GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# if not GOOGLE_APPLICATION_CREDENTIALS:
#     print("GOOGLE_APPLICATION_CREDENTIALS not set. Using default credentials.")
    # Replacing error with print
    # raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS environment variable.")

storage_client = storage.Client()
firestore_client = firestore.Client()  

def get_videos_bucket(bucket_name: str = BUCKET_NAME):
    return storage_client.bucket(BUCKET_NAME)

def get_firestore_collection(collection_name):
    return firestore_client.collection(collection_name)
