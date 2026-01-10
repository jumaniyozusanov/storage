import streamlit as st
import requests
import base64

st.set_page_config(page_title="☁️ My Cloud ", layout="wide")
st.title("☁️ My Personal Cloud Drive")

# 🔹 Streamlit Secrets
TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]

HEADERS = {"Authorization": f"token {TOKEN}"}

# ----------------------
# 1️⃣ Fayl yuklash
uploaded = st.file_uploader("📤 Rasm, video yoki fayl yuklash")

if uploaded:
    content = uploaded.read()
    encoded_content = base64.b64encode(content).decode()
    path = f"storage/{uploaded.name}"

    url_put = f"https://api.github.com/repos/{REPO}/contents/{path}"

    data = {
        "message": f"Upload {uploaded.name}",
        "content": encoded_content
    }

    response = requests.put(url_put, json=data, headers=HEADERS)

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

url_get = f"https://api.github.com/repos/{REPO}/contents/storage?ref=main"
response = requests.get(url_get, headers=HEADERS)

if response.status_code == 200:
    files = response.json()
    if len(files) == 0:
        st.info("📂 Storage bo‘sh, birinchi faylni yuklang")
    else:
        for file in files:
            file_name = file["name"]
            download_url = file["download_url"]

            st.write(file_name)

            if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                st.image(download_url, width=300)

            st.download_button("⬇ Download", requests.get(download_url).content, file_name)
elif response.status_code == 404:
    st.info("📂 Storage papkasi mavjud emas, birinchi faylni yuklang")
else:
    st.error(f"❌ Xatolik: {response.status_code} - {response.text}")

