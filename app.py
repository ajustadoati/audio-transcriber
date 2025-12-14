import streamlit as st
import soundfile as sf
from openai import OpenAI
import os

st.set_page_config(page_title="English Audio Transcriber", layout="centered")

st.title("🎙️ English Audio Transcriber")
st.write("Record up to **2 minutes** of audio in English and get the transcription.")

# Audio input
audio = st.audio_input("Record your audio")

if audio:
    # Save audio temporarily
    audio_path = "audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio.read())

    # Validate duration
    data, samplerate = sf.read(audio_path)
    duration = len(data) / samplerate

    if duration > 120:
        st.error("❌ Audio must be 2 minutes or less")
        os.remove(audio_path)
        st.stop()

    st.success(f"✅ Audio duration: {round(duration, 1)} seconds")

    # Transcribe
    with st.spinner("Transcribing audio..."):
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]) # is for local-test change by = st.secrets["OPENAI_API_KEY"])

        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en"
            )

        text = transcription.text

    st.subheader("📝 Transcription")
    st.write(text)

    # Save transcription to file
    txt_path = "transcription.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Download buttons
    st.subheader("⬇️ Downloads")

    with open(audio_path, "rb") as f:
        st.download_button(
            label="Download Audio (WAV)",
            data=f,
            file_name="audio.wav",
            mime="audio/wav"
        )

    with open(txt_path, "rb") as f:
        st.download_button(
            label="Download Transcription (TXT)",
            data=f,
            file_name="transcription.txt",
            mime="text/plain"
        )

    # Cleanup (optional)
    # os.remove(audio_path)
    # os.remove(txt_path)
