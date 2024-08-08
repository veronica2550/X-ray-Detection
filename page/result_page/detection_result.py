import streamlit as st
import os
from PIL import Image


def detection_result_UI():
    st.write("## 위해물품 감지")
    st.write("---")

    image_paths = load_image_paths("video_2_frame")
    num_images = len(image_paths)
    images_per_row = 5

    st.write(f"총 {num_images}개의 이미지가 있습니다.")

    num_rows = (num_images + images_per_row - 1) // images_per_row
    row_slider = st.slider("Slider", 0, num_rows - 1, 0)

    display_images(image_paths, start_idx=row_slider * images_per_row, images_per_row=images_per_row)

def load_image_paths(frames_directory):
    image_paths = sorted([os.path.join(frames_directory, f) for f in os.listdir(frames_directory) if f.endswith('.jpg')])
    return image_paths

def display_images(image_paths, start_idx=0, images_per_row=20):
    end_idx = start_idx + images_per_row
    selected_images = image_paths[start_idx:end_idx]
    
    cols = st.columns(images_per_row)
    for idx, img_path in enumerate(selected_images):
        img = Image.open(img_path)
        with cols[idx]:
            st.image(img, use_column_width=True)