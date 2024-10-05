import json
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

def load_description(json_directory):
    description_list = []
    # 모든 .json 파일 경로 가져오기
    description_paths = sorted([os.path.join(json_directory, f) for f in os.listdir(json_directory) if f.endswith('.json')])

    # 각 파일에서 'description'을 읽어와서 리스트에 저장
    for path in description_paths:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            description = data.get('descriptions', '')  # description은 str로 가정
            description_list.append(description)
    
    return description_list

def display_images(image_paths, start_idx=0, images_per_row=5):
    end_idx = start_idx + images_per_row
    selected_images = image_paths[start_idx:end_idx]

    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None

    selected_image = image_select("Select an image", selected_images, captions=[os.path.basename(img) for img in selected_images], use_container_width=True, return_value="index")

    # 이미지 선택 시 상태 업데이트
    if selected_image is not None:
        st.session_state.selected_image = selected_images[selected_image]
        # st.write(f"선택된 이미지: {st.session_state.selected_image}")
        selected_image_index = start_idx + selected_image  # 전체 이미지 리스트에서의 인덱스 계산
        #st.write(f"선택된 이미지의 전체 인덱스: {selected_image_index}")
        st.session_state.image_index = selected_image_index
    
