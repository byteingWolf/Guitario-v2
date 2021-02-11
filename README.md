# Guitario

<img src="/guiIcons/music.png" width="200" height="200">
Guitario is a simple guitar chords recognition.

* Project is based on AI recognition of chroma-based features

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

## Training database contain 2000 images created from 2000 recordings of 10 guitar chords

## Recording database

* For each chord, there are 200 wav files sampled at 44.100 Hz and quantized at 16 bits.

* 100 first chords are recorded in an anechoic chamber and the 100 last are recorded in a noisy room 

Four guitar were used, WAV file numbers

* [1-25]   : Guitar 1

* [26-50]  : Guitar 2

* [51-75]  : Guitar 3

* [76-100] : Guitar 4

* Database was provided by INTELSIG Laboratory, University of Liège, Departement EECS
<http://www.montefiore.ulg.ac.be/services/acous/STSI/file/jim2012Chords.zip>
## Model training

For training purpose tensorflow 2.3.1 was used.
Model was trained by usising 256x256 pixels images of chroma fetures of each recorded chord

## Requirements

All requied python packages with their versions are specified in the requirements.txt file

## Setup

To run this project, all modules listed in requirements.txt file must be installed

If package installer pip is installed you can install all required modules using this line

`pip install -r requirements.txt`

To run this project, compile main.py file using python interpreter

`python main.py`

