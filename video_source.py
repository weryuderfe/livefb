import cv2
import numpy as np
from typing import Optional, Tuple

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