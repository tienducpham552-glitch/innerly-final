import streamlit as st
import time

st.set_page_config(page_title="Hộp Thả Trôi", page_icon="🗑️")

st.header("Viết ra những gì đang làm phiền bạn...")
vent_text = st.text_area("Đừng giữ trong lòng, viết ra đây đi:", height=200)

if st.button("🌬️ Thả trôi nỗi buồn này"):
    if vent_text:
        placeholder = st.empty()
        # Logic hiệu ứng chữ tan biến của bạn
        for i in range(len(vent_text), 0, -5):
            placeholder.code(vent_text[:i] + " ☁️")
            time.sleep(0.04)
        st.balloons()
        st.session_state.tree_xp = st.session_state.get("tree_xp", 0) + 10
        st.success("Nỗi buồn đã tan thành mây khói!")
