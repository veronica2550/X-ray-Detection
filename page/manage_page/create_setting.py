import streamlit as st
import io
import pandas as pd

def object_setting_UI():
    st.title("B 페이지")

    with st.form(key='input_form'):
        name = st.text_input('이름 입력')
        items = st.text_area('리스트 항목 입력 (각 항목은 줄 바꿈으로 구분)')
        submit_button = st.form_submit_button(label='저장하기')
        
        if submit_button:
            # 입력된 데이터를 데이터프레임으로 변환
            item_list = items.split('\n')
            data = {'Name': [name] * len(item_list), 'Item': item_list}
            df = pd.DataFrame(data)
            
            # 데이터프레임을 텍스트 파일로 변환
            txt = df.to_csv(index=False, sep='\t')
            buffer = io.StringIO()
            buffer.write(txt)
            buffer.seek(0)
            
            # 다운로드 버튼 생성
            st.download_button(
                label="파일 다운로드",
                data=buffer,
                file_name="data.txt",
                mime="text/plain"
            )
            