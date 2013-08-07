from music21 import *
from copy import deepcopy

def _note(name, dur):
	n = note.Note(name)
	n.duration = duration.Duration(dur)
	return n

def _rest(dur):
	r = note.Rest()
	r.duration = duration.Duration(dur)
	return r

def _chord(name, dur):
	c = harmony.ChordSymbol(name)
	c.duration = duration.Duration(dur)
	return c

def IGotRhythm():
	"""
	Creates a harmony and melody based on the song IGotRhythm by
	George Gershwin.
	"""
	# song is AABA format
	melodyA = [
		_rest(1.0),
		_note("F4", 1.5),
		_note("G4", 1.5),

		_note("B-4", 1.5),
		_note("C5", 2.5),

		_rest(1.0),
		_note("C5", 1.5),
		_note("B-4", 1.5),

		_note("G4", 1.5),
		_note("F4", 2.5),

		_rest(1.0),
		_note("F4", 1.5),
		_note("G4", 1.5),

		_note("B-4", 1.5),
		_note("C5", 0.5),
		_rest(0.5),
		_note("E-5", 0.5),
		_rest(0.5),
		_note("C5", 0.5),

		_note("D5", 1.0),
		_note("D5", 1.0),
		_note("C5", 0.5),
		_note("D5", 0.5),
		_note("C5", 0.5),
		_note("B-4", 0.5),

		_note("B-4", 3.0),
		_rest(1.0)
	]

	melodyB = [
		_rest(1.0),
		_note("D5", 1.5),
		_note("D5", 1.5),

		_note("D5", 1.5),
		_note("E5", 2.5),

		_rest(1.0),
		_note("D5", 1.5),
		_note("D5", 1.5),

		_note("D5", 1.5),
		_note("G4", 2.5),

		_rest(1.0),
		_note("C5", 1.5),
		_note("C5", 1.5),

		_note("C5", 1.5),
		_note("D5", 2.5),

		_rest(1.0),
		_note("C5", 1.5),
		_note("C5", 1.5),

		_note("C5", 4.0),
	]

	_chord2 = lambda name : _chord(name, 2.0)

	harmonyA = [
		_chord2("B-6"),
		_chord2("Gmin7"),
		_chord2("Cmin7"),
		_chord2("F7"),
		_chord2("Dmin7"),
		_chord2("D-dim7"),
		_chord2("Cmin7"),
		_chord2("F7"),
		_chord2("B-6"),
		_chord2("B-7"),
		_chord2("E-7"),
		_chord2("A-7"),
		_chord("F7", 4.0),
		_chord("B-6", 4.0)
	]

	harmonyB = [
		_chord("D7", 4.0),
		_chord("D7", 4.0),
		_chord("G7", 4.0),
		_chord("G7", 4.0),
		_chord("C7", 4.0),
		_chord("C7", 4.0),
		_chord("F7", 4.0),
		_chord("F7", 4.0)
	]

	melody = stream.Part()
	melody.append(key.Key("B-"))
	for part in [melodyA, deepcopy(melodyA), melodyB, deepcopy(melodyA)]:
		for n in part:
			melody.append(n)

	harm = stream.Part()
	harm.append(key.Key("B-"))
	for part in [harmonyA, deepcopy(harmonyA), harmonyB, deepcopy(harmonyA)]:
		for c in part:
			harm.append(c)
	return (harm, melody)
