import cv2
import numpy as np
from PIL import Image

def frame_to_image(frame: np.ndarray) -> Image.Image:
    """Convert a numpy array frame to PIL Image"""
    return Image.fromarray(frame)