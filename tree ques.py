import streamlit as st
import random
import os

# 1. දත්ත පද්ධතිය
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

# --- Page Config & CSS (Scroll ඉවත් කිරීම සඳහා) ---
st.set_page_config(page_title="ශාක පත්‍ර Quiz", page_icon="🍃", layout="centered")

st.markdown("""
    <style>
    /* මුළු පිටුවේම උඩ ඉඩ අඩු කිරීම */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    .stApp { background: linear-gradient(to right, #f1f8e9, #ffffff); }
    h1 { color: #2e7d32; text-align: center; font-size: 28px !important; margin-bottom: 0px; }
    .stSubheader { font-size: 20px !important; color: #1b5e20; margin-top: 0px; }
    /* පිළිතුරු වල අකුරු */
    div[data-testid="stMarkdownContainer"] > p { font-size: 18px !important; }
    /* Radio button එකේ ඉඩ අඩු කිරීම */
    div[data-testid="stRadio"] > label { padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Session State ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'options' not in st.session_state: st.session_state.options = None
if 'answered' not in st.session_state: st.session_state.answered = False

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
    if 'user_choice' in st.session_state:
        st.session_state.user_choice = None

# --- UI Content ---
st.title("🍃 ශාක පත්‍ර හඳුනාගනිමු")

if st.session_state.current_q >= len(quiz_data):
    st.balloons()
    st.success(f"තරඟය අවසන්! ඔබේ ලකුණු: {st.session_state.score} / 25")
    if st.button("නැවත අරඹන්න"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
else:
    img_name, correct_ans = quiz_data[st.session_state.current_q]
    
    if st.session_state.options is None:
        wrong = random.sample([p for p in all_plants if p != correct_ans], 3)
        opts = wrong + [correct_ans]
        random.shuffle(opts)
        st.session_state.options = opts

    st.subheader(f"ප්‍රශ්නය {st.session_state.current_q + 1}:")
    
    # පින්තූරය (
