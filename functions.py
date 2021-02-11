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

def create_onset_info(SONG_NAME,SONG_DURATION,SET_DUARTION = False):

    # warnings for this function are disabled because of CQT window parametr not fitting for short samples of audio
    # we are using hybrid cqt which solves the problem by using STFT on short fragment instead but warnings still pop up
    warnings.simplefilter("ignore")

    plt.ioff()

    if SET_DUARTION:
        y, sr = librosa.load(SONG_NAME,duration = SONG_DURATION)
    else:
        y, sr = librosa.load(SONG_NAME)
        SONG_DURATION = librosa.get_duration(y=y,sr=sr)

    onset_times = librosa.onset.onset_detect(y = y, sr=sr,backtrack = True , units= 'time')
    
    #! Setting time-lapse bettween each posible accord recognistion
    # joing short fragments
    # ONSET_TIMES_LENGTH = len(onset_times)
    # CUT_SHORT_SIZE = 0.2

    # arr = np.ones(ONSET_TIMES_LENGTH,dtype = bool)

    # i = 1
    # while i<ONSET_TIMES_LENGTH:
    #     duration = 0
    #     while(i<ONSET_TIMES_LENGTH and duration<CUT_SHORT_SIZE):
    #         duration+= onset_times[i] - onset_times[i-1]
    #         if duration >= CUT_SHORT_SIZE:
    #             i+=1
    #             break
    #         if i > 0:
    #             arr[i-1] = False
    #         i+=True
    #     # arr[i] = 1
    # arr[ONSET_TIMES_LENGTH-1] = 0

    # onset_times = onset_times[arr]

    ONSET_TIMES_LENGTH = len(onset_times)
    if ONSET_TIMES_LENGTH == 0:
        raise Exception('No chords were played in song')

    detection_list = []
    duration_list = []
    for start in range(ONSET_TIMES_LENGTH-1):

        duration_chord = onset_times[start+1] - onset_times[start]
        if duration_chord <= 0.01: #ignoring sound which length is smaller than 10ms
            continue
        duration_list.append(duration_chord)
        
        y, sr = librosa.load(SONG_NAME,offset = onset_times[start], duration = duration_chord)
        detection_list.append(librosa.feature.chroma_cqt(y=y, sr=sr,cqt_mode = 'hybrid'))

    duration_chord = SONG_DURATION - onset_times[ONSET_TIMES_LENGTH-1]
    duration_list.append(duration_chord)
    y, sr = librosa.load(SONG_NAME,offset = onset_times[ONSET_TIMES_LENGTH-1], duration = duration_chord)

    detection_list.append(librosa.feature.chroma_cqt(y=y, sr=sr,cqt_mode = 'hybrid'))
    return detection_list,onset_times,duration_list

