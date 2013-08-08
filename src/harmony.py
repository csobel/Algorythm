from music21 import *
import random

# represents the different possible
# rhythms for a half measure (2.0).
# currently uses only half, quarter, or
# eight notes
hm_rhythm_choices = [
	[2.0],
	[1.0,1.0],
	[1.0,0.5,0.5],
	[0.5,0.5,1.0],
	[0.5,1.0,0.5],
	[0.5,0.5,0.5,0.5]
]

def rel(source, target, isAbove):
	"""
	finds closest target to pitch by changing octaves.
	uses isAbove to restrict searching
	"""
	while abs(source - target) >= 12:
		if target > source:
			target -= 12
		else:
			target += 12
	if isAbove and target < source:
		target += 12
	if (not isAbove) and target > source:
		target -= 12
	return target

class HarmonyPhrase:
    """
    Class to help with improvising a segment using just
    the harmony of the song
    """
    def __init__(self, chordProg, key):
        self.chordProg = chordProg
        self.key = key

    def get_rhythm(self, dur):
    	"""
    	Given a duration (integer) where 1.0 = 1 quarter note,
    	returns a list of durations where the sum of the durations
    	is equal to dur
    	"""
    	ret = []
    	for _ in range(int(dur)/2):
    		ret.extend(hm_rhythm_choices[random.randint(0,len(hm_rhythm_choices)-1)])
    	if dur % 2:
    		ret.append(1.0)
    	return ret
    	
    def get_pitches(self, rhythm, chords, prev_note = None):
    	"""
    	Given a rhythm, and a sequence of chords, constructs
    	some notes that will go well with the chords.
    	ASSUMPTION: sum(rhythm duration) == sum(chords durations)
    	"""
    	if prev_note is None:
    		prev_note = note.Note(chords[0].root()).transpose(12) # HACKY!!!!
    	notes = []
    	curr_dur = 0 # tracks the progress through the song
    	chord_idx = 0 # index in the chord progression
    	offset = lambda n: chords[n].offset - chords[0].offset
    	for i in range(len(rhythm)):
    		curr_rhythm = rhythm[i]
    		# first decide a direction at random
    		direction = Direction.decide(prev_note)
    		# next decide what type of tone we'd like to select
    		tone_type = ToneType.decide(curr_rhythm)
    		if chord_idx < len(chords) - 1 and offset(chord_idx + 1) < curr_dur:
    			chord_idx += 1
    		curr_chord = chords[chord_idx]
    		n = self.compute_next_note(prev_note, direction, tone_type, curr_chord)
    		print "next note has value {}".format(n.midi)
    		n.duration = duration.Duration(curr_rhythm)
    		notes.append(n)
    		prev_note = n
    		curr_dur += curr_rhythm
    	return notes

    def compute_next_note(self, prev_note, direction, tone_type, chord):
    	"""
    	Use the arguments to determine the next note to play.
    	User must specify duration
    	"""
    	def d(t):
    		if t == ToneType.ScaleTone:
    			return "ScaleTone"
    		if t == ToneType.ChordTone:
    			return "ChordTone"
    		return "AccidentalTone"
    	print "next note is {}".format(d(tone_type))
    	print "next note had direction {}".format('UP' if direction == Direction.UP else "DOWN")
    	# case on the tone_type
    	if tone_type == ToneType.AccidentalTone:
    		return prev_note.transpose(direction)
    	elif tone_type == ToneType.ChordTone:
    		tones = [p.midi for p in chord.pitches]
    		tones = [rel(prev_note.midi, t, direction == Direction.UP) for t in tones]
    		if random.random() < 0.7:
    			tones = [t for t in tones if t != prev_note.midi]
    		selectedTone = min(tones, key=lambda t:abs(t-prev_note.midi))
    		ret = note.Note()
    		ret.midi = selectedTone
    		return ret
    	elif tone_type == ToneType.ScaleTone:
    		scale = self.key.getScale().getPitches()
    		while min([n.midi for n in scale]) - prev_note.midi >= 6:
    			scale = [n.transpose(-12) for n in scale]
    		while min([n.midi for n in scale]) - prev_note.midi <= -6:
    			scale = [n.transpose(12) for n in scale]
    		# remove the actual tone from the scale, with high probability
    		if random.random() < 0.8:
    			scale = [n for n in scale if n.midi != prev_note.midi]
    		if Direction.UP == direction:
    			scale = [n for n in scale if n.midi > prev_note.midi]
    		else:
    			cale = [n for n in scale if n.midi < prev_note.midi]
    		selectedTone = min(scale, key=lambda n:abs(n.midi - prev_note.midi))
    		print "scale is {}".format([s.midi for s in scale])
    		print "select {} and source was {}".format(selectedTone.midi, prev_note.midi)
    		ret = note.Note()
    		ret.midi = selectedTone.midi
    		return ret
    	else:
    		assert False, "Unknown Tone Type"


    def create_phrase(self, dur, chords):
    	rhythm = self.get_rhythm(dur)
    	notes = self.get_pitches(rhythm, chords)
    	return notes

class Direction:
	UP = -1
	DOWN = 1

	@staticmethod
	def decide(prev_note):
		if prev_note.midi > 12*6 + 3:
			return Direction.DOWN
		elif prev_note.midi < 12*5 -3:
			return Direction.UP
		return Direction.UP if random.randint(0,1) else Direction.DOWN

class ToneType:
	ChordTone = 1
	ScaleTone = 2
	AccidentalTone = 3

	@staticmethod
	def decide(dur):
		"""
		decides type of tone
		"""
		r = random.random()
		if dur <= 0.5:
			# favor AccidentalTones and scale tones
			if r < 0.3:
				return ToneType.AccidentalTone
			elif r < 0.8:
				return ToneType.ScaleTone
			else:
				return ToneType.ChordTone
		elif dur <= 1.5:
			# favor chord and scale tones
			if r < 0.5:
				return ToneType.ScaleTone
			elif r < 0.9:
				return ToneType.ChordTone
			else:
				return ToneType.AccidentalTone
		else:
			# favor chordal tones. Ignore AccidentalTone
			if r < 0.7:
				return ToneType.ChordTone
			else:
				return ToneType.ScaleTone
