import streamlit as st
from streamlit_option_menu import option_menu

from page.manage_page.create_setting import object_setting_UI
from page.result_page.detection_result import detection_result_UI
from page.manage_page.object_manage import object_manage_UI
from page.edit_page.result_edit import result_manage_UI

def navigate_to_page(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

with st.sidebar:
    button_style = """
        <style>
        div.stButton > button {
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    selected = option_menu("Shark Homels", ["위해물품 감지", '감지 물체 관리', '감지 결과 관리'], 
        icons=['cone-striped', 'bag-dash-fill', 'intersect'], menu_icon="award fill", default_index=0)

if selected == "위해물품 감지":
    uploaded_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
    detection_result_UI()

if selected == "감지 결과 관리":
    result_manage_UI()

if selected == "감지 물체 관리":
    object_manage_UI()