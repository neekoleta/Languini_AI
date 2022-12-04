import streamlit as st
from audio_recorder_streamlit import audio_recorder
import numpy as np
#from PIL import Image
#import soundfile as sf
#from scipy.io import wavfile
import io
import librosa
import librosa.display
from librosa.feature import melspectrogram
#from scipy import signal
import matplotlib.pyplot as plt
#import soundfile as sf
import requests

audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    #sample_rate, samples = wavfile.read(io.BytesIO(audio_bytes))
    #frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    y, sr = librosa.load(io.BytesIO(audio_bytes))[0], 44100
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_dB = librosa.power_to_db(S, ref=np.max)
    plt.figure()
    librosa.display.specshow(S_dB)

    # plt.savefig("original_sg/s_7.jpg")
    st.pyplot(plt)

    # plt.pcolormesh(times, frequencies, spectrogram)
    # plt.imshow(spectrogram)
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # plt.show()

    st.download_button('TEST',audio_bytes,'test.wav')
   
    res = requests.post('http://192.168.1.126:8080/pic', files={ 'audio': audio_bytes })
    st.markdown(res)
