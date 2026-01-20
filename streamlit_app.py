import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN (Hồng & Xanh) ---
st.set_page_config(page_title="Innerly Studio", page_icon="🧸", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .card-pink { background-color: #ffe4e1; border: 2px solid #ffb6c1; padding: 20px; border-radius: 15px; color: #d02090; font-weight: bold; }
    .card-blue { background-color: #e0ffff; border: 2px solid #afeeee; padding: 20px; border-radius: 15px; color: #008b8b; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- KẾT NỐI AI ---
# Lấy API Key từ Secrets của Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY. Hãy kiểm tra lại file secrets.toml hoặc cài đặt trên Streamlit Cloud!")

def get_ai_response(prompt):
    if not api_key:
        return "❌ Lỗi: API Key đang trống. Vui lòng cấu hình Key để bắt đầu trò chuyện."
    
    # Sử dụng các model ổn định nhất hiện nay
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro']
    last_error = "Không xác định"

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue # Thử model tiếp theo nếu model này lỗi
            
    # Nếu tất cả các model đều thất bại, trả về chi tiết lỗi thật sự
    return f"🚨 Innerly gặp sự cố kỹ thuật: {last_error}"

# --- GIAO DIỆN CHÍNH ---
st.title("Tâm sự cùng Innerly 🧸")

# Khởi tạo lịch sử chat
if "history" not in st.session_state:
    st.session_state.history = []

# Hiển thị các tin nhắn cũ
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Xử lý nhập liệu từ người dùng
if prompt := st.chat_input("Hãy nói gì đó với mình..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Phản hồi từ AI
    with st.chat_message("assistant"):
        with st.spinner("Innerly đang lắng nghe..."):
            res = get_ai_response(prompt)
            st.write(res)
            st.session_state.history.append({"role": "assistant", "content": res})

# --- PHẦN THÔNG ĐIỆP DƯỚI TRANG ---
st.divider()
c1, c2 = st.columns(2)
with c1: 
    st.markdown('<div class="card-pink">🌸 Vỗ về: Bạn đã làm rất tốt rồi!</div>', unsafe_allow_html=True)
with c2: 
    st.markdown('<div class="card-blue">🌊 Tĩnh lặng: Hít sâu một hơi nhé.</div>', unsafe_allow_html=True)
