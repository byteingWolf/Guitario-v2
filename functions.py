"""functions"""
import warnings
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

def read_song(SONG_NAME):
    _, file_extension = os.path.splitext(SONG_NAME)
    if file_extension != '.mp3' and file_extension != '.wav':
        return None,False 

    return SONG_NAME,False

def create_onset_info(SONG_NAME,SONG_DURATION=60,SET_DUARTION = False):

    # warnings for this function are disabled because of CQT window parametr not fitting for short samples of audio
    # we are using hybrid cqt which solves the problem by using STFT on short fragment instead but warnings still pop up
    warnings.simplefilter("ignore")

    plt.ioff()

    if SET_DUARTION:
        y, sr = librosa.load(SONG_NAME,duration = SONG_DURATION)
    else:
        y, sr = librosa.load(SONG_NAME)
        SONG_DURATION = librosa.get_duration(y=y,sr=sr)
    
    onset_samples  = librosa.onset.onset_detect(y = y, sr=sr,backtrack = True , units= 'samples')
    # onset_samples  = np.concatenate(onset_samples , len(y))
    starts = onset_samples[0:-1]
    ends = onset_samples[1:]
    detection_list = []
    duration_list = []
    for _,(start, end) in enumerate(zip(starts, ends)):
        fragment = y[start:end]
        fragment_time = librosa.get_duration(y=fragment,sr=sr)
        if fragment_time < 0.1:
            continue
        duration_list.append(fragment_time)
        detection_list.append(librosa.feature.chroma_cqt(y=fragment, sr=sr,cqt_mode = 'hybrid'))

    return detection_list,duration_list

