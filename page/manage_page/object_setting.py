import streamlit as st
import io
import pandas as pd
from object import object


def object_setting_UI():
    st.title("감지 물체 세팅")
    set_name = st.text_input("세트 이름")
    selected_options = st.multiselect(
        '검출할 물체 선택', 
        list(object.values()),
        default=[""]
    )
    print(selected_options)
    #st.write(selected_options)
            