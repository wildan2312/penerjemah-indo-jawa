import streamlit as st
import requests

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Translasi Indo-Jawa NLLB", page_icon="🔄", layout="centered")

st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web NLP menggunakan API Serverless **NLLB-200-Distilled-600M** dari Meta AI.")
st.markdown("---")

# 2. Mengambil HF_TOKEN dari Fitur Secrets Management Streamlit
# (Token aman, tidak bocor di kode GitHub publik)
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("Error: Rahasia 'HF_TOKEN' belum dikonfigurasi di pengaturan Streamlit Cloud!")
    st.stop()

# URL API resmi Hugging Face untuk model NLLB-200
API_URL = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Fungsi untuk menembak API Hugging Face
def query_translation(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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
            # Struktur payload khusus untuk konfigurasi translasi bahasa NLLB
            payload = {
                "inputs": teks_input,
                "parameters": {
                    "src_lang": "ind_Latn",
                    "tgt_lang": "jav_Latn"
                }
            }
            
            # Memanggil fungsi API
            output = query_translation(payload)
            
            try:
                # Format response default API HF: [{"translation_text": "hasil"}]
                if isinstance(output, list) and "translation_text" in output[0]:
                    hasil_terjemahan = output[0]["translation_text"]
                    
                    st.markdown("### 🎯 Hasil Terjemahan (Bahasa Jawa):")
                    st.info(hasil_terjemahan)
                
                # Jika model sedang dalam status "loading/warming up" di server HF
                elif "estimated_time" in output:
                    st.warning(f"Server model sedang bersiap di Hugging Face. Silakan klik tombol kembali dalam {int(output['estimated_time'])} detik.")
                else:
                    st.error("Terjadi respons tidak terduga dari API.")
                    st.json(output)
                    
            except Exception as e:
                st.error(f"Gagal memproses hasil translasi. Error: {str(e)}")
                st.json(output)

st.markdown("---")
st.caption("Proyek Pengembangan Sistem NLP | Dataset Evaluasi: NusaX")
