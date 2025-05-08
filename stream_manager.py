import cv2
import numpy as np
from video_source import VideoSource
from typing import Optional

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