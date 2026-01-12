import streamlit as st
import os

# ===== UI =====
st.set_page_config(page_title="☁️ Cloud Wallet", layout="wide")
st.title("☁️ Munavvara's cloud wallet")

# ===== Papka va parol =====
FILES = "files"
PASSFILE = "password.txt"
os.makedirs(FILES, exist_ok=True)

if not os.path.exists(PASSFILE):
    with open(PASSFILE, "w") as f:
        f.write("1234")  # default parol

with open(PASSFILE) as f:
    APP_PASSWORD = f.read().strip()

# ===== Login =====
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    p = st.text_input("🔑 Parolni kiriting", type="password")
    if st.button("Kirish"):
        if p == APP_PASSWORD:
            st.session_state.auth = True
            st.experimental_rerun()  # Cloud mos
        else:
            st.error("Noto‘g‘ri parol")
    st.stop()

# ===== Fayl yuklash =====
uploaded = st.file_uploader("📤 Fayl tanlang")
if uploaded:
    file_path = os.path.join(FILES, uploaded.name)
    with open(file_path, "wb") as f:
        f.write(uploaded.read())
    st.success(f"Fayl muvaffaqiyatli yuklandi: {uploaded.name}")
    st.experimental_rerun()

# ===== Saqlangan fayllar =====
files = os.listdir(FILES)
for f in files:
    st.write(f)
    with open(os.path.join(FILES, f), "rb") as file:
        st.download_button("⬇ Yuklab olish", file, f)
