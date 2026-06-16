import streamlit as st
import requests

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Translasi Indo-Jawa NLLB", page_icon="🔄", layout="centered")

st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web NLP menggunakan API Serverless **NLLB-200-Distilled-600M** dari Meta AI.")
st.markdown("---")

# 2. Mengambil HF_TOKEN dari Fitur Secrets Management Streamlit
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("Error: Rahasia 'HF_TOKEN' belum dikonfigurasi di pengaturan Streamlit Cloud!")
    st.stop()

# URL API resmi Hugging Face untuk model NLLB-200
API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 3. Komponen Input Teks Antarmuka Web
teks_input = st.text_area(
    "Masukkan Kalimat (Bahasa Indonesia):", 
    placeholder="Ketik di sini... Contoh: namaku wildan, kamu siapa",
    height=150
)

# 4. Tombol Eksekusi Translasi
if st.button("Terjemahkan ke Bahasa Jawa ✨", type="primary"):
    if teks_input.strip() == "":
        st.warning("Silakan masukkan kalimat terlebih dahulu!")
    else:
        with st.spinner("Menghubungi server Hugging Face AI..."):
            payload = {
                "inputs": teks_input,
                "parameters": {
                    "src_lang": "ind_Latn",
                    "tgt_lang": "jav_Latn"
                }
            }
            
            try:
                # Menggunakan requests.post mentah agar tidak terikat bug versi SDK
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                # Skenario A: Jika Server Merespons Sukses (Status 200)
                if response.status_code == 200:
                    output = response.json()
                    if isinstance(output, list) and "translation_text" in output[0]:
                        st.markdown("### 🎯 Hasil Terjemahan (Bahasa Jawa):")
                        st.info(output[0]["translation_text"])
                    else:
                        st.error("Format data yang diterima tidak sesuai.")
                        st.json(output)
                
                # Skenario B: Jika Model Sedang Loading di Server Hugging Face (Status 503)
                elif response.status_code == 503:
                    output = response.json()
                    if "estimated_time" in output:
                        st.warning(f"Model sedang bersiap di server Hugging Face. Silakan klik tombol kembali dalam {int(output['estimated_time'])} detik.")
                    else:
                        st.error("Server Hugging Face sedang sibuk. Silakan coba lagi beberapa saat lagi.")
                
                # Skenario C: Jika Terjadi Eror Lain (Misal 401 Token Salah, atau 404 URL Salah)
                else:
                    st.error(f"Server Hugging Face menolak permintaan dengan Status Kode: {response.status_code}")
                    st.json(response.json())
                    
            except Exception as e:
                st.error("Aplikasi gagal melakukan koneksi internet ke Hugging Face.")
                # Membongkar laporan eror sistem secara transparan ke layar web
                st.exception(e)

st.markdown("---")
st.caption("Proyek Pengembangan Sistem NLP | Dataset Evaluasi: NusaX")
