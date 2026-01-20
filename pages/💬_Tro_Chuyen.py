import streamlit as st
import google.generativeai as genai
from styles import apply_styles

apply_styles()
st.header("🧸 Tâm sự cùng Innerly")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Chia sẻ cùng tớ nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Hướng dẫn AI cách xưng hô theo tuổi/tên đã lưu ở main.py
            context = f"Tên user là {st.session_state.user_name}. Hãy xưng hô thân thiện."
            res = model.generate_content(context + prompt)
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.error("Innerly đang bận một chút, thử lại sau nhé!")
