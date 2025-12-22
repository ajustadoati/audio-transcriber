import streamlit as st
import json
import os
from pathlib import Path

st.set_page_config(page_title="Audio Player", layout="centered")

# Get the audio ID from query parameters
audio_id = st.query_params.get("id")

if not audio_id:
    st.error("❌ No audio ID provided in the URL")
    st.info("Please use a valid share link")
    st.stop()

# Get absolute path to shared_audios directory
# In Docker: /app, In local: parent of pages directory
BASE_DIR = Path(__file__).resolve().parent.parent
SHARED_DIR = BASE_DIR / "shared_audios"

# Check if the audio exists
metadata_path = SHARED_DIR / f"{audio_id}.json"
audio_path = SHARED_DIR / f"{audio_id}.wav"

if not os.path.exists(metadata_path) or not os.path.exists(audio_path):
    st.error("❌ Audio not found")
    st.info("This audio may have been deleted or the link is invalid")
    st.stop()

# Load metadata
with open(metadata_path, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Display audio player
st.title("🎙️ Audio Player")

st.subheader("🔊 Audio")
with open(audio_path, "rb") as audio_file:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/wav")

# Display metadata
col1, col2 = st.columns(2)
with col1:
    st.metric("Duration", f"{round(metadata['duration'], 1)}s")
with col2:
    st.metric("Created", metadata['timestamp'].split('T')[0])

# Display transcription
st.subheader("📝 Transcription")
st.write(metadata['transcription_text'])

# Download options
st.subheader("⬇️ Downloads")

col1, col2 = st.columns(2)

with col1:
    with open(audio_path, "rb") as f:
        st.download_button(
            label="Download Audio",
            data=f,
            file_name=f"{audio_id}.wav",
            mime="audio/wav",
            use_container_width=True
        )

with col2:
    txt_path = SHARED_DIR / f"{audio_id}.txt"
    with open(txt_path, "rb") as f:
        st.download_button(
            label="Download Transcription",
            data=f,
            file_name=f"{audio_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

# Back button
st.divider()
if st.button("🏠 Go to Transcriber", use_container_width=True):
    st.switch_page("app.py")
