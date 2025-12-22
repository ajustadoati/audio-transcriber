import streamlit as st
import soundfile as sf
from openai import OpenAI
import os
import uuid
import json
from datetime import datetime

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

    # Generate unique ID for this transcription
    unique_id = str(uuid.uuid4())

    # Create shared_audios directory if it doesn't exist
    os.makedirs("shared_audios", exist_ok=True)

    # Save audio with unique ID
    shared_audio_path = f"shared_audios/{unique_id}.wav"
    os.rename(audio_path, shared_audio_path)

    # Save transcription to file
    txt_path = f"shared_audios/{unique_id}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Save metadata
    metadata = {
        "id": unique_id,
        "audio_file": f"{unique_id}.wav",
        "transcription_file": f"{unique_id}.txt",
        "transcription_text": text,
        "duration": duration,
        "timestamp": datetime.now().isoformat()
    }

    metadata_path = f"shared_audios/{unique_id}.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Generate shareable link
    base_url = st.secrets.get("base_url", "http://localhost:8501")
    share_link = f"{base_url}/player?id={unique_id}"

    st.subheader("🔗 Share Link")
    st.code(share_link, language="text")
    st.info("Copy this link to share the audio player with the transcription")

    # Download buttons
    st.subheader("⬇️ Downloads")

    with open(shared_audio_path, "rb") as f:
        st.download_button(
            label="Download Audio (WAV)",
            data=f,
            file_name=f"{unique_id}.wav",
            mime="audio/wav"
        )

    with open(txt_path, "rb") as f:
        st.download_button(
            label="Download Transcription (TXT)",
            data=f,
            file_name=f"{unique_id}.txt",
            mime="text/plain"
        )
