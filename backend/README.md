# Backend

### Setup Instructions

1. **Set up the virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Run `trackBall.py`**:
    ```bash
    cd be
    python trackBall.py
    ```
    Processes videos in `datasets/videos`, tracks ball positions, saves frames in `tracked_frames`, and logs positions to a text file.

3. **Run `ballMotion.py`**:
    ```bash
    python ballMotion.py
    ``` 
    Use the tracked ball positions from `trackBall.py` to analyze the motion of the ball and calculate the launch angle and exit velocity.   

    NOTE: Take a look into the data_process Jupyter Notebook to see the stat measures on the mean of launch angle and exit velocity.

4. **Run the Backend API (Port 8080)**
    ```bash
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
    ```
    - ✅ This should make you be able to access the APIs at: http://127.0.0.1:8080/docs

5. **Upload a Test Video**
    ```bash
    curl -X POST "http://127.0.0.1:8080/upload_video" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/sample.mp4"
    ```
    - ✅ This will upload a sample video

6. **Run Video Analysis**
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

7. **Get Coaching Feedback**
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