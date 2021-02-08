"""testModel"""
import numpy as np

from settings import KEY_LIST,SONG_NAME,SONG_DURATION
from modelPredict import model_predict
from functions import create_onset_info, model_predict, read_song

def check_results(predictions_list,onset_times):
    ONSET_TIMES_LENGTH = len(onset_times)
    
    def show_result1():
        beats_bool = np.zeros(ONSET_TIMES_LENGTH,dtype = int)
        beats_bool[0] = 1
        for i in range(1,len(predictions_list)):
            if predictions_list[i] != predictions_list[i-1]:
                beats_bool[i] = 1

        for i in range(ONSET_TIMES_LENGTH):
            if i < ONSET_TIMES_LENGTH - 1:
                print(predictions_list[i].ljust(10), round(onset_times[i], 2),'-',round(onset_times[i+1], 2))
            else:
                print(predictions_list[i].ljust(10), round(onset_times[i], 2),'- Koniec')

    def show_result2():
        beats_bool = np.zeros(ONSET_TIMES_LENGTH,dtype = int)
        for i in range(1,len(predictions_list)):
            if predictions_list[i] != predictions_list[i-1]:
                beats_bool[i] = 1

        assert(len(beats_bool) == len(predictions_list) == ONSET_TIMES_LENGTH)
        song_dur = 0.0
        for i in range(ONSET_TIMES_LENGTH):
            if i < ONSET_TIMES_LENGTH - 1:
                if beats_bool[i]:
                    song_dur+= (onset_times[i] - onset_times[i-1])
                    print(predictions_list[i-1].ljust(10),round(song_dur,2))
                    song_dur = 0.0
                else:
                    song_dur+= (onset_times[i+1] - onset_times[i])
            else:
                print(predictions_list[i].ljust(10),round(song_dur,2))

    show_result1()
if __name__ == '__main__':

    SONG_NAME = read_song(SONG_NAME)
    detection_list,oneset_times = create_onset_info(SONG_NAME,20)

    import glob
    arr = glob.glob("models\\*")
    for model in arr:
        pred = model_predict(model,detection_list)
        check_results(pred,oneset_times)

    # check_accordACC()