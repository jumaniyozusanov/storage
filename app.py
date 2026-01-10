import streamlit as st
import requests
import base64

st.set_page_config(page_title="☁️ My Cloud Drive", layout="wide")
st.title("☁️ My Personal Cloud")

# 🔹 GitHub public repo nomi
REPO = "jumaniyozusanov/storage"
HEADERS = {}  # Public repo, shuning uchun token shart emas

# ----------------------
# 1️⃣ Fayl yuklash
uploaded = st.file_uploader("📤 Rasm, video yoki fayl yuklash")

if uploaded:
    content = uploaded.read()
    encoded_content = base64.b64encode(content).decode()
    path = f"storage/{uploaded.name}"

    url = f"https://github.com/jumaniyozusanov/storage.git"

    data = {
        "message": f"Upload {uploaded.name}",
        "content": encoded_content
    }

    response = requests.put(url, json=data, headers=HEADERS)

    if response.status_code == 201:
        st.success(f"✅ Saqlandi: {uploaded.name}")
    elif response.status_code == 422:
        st.warning("⚠️ Bu fayl allaqachon mavjud")
    else:
        st.error(f"Xatolik: {response.status_code} - {response.text}")

st.divider()

# ----------------------
# 2️⃣ Gallery va Download
st.subheader("📂 Cloud ichidagi fayllar")

url_get = f"https://github.com/jumaniyozusanov/storage.git"
response = requests.get(url_get, headers=HEADERS)

if response.status_code == 200:
    files = response.json()
    for file in files:
        file_name = file["name"]
        download_url = file["download_url"]

        st.write(file_name)

        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            st.image(download_url, width=300)

        st.download_button("⬇ Download", requests.get(download_url).content, file_name)
else:
    st.error("❌ Fayllarni olishda xatolik yuz berdi")
