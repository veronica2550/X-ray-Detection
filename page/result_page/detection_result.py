import streamlit as st
from func.detection_page import convert_png_to_jpg, display_images, load_image_paths

def detection_result_UI():
    st.write("## 위해물품 감지")
    st.write("---")

    # PNG 파일을 JPG로 변환
    convert_png_to_jpg("C:/Users/SM-PC/python-workspace/xray-detection/frames")

    image_paths = load_image_paths("C:/Users/SM-PC/python-workspace/xray-detection/frames")
    num_images = len(image_paths)
    images_per_row = 5

    if num_images != 0:
        st.write(f"총 {num_images}개의 이미지가 있습니다.")

    if num_images == 0:
        st.write("영상을 업로드 해주세요")
        st.image("assets/vid_upload.jpg")
        return

    num_rows = (num_images + images_per_row - 1) // images_per_row

    # if num_rows > 1:
    #     row_slider = st.slider("Slider", 0, num_rows - 1, 0)
    # else:
    #     row_slider = 0  # Slider가 필요 없는 경우
    # 이전 및 다음 버튼을 위한 인덱스 관리

    if 'row_slider' not in st.session_state:
        st.session_state.row_slider = 0

    col1, col2, col3, col4, col5 = st.columns([1, 4, 2, 4, 1])

    with col1:
        if st.button("< 이전"):
            st.session_state.row_slider = max(0, st.session_state.row_slider - 1)

    with col3:
        st.write(f"페이지 {st.session_state.row_slider + 1} / {num_rows}")

    with col5:
        if st.button("다음 >"):
            st.session_state.row_slider = min(num_rows - 1, st.session_state.row_slider + 1)
            st.rerun()

    display_images(image_paths, start_idx=st.session_state.row_slider * images_per_row, images_per_row=images_per_row)


    #display_images(image_paths, start_idx=row_slider * images_per_row, images_per_row=images_per_row)



