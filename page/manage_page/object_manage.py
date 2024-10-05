import streamlit as st
from object import object

def object_manage_UI():
    # Initialize session state if not already
    if 'default_selected_values' not in st.session_state:
        st.session_state.default_selected_values = ["Hammer", "SSD", "Camera"]
    
    st.write("## 감지 물체 관리")
    st.write("---")
    if st.button('세트 추가'):
        st.session_state.page = "감지 물체 세팅"
        st.rerun()
    st.write("---")

    # API로 받아올 부분
    st.session_state.default_selected_values = list(object.values())

    num_columns = 4
    columns = st.columns(num_columns)
    with columns[0]:
        if st.button('공항 기본 세팅'):
            # 버튼이 클릭되었을 때 실행될 코드
            #default_selected_values = list(object.values())
            st.session_state.default_selected_values = list(object.values())
            st.rerun()
            # 그대로 API로 보내기

    # 사용자에게 선택 옵션 제공
    selected_options = st.multiselect(
        '검출할 물체 선택', 
        list(object.values()),
        default=st.session_state.default_selected_values
    )

    # Update the default values based on the selected options
    if selected_options != st.session_state.default_selected_values:
        st.session_state.default_selected_values = selected_options
        st.rerun()
