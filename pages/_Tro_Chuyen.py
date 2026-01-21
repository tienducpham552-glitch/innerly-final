import streamlit as st
import google.generativeai as genai
from styles import apply_styles

# 1. Cài đặt trang và giao diện
st.set_page_config(page_title="Trò chuyện cùng Innerly", page_icon="🧸")
apply_styles()

st.title("🧸 Trò Chuyện cùng Innerly")

# 2. Kiểm tra API Key từ Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ Chưa tìm thấy API Key. Bạn hãy vào Settings -> Secrets để dán Key nhé.")
    st.stop()

# 3. Cấu hình AI (Dùng gemini-pro cho ổn định nhất)
genai.configure(api_key=api_key)

# 4. Quản lý lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Xử lý khi bạn nhập tin nhắn
if prompt := st.chat_input("Chia sẻ với mình nhé..."):
    # Lưu tin nhắn của bạn
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # --- ĐOẠN QUAN TRỌNG ĐÃ SỬA: DÙNG GEMINI-PRO ---
            model = genai.GenerativeModel('gemini-pro') 
            
            # Gửi tin nhắn
            response = model.generate_content(prompt)
            text_response = response.text
            
            # Hiển thị và lưu câu trả lời
            message_placeholder.write(text_response)
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"🚨 Có lỗi xảy ra: {str(e)}")
            st.info("Mẹo: Hãy kiểm tra lại API Key hoặc mạng internet của bạn.")
