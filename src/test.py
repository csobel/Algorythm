# contains simple functions to test improv code
import src.improv as improv
from music21 import *

def test_on_prog(chordStrs):
    num_measures = 64
    s = stream.Score()
    harm = improv.createHarmony(chordStrs, num_measures/2)
    solo = improv.createSolo(chordStrs, num_measures)
    s.append(harm)
    s.append(solo)
    return s
    
