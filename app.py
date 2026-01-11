import streamlit as st
import os
import requests
from io import BytesIO

# ======================
# STREAMLIT UI SECURITY
# ======================
st.set_page_config(page_title="My Private App", layout="wide")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ======================
# SECRETS / TOKEN
# ======================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "jumaniyozusanov/storage")

if GITHUB_TOKEN == "":
    st.error("❌ GitHub token topilmadi! App ishlamaydi. Secrets qo‘ying va Reboot qiling.")
    st.stop()

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ======================
# LOGIN PANEL
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "password" not in st.session_state:
    st.session_state.password = "1234"  # default parol, keyin o‘zgartiriladi

def login():
    if st.session_state.input_password == st.session_state.password:
        st.session_state.logged_in = True
    else:
        st.error("❌ Noto‘g‘ri parol!")

if not st.session_state.logged_in:
    st.title("🔒 Kirish")
    st.session_state.input_password = st.text_input("Parolni kiriting", type="password")
    st.button("Kirish", on_click=login)
    st.stop()

# ======================
# DASHBOARD
# ======================
st.title("✅ Welcome to Private App")

# ======================
# PAROL O'ZGARTIRISH
# ======================
with st.expander("🔑 Parolni o‘zgartirish", expanded=False):
    old_pw = st.text_input("Joriy parolni kiriting", type="password")
    new_pw = st.text_input("Yangi parolni kiriting", type="password")
    if st.button("O‘zgartirish"):
        if old_pw == st.session_state.password:
            st.session_state.password = new_pw
            st.success("Parol muvaffaqiyatli o‘zgartirildi ✅")
        else:
            st.error("❌ Joriy parol noto‘g‘ri!")

# ======================
# FILE UPLOAD / DISPLAY
# ======================
st.header("📁 Fayllar bo‘limi")

uploaded_file = st.file_uploader("Rasm yoki video yuklash", type=["png","jpg","jpeg","mp4","mov"])
if uploaded_file:
    st.success(f"{uploaded_file.name} yuklandi ✅")
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file)
    elif uploaded_file.type.startswith("video/"):
        st.video(uploaded_file)

# ======================
# GITHUB PRIVATE REPO FILES
# ======================
st.header("🌐 GitHub Private Repo Fayllari")

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/"

response = requests.get(GITHUB_API_URL, headers=HEADERS)
if response.status_code == 200:
    files = response.json()
    for file in files:
        st.write(f"- [{file['name']}]({file['download_url']})")
else:
    st.error(f"❌ GitHub fayllarni olishda xatolik ({response.status_code})")
