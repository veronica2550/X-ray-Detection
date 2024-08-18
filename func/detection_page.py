import streamlit as st
import os
from PIL import Image
from streamlit_image_select import image_select

def convert_png_to_jpg(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            png_path = os.path.join(directory, filename)
            jpg_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}.jpg")
            
            # PNG 이미지를 열고 JPG로 저장
            with Image.open(png_path) as img:
                rgb_img = img.convert('RGB')  # PNG를 RGB 모드로 변환
                rgb_img.save(jpg_path, "JPEG")
            
            # 변환이 완료된 후 원본 PNG 파일 삭제
            os.remove(png_path)

def load_image_paths(frames_directory):
    image_paths = sorted([os.path.join(frames_directory, f) for f in os.listdir(frames_directory) if f.endswith('.jpg')])
    return image_paths

def display_images(image_paths, start_idx=0, images_per_row=5):
    end_idx = start_idx + images_per_row
    selected_images = image_paths[start_idx:end_idx]

    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None

    selected_image = image_select("Select an image", selected_images, captions=[os.path.basename(img) for img in selected_images], use_container_width=True, return_value="index")

    # 이미지 선택 시 상태 업데이트
    if selected_image is not None:
        st.session_state.selected_image = selected_images[selected_image]
        st.write(f"선택된 이미지: {st.session_state.selected_image}")
