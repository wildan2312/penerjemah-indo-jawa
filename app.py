import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Translasi Indo-Jawa NLLB", page_icon="🔄", layout="centered")

st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web NLP menggunakan model **NLLB-200-Distilled-600M** yang berjalan secara lokal di Hugging Face Spaces.")
st.markdown("---")

# 2. Memuat Model Secara Lokal dengan Caching RAM
@st.cache_resource
def load_model_lokal():
    model_name = "facebook/nllb-200-distilled-600M"
    # Menggunakan CPU karena Hugging Face Spaces gratisan menyediakan CPU dengan RAM 16GB
    tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="ind_Latn")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cpu")
    return tokenizer, model

# Menampilkan loading agak lama di awal karena server sedang mengunduh model 2.4 GB ke RAM Space
with st.spinner("Memuat model NLLB-200 ke dalam RAM Space (Mohon tunggu, sekitar 1-2 menit untuk pertama kali)..."):
    tokenizer, model = load_model_lokal()

st.success("Model AI Berhasil Dimuat secara Lokal dan Siap Digunakan!")

# 3. Komponen Antarmuka Web
teks_input = st.text_area(
    "Masukkan Kalimat (Bahasa Indonesia):", 
    placeholder="Ketik di sini... Contoh: namaku wildan, kamu siapa",
    height=150
)

# 4. Eksekusi Translasi Lokal
if st.button("Terjemahkan ke Bahasa Jawa ✨", type="primary"):
    if teks_input.strip() == "":
        st.warning("Silakan masukkan kalimat terlebih dahulu!")
    else:
        with st.spinner("Sedang memproses translasi..."):
            try:
                # Proses tokenisasi lokal
                inputs = tokenizer(teks_input, return_tensors="pt").to("cpu")
                
                # Proses generate lokal
                translated_tokens = model.generate(
                    **inputs,
                    forced_bos_token_id=tokenizer.convert_tokens_to_ids("jav_Latn"),
                    max_length=300
                )
                
                # Decode lokal
                hasil_terjemahan = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
                
                st.markdown("### 🎯 Hasil Terjemahan (Bahasa Jawa):")
                st.info(hasil_terjemahan)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan sistem: {str(e)}")

st.markdown("---")
st.caption("Proyek Pengembangan Sistem NLP | Hosted on Hugging Face Spaces")
