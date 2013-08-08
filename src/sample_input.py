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

def AutumnLeaves():
	melodyA = [
		_note("C5", 4.0),

		_note("C5", 1.0),
		_note("D4", 1.0),
		_note("E4", 1.0),
		_note("F#4", 1.0),

		_note("B4", 2.0),
		_note("B4", 2.0),

		_note("B4", 1.0),
		_note("C4", 1.0),
		_note("D4", 1.0),
		_note("E4", 1.0),

		_note("A4", 4.0),

		_note("A4", 1.0),
		_note("B3", 1.0),
		_note("C#4", 1.0),
		_note("D#4", 1.0),

		_note("G4", 4.0),

		_rest(1.0),
		_note("E4", 1.0),
		_note("F#4", 1.0),
		_note("G4", 1.0)
	]

	melodyB = [
		_note("F#4", 1.0),
		_note("B3", 1.0),
		_note("F#4", 2.0),

		_note("F#4", 1.0),
		_note("F#4", 1.0),
		_note("E4", 1.0),
		_note("F#4", 1.0),

		_note("G4", 4.0),

		_note("G", 1.0),
		_note("G", 1.0),
		_note("F#4", 1.0),
		_note("G", 1.0),

		_note("A4", 4.0),

		_note("A4", 1.0),
		_note("D4", 1.0),
		_note("D5", 1.0),
		_note("C5", 1.0),

		_note("B4", 4.0),

		_note("B4", 1.0),
		_rest(1.0),
		_note("A#4", 1.0),
		_note("B4", 1.0),

		_note("C5", 1.0),
		_note("C5", 1.0),
		_note("A4", 1.0),
		_note("A4", 1.0),

		_note("F#4", 3.0),
		_note("C5", 1.0),

		_note("B4", 2.0),
		_note("B4", 2.0),

		_note("B4", 3.0),
		_note("E4", 1.0),

		_note("A4", 3.0),
		_note("G4", 1.0),

		_note("F#4", 2.0),
		_note("G4", 1.0),
		_note("B3", 1.0),

		_note("E4", 4.0),

		_rest(1.0),
		_note("E4", 1.0),
		_note("F#4", 1.0),
		_note("G4", 1.0)
	]

	harmonyA = [
		_chord("Am7", 4.0),
		_chord("D7", 4.0),
		_chord("Gmaj7", 4.0),
		_chord("Cmaj7", 4.0),
		_chord("F#m7b5", 4.0),
		_chord("B7", 4.0),
		_chord("Emin", 4.0),
		_chord("Emin", 4.0)
	]

	harmonyB = [
		_chord("F#m7b5", 4.0),
		_chord("B7", 4.0),
		_chord("Emin", 4.0),
		_chord("Emin", 4.0),
		_chord("Amin7", 4.0),
		_chord("D7", 4.0),
		_chord("Gmaj7", 4.0),
		_chord("Gmaj7", 4.0),
		_chord("F#m7b5", 4.0),
		_chord("B7", 4.0),
		_chord("Emin7", 2.0),
		_chord("E-7", 2.0),
		_chord("Dmin7", 2.0),
		_chord("D7", 2.0),
		_chord("Cmaj7", 4.0),
		_chord("B7", 4.0),
		_chord("Emin", 4.0),
		_chord("Emin", 4.0)

	]

	melody = stream.Part()
	melody.append(key.Key("G"))
	for part in [melodyA, deepcopy(melodyA), melodyB]:
		for n in part:
			melody.append(n)

	harm = stream.Part()
	harm.append(key.Key("G"))
	for part in [harmonyA, deepcopy(harmonyA), harmonyB]:
		for c in part:
			harm.append(c)

	return (harm, melody)
