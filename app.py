
import streamlit as st
import time
from google import genai

# =====================================================
# 1. KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="Smart Daily Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. DESAIN / CSS
# =====================================================

st.markdown("""
<style>

/* Background utama */
.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #121a32 55%, #17132e 100%);
    color: #f8fafc;
}

/* Konten utama */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #10182b;
    border-right: 1px solid #273451;
}

/* Judul */
.hero-title {
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-subtitle {
    color: #aab7d0;
    font-size: 16px;
    line-height: 1.7;
}

/* Kartu */
.feature-card {
    background: linear-gradient(145deg, #1b2944, #182038);
    border: 1px solid #334466;
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
    transition: 0.2s;
}

.feature-card:hover {
    border-color: #8b5cf6;
    transform: translateY(-3px);
}

.feature-icon {
    font-size: 27px;
    margin-bottom: 10px;
}

.feature-title {
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 7px;
}

.feature-desc {
    color: #aab7d0;
    font-size: 13px;
    line-height: 1.5;
}

/* Tombol */
.stButton > button {
    border-radius: 12px;
    min-height: 45px;
    border: 1px solid #465578;
    background: #202e4b;
    color: white;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #49358a;
    border-color: #a78bfa;
    color: white;
}

/* Input */
.stChatInput textarea {
    border-radius: 15px;
}

/* Pesan chat */
[data-testid="stChatMessage"] {
    background: rgba(32, 46, 75, 0.65);
    border: 1px solid #344563;
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 12px;
}

/* Garis */
hr {
    border-color: #334155;
}

/* Status */
.status-box {
    background: #172b38;
    border: 1px solid #285a55;
    border-radius: 12px;
    padding: 12px;
    color: #a7f3d0;
    font-size: 13px;
}

/* Footer */
.footer {
    text-align: center;
    color: #8492ad;
    font-size: 12px;
    padding: 25px 0 5px 0;
}

/* HP */
@media (max-width: 640px) {
    .block-container {
        padding: 1rem 0.8rem 2rem 0.8rem;
    }

    .feature-card {
        padding: 14px;
        min-height: 130px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. MENGHUBUNGKAN GEMINI AI
# =====================================================

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=API_KEY
    )

except Exception:
    st.error(
        "API Key belum ditemukan. "
        "Periksa file .streamlit/secrets.toml"
    )
    st.stop()


# =====================================================
# 4. PENGATURAN MODEL AI
# =====================================================

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite"
]

SYSTEM_INSTRUCTION = """
Kamu adalah Smart Daily Assistant,
asisten kecerdasan buatan yang ramah,
pintar, sopan, dan membantu pengguna.

Tugas utama kamu:

1. Membantu mahasiswa memahami pelajaran.
2. Membantu membuat tugas dan laporan.
3. Menjelaskan materi dengan bahasa sederhana.
4. Membantu menulis dan memperbaiki program.
5. Membantu menerjemahkan bahasa.
6. Memberikan ide dan inspirasi.
7. Menjawab pertanyaan sehari-hari.

Gunakan bahasa Indonesia sebagai bahasa utama.

Jika pengguna menggunakan bahasa lain,
sesuaikan bahasa jawaban dengan pengguna.

Berikan jawaban yang jelas, terstruktur,
mudah dipahami, dan tidak bertele-tele.

Jika membuat kode program,
berikan kode lengkap yang dapat dijalankan.

Jika menjelaskan sesuatu yang sulit,
gunakan contoh sederhana.

Jangan mengarang fakta jika tidak yakin.
"""


# =====================================================
# 5. RIWAYAT PERCAKAPAN
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# =====================================================
# 6. FUNGSI MENGIRIM PERTANYAAN KE AI
# =====================================================

def tanya_ai(riwayat):

    error_terakhir = None

    for model in MODELS:

        # Maksimal dua percobaan per model
        for percobaan in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=riwayat,
                    config={
                        "system_instruction": SYSTEM_INSTRUCTION
                    }
                )

                if response.text:
                    return response.text, model

                raise Exception("AI tidak memberikan jawaban.")

            except Exception as e:

                error_terakhir = e
                pesan = str(e).lower()

                # Error yang mungkin sementara
                error_sementara = any(
                    kode in pesan
                    for kode in [
                        "503",
                        "429",
                        "500",
                        "502",
                        "504",
                        "unavailable",
                        "resource_exhausted",
                        "overloaded",
                        "deadline_exceeded"
                    ]
                )

                # Coba lagi jika gangguan sementara
                if error_sementara and percobaan == 0:

                    time.sleep(2)

                    continue

                # Jika gagal, lanjut ke model cadangan
                break

    raise Exception(
        f"Semua model AI gagal digunakan. "
        f"Detail: {error_terakhir}"
    )


# =====================================================
# 7. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:15px 5px;">
            <div style="font-size:55px;">🤖</div>
            <h2 style="color:white; margin-bottom:0;">
                Smart Daily
            </h2>
            <h3 style="color:#a78bfa; margin-top:0;">
                Assistant
            </h3>
            <p style="color:#9caec9; font-size:12px;">
                Your AI Personal Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Menu Utama")

    st.markdown(
        """
        <div style="color:#cbd5e1; line-height:2.2;">
        💬 Chat AI<br>
        📚 Asisten Belajar<br>
        📝 Pembuat Laporan<br>
        🌐 Penerjemah Bahasa<br>
        💡 Ide dan Inspirasi
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ⚙️ Pengaturan")

    if st.button(
        "🗑️ Hapus Semua Percakapan",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📊 Statistik")

    st.metric(
        "Jumlah Pesan",
        len(st.session_state.messages)
    )

    st.markdown(
        """
        <div class="status-box">
        🟢 Aplikasi siap digunakan
        <br><br>
        Gemini AI Connection
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("Dibuat menggunakan Python")
    st.caption("Streamlit + Google Gemini AI")
    st.caption("Smart Daily Assistant © 2026")


# =====================================================
# 8. HEADER UTAMA
# =====================================================

st.markdown(
    """
    <div style="margin-bottom:25px;">
        <div class="hero-title">
            Smart Daily Assistant ✨
        </div>

        <div class="hero-subtitle">
            Teman pintar untuk belajar, bekerja,
            mencari inspirasi, dan membantu aktivitas
            sehari-hari.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 9. HALAMAN SELAMAT DATANG
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div style="
            background:linear-gradient(120deg,#263967,#49358a,#174a67);
            border:1px solid #596b9d;
            border-radius:22px;
            padding:28px;
            margin-bottom:25px;
        ">
            <div style="font-size:35px;">👋</div>

            <h2 style="color:white;">
                Halo! Selamat datang.
            </h2>

            <p style="
                color:#dbeafe;
                line-height:1.8;
                font-size:15px;
            ">
                Saya Smart Daily Assistant,
                asisten AI yang siap membantu kebutuhan
                kamu kapan saja.
                Mulai percakapan dengan menuliskan
                pertanyaan di bawah.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚀 Apa yang ingin kamu lakukan?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">
                    Asisten Belajar
                </div>
                <div class="feature-desc">
                    Memahami pelajaran dan materi kuliah
                    dengan penjelasan sederhana.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Mulai Belajar",
            key="belajar",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Bantu saya belajar. "
                "Jelaskan materi dengan bahasa sederhana."
            )
            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">
                    Pembuat Laporan
                </div>
                <div class="feature-desc">
                    Membantu menyusun laporan,
                    makalah, dan tugas.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Buat Laporan",
            key="laporan",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Bantu saya membuat laporan "
                "dengan susunan yang rapi."
            )
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">
                    Penerjemah Bahasa
                </div>
                <div class="feature-desc">
                    Menerjemahkan berbagai bahasa
                    dengan mudah.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Terjemahkan",
            key="translate",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Bantu saya menerjemahkan bahasa "
                "Inggris ke bahasa Indonesia."
            )
            st.rerun()

    with col4:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <div class="feature-title">
                    Ide dan Inspirasi
                </div>
                <div class="feature-desc">
                    Mencari ide kreatif untuk
                    berbagai kebutuhan.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Cari Inspirasi",
            key="inspirasi",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Berikan saya ide kreatif "
                "yang bermanfaat dalam kehidupan sehari-hari."
            )
            st.rerun()

    st.markdown("### 💬 Contoh pertanyaan")

    contoh = [
        "Apa itu Artificial Intelligence?",
        "Buatkan jadwal belajar mahasiswa.",
        "Jelaskan cara kerja Python.",
        "Buatkan ringkasan tentang teknologi."
    ]

    cols = st.columns(2)

    for i, pertanyaan in enumerate(contoh):

        with cols[i % 2]:

            if st.button(
                pertanyaan,
                key=f"contoh_{i}",
                use_container_width=True
            ):

                st.session_state.pending_prompt = pertanyaan
                st.rerun()


