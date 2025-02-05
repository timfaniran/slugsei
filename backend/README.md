# Backend

### Setup Testing Instructions

1. **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Run the Backend API (Port 8080)**
    ```bash
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    ```
    - ✅ This should make you be able to access the APIs at: http://127.0.0.1:8080/docs

3. **Upload a Test Video**
    ```bash
    curl -X POST "http://127.0.0.1:8080/upload_video" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/sample.mp4"
    ```
    - ✅ This will upload a sample video

4. **Run Video Analysis**
    ```bash
    curl -X POST "http://127.0.0.1:8080/analysis" \
     -H "Content-Type: application/json" \
     -d '{"video_id": "your_test_video_id"}'
    ```
    This will:
    - ✅ Download the video
    - ✅ Track baseball movement
    - ✅ Analyze ball motion
    - ✅ Store results in Firestore

5. **Get Coaching Feedback**
    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:8080/coaching/feedback' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "video_id": "your_test_video_id"
    }'
    ```
    This will:
    - ✅ Give coaching feedback based on the analysis of the uploaded video.