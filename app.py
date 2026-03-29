import streamlit as st
import os

from audio_processing import get_audio_from_youtube, get_audio_from_file
from video_processing import process_audio_whisper
from text_processing import generate_summary_keywords, translate_text, create_pdf
from chatbot import chat_with_bot

st.set_page_config(page_title="ISKIF", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;600;700;900&display=swap');

:root {
    --teal-dark:   #001E1E;
    --teal-mid:    #002a2a;
    --teal-border: #0a3535;
    --accent:      #00726a;
    --accent-hi:   #00968c;
    --bg:          #f4f6f8;
    --card:        #ffffff;
    --border:      #dde3ea;
    --border-hi:   #c4ced8;
    --text:        #1e2d38;
    --muted:       #7a8fa0;
}

* { box-sizing: border-box; }
html, body, .stApp {
    background-color: var(--bg) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }

/* Remove ALL top padding */
.stApp, .stApp > div, .stApp > div > div,
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
.block-container {
    padding-left: 0 !important;
    padding-right: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ══ FAKE SIDEBAR — ONLY THESE 3 LINES CHANGED: position fixed instead of sticky ══ */
.fake-sidebar {
    background: var(--teal-dark);
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    width: 18%;
    padding: 28px 20px;
    border-right: 1px solid var(--teal-border);
    display: flex;
    flex-direction: column;
    gap: 0;
    overflow-y: auto;
    z-index: 999;
}
.sb-brand {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.25;
    margin-bottom: 20px;
    letter-spacing: 0.01em;
}
.sb-divider {
    border: none;
    border-top: 1px solid var(--teal-border);
    margin: 14px 0;
}
.sb-label {
    font-family: 'Playfair Display', serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ffffff;
    margin-bottom: 8px;
}
.sb-user {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
    margin-bottom: 2px;
}
.sb-status {
    font-size: 11px;
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
}
.sb-about {
    font-size: 12px;
    color: #ffffff;
    line-height: 1.65;
    font-family: 'Outfit', sans-serif;
}

/* ══ HEADER ══ */
.iskif-header {
    background: var(--teal-dark);
    border-bottom: 1px solid var(--teal-border);
    text-align: center;
    padding: 36px 32px 28px;
    position: relative;
    overflow: hidden;
    width: 100%;
}
.iskif-header::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 70% 80% at 50% -10%, #003535 0%, transparent 70%);
    pointer-events: none;
}
.iskif-eyebrow {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.36em;
    text-transform: uppercase;
    color: var(--accent-hi);
    margin-bottom: 12px;
    position: relative;
}
.iskif-title {
    font-size: clamp(18px, 2.2vw, 28px);
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.05em;
    line-height: 1.2;
    text-transform: uppercase;
    position: relative;
}
.iskif-subtitle {
    font-size: 10px;
    color: #3d8080;
    margin-top: 8px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    position: relative;
}
.iskif-rule {
    width: 36px; height: 2px;
    background: var(--accent);
    margin: 12px auto 0;
    border-radius: 2px;
}

/* ══ LOGIN ══ */
.login-hero {
    background: var(--teal-dark);
    border-bottom: 1px solid var(--teal-border);
    text-align: center;
    padding: 44px 32px 36px;
    position: relative;
    overflow: hidden;
    width: 100%;
}
.login-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 80% at 50% 0%, #004040 0%, transparent 65%);
    pointer-events: none;
}

/* ══ CONTENT ══ */
.content-wrap {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px 24px 48px;
}

/* ══ SECTION LABELS ══ */
[data-testid="stSubheader"] p,
[data-testid="stSubheader"] > div > p {
    font-family: 'Outfit', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 16px !important;
}

/* ══ INPUT CARDS ══ */
.input-card {
    background: var(--card);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 22px 16px 18px;
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    text-align: center;
    min-height: 95px;
    transition: all 0.15s;
    cursor: pointer;
    margin-bottom: 4px;
}
.input-card:hover { border-color: var(--border-hi); background: #f8fafb; }
.input-card.active {
    background: #e6f4f3;
    border-color: var(--accent);
    color: var(--teal-dark);
    font-weight: 700;
}
.input-card:not(.active) { opacity: 0.65; }

/* ══ INPUTS ══ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    padding: 11px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: var(--accent) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,114,106,0.15) !important;
    outline: none !important;
    background-color: #fafffe !important;
}
.stTextInput > div > div > input::placeholder { color: #aabbc8 !important; }
.stTextInput label, .stTextArea label,
.stSelectbox label, .stFileUploader label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ══ SELECTBOX ══ */
.stSelectbox > div > div {
    background-color: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ══ BUTTONS ══ */
div.stButton > button {
    background: var(--teal-dark) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 11px 28px !important;
    transition: all 0.15s !important;
}
div.stButton > button:hover { background: var(--teal-mid) !important; }
div.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    border: 1.5px solid var(--accent) !important;
    border-radius: 6px !important;
    padding: 10px 22px !important;
    transition: all 0.15s !important;
}
div.stDownloadButton > button:hover { background: #e6f4f3 !important; }

/* ══ CHATBOT ══ */
.chat-response-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 16px;
}
.chat-response-header {
    background: var(--teal-dark);
    padding: 11px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.chat-response-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--accent-hi);
}
.chat-response-body {
    padding: 18px 20px;
    border-left: 3px solid var(--accent);
}
.chat-response-text {
    font-size: 14px;
    color: var(--text);
    line-height: 1.85;
    white-space: pre-wrap;
}

