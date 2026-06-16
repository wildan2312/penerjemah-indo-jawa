import streamlit as st
import json
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Translasi Indo-Jawa NLLB", page_icon="🔄", layout="centered")
st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web NLP menggunakan API Resmi Hugging Face Inference Client.")
st.markdown("---")

if "HF_TOKEN" in st.secrets:
    HF_TOKEN = st.secrets["HF_TOKEN"]
else:
    st.error("Error: Rahasia 'HF_TOKEN' belum dikonfigurasi di pengaturan Streamlit Cloud!")
    st.stop()

@st.cache_resource
def get_hf_client():
    return InferenceClient(model="facebook/nllb-200-distilled-600M", token=HF_TOKEN)

client = get_hf_client()

teks_input = st.text_area(
    "Masukkan Kalimat (Bahasa Indonesia):", 
    placeholder="Ketik di sini... Contoh: namaku wildan, kamu siapa",
    height=150
)

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
                # PERBAIKAN DI SINI: Menggunakan method="POST" di dalam fungsi .request()
                response = client.request(method="POST", json=payload)
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
                st.error("Gagal menyambung ke server Hugging Face.")
                st.warning(f"🔧 **Detail Teknis Eror:** {str(e)}")

st.markdown("---")
st.caption("Proyek Pengembangan Sistem NLP | Dataset Evaluasi: NusaX")
