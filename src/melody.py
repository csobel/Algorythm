# contains simple functions to test improv code
import improv
from music21 import *

def test_on_prog(chordStrs):
    num_measures = 4
    s = stream.Score()
    harm = improv.createHarmony(chordStrs, num_measures/2)
    solo = improv.createSolo(chordStrs, num_measures)
    s.append(solo)
    s.append(harm)
    return s
    