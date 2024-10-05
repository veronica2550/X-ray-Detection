import streamlit as st
from streamlit_option_menu import option_menu

from func.file_upload import file_upload
# from func.process_video import process_video
from page.manage_page.object_setting import object_setting_UI
from page.result_page.detection_result import detection_result_UI
from page.manage_page.object_manage import object_manage_UI
from page.edit_page.result_edit import result_manage_UI

st.set_page_config(layout="wide")

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

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "위해물품 감지"
    st.session_state.from_save = False

if 'file_name_store' not in st.session_state:
    st.session_state.file_name_store = ""

# Sidebar menu
with st.sidebar:
    if st.session_state.from_save:
        default_index = 1  # '감지 물체 관리' for after saving
    else:
        default_index = 0  # '위해물품 감지' for first load or normal navigation

    if st.session_state.page in ["위해물품 감지", '감지 물체 관리', '감지 결과 관리', '챗봇']:
        st.session_state.page = option_menu("Shark Holmes", ["위해물품 감지", '감지 물체 관리', '감지 결과 관리', '챗봇'], 
                            icons=['cone-striped', 'bag-dash-fill', 'intersect', 'chat-right-text-fill'], 
                            menu_icon="award fill", 
                            default_index=default_index)
        
#st.session_state.from_save = False

# Update page state based on sidebar selection
if st.session_state.page == "위해물품 감지":
    if st.session_state.from_save == True:
        st.session_state.from_save = False
        st.rerun()
    
    st.session_state.from_save = False
    uploaded_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
    if uploaded_file:
        print(st.session_state.file_name_store)
        print(uploaded_file.name)
        if st.session_state.file_name_store != uploaded_file.name:
            file_upload(uploaded_file)
    detection_result_UI()
    
elif st.session_state.page == "감지 결과 관리":
    result_manage_UI()
    
elif st.session_state.page == "감지 물체 관리":
    object_manage_UI()

elif st.session_state.page == "감지 물체 세팅":
    object_setting_UI()
    
    # D 화면에서 B 화면으로 돌아가는 버튼 배치
    if st.button("저장"):
        st.session_state.page = "감지 물체 관리"
        st.session_state.from_save = True
        st.rerun()

elif st.session_state.page == '챗봇':
    st.write("챗봇")

#st.write(st.session_state.page)
#st.write(st.session_state.from_save)