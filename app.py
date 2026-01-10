import streamlit as st
import requests
import base64
import json
import os

st.set_page_config(page_title="☁️ My Cloud Drive", layout="wide")
st.title("☁️ My Personal Cloud Drive")

# ----------------------
# Local password fayli
PASSWORD_FILE = "password.json"
if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "w") as f:
        json.dump({"password": "1234"}, f)  # default parol

# password o'qish
with open(PASSWORD_FILE, "r") as f:
    APP_PASSWORD = json.load(f)["password"]

# ----------------------
# Secrets (GitHub)
TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]
HEADERS = {"Authorization": f"token {TOKEN}"}

# ----------------------
# 1️⃣ Login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    user_pass = st.text_input("Parolni kiriting:", type="password")
    if st.button("Kirish"):
        if user_pass == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("✅ Tizimga kirdingiz")
        else:
            st.error("❌ Noto‘g‘ri parol")
    st.stop()

# ----------------------
# 2️⃣ Tabs: Rasmlar, Videolar, Boshqalar
tabs = st.tabs(["Rasmlar", "Videolar", "Boshqalar"])
file_types = {
    "Rasmlar": [".png", ".jpg", ".jpeg", ".webp"],
    "Videolar": [".mp4", ".mov", ".avi"],
    "Boshqalar": []
}

# ----------------------
# 3️⃣ Fayl upload
uploaded = st.file_uploader("📤 Fayl yuklash")
if uploaded:
    content = uploaded.read()
    encoded_content = base64.b64encode(content).decode()
    path = f"storage/{uploaded.name}"
    url_put = f"https://api.github.com/repos/{REPO}/contents/{path}"
    data = {"message": f"Upload {uploaded.name}", "content": encoded_content}
    response = requests.put(url_put, json=data, headers=HEADERS)

    if response.status_code == 201:
        st.success(f"✅ Saqlandi: {uploaded.name}")
    elif response.status_code == 422:
        st.warning("⚠️ Bu fayl allaqachon mavjud")
    else:
        st.error(f"Xatolik: {response.status_code} - {response.text}")

# ----------------------
# 4️⃣ Fayllarni olish va bo‘limlash
url_get = f"https://api.github.com/repos/{REPO}/contents/storage?ref=main"
response = requests.get(url_get, headers=HEADERS)
files = []
if response.status_code == 200:
    files = response.json()
elif response.status_code == 404:
    st.info("📂 Storage papkasi mavjud emas, birinchi faylni yuklang")
else:
    st.error(f"❌ Xatolik: {response.status_code} - {response.text}")

# ----------------------
# 5️⃣ Har tab uchun fayllarni ko‘rsatish
for i, tab in enumerate(["Rasmlar", "Videolar", "Boshqalar"]):
    with tabs[i]:
        st.subheader(f"📂 {tab}")
        if not files:
            st.info("📂 Hozircha fayl yo‘q")
        else:
            for file in files:
                file_name = file["name"]
                download_url = file["download_url"]
                ext = "." + file_name.lower().split(".")[-1]

                # Tabga filterlash
                if tab != "Boshqalar" and ext not in file_types[tab]:
                    continue
                if tab == "Boshqalar" and ext in sum(file_types.values(), []):
                    continue

                st.write(file_name)

                # Rasmlar
                if ext in file_types["Rasmlar"]:
                    st.image(download_url, width=300)
                # Videolar
                elif ext in file_types["Videolar"]:
                    st.video(download_url)

                # Download tugmasi
                st.download_button("⬇ Download", requests.get(download_url).content, file_name)

                # Delete tugmasi
                if st.button(f"🗑 O‘chirish: {file_name}", key=file_name):
                    url_del = f"https://api.github.com/repos/{REPO}/contents/storage/{file_name}"
                    file_sha = file["sha"]
                    del_response = requests.delete(
                        url_del,
                        headers=HEADERS,
                        json={"message": f"Delete {file_name}", "sha": file_sha}
                    )
                    if del_response.status_code in [200, 204]:
                        st.success(f"❌ O‘chirildi: {file_name}")
                        st.experimental_rerun()
                    else:
                        st.error(f"Xatolik: {del_response.status_code} - {del_response.text}")

# ----------------------
# 6️⃣ Footer: Parolni o‘zgartirish
st.markdown("---")
with st.expander("🔑 Parolni o‘zgartirish"):
    new_pass = st.text_input("Yangi parol kiriting:", type="password", key="new_pass")
    confirm_pass = st.text_input("Tasdiqlang:", type="password", key="confirm_pass")
    if st.button("Parolni yangilash"):
        if not new_pass or new_pass != confirm_pass:
            st.error("❌ Parollar mos emas yoki bo‘sh")
        else:
            with open(PASSWORD_FILE, "w") as f:
                json.dump({"password": new_pass}, f)
            st.success("✅ Parol muvaffaqiyatli yangilandi")
