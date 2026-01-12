import streamlit as st
import os
import json
from PIL import Image

# ----------------- UI ni tozalash -----------------
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

# ----------------- Yashirin papkalar -----------------
BASE = "/data"
FILES = BASE + "/files"
PASSFILE = BASE + "/password.txt"

os.makedirs(FILES, exist_ok=True)

# ----------------- Parol -----------------
if not os.path.exists(PASSFILE):
    with open(PASSFILE, "w") as f:
        f.write("1234")   # default parol

with open(PASSFILE) as f:
    APP_PASSWORD = f.read().strip()

# ----------------- Login -----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    p = st.text_input("🔑 Parolni kiriting", type="password")
    if st.button("Kirish"):
        if p == APP_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Noto‘g‘ri parol")
    st.stop()

# ----------------- Fayl yuklash -----------------
st.subheader("📤 Fayl yuklash")
uploaded = st.file_uploader("Fayl tanlang")
if uploaded:
    with open(os.path.join(FILES, uploaded.name), "wb") as f:
        f.write(uploaded.read())
    st.success("Yuklandi")

# ----------------- Fayllarni o‘qish -----------------
files = os.listdir(FILES)

images = [f for f in files if f.lower().endswith((".png",".jpg",".jpeg",".webp"))]
videos = [f for f in files if f.lower().endswith((".mp4",".mov",".avi"))]
others = [f for f in files if f not in images and f not in videos]

tabs = st.tabs(["🖼 Rasmlar","🎬 Videolar","📁 Ma’lumotlar"])

# ---------- Rasmlar ----------
with tabs[0]:
    for f in images:
        st.image(os.path.join(FILES,f), width=300)
        if st.button(f"❌ {f}", key=f):
            os.remove(os.path.join(FILES,f))
            st.rerun()

# ---------- Videolar ----------
with tabs[1]:
    for f in videos:
        st.video(os.path.join(FILES,f))
        if st.button(f"❌ {f}", key=f+"v"):
            os.remove(os.path.join(FILES,f))
            st.rerun()

# ---------- Boshqa ----------
with tabs[2]:
    for f in others:
        st.write(f)
        with open(os.path.join(FILES,f),"rb") as file:
            st.download_button("⬇ Yuklab olish", file, f)
        if st.button(f"❌ {f}", key=f+"o"):
            os.remove(os.path.join(FILES,f))
            st.rerun()

# ----------------- Parolni o‘zgartirish -----------------
st.markdown("---")
with st.expander("🔑 Parolni o‘zgartirish"):
    new = st.text_input("Yangi parol", type="password")
    confirm = st.text_input("Tasdiqlash", type="password")
    if st.button("Saqlash"):
        if new and new == confirm:
            with open(PASSFILE,"w") as f:
                f.write(new)
            st.success("Parol yangilandi")
        else:
            st.error("Parollar mos emas")

# import streamlit as st
# import os
# import json

# # ----------------- UI -----------------
# st.set_page_config(page_title="☁️ My Cloud", layout="wide")
# st.markdown("""
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# a[href*="github.com"] {display: none !important;}
# button[kind="header"] {display:none !important;}
# </style>
# """, unsafe_allow_html=True)

# st.title("☁️ My Private Cloud Drive")

# # ----------------- Papkalar -----------------
# BASE = "data"
# FILES = os.path.join(BASE, "files")
# PASSFILE = os.path.join(BASE, "password.txt")
# NOTESFILE = os.path.join(BASE, "notes.json")

# os.makedirs(FILES, exist_ok=True)

# # ----------------- Parol -----------------
# if not os.path.exists(PASSFILE):
#     with open(PASSFILE, "w") as f:
#         f.write("1234")  # default parol

# APP_PASSWORD = open(PASSFILE).read().strip()

# # ----------------- Zametkalar -----------------
# if not os.path.exists(NOTESFILE):
#     json.dump([], open(NOTESFILE, "w"))
# NOTES = json.load(open(NOTESFILE, "r"))

# # ----------------- Session state -----------------
# if "auth" not in st.session_state:
#     st.session_state.auth = False
# if "refresh" not in st.session_state:
#     st.session_state.refresh = False

# # ----------------- Login -----------------
# if not st.session_state.auth:
#     p = st.text_input("🔑 Parolni kiriting", type="password")
#     if st.button("Kirish"):
#         if p == APP_PASSWORD:
#             st.session_state.auth = True
#             st.session_state.refresh = not st.session_state.refresh  # flag to refresh
#         else:
#             st.error("❌ Noto‘g‘ri parol")
#     st.stop()

