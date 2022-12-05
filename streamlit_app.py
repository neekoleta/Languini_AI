import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
import io
import librosa.display
from librosa.feature import melspectrogram
import matplotlib.pyplot as plt
import requests
import json
from PIL import Image
#from scipy.io import wavfile
#import soundfile as sf
#from scipy import signal

# Global styles
st.markdown('<style>.block-container { padding-top: 20px } h2#languini-ai { color: coral; text-align: center; padding-bottom: 0 }</style>', unsafe_allow_html=True)

# App header
st.header('Languini_AI')

# Nice centered image
_, image_col, _ = st.columns(3)
img = Image.open('./img1.jpg')
with image_col:
    st.image(img, width=220)

# App Description
st.markdown('''
<p style="text-align: center; margin-bottom: 50px;">Languini is an application that does cool stuff.</p>
''', unsafe_allow_html=True)

# Getting Started
st.markdown('<h3 style="text-align: center;">Get Started</h3>', unsafe_allow_html=True)

# Center the audio recorder (this collapses to the left if screen too small though)
_, audio_recorder_col, _ = st.columns(3)
with audio_recorder_col:
    audio_bytes = audio_recorder()

# audio_bytes will be set once audio_recorder finished recording audio
if audio_bytes:
    # Display the audio player
    st.audio(audio_bytes, format="audio/wav")
    # Convert the raw audio byte array to numpy n-dimensional array
    # of the audio power, and also the sample rate.
    y, sr = librosa.load(io.BytesIO(audio_bytes))[0], 44100
    # Calculate melspectrogram data of the audio (frequency intensity against time)
    S = melspectrogram(y=y, sr=sr)
    # Normalize raw spectrogram data to decibels, making it more presentable.
    S_dB = librosa.power_to_db(S, ref=np.max)

    plt.figure()
    librosa.display.specshow(S_dB)

    st.pyplot(plt)
    st.download_button('Download Audio',audio_bytes,'test.wav')

    # Demo functionality showing how to send the audio bytes as a "file"
    # in a POST request, and how to extract data from the response.
    #if st.button('Send Audio Data'):
    #   res = requests.post('http://192.168.1.126:8080/pic', files={ 'audio': audio_bytes })
    #    parsed_res_body = json.loads(res.text)
    #   st.markdown(parsed_res_body["hello"])
