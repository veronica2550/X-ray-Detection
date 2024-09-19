import streamlit as st

from func.process_video import process_video

def file_upload(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        st.session_state.file_name_store = uploaded_file.name
        with open(f"{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the video and extract frames
        frames_dir = process_video(f"{uploaded_file.name}")
        st.session_state.frames_directory = frames_dir
        return frames_dir
    return None