import streamlit as st

from func import process_video


def check_video(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the video and extract frames
        frames_dir = process_video("temp_video.mp4")
        st.session_state.frames_directory = frames_dir
        return frames_dir
    return None