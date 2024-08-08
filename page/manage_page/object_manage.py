import streamlit as st
from object import object
from page.manage_page.create_setting import object_setting_UI

def object_manage_UI():
    # Initialize session state if not already
    if 'default_selected_values' not in st.session_state:
        st.session_state.default_selected_values = ["Hammer", "SSD", "Camera"]
    
    st.write("## 감지 물체 관리")
    st.write("---")

    col1, col2 = st.columns([4, 1])  # 비율을 조절하여 열 크기를 설정할 수 있습니다.

    # 첫 번째 열에 제목 추가
    with col1:
        st.write("## 감지 물체 관리")

    # 두 번째 열에 버튼 추가
    with col2:
        if st.button('세트 추가'):


            print()

    st.write("---")

    # API로 받아올 부분
    #default_selected_values = ["Hammer", "SSD", "Camera"]

    if st.button('공항 기본 세팅'):
        # 버튼이 클릭되었을 때 실행될 코드
        #default_selected_values = list(object.values())
        st.session_state.default_selected_values = list(object.values())
        st.experimental_rerun()
        # 그대로 API로 보내기

    # 사용자에게 선택 옵션 제공
    selected_options = st.multiselect(
        '검출할 물체 선택', 
        list(object.values()),
        default=st.session_state.default_selected_values
    )

    # Update the default values based on the selected options
    st.session_state.default_selected_values = selected_options

    # 선택된 옵션 표시
    sorted_values = sorted(selected_options)
    st.write('선택한 물체:', sorted_values)
    print(sorted_values)

