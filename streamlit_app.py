import streamlit as st
from styles import apply_styles

st.set_page_config(page_title="Innerly Studio", page_icon="🧸", layout="wide")
apply_styles()

# Khởi tạo dữ liệu hệ thống
if "tree_xp" not in st.session_state: st.session_state.tree_xp = 0
if "messages" not in st.session_state: st.session_state.messages = []
if "flipped_cards" not in st.session_state: st.session_state.flipped_cards = {}

# --- SIDEBAR CHUNG ---
with st.sidebar:
    st.title("🧸 Innerly Studio")
    st.subheader("👤 Hồ sơ cá nhân")
    st.session_state.user_name = st.text_input("Tên cậu là gì?", "Bạn")
    st.session_state.user_gender = st.radio("Chế độ hiển thị:", ["Nữ 🌸", "Nam 🧢"], horizontal=True)
    
    st.divider()
    st.write(f"🌟 Cấp độ: {st.session_state.tree_xp} XP")
    st.progress(min((st.session_state.tree_xp % 100) / 100, 1.0))

# --- NỘI DUNG TRANG CHỦ ---
st.write("# Chào mừng cậu đến với không gian của Innerly! ✨")
st.write(f"Chào **{st.session_state.user_name}**, hôm nay cậu thấy thế nào?")
st.info("👈 Hãy chọn các tính năng ở thanh bên trái để bắt đầu hành trình chữa lành nhé!")

# Hiển thị ảnh minh họa hoặc châm ngôn
st.image("https://images.unsplash.com/photo-1516589174184-c68526514b48?q=80&w=1000&auto=format&fit=crop", use_container_width=True)