# =====================================================
# 10. MENAMPILKAN RIWAYAT CHAT
# =====================================================

else:

    st.markdown("### 💬 Percakapan Kamu")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# =====================================================
# 11. INPUT CHAT
# =====================================================

prompt = st.chat_input(
    "Tanyakan apa saja kepada Smart Daily Assistant..."
)

# Memproses tombol pertanyaan cepat
if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# =====================================================
# 12. PROSES PERTANYAAN DAN JAWABAN AI
# =====================================================

if prompt:

    # Simpan pesan pengguna
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # Mengubah riwayat ke format Gemini
    history = []

    for message in st.session_state.messages:

        history.append({
            "role": (
                "model"
                if message["role"] == "assistant"
                else "user"
            ),
            "parts": [
                {"text": message["content"]}
            ]
        })

    # Memproses jawaban AI
    with st.chat_message("assistant"):

        with st.spinner(
            "✨ Smart Daily Assistant sedang berpikir..."
        ):

            try:

                jawaban, model_dipakai = tanya_ai(history)

                st.markdown(jawaban)

                st.caption(
                    f"🤖 Dijawab menggunakan {model_dipakai}"
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": jawaban
                })

            except Exception as e:

                pesan = str(e)

                st.error(
                    "Maaf, AI sedang mengalami gangguan. "
                    "Silakan coba kembali beberapa saat lagi."
                )

                with st.expander("Lihat detail error"):

                    st.code(pesan)

    st.rerun()


# =====================================================
# 13. FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        🤖 Smart Daily Assistant
        <br>
        Powered by Python, Streamlit & Google Gemini AI
        <br><br>
        AI dapat melakukan kesalahan.
        Periksa kembali informasi penting.
    </div>
    """,
    unsafe_allow_html=True
)