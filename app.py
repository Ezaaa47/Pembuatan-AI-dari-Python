
import streamlit as st

from config import APP_NAME
from styles import load_styles
from components import (
    render_header,
    render_feature_card,
    render_footer
)

from ai_engine import generate_answer
from chat_manager import (
    initialize_chat,
    add_message,
    get_history,
    clear_chat
)

from tools import run_feature, translate_text


# ==========================================
# KONFIGURASI
# ==========================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()
initialize_chat()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        "<h1 style='text-align:center;'>🔴 SDA</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;'>Smart Daily Assistant</h3>",
        unsafe_allow_html=True
    )

    st.caption("Your Personal AI Assistant")

    st.divider()

    st.markdown("### 📊 Dashboard")

    st.metric(
        "Total Pertanyaan",
        st.session_state.total_questions
    )

    st.metric(
        "Total Pesan",
        len(st.session_state.messages)
    )

    st.divider()

    st.markdown("### ⚙️ Pengaturan")

    if st.button(
        "🗑️ Hapus Riwayat Chat",
        use_container_width=True
    ):
        clear_chat()
        st.rerun()

    st.markdown("### 🟢 Status Sistem")

    st.success("Aplikasi siap digunakan")

    st.divider()

    st.caption("Python Application")
    st.caption("Gemini AI Integration")
    st.caption("Version 2.0.0")


# ==========================================
# HEADER
# ==========================================

render_header()


# ==========================================
# NAVIGASI FITUR
# ==========================================

tabs = st.tabs([
    "🏠 Beranda",
    "💬 Chat AI",
    "📚 Belajar",
    "📝 Laporan",
    "📄 Ringkas",
    "🌐 Terjemahan",
    "💻 Coding"
])


# ==========================================
# BERANDA
# ==========================================

