from harmony import HarmonyPhrase
from sample_input import (
	IGotRhythm,
	AutumnLeaves
)
from music21 import *

def test():
	(harm, _) = IGotRhythm()
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

def testTrip():
	p = stream.Part()
	p2 = stream.Part()
	p.append(meter.TimeSignature('4/4'))
	p2.append(meter.TimeSignature('4/4'))
	for i in range(2):
		for j in range(2):
			n1 = note.Note("C")
			n2 = note.Note("D")
			n3 = note.Note("E")
			n1.duration = duration.Duration(.333333333)
			n2.duration = duration.Duration(.333333333)
			n3.duration = duration.Duration(.333333333)
			p.append(n1)
			p.append(n2)
			p.append(n3)
		n4 = note.Note("F")
		n5 = note.Note("G")
		n4.duration = duration.Duration(1.0)
		n5.duration = duration.Duration(1.0)
		p.append(n4)
		p.append(n5)

	for i in range(2*4):
		c = harmony.ChordSymbol("Cmaj7")
		c.duration = duration.Duration(1.0)
		p2.append(c)
	s = stream.Score()
	s.append(meter.TimeSignature('4/4'))
	s.append(p)
	s.append(p2)
	return s
