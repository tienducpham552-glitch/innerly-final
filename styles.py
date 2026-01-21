import streamlit as st
import google.generativeai as genai
from styles import apply_styles
from prompts import SYSTEM_PROMPT

# 1. Áp dụng giao diện bạn đã thiết kế
st.set_page_config(page_title="Trò chuyện cùng Innerly", page_icon="🧸")
apply_styles()

# 2. Cấu hình AI
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ Chưa tìm thấy API Key trong Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Quản lý logic bộ nhớ (Context)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Hiển thị Giao diện
st.markdown("<div class='card-inner'><h1 class='main-title'>🧸 Trò Chuyện cùng Innerly</h1><p>Mình luôn ở đây để lắng nghe bạn.</p></div>", unsafe_allow_html=True)

# Hiển thị lịch sử chat
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# 5. Khung nhập tin nhắn
if prompt := st.chat_input("Hôm nay của bạn thế nào?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"🚨 Innerly gặp chút sự cố: {str(e)}")
