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


# Load available words
f = open('words_paths.json')

# Add words to a list
word_array=np.array([' ', *list(json.load(f).keys())], dtype=str)

# Global styles
st.markdown('<style>.block-container { padding-top: 20px } h2#languini-ai { color: coral; text-align: center; padding-bottom: 0 }</style>', unsafe_allow_html=True)

# App header
st.header('Languini_AI')

# Nice centered image
# _, image_col, _= st.columns(3)
# img = Image.open('./img1.jpg')
# with image_col:
#     st.image(img, width=220)

# App Description
st.markdown('''
<p style="text-align: center; margin-bottom: 50px;">Languini is an application that does cool stuff.</p>
''', unsafe_allow_html=True)

# Getting Started
st.markdown('<h3 style="text-align: center;">Type in the word you want to learn</h3>', unsafe_allow_html=True)
word=st.selectbox(label='Type in the word you want to learn',options=word_array,key='test',label_visibility='hidden')
# Center the audio recorder (this collapses to the left if screen too small though)
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
if word != ' ':

    params = {
        'word' : word
        , 'user' : 'root'
    }
    res = requests.post('https://languiniai-api-okwty2epfq-ew.a.run.app/get_example', params=params, headers = { 'accept': 'application/json' })
    st.audio(res.content, format='audio/mp3')

# Returns an audio example of the word correctly pronounced
    if res:
        col1,col2,col3=st.columns(3)
        with col2:
            audio_bytes = audio_recorder()
            st.markdown('<div style="height: 0px;"></div>', unsafe_allow_html=True)
        if audio_bytes:
        # Display the audio player
            st.audio(audio_bytes, format="audio/wav")
    # audio_bytes will be set once audio_recorder finished recording audio


        col1,col2,col3=st.columns(3)
        with col3:
                # Demo functionality showing how to send the audio bytes as a "file"
                # in a POST request, and how to extract data from the response.
            if st.button('Send Audio Data'):
                params = {
                    'word' : word
                    , 'user' : 'niko'
                }
                res = requests.post('https://languiniai-api-okwty2epfq-ew.a.run.app/get_result', params=params, files={'file': audio_bytes }, headers = { 'accept': 'application/json' },timeout=15 )
                parsed_res_body = json.loads(res.text)
                st.markdown(parsed_res_body['dates'])
