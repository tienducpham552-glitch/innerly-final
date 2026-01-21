# ... (Các phần trên giữ nguyên)

# 5. Xử lý khi bạn nhập tin nhắn
if prompt := st.chat_input("Chia sẻ với mình nhé..."):
    # Lưu tin nhắn của bạn
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # --- SỬA DÒNG NÀY ---
            # Thay 'gemini-pro' bằng 'gemini-1.5-flash'
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            # Gửi tin nhắn
            response = model.generate_content(prompt)
            text_response = response.text
            
            # Hiển thị và lưu câu trả lời
            message_placeholder.write(text_response)
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"🚨 Có lỗi xảy ra: {str(e)}")
            st.info("Mẹo: Hãy kiểm tra lại API Key hoặc mạng internet của bạn.")
