"""settings"""

#! OLD CHORDS NAMING
# CHORDS_AND_NOTES ={'A:maj': 0, 'A:min': 1, 'B:min': 2, 'C:maj': 3, 'D:maj': 4, 'D:min': 5, 'E:maj': 6, 'E:min': 7, 'F:maj': 8, 'G:maj': 9, 'note_A': 10, 'note_A#': 11, 'note_B': 12, 'note_C': 13, 'note_C#': 14, 'note_D': 15, 'note_D#': 16, 'note_E': 17, 'note_F': 18, 'note_F#': 19, 'note_G': 20, 'note_G#': 21}

CHORDS_AND_NOTES ={'A': 0, 'Am': 1, 'Bm': 2, 'C': 3, 'D': 4, 'Dm': 5, 'E': 6, 'Em': 7, 'F': 8, 'G': 9, 'note_A': 10, 'note_A#': 11, 'note_B': 12, 'note_C': 13, 'note_C#': 14, 'note_D': 15, 'note_D#': 16, 'note_E': 17, 'note_F': 18, 'note_F#': 19, 'note_G': 20, 'note_G#': 21}

KEY_LIST = list(CHORDS_AND_NOTES.keys())

#! ONLY CHORDS (Song progression)
# CHORDS ={'A': 0, 'Am': 1, 'Bm': 2, 'C': 3, 'D': 4, 'Dm': 5, 'E': 6, 'Em': 7, 'F': 8, 'G': 9, 'note_A': 10, 'note_A#': 11, 'note_B': 12, 'note_C': 13, 'note_C#': 14, 'note_D': 15, 'note_D#': 16, 'note_E': 17, 'note_F': 18, 'note_F#': 19, 'note_G': 20, 'note_G#': 21}

# KEY_LIST = list(CHORDS.keys())

IMG_HEIGHT = 256
IMG_WIDTH = 256

MODEL_PATH = "models\\modelDlugaNauka"
# MODEL_PATH = "models\\modelDobryChords"
# MODEL_PATH = 'models\\model'

# SONG_NAME = r'full_song_test\Blessid Union Of Souls - I Wanna Be There.wav'
# SONG_NAME = r'full_song_test\Blessid Union Of Souls - I Wanna Be There InstrumentalTest.wav'
# SONG_NAME = r'full_song_test\lemon tree.mp3'
# SONG_NAME = r'GuitarSet\audio\00_BN1-129-Eb_comp_hex_cln.wav'
# SONG_NAME = r'GuitarSet\audio\00_BN1-129-Eb_solo_hex_cln.wav'
# SONG_NAME = r'GuitarSet\audio\00_BN1-147-Gb_comp_hex_cln.wav'
# SONG_NAME = r'GuitarSet\audio\00_BN2-166-Ab_solo_hex_cln.wav'
SONG_NAME = r'GuitarSet\audio\03_Rock3-148-C_comp_hex_cln.wav'
# SONG_NAME = r'full_song_test\maroon_5_payphone_fingerstyle_guitar_cover_by_james_bartholomew.mp3'

#! only works if flag: SET_DUARTION in create_onset_info funcion is set to True
SONG_DURATION = 5