import streamlit as st
from func.detection_page import convert_png_to_jpg, display_images, load_image_paths, load_description

from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager
import os

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

#--------------------------위에까지 이미지 선택하는 부분--------------------------#
    run("frames", custom_labels)
#--------------------------아래부터 streamlit-img-label 파트--------------------------#

def run(img_dir, labels):
    #st.set_option("deprecation.showfileUploaderEncoding", False)
    idm = ImageDirManager(img_dir)

    if "files" not in st.session_state:
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0
    else:
        idm.set_all_files(st.session_state["files"])
        idm.set_annotation_files(st.session_state["annotation_files"])
    
    # def refresh():
    #     st.session_state["files"] = idm.get_all_files()
    #     st.session_state["annotation_files"] = idm.get_exist_annotation_files()
    #     st.session_state["image_index"] = 0

    # def next_image():
    #     image_index = st.session_state["image_index"]
    #     if image_index < len(st.session_state["files"]) - 1:
    #         st.session_state["image_index"] += 1
    #     else:
    #         st.warning('This is the last image.')

    # def previous_image():
    #     image_index = st.session_state["image_index"]
    #     if image_index > 0:
    #         st.session_state["image_index"] -= 1
    #     else:
    #         st.warning('This is the first image.')

    # def next_annotate_file():
    #     image_index = st.session_state["image_index"]
    #     next_image_index = idm.get_next_annotation_image(image_index)
    #     if next_image_index:
    #         st.session_state["image_index"] = idm.get_next_annotation_image(image_index)
    #     else:
    #         st.warning("All images are annotated.")
    #         next_image()

    # def go_to_image():
    #     file_index = st.session_state["files"].index(st.session_state["file"])
    #     st.session_state["image_index"] = file_index

    # def annotate():
    #     im.save_annotation()
    #     image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
    #     if image_annotate_file_name not in st.session_state["annotation_files"]:
    #         st.session_state["annotation_files"].append(image_annotate_file_name)
    #     next_annotate_file()

#-------------------------------위에까지는 함수 아래는 UI------------------------------

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.button(label="Previous image", on_click=previous_image)
    # with col2:
    #     st.button(label="Next image", on_click=next_image)
    # st.sidebar.button(label="Next need annotate", on_click=next_annotate_file)
    # st.sidebar.button(label="Refresh", on_click=refresh)

    # st.write(f"선택된 이미지: {st.session_state.image_index}")

    # Main content: annotate images
    descriptions = load_description("C:/Users/SM-PC/python-workspace/xray-detection/descriptions")
    img_file_name = idm.get_image(st.session_state["image_index"])
    img_path = os.path.join(img_dir, img_file_name)
    im = ImageManager(img_path)
    main_col1, main_col2 = st.columns([6, 4])

    with main_col1:
        #img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

    with main_col2:
        # st.write(f"**{descriptions[st.session_state.image_index]}**")
        st.markdown(f"<p style='font-size:24px;'>{descriptions[st.session_state.image_index]}</p>", unsafe_allow_html=True)
        if rects:
            # st.button(label="Save", on_click=annotate)
            preview_imgs = im.init_annotation(rects)

            for i, prev_img in enumerate(preview_imgs):
                prev_img[0].thumbnail((200, 200))
                col1, col2 = st.columns(2)
                with col1:
                    col1.image(prev_img[0])
                with col2:
                    default_index = 0
                    if prev_img[1]:
                        default_index = labels.index(prev_img[1])

                    select_label = col2.selectbox(
                        "Label", labels, key=f"label_{i}", index=default_index
                    )
                    im.set_annotation(i, select_label)


custom_labels = [
    '', 
    'Hammer',
    'SSD',
    'Alcohol',
    'Spanner',
    'Axe',
    'Awl',
    'Throwing Knife',
    'Firecracker',
    'Thinner',
    'Plier',
    'Match',
    'Smart Phone',
    'Scissors',
    'Tablet PC',
    'Solid Fuel',
    'Bat',
    'Portable Gas',
    'Nail Clippers',
    'Knife',
    'Metal Pipe',
    'Electronic Cigarettes(Liquid)',
    'Supplementary Battery',
    'Bullet',
    'Gun Parts',
    'USB',
    'Liquid',
    'Aerosol',
    'Screwdriver',
    'Chisel',
    'Handcuffs',
    'Lighter',
    'HDD',
    'Electronic Cigarettes',
    'Battery',
    'Gun',
    'Laptop',
    'Saw',
    'Zippo Oil',
    'Stun Gun',
    'Camera',
    'Camcorder',
    'SD Card',
    'Fretsaw'
]
