import streamlit as st
import random
import string
import datetime
import io
import qrcode
from random_word import RandomWords
from languages import languages 

# SELECT LANGUAGE
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

# Language Selection
selected_lang = st.sidebar.selectbox("🌎 Select Language | زبان منتخب کریں | 选择语言 | اختر اللغة", list(languages.keys()))
st.session_state.selected_language = selected_lang
L = languages[selected_lang] 

# Random Words Object
r = RandomWords()

def password_generator(length, use_digits, special_char, similar_charc):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if special_char:
        characters += string.punctuation
    if similar_charc:
        characters = characters.translate(str.maketrans("", "", "O0l1I"))
    return "".join(random.choice(characters) for _ in range(length))

# Check password strength
def check_strength(password):
    length = len(password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    
    if length >= 12 and has_digit and has_special:
        return "🟢 Strong"
    elif length >= 8 and (has_digit or has_special):
        return "🟡 Medium"
    else:
        return "🔴 Weak"

st.title(L["title"])
length = st.slider(L["length"], 6, 20, 12)
use_digits = st.checkbox(L["digits"])
special_char = st.checkbox(L["special_char"])
exclude_similar = st.checkbox(L["exclude_similar"])
num_passwords = st.number_input(L["num_passwords"], 1, 10, 1)

if st.button(L["generate"]):
    passwords = [password_generator(length, use_digits, special_char, exclude_similar) for _ in range(num_passwords)]
    
    for i, password in enumerate(passwords, 1):
        strength = check_strength(password)
        st.text_input(f"🔑 Password {i}:", password, disabled=True)
        
        # Strength meter
        progress = {"🔴 Weak": 0.3, "🟡 Medium": 0.6, "🟢 Strong": 1.0}
        st.progress(progress[strength])
        st.write(f"🔍 {L['strength']}: {strength}")

        # Password expiry reminder
        expiry_date = datetime.date.today() + datetime.timedelta(days=30)
        st.write(f"🔔 {L['expiry_reminder']}: **{expiry_date}**")

        # QR Code Generation
        img = qrcode.make(password)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="📱 Scan to Save Password")

    st.success(L["success"])

# Passphrase Generator
st.subheader(L["Generate_Random_Password"])
num_words = st.slider(L["num_words"], 2, 5, 3)

def passphrase_generator(num_words):
    return "-".join([r.get_random_word() for _ in range(num_words)])

if st.button(L["Generate_Random_Password"]):
    passphrase = passphrase_generator(num_words)
    st.write(f"📝 {L['Generate_Random_Password']}: **{passphrase}**")
    st.success(L["success"])

st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: #555;">
        Created by <strong>NēA⚡ </strong>
    </div>
    """,
    unsafe_allow_html=True
)