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
