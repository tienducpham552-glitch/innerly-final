import streamlit as st
import google.generativeai as genai

# 1. Khai báo Streamlit phải luôn ở dòng đầu tiên
st.set_page_config(page_title="Innerly Chat", page_icon="🧸")

# 2. Cấu hình API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("Chưa tìm thấy API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# 3. Giao diện
st.title("🧸 Trò Chuyện cùng Innerly")

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
            # Thử dùng bản flash mới nhất
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            full_response = response.text
            st.write(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Lỗi hệ thống: {str(e)}")
            st.info("Mẹo: Đảm bảo bạn đã Reboot app sau khi sửa requirements.txt")
