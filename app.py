import streamlit as st
import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple
import tempfile
import os
import subprocess

# Configuration
class StreamConfig:
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    FPS = 30
    STREAM_KEY = "FB-1143878627753140-0-Ab2Z4F8tqQF4IPNuKIh2MRS9"
    RTMP_URL = f"rtmps://live-api-s.facebook.com:443/rtmp/{STREAM_KEY}"

# Video Source
class VideoSource:
    def __init__(self, video_file: str):
        self.source = video_file
        self.cap = None
        
    def start(self) -> bool:
        """Start the video capture"""
        try:
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                st.error(f"Failed to open video file: {self.source}")
                return False
            return True
        except Exception as e:
            st.error(f"Error starting video capture: {str(e)}")
            return False
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a frame from the video source"""
        if not self.cap or not self.cap.isOpened():
            return False, None
        return self.cap.read()
    
    def release(self):
        """Release the video capture"""
        if self.cap:
            self.cap.release()
            
    def get_dimensions(self) -> Tuple[int, int]:
        """Get the dimensions of the video stream"""
        if not self.cap:
            return StreamConfig.WINDOW_WIDTH, StreamConfig.WINDOW_HEIGHT
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

# Stream Manager
class StreamManager:
    def __init__(self, video_path: str):
        self.video_source = VideoSource(video_path)
        self.is_streaming = False
        self.ffmpeg_process = None
        
    def start_stream(self) -> bool:
        """Start the video stream"""
        if not self.is_streaming:
            success = self.video_source.start()
            if success:
                width, height = self.video_source.get_dimensions()
                command = [
                    'ffmpeg',
                    '-re',
                    '-i', self.video_source.source,
                    '-c:v', 'libx264',
                    '-preset', 'veryfast',
                    '-maxrate', '3000k',
                    '-bufsize', '6000k',
                    '-pix_fmt', 'yuv420p',
                    '-g', '50',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-ar', '44100',
                    '-f', 'flv',
                    StreamConfig.RTMP_URL
                ]
                try:
                    self.ffmpeg_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.is_streaming = True
                    return True
                except Exception as e:
                    st.error(f"Failed to start streaming: {str(e)}")
                    return False
            return False
        return True
    
    def stop_stream(self):
        """Stop the video stream"""
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process = None
        self.video_source.release()
        self.is_streaming = False
        
    def get_frame(self) -> Optional[np.ndarray]:
        """Get the next frame from the stream"""
        if not self.is_streaming:
            return None
            
        success, frame = self.video_source.read()
        if not success:
            return None
            
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Utility Functions
def frame_to_image(frame: np.ndarray) -> Image.Image:
    """Convert a numpy array frame to PIL Image"""
    return Image.fromarray(frame)

def save_uploaded_file(uploaded_file):
    """Save uploaded file and return the path"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving uploaded file: {str(e)}")
        return None

# Main Application
def main():
    st.title("Facebook Live Video Streaming")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'])
    
    if uploaded_file is not None:
        # Save the uploaded file
        video_path = save_uploaded_file(uploaded_file)
        
        if video_path:
            # Initialize the stream manager in session state
            if 'stream_manager' not in st.session_state:
                st.session_state.stream_manager = StreamManager(video_path)
            
            # Start/Stop stream button
            if st.button('Start Stream' if not st.session_state.stream_manager.is_streaming else 'Stop Stream'):
                if st.session_state.stream_manager.is_streaming:
                    st.session_state.stream_manager.stop_stream()
                    # Clean up temporary file
                    if os.path.exists(video_path):
                        os.unlink(video_path)
                else:
                    if st.session_state.stream_manager.start_stream():
                        st.success("Streaming started successfully!")
                    else:
                        st.error("Failed to start streaming")
            
            # Create a placeholder for the video stream
            stream_placeholder = st.empty()
            
            # Main streaming loop
            while st.session_state.stream_manager.is_streaming:
                frame = st.session_state.stream_manager.get_frame()
                if frame is not None:
                    image = frame_to_image(frame)
                    stream_placeholder.image(image, channels="RGB", use_column_width=True)
                else:
                    st.warning("End of video stream reached")
                    st.session_state.stream_manager.stop_stream()
                    # Clean up temporary file
                    if os.path.exists(video_path):
                        os.unlink(video_path)
                    break

if __name__ == "__main__":
    main()
