import streamlit as st
import random
import os

# --- 1. දත්ත පද්ධතිය ---
CATEGORY = "ශාක විද්‍යාව (Botany)"
all_plants = [
    "කොස්", "අඹ", "පොල්", "නෙළුම්", "රබර්", "තේ", "කෙසෙල්", "පුවක්", "කුඹුක්", "මහෝගනී",
    "තක්කාලි", "මිරිස්", "බතල", "කැරට්", "රාබු", "ගෝවා", "කරවිල", "පතෝල", "වට්ටක්කා", "දෙහි",
    "දොඩම්", "අන්නාසි", "පැපොල්", "පේර", "ජම්බු", "කජු", "දිවුල්", "බෙලි", "නාරං", "වෙරළු",
    "බෝධි", "නුග", "ඇසතු", "නා", "සල්", "අරලිය", "සපතේරු", "රෝස", "පිච්ච", "නිල්කටරොලු",
    "කුරුඳු", "කරාබුනැටි", "ගම්මිරිස්", "සාදික්කා", "ඉඟුරු", "කහ", "එනසාල්", "ගොටුකොළ", "කංකුන්", "මුකුණුවැන්න"
]

quiz_data = [
    ("1", "කොස්"), ("2", "අඹ"), ("3", "පොල්"), ("4", "නෙළුම්"), ("5", "රබර්"),
    ("6", "තේ"), ("7", "කෙසෙල්"), ("8", "පුවක්"), ("9", "කුඹුක්"), ("10", "මහෝගනී"),
    ("11", "තක්කාලි"), ("12", "මිරිස්"), ("13", "බතල"), ("14", "කැරට්"), ("15", "රාබු"),
    ("16", "ගෝවා"), ("17", "කරවිල"), ("18", "පතෝල"), ("19", "වට්ටක්කා"), ("20", "දෙහි"),
    ("21", "දොඩම්"), ("22", "අන්නාසි"), ("23", "පැපොල්"), ("24", "පේර"), ("25", "ජම්බු")
]

# --- 2. Page Config & Styling ---
st.set_page_config(page_title="ශාක පත්‍ර Quiz", page_icon="🍃", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #f1f8e9, #ffffff); }
    .main-title { color: #2e7d32; text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 20px; }
    .cat-box { background-color: #c8e6c9; color: #1b5e20; padding: 5px 15px; border-radius: 15px; font-size: 14px; font-weight: bold; margin-bottom: 10px; display: inline-block; }
    .stButton > button { width: 100%; border-radius: 10px; background-color: #2e7d32; color: white; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Session State ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'options' not in st.session_state: st.session_state.options = None
if 'answered' not in st.session_state: st.session_state.answered = False

# --- 4. Logic Functions ---
def check_ans():
    if st.session_state.user_choice is not None and not st.session_state.answered:
        st.session_state.answered = True
        _, correct = quiz_data[st.session_state.current_q]
        if st.session_state.user_choice == correct:
            st.session_state.score += 1

def next_q():
    st.session_state.current_q += 1
    st.session_state.options = None
    st.session_state.answered = False

# --- 5. UI Layout ---
st.markdown(f'<div style="text-align: center;"><span class="cat-box">Category: {CATEGORY}</span></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🍃 ශාක පත්‍ර හඳුනාගැනීමේ අභියෝගය</div>', unsafe_allow_html=True)

# Quiz අවසන් වූ පසු පෙන්වන කොටස
if st.session_state.current_q >= len(quiz_data):
    st.balloons()
    st.success(f"සියල්ල අවසන්! ඔබේ ලකුණු ප්‍රමාණය: {st.session_state.score} / 25")
    if st.button("නැවත අරඹන්න"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    img_name, correct_ans = quiz_data[st.session_state.current_q]
    
    if st.session_state.options is None:
        wrong = random.sample([p for p in all_plants if p != correct_ans], 3)
        opts = wrong + [correct_ans]
        random.shuffle(opts)
        st.session_state.options = opts

    st.subheader(f"ප්‍රශ්නය {st.session_state.current_q + 1} / 25")

    # Layout බෙදීම
    col1, col2 = st.columns([1.2, 1], gap="medium")

    with col1:
        # පින්තූරය පෙන්වීම
        found_path = None
        for ext in [".jpg", ".JPG", ".jpeg", ".png", ".PNG"]:
            if os.path.exists(f"{img_name}{ext}"):
                found_path = f"{img_name}{ext}"
                break
        
        if found_path:
            st.image(found_path, width=320)
        else:
            st.error(f"පින්තූරය ({img_name}) හමු නොවීය ❌")

    with col2:
        st.write("**පින්තූරයේ ඇති ශාකය කුමක්ද?**")
        st.radio("පිළිතුරක් තෝරන්න:", st.session_state.options, 
                 index=None, key="user_choice", on_change=check_ans, 
                 disabled=st.session_state.answered, label_visibility="collapsed")

        if st.session_state.answered:
            st.write("---")
            if st.session_state.user_choice == correct_ans:
                st.success("නිවැරදියි! 🎉")
            else:
                st.error(f"වැරදියි! පිළිතුර: {correct_ans}")
            
            st.button("ඊළඟ ප්‍රශ්නය ➡️", on_click=next_q)

# Sidebar - Progress & Score
st.sidebar.markdown(f"### 📊 ඔබේ දක්ෂතාවය")
st.sidebar.write(f"**ලකුණු:** {st.session_state.score}")

# Progress bar එක error එකක් නැතිව පෙන්වීම
progress_val = min((st.session_state.current_q) / 25, 1.0)
st.sidebar.progress(progress_val)
st.sidebar.write(f"ප්‍රගතිය: {int(progress_val * 100)}%")
