import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG & GIAO DIỆN ---
st.set_page_config(page_title="Innerly Studio", page_icon="🧸", layout="wide")

st.markdown("""
<style>
    /* Nền gradient hồng xanh nhẹ nhàng */
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    
    /* Tùy chỉnh khung chat */
    .stChatMessage { border-radius: 20px; border: 1px solid rgba(255,255,255,0.5); background: rgba(255,255,255,0.2); }
    
    /* Thẻ vỗ về đặc trưng của Innerly */
    .innerly-card {
        background-color: #ffe4e1;
        border: 2px solid #ffb6c1;
        padding: 15px;
        border-radius: 15px;
        color: #d02090;
        font-weight: 500;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- KẾT NỐI AI ---
# Lấy API Key mới nhất từ Secrets để đảm bảo an toàn
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Vui lòng kiểm tra lại GEMINI_API_KEY trong cấu hình Secrets.")

def get_ai_response(prompt):
    try:
        # Sử dụng model Flash để có tốc độ phản hồi nhanh nhất
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 Innerly đang nghỉ ngơi một chút: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.title("Tâm sự cùng Innerly 🧸")
st.caption("Đồng hành cùng cảm xúc học đường © 2024")

# Khởi tạo lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý nhập liệu
if prompt := st.chat_input("Hôm nay của bạn thế nào?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Innerly đang lắng nghe bạn..."):
            full_response = get_ai_response(prompt)
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- PHẦN CUỐI TRANG ---
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="innerly-card">🌸 Vỗ về: Bạn đã rất kiên trì để kết nối được với mình. Tự hào về bạn!</div>', unsafe_allow_html=True)

# Nút xóa lịch sử để bắt đầu lại
if st.button("Làm mới cảm xúc 🌿"):
    st.session_state.messages = []
    st.rerun()
