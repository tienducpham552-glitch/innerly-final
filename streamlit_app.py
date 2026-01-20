import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Innerly Studio", page_icon="🧸", layout="wide")
st.markdown("""<style>
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    .card-pink { background-color: #ffe4e1; border: 2px solid #ffb6c1; padding: 20px; border-radius: 15px; color: #d02090; font-weight: bold; }
</style>""", unsafe_allow_html=True)

# --- KẾT NỐI AI ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Vui lòng dán API Key MỚI vào phần Secrets!")

def get_ai_response(prompt):
    try:
        # Tự động tìm model khả dụng nhất trong tài khoản của bạn
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Ưu tiên dùng gemini-1.5-flash nếu có trong danh sách
        target_model = next((m for m in models if "1.5-flash" in m), models[0] if models else None)
        
        if not target_model:
            return "🚨 Không tìm thấy model nào khả dụng. Hãy kiểm tra lại trạng thái Key của bạn!"

        model = genai.GenerativeModel(target_model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 Lỗi: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("Tâm sự cùng Innerly 🧸")

if "history" not in st.session_state: st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]): st.write(msg["content"])

if prompt := st.chat_input("Hãy nói gì đó với mình..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Innerly đang lắng nghe..."):
            res = get_ai_response(prompt)
            st.write(res)
            st.session_state.history.append({"role": "assistant", "content": res})

st.divider()
st.markdown('<div class="card-pink">🌸 Vỗ về: Bạn đã xử lý lỗi rất kiên trì, kết quả sẽ xứng đáng thôi!</div>', unsafe_allow_html=True)
