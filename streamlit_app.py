import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN (Hồng & Xanh) ---
st.set_page_config(page_title="Innerly Studio", page_icon="🧸", layout="wide")
st.markdown("""<style>
    .stApp { background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%); }
    .card-pink { background-color: #ffe4e1; border: 2px solid #ffb6c1; padding: 20px; border-radius: 15px; color: #d02090; }
    .card-blue { background-color: #e0ffff; border: 2px solid #afeeee; padding: 20px; border-radius: 15px; color: #008b8b; }
</style>""", unsafe_allow_html=True)

# --- KẾT NỐI AI ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

def get_ai_response(prompt):
    # Thử lần lượt các đời AI để tránh lỗi 404
    models = ['gemini-1.5-flash', 'gemini-pro']
    for m in models:
        try:
            model = genai.GenerativeModel(m)
            return model.generate_content(prompt).text
        except:
            continue
    return "🚨 Innerly đang quá tải hoặc Key của bạn gặp sự cố. Bạn hãy kiểm tra lại Key nhé!"

# --- GIAO DIỆN CHÍNH ---
st.title("Tâm sự cùng Innerly 🧸")
if "history" not in st.session_state: st.session_state.history = []

for msg in st.session_state.history:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Hãy nói gì đó với mình..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        res = get_ai_response(prompt)
        st.write(res)
        st.session_state.history.append({"role": "assistant", "content": res})

st.divider()
c1, c2 = st.columns(2)
with c1: st.markdown('<div class="card-pink">🌸 Vỗ về: Bạn đã làm rất tốt rồi!</div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card-blue">🌊 Tĩnh lặng: Hít sâu một hơi nhé.</div>', unsafe_allow_html=True)
