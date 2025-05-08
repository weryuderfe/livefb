# Video Streaming Application

A simple video streaming application built with Streamlit and OpenCV.

## Features

- Real-time video streaming from webcam
- Start/Stop stream control
- Clean architecture with separate components

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Components

- `app.py`: Main Streamlit application
- `video_source.py`: Handles video capture
- `stream_manager.py`: Manages the video stream
- `utils.py`: Utility functions
- `stream_config.py`: Configuration settings