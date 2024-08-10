import streamlit as st
from streamlit_option_menu import option_menu

# 페이지 상태 관리
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'A'

# 사이드바에서 option_menu를 사용하여 페이지 선택
with st.sidebar:
    # 사이드바 메뉴는 'D' 화면이 아닌 경우에만 표시
    if st.session_state.current_page in ['A', 'B', 'C']:
        st.session_state.current_page = option_menu("Main Menu", ["A", "B", "C"],
                                                     icons=['house', 'cloud-upload', "list-task"],
                                                     menu_icon="cast", default_index=0)
    
# 페이지 전환 로직
if st.session_state.current_page == "A":
    st.title("A Screen")
    st.write("This is the A screen.")

elif st.session_state.current_page == "B":
    st.title("B Screen")
    st.write("This is the B screen.")
    
    # B 화면에 버튼 배치
    if st.button("Go to D Screen"):
        st.session_state.current_page = "D"
        st.rerun()

elif st.session_state.current_page == "C":
    st.title("C Screen")
    st.write("This is the C screen.")

elif st.session_state.current_page == "D":
    st.title("D Screen")
    st.write("You are now on the D screen.")
    
    # D 화면에서 B 화면으로 돌아가는 버튼 배치
    if st.button("Go Back to B Screen"):
        st.session_state.current_page = "B"
        st.rerun()
