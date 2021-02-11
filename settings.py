"""settings"""

#! CHORDS
CHORDS ={'A': 0, 'Am': 1, 'Bm': 2, 'C': 3, 'D': 4, 'Dm': 5, 'E': 6, 'Em': 7, 'F': 8, 'G': 9}
KEY_LIST = list(CHORDS.keys())

IMG_HEIGHT = 256
IMG_WIDTH = 256

MODEL_PATH = "models\\modelChords"

#Song example
SONG_NAME = r'song_examples\song_example_rock.wav'
# SONG_NAME2 = r'song_examples\jazz.wav'

#! Triming the length of song, only works if flag: SET_DUARTION in create_onset_info funcion is set to True
SONG_DURATION = 5