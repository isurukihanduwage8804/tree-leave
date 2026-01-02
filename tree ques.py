import streamlit as st
import random
import os

# 1. ශාක වර්ග 50ක ලැයිස්තුව
all_plants = [
    "කොස්", "අඹ", "පොල්", "නෙළුම්", "රබර්", "තේ", "කෙසෙල්", "පුවක්", "කුඹුක්", "මහෝගනී",
    "තක්කාලි", "මිරිස්", "බතල", "කැරට්", "රාබු", "ගෝවා", "කරවිල", "පතෝල", "වට්ටක්කා", "දෙහි",
    "දොඩම්", "අන්නාසි", "පැපොල්", "පේර", "ජම්බු", "කජු", "දිවුල්", "බෙලි", "නාරං", "වෙරළු",
    "බෝධි", "නුග", "ඇසතු", "නා", "සල්", "අරලිය", "සපතේරු", "රෝස", "පිච්ච", "නිල්කටරොලු",
    "කුරුඳු", "කරාබුනැටි", "ගම්මිරිස්", "සාදික්කා", "ඉඟුරු", "කහ", "එනසාල්", "ගොටුකොළ", "කංකුන්", "මුකුණුවැන්න"
]

# 2. ප්‍රශ්න 25
quiz_data = [
    ("1", "කොස්"), ("2", "අඹ"), ("3", "පොල්"), ("4", "නෙළුම්"), ("5", "රබර්"),
    ("6", "තේ"), ("7", "කෙසෙල්"), ("8", "පුවක්"), ("9", "කුඹුක්"), ("10", "මහෝගනී"),
    ("11", "තක්කාලි"), ("12", "මිරිස්"), ("13", "බතල"), ("14", "කැරට්"), ("15", "රාබු"),
    ("16", "ගෝවා"), ("17", "කරවිල"), ("18", "පතෝල"), ("19", "වට්ටක්කා"), ("20", "දෙහි"),
    ("21", "දොඩම්"), ("22", "අන්නාසි"), ("23", "පැපොල්"), ("24", "පේර"), ("25", "ජම්බු")
]

# --- පිටුව ලස්සන කිරීමට CSS ---
st.set_page_config(page_title="ශාක පත්‍ර Quiz", page_icon="🍃", layout="centered")

st.markdown("""
    <style>
    /* පසුබිම ලස්සන කිරීම */
    .stApp {
        background: linear-gradient(to right, #e8f5e9, #ffffff);
    }
    /* අකුරු ලොකු කිරීම */
    h1 { color: #2e7d32; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stSubheader { font-size: 24px !important; font-weight: bold; color: #1b5e20; }
    /* Radio buttons (පිළිතුරු) වල අකුරු ලොකු කිරීම */
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px !important;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State පාලනය
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'options' not in st.session_state:
    st.session_state.options = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

st.title("🍃 ශාක පත්‍ර හඳුනාගනිමු")

# Game එක අවසන් නම්
if st.session_state.current_q >= len(quiz_data):
    st.balloons()
    st.markdown(f"<h2 style='text-align: center; color: #2e7d32;'>තරඟය අවසන්!</h2>", unsafe_allow_html=True)
    st.success(f"ඔබේ මුළු ලකුණු ප්‍රමාණය: {st.session_state.score} / 25")
    if st.button("නැවත අරඹන්න"):
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.options = None
        st.session_state.answered = False
        st.rerun()
else:
    img_name, correct_ans = quiz_data[st.session_state.current_q]
    
    # පිළිතුරු 4ක් සකස් කිරීම
    if st.session_state.options is None:
        # වැරදි පිළිතුරු 3ක් තෝරා ගැනීම
        wrong_choices = random.sample([p for p in all_plants if p != correct_ans], 3)
        current_options = wrong_choices + [correct_ans]
        random.shuffle(current_options)
        st.session_state.options = current_options

    st.subheader(f"ප්‍රශ්නය {st.session_state.current_q + 1}:")
    
    # පින්තූරය පෙන්වීම
    found_image = False
    for ext in [".jpg", ".JPG", ".jpeg", ".png"]:
        full_path = img_name + ext
        if os.path.exists(full_path):
            st.image(full_path, width=450)
            found_image = True
            break
            
    if not found_image:
        st.error(f"❌ '{img_name}' පින්තූරය සොයාගත නොහැක.")

    # පිළිතුර තේරීම
    st.markdown("### පිළිතුර තෝරන්න:")
    user_choice = st.radio("", st.session_state.options, index=None, disabled=st.session_state.answered, key="quiz_radio")

    # බොත්තම් පාලනය
    if not st.session_state.answered:
        if st.button("පිළිතුර පරීක්ෂා කරන්න ✅"):
            if user_choice is None:
                st.warning("කරුණාකර පිළිතුරක් තෝරන්න.")
            else:
                st.session_state.answered = True
                if user_choice == correct_ans:
                    st.session_state.score += 1
                st.rerun()
    else:
        # ප්‍රතිඵලය පෙන්වීම
        if user_choice == correct_ans:
            st.success(f"නිවැරදියි! 🎉 (පිළිතුර: {correct_ans})")
        else:
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_ans} ❌")
            
        if st.button("ඊළඟ ප්‍රශ්නය ➡️"):
            st.session_state.current_q += 1
            st.session_state.options = None
            st.session_state.answered = False
            st.rerun()

# Sidebar එකේ ලකුණු පෙන්වීම
st.sidebar.markdown(f"## 🏆 ලකුණු පුවරුව")
st.sidebar.markdown(f"### {st.session_state.score} / {st.session_state.current_q if not st.session_state.answered else st.session_state.current_q + 1}")
