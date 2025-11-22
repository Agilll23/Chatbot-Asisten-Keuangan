# Chatbot-Asisten-Keuangan
Membuat Asisten Chatbot keuangan berbasis model AI, supaya kegiatan mencatat keuangan menjadi lebih mudah dan tidak ribet tanpa menghitung sendiri atau manual

# 💰 Chatbot Asisten Keuangan Kamu

Chatbot cerdas berbasis AI yang membantu mencatat pengeluaran keuangan hanya dengan mengupload foto struk belanja. Dibangun menggunakan **Streamlit** dan **Google Gemini AI**.

## ✨ Fitur Utama
1.  **Scan Struk Otomatis:** Menggunakan AI (Gemini Vision) untuk mengekstrak Tanggal, Item, Kategori, dan Harga dari gambar struk.
2.  **Dashboard Keuangan:** Visualisasi grafik pengeluaran per kategori secara otomatis.
3.  **AI Chatbot:** Tanya jawab interaktif mengenai data keuanganmu (contoh: "Berapa total pengeluaran makanan bulan ini?").

## 🛠️ Teknologi yang Digunakan
* **Bahasa:** Python
* **Framework:** Streamlit
* **AI Model:** Google Gemini 2.5 Flash
* **Data Processing:** Pandas

## 🚀 Cara Menjalankan di Lokal

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/username-kamu/nama-repo.git](https://github.com/username-kamu/nama-repo.git)
    cd nama-repo
    ```

2.  **Install Library:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup API Key:**
    * Buat folder `.streamlit` di dalam folder proyek.
    * Buat file `secrets.toml` di dalam folder `.streamlit`.
    * Isi file tersebut dengan:
        ```toml
        GOOGLE_API_KEY = "masukkan_api_key_google_disini"
        ```

4.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

## 👨‍💻 Author
[Agil Irman Fadri] - [Link LinkedIn Kamu jika mau]
