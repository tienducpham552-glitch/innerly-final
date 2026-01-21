import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH TRANG (Bắt buộc phải có dòng này đầu tiên) ---
st.set_page_config(page_title="Trò chuyện cùng Innerly", page_icon="🧸")

# --- 2. LẤY API KEY TỪ SECRETS ---
# Vì đây là trang con nên phải lấy lại API key, nó không tự hiểu từ trang chủ
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ Chưa tìm thấy API Key. Bạn hãy kiểm tra lại file secrets.toml nhé.")
    st.stop()

# Cấu hình AI
genai.configure(api_key=api_key)

# --- 3. GIAO DIỆN CHAT ---
st.title("🧸 Trò Chuyện cùng Innerly")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Xử lý khi nhập tin nhắn mới
if prompt := st.chat_input("Chia sẻ với mình nhé..."):
    # Lưu tin nhắn user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Dùng model Flash để nhanh và ổn định hơn
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            response = model.generate_content(prompt)
            text_response = response.text
            
            message_placeholder.write(text_response)
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"🚨 Có lỗi xảy ra: {str(e)}")
