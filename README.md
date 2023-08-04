# Guitario

<img src="/guiIcons/music.png" width="200" height="200">
Guitario is a simple guitar chords recognition tool.

The project is based on AI recognition of chroma-based features

## Chords currently implemented

* a
* am
* bm
* c
* d
* dm
* e
* em
* f
* g

## Training database contains 2000 images created from 2000 recordings of 10 guitar chords

## Recording database

* For each chord, there are 200 .wav files sampled at 44.100 Hz and quantized at 16 bits.

* 100 first chords are recorded in an anechoic chamber and the 100 last are recorded in a noisy room 

Four guitars were used, and WAV file numbers

* [1-25]: Guitar 1

* [26-50]: Guitar 2

* [51-75]: Guitar 3

* [76-100]: Guitar 4

* Database was provided by INTELSIG Laboratory, University of Liège, Departement EECS
<http://www.montefiore.ulg.ac.be/services/acous/STSI/file/jim2012Chords.zip>
(*Update 2023 seems like the dataset is no longer available, feel free to PM if it would be useful for your project I will try to find and torrent)
## Model training

For training purposes, TensorFlow 2.3.1 was used.
The model was trained by using 256x256 pixels images of chroma features of each recorded chord

## Requirements

All required Python packages with their versions are specified in the requirements.txt file

## Setup

To run this project, all modules listed in the requirements.txt file must be installed

If package installer pip is installed you can install all required modules using this command

`pip install -r requirements.txt`

To run this project, run the main.py file using Python interpreter

`python main.py`

