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
import time

@st.cache
def get_example_response(word: str, user: str):
    params = {
        'word' : word
        , 'user' : user
    }
    return requests.post('https://languiniai-api-okwty2epfq-ew.a.run.app/get_example', params=params, headers = { 'accept': 'application/json' })

def get_word_score(score:float,top:float,bottom:float)->str:
    '''
    gets the score from the latest attempt (user), and compares it to
    the best score (top) and baseline (bottom) scores.
    returns a string which has UTF characters, IT HAS TO BE PRINTED to see
    the emojis, wont work in notebook without print
    if anything goes wrong it returns a 0
    '''
    word_scores = {1:'Do you even English? 🥴',
                   2:'Keep on going! Practice make is perfect 🙃',
                   3:'Great start, you are on the right track 🏎️',
                   4:'Well done! You are doing great 🤩',
                   5:"😍 Thou art the mast'r of English tongue 🇬🇧"}
    bins = 5
    try:
        local_score = (score-bottom)/((top-bottom)/bins)
    except:
        return 0

    if local_score<1: local_score=1
    if score>top: local_score=5
    return word_scores.get(round(local_score),0)

start_get_example = 0
end_get_example= 0
start_get_response = 0
end_get_response = 0
# Load available words
f = open('words_paths.json')

# Add words to a list
word_array=np.array([' ', *list(json.load(f).keys())], dtype=str)

with st.sidebar:
    # App header
    st.markdown('<h1 style="color: #FF6D00; padding-top:0; text-align: center; padding-bottom: 300; font-size: 50px">Languini_AI</h1>',unsafe_allow_html=True)
    st.markdown('<div style="height: 200px;"></div>', unsafe_allow_html=True)

# Getting Started
user= st.sidebar.text_input('username')
if user:
    st.markdown(f"""
                <h1 style=" color: #240046; text-align: center;">Welcome {user}</h1>
                """,unsafe_allow_html=True)
    st.markdown('<h4 style="text-align: center;color: #240046;padding-bottom:0">Type in the word you want to learn</h4>', unsafe_allow_html=True)
    word=st.selectbox(label='Type in the word you want to learn',options=word_array,key='test',label_visibility='hidden')

    # Center the audio recorder (this collapses to the left if screen too small though)
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    if word != ' ':
        with st.spinner("![Alt Text](http://www.rob-wtd.co.uk/rob/wp-content/uploads/2014/07/FOX_WALK_alpha.gif) spinner1"):
            start_get_example = time.time()

            get_example_res = get_example_response(word,user)
            end_get_example = time.time()
        st.markdown('<h5 style="text-align: center;color: #240046;">Listen to the word 🎧</h5>',unsafe_allow_html=True)
        st.audio(get_example_res.content, format='audio/mp3')



    # Returns an audio example of the word correctly pronounced
        if get_example_res:
            st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
            st.markdown(f'<h5 style="text-align: center;color:#5A189A;font-size: 30px";>Your turn! Press the recorder and say "{word}".</h5>',unsafe_allow_html=True)
            st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
            col1,col2,col3=st.columns(3)
            with col2:
                audio_bytes = audio_recorder()
                st.markdown('<div style="height: 0px;"></div>', unsafe_allow_html=True)
            if audio_bytes:
            # Display the audio player
                st.audio(audio_bytes, format="audio/wav")
        # audio_bytes will be set once audio_recorder finished recording audio
                # Demo functionality showing how to send the audio bytes as a "file"
                # in a POST request, and how to extract data from the response.

                with st.spinner("![Alt Text](http://www.rob-wtd.co.uk/rob/wp-content/uploads/2014/07/FOX_WALK_alpha.gif) doing things"):
                        start_get_response = time.time()
                        params = {
                            'word' : word
                            , 'user' : user
                        }
                        res = requests.post('https://languiniai-api-okwty2epfq-ew.a.run.app/get_result', params=params, files={'file': audio_bytes }, headers = { 'accept': 'application/json' })
                        parsed_res_body = json.loads(res.text)
                        score=parsed_res_body['scores'][-1]
                        top_score=parsed_res_body['good'][0]
                        bottom_score=parsed_res_body['bad'][0]
                        word_result=get_word_score(score,top_score,bottom_score)
                        st.markdown(score)
                        st.markdown(top_score)
                        st.markdown(bottom_score)
                        st.markdown(word_result)
                        end_get_response = time.time()