with tabs[0]:

    st.markdown("## 👋 Selamat Datang!")

    st.markdown(
        "Apa yang ingin kamu lakukan hari ini?"
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        render_feature_card(
            "💬",
            "Chat AI",
            "Bertanya dan berdiskusi dengan kecerdasan buatan."
        )

    with col2:
        render_feature_card(
            "📚",
            "Asisten Belajar",
            "Membantu memahami materi perkuliahan."
        )

    with col3:
        render_feature_card(
            "📝",
            "Pembuat Laporan",
            "Membantu menyusun tugas dan laporan."
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        render_feature_card(
            "📄",
            "Perangkum Teks",
            "Mengubah materi panjang menjadi ringkasan."
        )

    with col5:
        render_feature_card(
            "🌐",
            "Penerjemah",
            "Menerjemahkan berbagai bahasa."
        )

    with col6:
        render_feature_card(
            "💻",
            "Asisten Coding",
            "Membantu membuat dan memperbaiki program."
        )

    st.markdown("---")

    st.markdown("### ✨ Mengapa menggunakan aplikasi ini?")

    st.info(
        "Smart Daily Assistant dirancang untuk membantu "
        "aktivitas sehari-hari melalui teknologi Artificial "
        "Intelligence yang mudah digunakan."
    )


# ==========================================
# CHAT AI
# ==========================================

with tabs[1]:

    st.markdown("## 💬 Chat dengan AI")

    st.caption("Tanyakan apa saja dan dapatkan bantuan AI.")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Tulis pertanyaan kamu di sini...",
        key="main_chat"
    )

    if prompt:

        history = get_history()

        add_message("user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("AI sedang berpikir..."):

                try:

                    answer, model = generate_answer(
                        prompt,
                        history
                    )

                    st.markdown(answer)

                    st.caption(f"Model: {model}")

                    add_message("assistant", answer)

                except Exception as error:

                    st.error(str(error))

        st.rerun()


# ==========================================
# ASISTEN BELAJAR
# ==========================================

with tabs[2]:

    st.markdown("## 📚 Asisten Belajar")

    st.write(
        "Masukkan materi atau pertanyaan yang ingin kamu pelajari."
    )

    with st.form("study_form"):

        question = st.text_area(
            "Materi atau pertanyaan",
            placeholder="Contoh: Jelaskan pengertian algoritma..."
        )

        submit = st.form_submit_button(
            "✨ Pelajari Sekarang",
            use_container_width=True
        )

    if submit and question.strip():

        with st.spinner("Sedang menyiapkan penjelasan..."):

            try:

                answer, model = run_feature(
                    "Belajar",
                    question
                )

                st.markdown("### 📖 Hasil Penjelasan")
                st.markdown(answer)
                st.caption(f"Model: {model}")

            except Exception as error:
                st.error(str(error))


# ==========================================
# PEMBUAT LAPORAN
# ==========================================

with tabs[3]:

    st.markdown("## 📝 Pembuat Laporan")

    with st.form("report_form"):

        topic = st.text_input(
            "Judul atau tema laporan",
            placeholder="Contoh: Perkembangan teknologi AI"
        )

        detail = st.text_area(
            "Penjelasan tambahan",
            placeholder="Tuliskan ketentuan laporan..."
        )

        submit = st.form_submit_button(
            "📝 Buat Laporan",
            use_container_width=True
        )

    if submit and topic.strip():

        prompt = (
            f"Buatkan laporan dengan tema: {topic}\n"
            f"Ketentuan: {detail}\n"
            "Susun secara sistematis dan formal."
        )

        with st.spinner("AI sedang membuat laporan..."):

            try:

                answer, model = run_feature(
                    "Laporan",
                    prompt
                )

                st.markdown("### 📄 Hasil Laporan")
                st.markdown(answer)

                st.download_button(
                    "⬇️ Download TXT",
                    data=answer,
                    file_name="laporan_ai.txt",
                    mime="text/plain"
                )

                st.caption(f"Model: {model}")

            except Exception as error:
                st.error(str(error))


# ==========================================
# PERANGKUM TEKS
# ==========================================

with tabs[4]:

    st.markdown("## 📄 Perangkum Teks")

    with st.form("summary_form"):

        text_input = st.text_area(
            "Masukkan teks yang ingin diringkas",
            height=220,
            placeholder="Tempel materi atau artikel di sini..."
        )

        submit = st.form_submit_button(
            "✨ Ringkas Sekarang",
            use_container_width=True
        )

    if submit and text_input.strip():

        with st.spinner("Sedang meringkas teks..."):

            try:

                answer, model = run_feature(
                    "Ringkas",
                    text_input
                )

                st.markdown("### 📌 Hasil Ringkasan")
                st.markdown(answer)

                st.download_button(
                    "⬇️ Download Ringkasan",
                    data=answer,
                    file_name="ringkasan.txt",
                    mime="text/plain"
                )

            except Exception as error:
                st.error(str(error))


# ==========================================
# PENERJEMAH
# ==========================================

with tabs[5]:

    st.markdown("## 🌐 Penerjemah Bahasa")

    with st.form("translate_form"):

        language = st.selectbox(
            "Terjemahkan ke bahasa",
            [
                "Bahasa Indonesia",
                "Bahasa Inggris",
                "Bahasa Jepang",
                "Bahasa Korea",
                "Bahasa Mandarin",
                "Bahasa Arab"
            ]
        )

        text_input = st.text_area(
            "Teks yang ingin diterjemahkan",
            height=180
        )

        submit = st.form_submit_button(
            "🌐 Terjemahkan",
            use_container_width=True
        )

    if submit and text_input.strip():

        with st.spinner("Menerjemahkan..."):

            try:

                answer, model = translate_text(
                    text_input,
                    language
                )

                st.markdown("### Hasil Terjemahan")
                st.markdown(answer)

                st.download_button(
                    "⬇️ Download Terjemahan",
                    data=answer,
                    file_name="terjemahan.txt",
                    mime="text/plain"
                )

            except Exception as error:
                st.error(str(error))


# ==========================================
# ASISTEN CODING
# ==========================================

with tabs[6]:

    st.markdown("## 💻 Asisten Coding")

    with st.form("coding_form"):

        question = st.text_area(
            "Apa yang ingin kamu buat atau perbaiki?",
            height=180,
            placeholder="Contoh: Buat program kalkulator menggunakan Python..."
        )

        submit = st.form_submit_button(
            "🚀 Jalankan Asisten Coding",
            use_container_width=True
        )

    if submit and question.strip():

        with st.spinner("AI sedang menulis kode..."):

            try:

                answer, model = run_feature(
                    "Coding",
                    question
                )

                st.markdown("### 💻 Hasil Coding")
                st.markdown(answer)

            except Exception as error:
                st.error(str(error))


# ==========================================
# FOOTER
# ==========================================

render_footer()
