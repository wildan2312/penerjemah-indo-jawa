import streamlit as st
from deep_translator import GoogleTranslator

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="Translasi Indo-Jawa", page_icon="🔄", layout="centered")

st.title("🔄 Aplikasi Penerjemah Bahasa Indonesia ke Bahasa Jawa")
st.write("Aplikasi web ringan menggunakan mesin penerjemah Google Translate.")
st.markdown("---")

# 2. Komponen Input Teks
teks_input = st.text_area(
    "Masukkan Kalimat (Bahasa Indonesia):", 
    placeholder="Ketik di sini... Contoh: namaku wildan, kamu siapa",
    height=150
)

# 3. Tombol Eksekusi Translasi
if st.button("Terjemahkan ke Bahasa Jawa ✨", type="primary"):
    if teks_input.strip() == "":
        st.warning("Silakan masukkan kalimat terlebih dahulu!")
    else:
        with st.spinner("Sedang menerjemahkan..."):
            try:
                # 'jw' adalah kode bahasa Jawa (Javanese) pada sistem Google Translate
                hasil_terjemahan = GoogleTranslator(source='id', target='jw').translate(teks_input)
                
                st.markdown("### 🎯 Hasil Terjemahan (Bahasa Jawa):")
                st.info(hasil_terjemahan)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menerjemahkan: {str(e)}")

st.markdown("---")
st.caption("Proyek Pengembangan Sistem Web Apps Translation")
