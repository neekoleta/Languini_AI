import streamlit as st
from audio_recorder_streamlit import audio_recorder

def main():
    audio_bytes = audio_recorder()
    # Do something with audio bytes
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.download_button('Download your voice :)', audio_bytes, 'yourvoice.wav', 'audio/wav')

    # Machine learning code to do something with audio bytes


if __name__ == "__main__":
    main()
