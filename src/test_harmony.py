from harmony import HarmonyPhrase
from sample_input import (
	IGotRhythm,
	AutumnLeaves
)
from music21 import *

def test():
	(harm, _) = AutumnLeaves()
	solo = stream.Part()
	key = harm[0]
	solo.append(key)
	chords = harm.notes
	phraseMaker = HarmonyPhrase(chords, key)
	dur = 0
	for chord in chords:
		dur += chord.duration.quarterLength
	notes = phraseMaker.create_phrase(dur, chords)
	for n in notes:
		solo.append(n)
	s = stream.Score()
	s.append(solo)
	s.append(harm)
	return s

