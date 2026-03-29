import streamlit as st
from faster_whisper import WhisperModel

# ── Load once, reuse forever across all reruns ──
@st.cache_resource
def load_model():
    # cpu with int8 = fastest on most machines, no GPU needed
    return WhisperModel("tiny", device="cpu", compute_type="int8")

def process_audio_whisper(audio_path):
    try:
        model = load_model()
        segments, _ = model.transcribe(audio_path, beam_size=1, language="en")
        return " ".join(segment.text.strip() for segment in segments)
    except Exception as e:
        print("Whisper transcription failed:", e)
        return ""