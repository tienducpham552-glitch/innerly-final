import streamlit as st
import google.generativeai as genai
from styles import apply_styles

apply_styles()

st.title("🧸 Trò Chuyện cùng Innerly")

# Lấy Key và kiểm tra
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ Chưa tìm thấy Key! Bạn hãy kiểm tra lại mục Secrets.")
else:
    genai.configure(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Chia sẻ với mình nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Thử kết nối
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # IN RA LỖI THẬT SỰ ĐỂ SỬA
            st.error(f"🚨 Lỗi chi tiết: {str(e)}")
            st.info("Hãy chụp ảnh lỗi này gửi cho mình để được hỗ trợ nhé!")
