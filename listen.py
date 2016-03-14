#! /usr/bin/env python

import os

import pyaudio
from pocketsphinx.pocketsphinx import *

modeldir = "/usr/local/Cellar/cmu-pocketsphinx/HEAD/share/pocketsphinx/model/"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
#config.set_string('-keyphrase', 'forward')
#config.set_float('-kws_threshold', 1e+20)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

# Process audio chunk by chunk. On keyword detected perform action and restart search
decoder = Decoder(config)
decoder.set_keyphrase("kws", "jarvis")
decoder.set_search("kws")
decoder.start_utt()
while True:
    buf = stream.read(256)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break
    if decoder.hyp() is not None:
        print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
        print ("Detected keyword, restarting search")
        decoder.end_utt()
        decoder.start_utt()
#    else:
#        print ("Nothing happened")
