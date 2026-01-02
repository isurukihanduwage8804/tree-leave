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

st.set_page_config(page_title="ශාක පත්‍ර Quiz", page_icon="🍃")
st.title("🍃 ශාක පත්‍ර හඳුනාගනිමු")

# Session State පාලනය
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'options' not in st.session_state:
    st.session_state.options = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

# Game එක අවසන් නම්
if st.session_state.current_q >= len(quiz_data):
    st.balloons()
    st.success(f"तरඟය අවසන්! ඔබේ මුළු ලකුණු ප්‍රමාණය: {st.session_state.score} / 25")
    if st.button("නැවත අරඹන්න"):
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.options = None
        st.session_state.answered = False
        st.rerun()
else:
    img_name, correct_ans = quiz_data[st.session_state.current_q]
    
    # පිළිතුරු සකස් කිරීම
    if st.session_state.options is None:
        wrong_choices = random.sample([p for p in all_plants if p != correct_ans], 2)
        current_options = wrong_choices + [correct_ans]
        random.shuffle(current_options)
        st.session_state.options = current_options

    st.subheader(f"ප්‍රශ්නය {st.session_state.current_q + 1}:")
    
    # පින්තූරය පෙන්වීම
    found_image = False
    for ext in [".jpg", ".JPG", ".jpeg", ".png"]:
        full_path = img_name + ext
        if os.path.exists(full_path):
            st.image(full_path, width=400)
            found_image = True
            break
            
    if not found_image:
        st.error(f"❌ '{img_name}' පින්තූරය සොයාගත නොහැක.")

    # පිළිතුර තේරීම
    user_choice = st.radio("මෙම පත්‍රය අයිති කුමන ශාකයටද?", st.session_state.options, index=None, disabled=st.session_state.answered)

    # බොත්තම් පාලනය
    if not st.session_state.answered:
        if st.button("පිළිතුර පරීක්ෂා කරන්න ✅"):
            if user_choice is None:
                st.warning("කරුණාකර පිළිතුරක් තෝරන්න.")
            else:
                st.session_state.answered = True
                if user_choice == correct_ans:
                    st.session_state.score += 1
                    st.success("නිවැරදියි! 🎉")
                else:
                    st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_ans} ❌")
                st.rerun() # ප්‍රතිඵලය පෙන්වීමට rerun කරයි
    else:
        # පිළිතුර දුන් පසු පෙන්වන පණිවිඩය (පිටුව rerun වුවත් මෙය පවතී)
        if user_choice == correct_ans:
            st.success(f"නිවැරදියි! 🎉 (පිළිතුර: {correct_ans})")
        else:
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_ans} ❌")
            
        if st.button("ඊළඟ ප්‍රශ්නය ➡️"):
            st.session_state.current_q += 1
            st.session_state.options = None
            st.session_state.answered = False
            st.rerun()

st.sidebar.write(f"ලකුණු: {st.session_state.score} / {st.session_state.current_q if not st.session_state.answered else st.session_state.current_q + 1}")
