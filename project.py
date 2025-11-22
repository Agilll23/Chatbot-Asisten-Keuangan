import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai
import json

# --- KONFIGURASI API ---
# ⚠️ PENTING: Ganti tulisan di bawah ini dengan API Key aslimu dari Google AI Studio
API_KEY = "google_api_key_kalian" 

# Setup Google AI
genai.configure(api_key=API_KEY)

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Asisten Keuangan AI", layout="wide")
st.title("💰 Chatbot Asisten Keuangan Kamu")
st.markdown("Upload struk belanjamu, dan biarkan AI mencatatnya!")

# --- Inisialisasi Session State (Memori Sementara) ---
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Silakan upload struk belanjaanmu di sebelah kiri."}
    ]

# --- FUNGSI AI (GEMINI) ---
def analyze_receipt_with_ai(image):
    """
    Fungsi ini mengirim gambar ke Google Gemini dan meminta data JSON.
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Prompt (Instruksi) untuk AI
        prompt = """
        Kamu adalah asisten keuangan. Tugasmu adalah mengekstrak data dari gambar struk belanja ini.
        Identifikasi: Tanggal transaksi, Nama Item, Kategori (misal: Makanan, Transport, Hiburan, Belanja Bulanan, dll), dan Harga per item.
        
        Keluaran HARUS berupa JSON Array murni tanpa markdown (jangan pakai ```json).
        Format contoh:
        [
            {"date": "2023-10-25", "item": "Kopi Susu", "category": "Makanan", "amount": 25000},
            {"date": "2023-10-25", "item": "Roti", "category": "Makanan", "amount": 12000}
        ]
        
        Jika gambar buram atau bukan struk, kembalikan array kosong [].
        """
        
        # Kirim ke AI
        response = model.generate_content([prompt, image])
        
        # Bersihkan hasil text dari AI (kadang AI suka nambahin backticks ```)
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "").replace("```", "")
        elif clean_text.startswith("```"):
            clean_text = clean_text.replace("```", "")
            
        # Ubah string JSON menjadi List Python
        data = json.loads(clean_text)
        return data

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses AI: {e}")
        return []

# --- Sidebar: Area Upload Struk ---
with st.sidebar:
    st.header("📸 Upload Struk")
    uploaded_file = st.file_uploader("Pilih gambar struk", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Tampilkan gambar
        image = Image.open(uploaded_file)
        st.image(image, caption='Preview Struk', use_column_width=True)
        
        if st.button("Analisa Struk dengan AI"):
            with st.spinner('Sedang membaca struk dengan AI...'):
                # Panggil fungsi AI yang asli
                new_data = analyze_receipt_with_ai(image)
                
                if new_data:
                    # Masukkan ke database sementara
                    st.session_state.expenses.extend(new_data)
                    st.success(f"Berhasil mencatat {len(new_data)} item!")
                    
                    # Tampilkan tabel data baru
                    st.dataframe(pd.DataFrame(new_data))
                else:
                    st.warning("Gagal membaca struk. Coba foto yang lebih jelas.")

# --- Area Utama: Dashboard & Chat ---

# 1. Tampilkan Ringkasan Data
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    
    # Pastikan kolom amount jadi angka
    df['amount'] = pd.to_numeric(df['amount'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Pengeluaran")
        total_spend = df['amount'].sum()
        st.metric(label="Rupiah", value=f"Rp {total_spend:,.0f}")
    
    with col2:
        st.subheader("Grafik Kategori")
        if not df.empty:
            chart_data = df.groupby("category")["amount"].sum()
            st.bar_chart(chart_data)
        
    st.write("### Detail Transaksi")
    st.dataframe(df, use_container_width=True)

st.divider()

# --- FUNGSI CHAT INTELEGEN (Supaya Chatbotnya Pinter) ---
def ask_ai_about_finance(question, data_expenses):
    try:
        # Gunakan model text biasa (Gemini Pro/Flash) karena kita tidak kirim gambar
        # Pastikan nama model ini sesuai dengan yang berhasil di komputer kamu tadi
        model = genai.GenerativeModel("gemini-2.5-flash") 
        
        # Kita ubah data pengeluaran jadi teks biar bisa dibaca AI
        data_str = json.dumps(data_expenses)
        
        # Prompt: Kita kasih datanya ke AI, lalu suruh dia jawab pertanyaan user
        prompt = f"""
        Kamu adalah asisten keuangan pribadi yang ramah.
        Di bawah ini adalah data pengeluaran pengguna dalam format JSON:
        {data_str}
        
        Tugasmu:
        1. Jawab pertanyaan pengguna berdasarkan data di atas.
        2. Jika pengguna bertanya "Total Makanan", kamu harus menjumlahkan semua item dengan kategori 'Makanan'.
        3. Gunakan format mata uang Rupiah (Rp xx.xxx) yang rapi.
        4. Jika data kosong atau tidak ada yang relevan, katakan kamu tidak tahu.
        
        Pertanyaan Pengguna: {question}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Maaf, aku bingung. Error: {e}"

# 2. Chatbot Interface
st.subheader("💬 Tanya Asisten Keuangan")

# Tampilkan history chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input user
if prompt := st.chat_input("Contoh: Berapa total buat beli Makanan?"):
    # 1. Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Pikirkan jawaban...
    with st.chat_message("assistant"):
        with st.spinner("Sedang menghitung..."):
            if not st.session_state.expenses:
                response_text = "Data pengeluaran masih kosong nih. Upload struk dulu yuk!"
            else:
                # Disini kita panggil AI untuk mikir
                response_text = ask_ai_about_finance(prompt, st.session_state.expenses)
            
            st.markdown(response_text)
            
    # 3. Simpan jawaban bot

    st.session_state.messages.append({"role": "assistant", "content": response_text})
