import streamlit.components.v1 as components
import streamlit as st

def chatbot_UI():
    components.html(
        """
        <style>
            /* 채팅창 스타일 */
            #chat_window {
                border-radius: 10px;
                padding: 15px;
                width: 97%;
                min-height: 450px; /* 최대 높이 설정 */
                overflow-y: auto; /* 스크롤 추가 */
                background-color: #f7f9fc;
            }

            /* 메시지 스타일 */
            .message {
                margin-bottom: 15px;
            }

            .user-message {
                text-align: right;
                font-family: Arial, sans-serif;
                color: #2d2d2d;
                font-size: 16px;
                padding-right: 20px;
            }

            .bot-message {
                text-align: left;
                font-family: Arial, sans-serif;
                color: #ffffff;
                background-color: #FF4B4B;
                border-radius: 8px;
                display: inline-block;
                padding: 8px 12px;
                font-size: 16px;
            }

            .user-message span {
                background-color: #e1e1e1;
                padding: 8px 12px;
                border-radius: 8px;
                display: inline-block;
            }

            /* 파일 선택 및 입력창 디자인 */
            #chat_form {
                margin-top: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #f1f1f1;
                border-radius: 25px;
                padding: 10px 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 97%;
            }

            /* 파일 선택 버튼 스타일 */
            #file_input_wrapper {
                position: relative;
                display: inline-block;
            }

            #file_input {
                opacity: 0;
                position: absolute;
                left: 0;
                top: 0;
                width: 150px;
                height: 40px;
                cursor: pointer;
            }

            .custom-file-upload {
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 6px;
                background-color: #f1f1f1;
                color: #333;
                border-radius: 50%;
                font-size: 20px;
                width: 28px;
                height: 40px;
                cursor: pointer;
            }

            /* 입력창 스타일 */
            #user_input {
                width: 100%;
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                background-color: #f1f1f1;
                margin-left: 8px;
            }

            /* 보내기 버튼 스타일 */
            button {
                background-color: #f7f9fc;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                font-size: 20px;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            button:hover {
                background-color: #f1f1f1;
            }

            /* 이미지 미리보기 스타일 */
            #image_preview {
                display: flex;
                justify-content: left;
                align-items: center;
                margin-bottom: 10px;
            }

            #image_preview img {
                max-width: 100px;
                max-height: 100px;
                border-radius: 10px;
                cursor: pointer;
            }

        </style>

        <div id="chat_window">
            <div id="messages"></div>
        </div>

        <div id="image_preview"></div>

        <form id="chat_form">
            <div id="file_input_wrapper">
                <label for="file_input" class="custom-file-upload">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-paperclip" viewBox="0 0 16 16">
                        <path d="M4.5 3a2.5 2.5 0 0 1 5 0v9a1.5 1.5 0 0 1-3 0V5a.5.5 0 0 1 1 0v7a.5.5 0 0 0 1 0V3a1.5 1.5 0 1 0-3 0v9a2.5 2.5 0 0 0 5 0V5a.5.5 0 0 1 1 0v7a3.5 3.5 0 1 1-7 0z"/>
                    </svg>
                </label>
                <input type="file" id="file_input" accept="image/*">
            </div>
            <input type="text" id="user_input" placeholder="메시지를 입력하세요...">
            <button type="submit" class="custom-file-upload">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-fill" viewBox="0 0 16 16">
                    <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471z"/>
                </svg>
            </button>
        </form>

        <script>
            var selectedImage = null;

            // 이미지 선택 이벤트 처리
            document.getElementById('file_input').onchange = function(event) {
                var file = event.target.files[0];
                if (file) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        var imagePreviewDiv = document.getElementById('image_preview');
                        imagePreviewDiv.innerHTML = '<img src="' + e.target.result + '" id="preview_image">';
                        selectedImage = e.target.result;

                        // 이미지 클릭 시 선택 취소
                        document.getElementById('preview_image').onclick = function() {
                            imagePreviewDiv.innerHTML = '';
                            selectedImage = null;
                            document.getElementById('file_input').value = '';
                        };
                    };
                    reader.readAsDataURL(file);
                }
            };

            document.getElementById('chat_form').onsubmit = function(event) {
                event.preventDefault();
                var user_input = document.getElementById('user_input').value;
                var messages_div = document.getElementById('messages');

                // 사용자 메시지 추가
                var user_message = '<div class="message user-message"><span>' + user_input + '</span></div>';
                if (selectedImage) {
                    user_message = '<div class="message user-message"><img src="' + selectedImage + '" style="width: 100px; height: 100px;"><br><span>' + user_input + '</span></div>';
                }
                messages_div.innerHTML += user_message;

                // 채팅창을 아래로 스크롤
                document.getElementById('chat_window').scrollTop = document.getElementById('chat_window').scrollHeight;

                // 챗봇 응답 로직 추가 (이미지 포함)
                var bot_response = '<div class="message bot-message">빨리 output 줘봐요<br>빨리빨리<br>빨리빨리빨리</div>';
                messages_div.innerHTML += bot_response;

                // 입력 필드 초기화
                document.getElementById('user_input').value = '';
                selectedImage = null;
                document.getElementById('image_preview').innerHTML = '';

                // 채팅창을 아래로 스크롤
                document.getElementById('chat_window').scrollTop = document.getElementById('chat_window').scrollHeight;
            };
        </script>
        """,
        height=1500,
    )
