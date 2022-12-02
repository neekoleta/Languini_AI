import streamlit as st
from audio_recorder_streamlit import audio_recorder
from PIL import Image

# Global styles
st.markdown('<style>.block-container { padding-top: 20px } h2#languini-ai { color: coral; text-align: center; padding-bottom: 0 }</style>', unsafe_allow_html=True)

# App header
st.header('Languini_AI')

# Nice centered image
_, image_col, _ = st.columns(3)
img = Image.open('./img1.jpg')
with image_col:
    st.image(img, width=200)

# App Description
st.markdown('''
<p style="text-align: center; margin-bottom: 50px;">Languini is an application that does cool stuff.</p>
''', unsafe_allow_html=True)

# Getting Started
st.markdown('<h3 style="text-align: center;">Get Started</h3>', unsafe_allow_html=True)

_, audio_recorder_col, _ = st.columns(3)

with audio_recorder_col:
    audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    if st.button('Process audio', 'btn-process-audio', 'This will use ML to analyze your audio'):
        st.balloons()
