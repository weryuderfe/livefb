import streamlit as st
from stream_manager import StreamManager
from stream_config import StreamConfig
from utils import frame_to_image

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