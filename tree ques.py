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

# --- Page Config & CSS ---
st.set_page_config(page_title="ශාක පත්‍ර Quiz", page_icon="🍃", layout="centered")

st.markdown("""
    <style>
    /* මුළු App එකේම layout එක සකස් කිරීම */
    .block-container { 
        padding-top: 2rem !important; 
    }
    .stApp { background: linear-gradient(to right, #f1f8e9, #ffffff); }
    
    /* මාතෘකාවට පහළින් ඉඩක් ලබා දීම */
    h1 { 
        color: #2e7d32; 
        text-align: center; 
        font-size: 30px !important; 
        margin-bottom: 30px !important; 
        padding-bottom: 10px;
    }
    
    /* ප්‍රශ්න පේළිය මදක් පහළට ගැනීම */
    .main-quiz-container {
        margin-top: 20px;
    }
    
    .stSubheader { font-size: 20px !important; color: #1b5e20; }
    div[data-testid="stMarkdownContainer"] > p { font-size: 19px !important; }
    
    /* Button එකේ පෙනුම */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        background-color: #2e7d32; 
        color: white; 
        height: 3em;
        font-weight: bold;
    }
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

# --- UI Content ---
st.title("🍃 ශාක පත්‍ර හඳුනාගනිමු")

if st.session_state.current_q >= len(quiz_data):
    st.balloons()
    st.success(f"තරඟය අවසන්! ඔබේ ලකුණු: {st.session_state.score} / 25")
    if st.button("නැවත අරඹන්න"):
        for key in list(st.session_state.keys
