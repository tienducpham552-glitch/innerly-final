import streamlit as st
import google.generativeai as genai
from styles import apply_custom_styles
from prompts import SYSTEM_PROMPT

# 1. Áp dụng giao diện
st.set_page_config(page_title="Innerly Chat", page_icon="🧸")
apply_custom_styles()

# 2. Cấu hình API
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("Chưa tìm thấy API Key!")
    st.stop()

genai.configure(api_key=api_key)

# 3. Khởi tạo phiên Chat có bộ nhớ (Context)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Hiển thị tiêu đề và lịch sử
st.markdown("<h1 class='main-title'>🧸 Trò Chuyện cùng Innerly</h1>", unsafe_allow_html=True)

for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# 5. Nhập tin nhắn
if prompt := st.chat_input("Chia sẻ tâm tư với Innerly nhé..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"Innerly đang gặp chút sự cố: {str(e)}")
