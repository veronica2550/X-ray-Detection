import streamlit as st
import streamlit as st
import os
from func.detection_page import convert_png_to_jpg, display_images, load_image_paths
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager, ImageDirManager

def result_manage_UI():
    st.write("## 감지 결과 관리")
    st.write("---")
    image_paths = load_image_paths("C:/Users/SM-PC/python-workspace/xray-detection/frames")
    num_images = len(image_paths)
    images_per_row = 5
    num_rows = (num_images + images_per_row - 1) // images_per_row

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

    run("frames", custom_labels)

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
    
    def refresh():
        st.session_state["files"] = idm.get_all_files()
        st.session_state["annotation_files"] = idm.get_exist_annotation_files()
        st.session_state["image_index"] = 0

    def next_image():
        image_index = st.session_state["image_index"]
        if image_index < len(st.session_state["files"]) - 1:
            st.session_state["image_index"] += 1
        else:
            st.warning('This is the last image.')

    def previous_image():
        image_index = st.session_state["image_index"]
        if image_index > 0:
            st.session_state["image_index"] -= 1
        else:
            st.warning('This is the first image.')

    def next_annotate_file():
        image_index = st.session_state["image_index"]
        next_image_index = idm.get_next_annotation_image(image_index)
        if next_image_index:
            st.session_state["image_index"] = idm.get_next_annotation_image(image_index)
        else:
            st.warning("All images are annotated.")
            next_image()

    def go_to_image():
        file_index = st.session_state["files"].index(st.session_state["file"])
        st.session_state["image_index"] = file_index

    # Sidebar: show status
    n_files = len(st.session_state["files"])
    n_annotate_files = len(st.session_state["annotation_files"])
    st.sidebar.write("Total files:", n_files)
    st.sidebar.write("Total annotate files:", n_annotate_files)
    st.sidebar.write("Remaining files:", n_files - n_annotate_files)

    st.sidebar.selectbox(
        "Files",
        st.session_state["files"],
        index=st.session_state["image_index"],
        on_change=go_to_image,
        key="file",
    )
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.button(label="Previous image", on_click=previous_image)
    with col2:
        st.button(label="Next image", on_click=next_image)
    st.sidebar.button(label="Next need annotate", on_click=next_annotate_file)
    st.sidebar.button(label="Refresh", on_click=refresh)

    # Main content: annotate images
    img_file_name = idm.get_image(st.session_state["image_index"])
    img_path = os.path.join(img_dir, img_file_name)
    im = ImageManager(img_path)

    main_col1, main_col2 = st.columns(2)
    with main_col1:
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

    def annotate():
        im.save_annotation()
        image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
        if image_annotate_file_name not in st.session_state["annotation_files"]:
            st.session_state["annotation_files"].append(image_annotate_file_name)
        next_annotate_file()

    with main_col2:
        if rects:
            st.button(label="Save", on_click=annotate)
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
