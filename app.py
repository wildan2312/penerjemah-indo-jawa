import streamlit as st
import json
from huggingface_hub import InferenceClient

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Translasi Indo-Jawa NLLB", page_icon="🔄", layout="centered")

st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web NLP menggunakan API Resmi **Hugging Face Inference Client**.")
st.markdown("---")

# 2. Mengambil HF_TOKEN dari Fitur Secrets Management Streamlit
if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("Error: Rahasia 'HF_TOKEN' belum dikonfigurasi di pengaturan Streamlit Cloud!")
    st.stop()

# 3. Inisialisasi Hugging Face Client Resmi (Optimized with Cache)
@st.cache_resource
def get_hf_client():
    # Mengunci ke model NLLB-200 Meta AI
    return InferenceClient(model="facebook/nllb-200-distilled-600M", token=HF_TOKEN)

client = get_hf_client()

# 4. Komponen Input Teks Antarmuka Web
teks_input = st.text_area(
    "Masukkan Kalimat (Bahasa Indonesia):", 
    placeholder="Ketik di sini... Contoh: namaku wildan, kamu siapa",
    height=150
)

# 5. Tombol Eksekusi Translasi
if st.button("Terjemahkan ke Bahasa Jawa ✨", type="primary"):
    if teks_input.strip() == "":
        st.warning("Silakan masukkan kalimat terlebih dahulu!")
    else:
        with st.spinner("Menghubungi server Hugging Face AI (Menggunakan Jalur Client Resmi)..."):
            payload = {
                "inputs": teks_input,
                "parameters": {
                    "src_lang": "ind_Latn",
                    "tgt_lang": "jav_Latn"
                }
            }
            
            try:
                response = client.post(json=payload)
                output = json.loads(response.decode("utf-8"))
                
                if isinstance(output, list) and "translation_text" in output[0]:
                    hasil_terjemahan = output[0]["translation_text"]
                    st.markdown("### 🎯 Hasil Terjemahan (Bahasa Jawa):")
                    st.info(hasil_terjemahan)
                elif isinstance(output, dict) and "estimated_time" in output:
                    st.warning(f"Server model sedang bersiap di Hugging Face. Silakan klik tombol kembali dalam {int(output['estimated_time'])} detik.")
                elif isinstance(output, dict) and "error" in output:
                    st.error(f"Pesan dari Hugging Face: {output['error']}")
                else:
                    st.error("Gagal memproses format data.")
                    st.json(output)
                    
            except Exception as e:
                # KODE DIUBAH DI SINI: Membongkar detail eror asli ke layar web
                st.error("Gagal menyambung ke server Hugging Face.")
                st.warning(f"🔧 **Detail Teknis Eror (Tunjukkan ini ke Wildan):** {str(e)}")
st.markdown("---")
st.caption("Proyek Pengembangan Sistem NLP | Dataset Evaluasi: NusaX")
