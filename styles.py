import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"] { font-family: 'Quicksand', sans-serif; }
        
        /* Nền Gradient đặc trưng */
        .stApp {
            background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
            background-attachment: fixed;
        }

        /* Thiết kế Card */
        .card-inner {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }

        .action-list {
            background: rgba(255, 255, 255, 0.6);
            padding: 15px;
            border-radius: 12px;
            text-align: left;
            border-left: 4px solid #ff9a9e;
        }
    </style>
    """, unsafe_allow_html=True)