import streamlit as st
import os
from PIL import Image

# ===== UI ni tozalash =====
st.set_page_config(page_title="☁️ My Cloud", layout="wide")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
a[href*="github.com"] {display: none !important;}
button[kind="header"] {display:none !important;}
</style>
""", unsafe_allow_html=True)

st.title("☁️ Munavvara's cloud wallet")

# ===== Papkalar =====
BASE = "."  # App papkasi ichida
FILES = os.path.join(BASE, "files")
PASSFILE = os.path.join(BASE, "password.txt")

os.makedirs(FILES, exist_ok=True)

# ===== Parol =====
if not os.path.exists(PASSFILE):
    with open(PASSFILE, "w") as f:
        f.write("1234")   # default parol

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
            st.runtime.legacy_rerun()  # Cloud mos rerun
        else:
            st.error("Noto‘g‘ri parol")
    st.stop()

# ===== Fayl yuklash =====
st.subheader("📤 Fayl yuklash")
uploaded = st.file_uploader("Fayl tanlang")
if uploaded:
    file_path = os.path.join(FILES, uploaded.name)
    with open(file_path, "wb") as f:
        f.write(uploaded.read())
    st.success(f"Fayl muvaffaqiyatli yuklandi: {uploaded.name}")
    st.runtime.legacy_rerun()

# ===== Fayllarni o‘qish =====
files = os.listdir(FILES)
images = [f for f in files if f.lower().endswith((".png",".jpg",".jpeg",".webp"))]
videos = [f for f in files if f.lower().endswith((".mp4",".mov",".avi"))]
others = [f for f in files if f not in images and f not in videos]

tabs = st.tabs(["🖼 Rasmlar","🎬 Videolar","📁 Ma’lumotlar"])

# ----- Rasmlar -----
with tabs[0]:
    for f in images:
        st.image(os.path.join(FILES,f), width=300)
        if st.button(f"❌ {f}", key=f):
            os.remove(os.path.join(FILES,f))
            st.runtime.legacy_rerun()

# ----- Videolar -----
with tabs[1]:
    for f in videos:
        st.video(os.path.join(FILES,f))
        if st.button(f"❌ {f}", key=f+"v"):
            os.remove(os.path.join(FILES,f))
            st.runtime.legacy_rerun()

# ----- Boshqa -----
with tabs[2]:
    for f in others:
        st.write(f)
        with open(os.path.join(FILES,f),"rb") as file:
            st.download_button("⬇ Yuklab olish", file, f)
        if st.button(f"❌ {f}", key=f+"o"):
            os.remove(os.path.join(FILES,f))
            st.runtime.legacy_rerun()

# ===== Parolni o‘zgartirish =====
st.markdown("---")
with st.expander("🔑 Parolni o‘zgartirish"):
    new = st.text_input("Yangi parol", type="password", key="new")
    confirm = st.text_input("Tasdiqlash", type="password", key="confirm")
    if st.button("Saqlash"):
        if new and new == confirm:
            with open(PASSFILE,"w") as f:
                f.write(new)
            st.success("Parol yangilandi")
            st.runtime.legacy_rerun()
        else:
            st.error("Parollar mos emas")