/* ══ MISC ══ */
.stMarkdown p, [data-testid="stText"] {
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
}
.stSpinner > div { border-top-color: var(--accent) !important; }
hr { border-color: var(--border) !important; }
.stAlert { background-color: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }
[data-testid="stFileUploader"] { background-color: var(--card) !important; border: 1px dashed var(--border-hi) !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOGIN
# --------------------------------------------------
def login():
    st.markdown("""
    <div class="login-hero">
        <div class="iskif-eyebrow">Multimedia Intelligence Platform</div>
        <div class="iskif-title">Intelligent Semantic Knowledge<br>Interpretation Framework</div>
        <div class="iskif-subtitle">for Multimedia Content</div>
        <div class="iskif-rule"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1.4, 1, 1.4])
    with col:
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SIGN IN", use_container_width=True):
            if username and password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Please enter both username and password.")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.query_params.get("signout") == "1":
    st.session_state["logged_in"] = False
    st.query_params.clear()
    st.rerun()

if not st.session_state["logged_in"]:
    login()
    st.stop()


# --------------------------------------------------
# MAIN LAYOUT: fake sidebar (col) + main content
# --------------------------------------------------
uname = st.session_state.get("username", "user")

sidebar_col, main_col = st.columns([1, 4])

with sidebar_col:
    st.markdown(f"""
    <div class="fake-sidebar">
        <div class="sb-brand">Semantic<br>Analysis</div>
        <hr class="sb-divider">
        <div class="sb-label">Signed In As</div>
        <div class="sb-user">👤 &nbsp;{uname}</div>
        <div class="sb-status">✅ &nbsp;Active Session</div>
        <hr class="sb-divider">
        <div class="sb-label">About</div>
        <div class="sb-about">Converts YouTube lectures and uploaded videos into transcriptions, summaries, keywords, and interactive Q&amp;A using AI.</div>
        <hr class="sb-divider">
        <a href="?signout=1" style="display:block;margin-top:auto;padding:10px;text-align:center;border:1px solid #1a5050;border-radius:6px;color:#6aacac;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;font-family:Outfit,sans-serif;">← Sign Out</a>
    </div>
    """, unsafe_allow_html=True)

with main_col:
    # HEADER
    st.markdown("""
    <div class="iskif-header">
        <div class="iskif-eyebrow">Multimedia Intelligence Platform</div>
        <div class="iskif-title">Intelligent Semantic Knowledge<br>Interpretation Framework</div>
        <div class="iskif-subtitle">for Multimedia Content</div>
        <div class="iskif-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

    # INPUT TYPE CARDS
    st.subheader("UPLOAD LECTURE")

    if "input_type" not in st.session_state:
        st.session_state["input_type"] = "YouTube URL"

    YT_ICON = """<svg width="36" height="36" viewBox="0 0 38 38" fill="none">
      <rect width="38" height="38" rx="9" fill="#FF0000" opacity="0.1"/>
      <path d="M29.4 14.2s-.3-1.9-1.1-2.7c-1.1-1.1-2.3-1.1-2.8-1.2C22.7 10 19 10 19 10s-3.7 0-6.5.3c-.6.1-1.8.1-2.8 1.2-.8.8-1.1 2.7-1.1 2.7S8.2 16.3 8.2 18.5v2c0 2.2.4 4.3.4 4.3s.3 1.9 1.1 2.7c1.1 1.1 2.5 1.1 3.2 1.2C15.1 29 19 29 19 29s3.7 0 6.5-.3c.6-.1 1.8-.1 2.8-1.2.8-.8 1.1-2.7 1.1-2.7s.4-2.1.4-4.3v-2c0-2.2-.4-4.3-.4-4.3zM16.8 22.4v-7.8l7.2 3.9-7.2 3.9z" fill="#FF0000"/>
    </svg>"""

    FOLDER_ICON = """<svg width="36" height="36" viewBox="0 0 38 38" fill="none">
      <rect width="38" height="38" rx="9" fill="#00726a" opacity="0.1"/>
      <path d="M10 15a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H12a2 2 0 01-2-2V15z" fill="#00968c" opacity="0.8"/>
      <path d="M10 17h18v8a2 2 0 01-2 2H12a2 2 0 01-2-2v-8z" fill="#00726a" opacity="0.5"/>
    </svg>"""

    c1, c2 = st.columns(2)
    with c1:
        yt = "active" if st.session_state["input_type"] == "YouTube URL" else ""
        st.markdown(f'<div class="input-card {yt}">{YT_ICON}<span>YouTube URL</span></div>', unsafe_allow_html=True)
        if st.button("YouTube URL", key="btn_yt", use_container_width=True):
            st.session_state["input_type"] = "YouTube URL"
            st.rerun()
    with c2:
        up = "active" if st.session_state["input_type"] == "Upload Video" else ""
        st.markdown(f'<div class="input-card {up}">{FOLDER_ICON}<span>Upload Video</span></div>', unsafe_allow_html=True)
        if st.button("Upload Video", key="btn_up", use_container_width=True):
            st.session_state["input_type"] = "Upload Video"
            st.rerun()

    input_type = st.session_state["input_type"]
    st.markdown("<br>", unsafe_allow_html=True)

    # INPUT FIELDS
    if input_type == "YouTube URL":
        url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        if st.button("PROCESS VIDEO"):
            if url:
                with st.spinner("Downloading audio from YouTube..."):
                    audio_path = get_audio_from_youtube(url)
                if audio_path is None:
                    st.error("Failed to download audio. Check the URL and try again.")
                else:
                    with st.spinner("Transcribing with Whisper..."):
                        transcription = process_audio_whisper(audio_path)
                    if transcription:
                        st.session_state["transcription"] = transcription
                        summary, keywords = generate_summary_keywords(transcription)
                        st.session_state["summary"] = summary
                        st.session_state["keywords"] = keywords
                        st.success("Transcription complete!")
                    else:
                        st.error("Transcription failed.")
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
            else:
                st.warning("Please enter a YouTube URL first.")
    else:
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mkv", "avi"])
        if uploaded_file:
            with st.spinner("Extracting audio..."):
                audio_path = get_audio_from_file(uploaded_file)
            if audio_path:
                with st.spinner("Transcribing with Whisper..."):
                    transcription = process_audio_whisper(audio_path)
                if transcription:
                    st.session_state["transcription"] = transcription
                    summary, keywords = generate_summary_keywords(transcription)
                    st.session_state["summary"] = summary
                    st.session_state["keywords"] = keywords
                    st.success("Transcription complete!")
                else:
                    st.error("Transcription failed.")
                if os.path.exists(audio_path):
                    os.remove(audio_path)

    # DISPLAY RESULTS
    if "transcription" in st.session_state:

        st.divider()
        st.subheader("TRANSCRIPTION")
        st.write(st.session_state["transcription"])

        st.divider()
        st.subheader("SUMMARY OPTIONS")

        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Language", ["English", "Tamil"])
        with col2:
            length = st.selectbox("Summary Length", ["Short", "Medium", "Long"])

        summary, keywords = generate_summary_keywords(
            st.session_state["transcription"],
            language=language,
            length=length
        )

        st.subheader(f"SUMMARY — {length.upper()} · {language.upper()}")
        st.write(summary)

        st.subheader("KEYWORDS")
        st.write(", ".join(keywords))

        st.markdown("<br>", unsafe_allow_html=True)
        pdf_file = create_pdf(summary, keywords)
        st.download_button(
            label="↓  Download PDF",
            data=pdf_file,
            file_name=f"lecture_summary_{language.lower()}.pdf",
            mime="application/pdf"
        )

        st.divider()
        st.subheader("LECTURE CHATBOT")

        user_question = st.text_input("Ask a question about the lecture", placeholder="What was the main topic discussed?")
        if st.button("ASK"):
            if user_question:
                with st.spinner("Thinking..."):
                    response = chat_with_bot(user_question, st.session_state["transcription"])
                st.session_state["chat_response"] = response
            else:
                st.warning("Please type a question first.")

        if "chat_response" in st.session_state:
            resp = st.session_state["chat_response"]
            st.markdown(f"""
            <div class="chat-response-box">
                <div class="chat-response-header">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <rect x="3" y="8" width="18" height="12" rx="3" fill="#00968c"/>
                      <circle cx="9" cy="14" r="1.8" fill="#001E1E"/>
                      <circle cx="15" cy="14" r="1.8" fill="#001E1E"/>
                      <rect x="9.5" y="3" width="5" height="5" rx="1.5" fill="#00968c"/>
                      <line x1="12" y1="8" x2="12" y2="8" stroke="#001E1E" stroke-width="1.5"/>
                      <rect x="0.5" y="11" width="2.5" height="5" rx="1.25" fill="#00968c"/>
                      <rect x="21" y="11" width="2.5" height="5" rx="1.25" fill="#00968c"/>
                      <rect x="8" y="18" width="3" height="2.5" rx="1" fill="#00968c"/>
                      <rect x="13" y="18" width="3" height="2.5" rx="1" fill="#00968c"/>
                    </svg>
                    <span class="chat-response-label">AI Response</span>
                </div>
                <div class="chat-response-body">
                    <div class="chat-response-text">{resp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)