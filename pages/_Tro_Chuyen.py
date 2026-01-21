import streamlit as st
import google.generativeai as genai
# Nếu bạn có file styles.py thì giữ dòng này, không thì xóa đi
# from styles import apply_styles 

# 1. Cài đặt trang (BẮT BUỘC PHẢI CÓ Ở ĐẦU MỖI TRANG)
st.set_page_config(page_title="Trò chuyện cùng Innerly", page_icon="🧸")

# 2. Lấy API Key lại (Vì trang này chạy độc lập)
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("⚠️ Chưa tìm thấy API Key trong Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Khởi tạo lịch sử chat nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Phần Chat (Dòng bị lỗi của bạn nằm ở đây)
if prompt := st.chat_input("Chia sẻ với mình nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Nhớ dùng model mới nhé
            model = genai.GenerativeModel('gemini-1.5-flash') 
            response = model.generate_content(prompt)
            text_response = response.text
            
            message_placeholder.write(text_response)
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"🚨 Lỗi: {str(e)}")
