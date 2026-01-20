import streamlit as st
from styles import apply_styles
# Giả sử bạn để DATA_NU/NAM vào file data.py, nếu không hãy dán trực tiếp vào đây
from data import DATA_NU, DATA_NAM 

apply_styles()
st.header("🌿 Thông điệp cho tâm hồn")

user_gender = st.session_state.get("user_gender", "Nữ 🌸")
current_data = DATA_NU if "Nữ" in user_gender else DATA_NAM

tabs = st.tabs(list(current_data.keys()))

for i, (group_name, cards) in enumerate(current_data.items()):
    with tabs[i]:
        cols = st.columns(3)
        for idx, card in enumerate(cards):
            card_key = f"card_{card['id']}"
            with cols[idx % 3]:
                if not st.session_state.flipped_cards.get(card_key, False):
                    st.markdown(f"""<div class="card-inner">
                        <div style="font-size:50px">{card['icon']}</div>
                        <h3>{card['title']}</h3>
                        <p><i>"{card['front']}"</i></p>
                    </div>""", unsafe_allow_html=True)
                    if st.button("🌀 Lật thẻ", key=f"btn_{card_key}"):
                        st.session_state.flipped_cards[card_key] = True
                        st.rerun()
                else:
                    st.markdown(f"""<div class="card-inner" style="border: 2px solid #ffb6c1">
                        <div class="action-list">{card['back'].replace(chr(10), '<br>')}</div>
                        <p style="margin-top:10px; font-weight:bold">{card['quote']}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button("↩️ Úp lại", key=f"rev_{card_key}"):
                        st.session_state.flipped_cards[card_key] = False
                        st.rerun()