# # ----------------- Fayl yuklash -----------------
# st.subheader("📤 Fayl yuklash")
# uploaded = st.file_uploader("Fayl tanlang")
# if uploaded:
#     save_path = os.path.join(FILES, uploaded.name)
#     with open(save_path,"wb") as f:
#         f.write(uploaded.read())
#     st.success(f"✅ Yuklandi: {uploaded.name}")
#     st.session_state.refresh = not st.session_state.refresh  # refresh

# # ----------------- Fayllarni ko‘rsatish -----------------
# def show_files():
#     files = os.listdir(FILES)
#     images = [f for f in files if f.lower().endswith((".png",".jpg",".jpeg",".webp"))]
#     videos = [f for f in files if f.lower().endswith((".mp4",".mov",".avi"))]
#     others = [f for f in files if f not in images + videos]

#     tabs = st.tabs(["🖼 Rasmlar","🎬 Videolar","📁 Boshqalar","📝 Zametkalar"])

#     # ---------- Rasmlar ----------
#     with tabs[0]:
#         for i,f in enumerate(images):
#             st.image(os.path.join(FILES,f), width=300)
#             if st.radio(f"🗑 O‘chirish: {f}? Ha / Yo‘q", ["Yo‘q","Ha"], key=f"confirm_img_{i}") == "Ha":
#                 os.remove(os.path.join(FILES,f))
#                 st.success(f"❌ O‘chirildi: {f}")
#                 st.session_state.refresh = not st.session_state.refresh
#                 st.experimental_rerun()
#             st.download_button("⬇ Yuklab olish", open(os.path.join(FILES,f),"rb"), f, key=f"dl_img_{i}")

#     # ---------- Videolar ----------
#     with tabs[1]:
#         for i,f in enumerate(videos):
#             st.video(os.path.join(FILES,f))
#             if st.radio(f"🗑 O‘chirish: {f}? Ha / Yo‘q", ["Yo‘q","Ha"], key=f"confirm_vid_{i}") == "Ha":
#                 os.remove(os.path.join(FILES,f))
#                 st.success(f"❌ O‘chirildi: {f}")
#                 st.session_state.refresh = not st.session_state.refresh
#                 st.experimental_rerun()
#             st.download_button("⬇ Yuklab olish", open(os.path.join(FILES,f),"rb"), f, key=f"dl_vid_{i}")

#     # ---------- Boshqalar ----------
#     with tabs[2]:
#         for i,f in enumerate(others):
#             st.write(f)
#             with open(os.path.join(FILES,f),"rb") as file:
#                 st.download_button("⬇ Yuklab olish", file, f, key=f"dl_other_{i}")
#             if st.radio(f"🗑 O‘chirish: {f}? Ha / Yo‘q", ["Yo‘q","Ha"], key=f"confirm_other_{i}") == "Ha":
#                 os.remove(os.path.join(FILES,f))
#                 st.success(f"❌ O‘chirildi: {f}")
#                 st.session_state.refresh = not st.session_state.refresh
#                 st.experimental_rerun()

#     # ---------- Zametkalar ----------
#     with tabs[3]:
#         # Yangi zametka
#         new_note_key = f"new_note_{st.session_state.refresh}"  # unikal key
#         new_note = st.text_area("✏️ Zametka yozing", key=new_note_key)
#         if st.button("Saqlash", key=f"save_note_{st.session_state.refresh}"):
#             if new_note.strip():
#                 NOTES.append(new_note.strip())
#                 json.dump(NOTES, open(NOTESFILE,"w"))
#                 st.success("✅ Zametka saqlandi")
#                 st.session_state.refresh = not st.session_state.refresh
#                 st.experimental_rerun()
#         st.markdown("---")
#         # Eski zametkalar
#         for i,n in enumerate(NOTES):
#             st.write(n)
#             if st.radio(f"🗑 O‘chirish: {i}-chi zametka? Ha / Yo‘q", ["Yo‘q","Ha"], key=f"confirm_note_{i}") == "Ha":
#                 NOTES.pop(i)
#                 json.dump(NOTES, open(NOTESFILE,"w"))
#                 st.success(f"❌ O‘chirildi: {i}-chi zametka")
#                 st.session_state.refresh = not st.session_state.refresh
#                 st.experimental_rerun()

# show_files()

# # ----------------- Parolni o‘zgartirish -----------------
# st.markdown("---")
# with st.expander("🔑 Parolni o‘zgartirish"):
#     new = st.text_input("Yangi parol", type="password", key="new_pass")
#     confirm = st.text_input("Tasdiqlash", type="password", key="confirm_pass")
#     if st.button("Saqlash parolni", key="save_pass"):
#         if new and new==confirm:
#             with open(PASSFILE,"w") as f:
#                 f.write(new)
#             st.success("✅ Parol yangilandi")
#         else:
#             st.error("❌ Parollar mos emas yoki bo‘sh")


# cd "C:\Users\hp\Desktop\python\web_app" 
# streamlit run  app.py   