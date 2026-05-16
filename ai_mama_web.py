import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Pendamping Mama", page_icon="❤️", layout="centered")

DATA_FILE = "data_mama.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"jadwal": [], "todo": [], "bisnis": {"transaksi": []}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# Database Resep
resep_detail = {
    "Ayam Kecap Manis": "Bahan utama: ayam, bawang putih, jahe, kecap manis...",
    "Capcay": "Bahan: wortel, buncis, kol, sawi...",
    "Sayur Lodeh": "Bahan: santan, terong, kacang panjang...",
    "Tempe Mendoan": "Tempe dicelup tepung dengan daun bawang...",
    "Nasi Goreng": "Nasi dingin + telur + kecap manis..."
}

def get_response(pesan):
    p = pesan.lower().strip()
    if any(x in p for x in ["sedih", "susah", "khawatir", "lelah", "stres", "capek", "berat"]):
        return "Saya mengerti perasaan Mama... Kadang memang berat ya. Tuhan tidak pernah meninggalkan kita. Ceritakan lebih detail, saya mendengarkan dengan sepenuh hati."
    elif any(x in p for x in ["resep", "masak", "masakan", "menu", "bikin"]):
        for nama, detail in resep_detail.items():
            if nama.lower() in p:
                return f"**{nama}**\n\n{detail}\n\nAda yang ingin ditanyakan lagi tentang resep ini?"
        return "Sebutkan bahan yang tersedia di rumah Mama, saya akan kasih rekomendasi resep yang cocok."
    elif any(x in p for x in ["uang", "keuangan", "transaksi", "saldo", "bisnis"]):
        return "Saya siap membantu urusan keuangan Mama. Mau catat transaksi hari ini?"
    else:
        return "Saya mendengarkan dengan baik... Ceritakan lebih lanjut ya Mama ❤️"

# UI
st.title("❤️ Pendamping Mama")
st.caption("Penasihat & Pendamping Setia untuk Mama")

jam = datetime.now().hour
greeting = "Selamat pagi Mama 🌅" if jam < 10 else "Selamat siang Mama ☀️" if jam < 15 else "Selamat sore Mama 🌇" if jam < 19 else "Selamat malam Mama 🌙"
st.markdown(f"### {greeting}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo Mama... Saya di sini mendampingi Mama setiap hari. Ada yang ingin diceritakan? ❤️"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ketik pesan di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = get_response(prompt)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("Menu Tambahan")
    st.info("Dibuat khusus sebagai hadiah untuk Mama.\nSemoga selalu memberkati ❤️")