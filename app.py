import streamlit as st
import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple

# Configuration
class StreamConfig:
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    FPS = 30
    STREAM_KEY = "video_stream"

# Video Source
class VideoSource:
    def __init__(self, source: int = 0):
        self.source = source
        self.cap = None
        
    def start(self) -> bool:
        """Start the video capture"""
        self.cap = cv2.VideoCapture(self.source)
        return self.cap.isOpened()
    
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
            return 0, 0
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

# Stream Manager
class StreamManager:
    def __init__(self):
        self.video_source = VideoSource()
        self.is_streaming = False
        
    def start_stream(self) -> bool:
        """Start the video stream"""
        if not self.is_streaming:
            success = self.video_source.start()
            self.is_streaming = success
            return success
        return True
    
    def stop_stream(self):
        """Stop the video stream"""
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
        
    def get_dimensions(self):
        """Get the dimensions of the video stream"""
        return self.video_source.get_dimensions()

# Utility Functions
def frame_to_image(frame: np.ndarray) -> Image.Image:
    """Convert a numpy array frame to PIL Image"""
    return Image.fromarray(frame)

# Main Application
def main():
    st.title("Video Streaming App")
    
    # Initialize the stream manager in session state
    if 'stream_manager' not in st.session_state:
        st.session_state.stream_manager = StreamManager()
    
    # Start/Stop stream button
    if st.button('Start Stream' if not st.session_state.stream_manager.is_streaming else 'Stop Stream'):
        if st.session_state.stream_manager.is_streaming:
            st.session_state.stream_manager.stop_stream()
        else:
            st.session_state.stream_manager.start_stream()
    
    # Create a placeholder for the video stream
    stream_placeholder = st.empty()
    
    # Main streaming loop
    while st.session_state.stream_manager.is_streaming:
        frame = st.session_state.stream_manager.get_frame()
        if frame is not None:
            image = frame_to_image(frame)
            stream_placeholder.image(image, channels="RGB", use_column_width=True)
        else:
            st.warning("Failed to get frame from stream")
            st.session_state.stream_manager.stop_stream()
            break

if __name__ == "__main__":
    main()
