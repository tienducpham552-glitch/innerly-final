import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Innerly Chat", page_icon="🧸")

# 1. Cấu hình API
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("Chưa tìm thấy API Key!")
    st.stop()

genai.configure(api_key=api_key)

# 2. KIỂM TRA VÀ CHỌN MODEL (Giải pháp mới)
@st.cache_resource
def get_available_model():
    try:
        # Liệt kê tất cả các model bạn có quyền truy cập
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ưu tiên các bản 1.5 mới, nếu không có thì lùi về các bản cũ hơn
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in models:
                return target
        return models[0] if models else None
    except:
        return 'models/gemini-1.5-flash' # Mặc định nếu lỗi

target_model = get_available_model()

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
            model = genai.GenerativeModel(target_model)
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi: {str(e)}")
            st.info(f"Đang cố gắng sử dụng model: {target_model}")
