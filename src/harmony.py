from music21 import *
import random

# Phrase length in measures
MIN_PHRASE_LENGTH = 2
MAX_PHRASE_LENGTH = 4

def nths(n):
	l = []
	for i in range(2*n):
		l.append(1.0/n)
	return l

def rep_n(elem, n = 1):
	ret = []
	for _ in range(n):
		ret.append(elem)
	return ret

def split_stream(chords, dur):
	"""
	splits a chord stream or list into two parts
	based on the duration
	"""
	dur_sum = 0
	idx = 0
	while dur_sum + chords[idx].duration.quarterLength <= dur and idx < len(chords) -1:
		dur_sum += chords[idx].duration.quarterLength
		idx += 1
	print "chords had len {} splitting at {} dur was {}".format(len(chords), idx, dur)
	return (chords[:idx], chords[idx:])

def nearest_chord_note(prev_note, chord, direction):
	tones = [p.midi for p in chord.pitches]
	tones = [rel(prev_note.midi, t, direction == Direction.UP) for t in tones]
	if random.random() < 0.7:
		tones = [t for t in tones if t != prev_note.midi]
	selectedTone = min(tones, key=lambda t:abs(t-prev_note.midi))
	ret = note.Note()
	ret.midi = selectedTone
	return ret

def d(t):
	if t == ToneType.ScaleTone:
		return "ScaleTone"
	if t == ToneType.ChordTone:
		return "ChordTone"
	return "AccidentalTone"

# represents the different possible
# rhythms for a half measure (2.0).
# currently uses only half, quarter, or
# eight notes
hm_rhythm_choices = []
hm_rhythm_choices.extend(rep_n([2.0],4))
hm_rhythm_choices.extend(rep_n([2.0/3.0, 1.0/3.0, 2.0/3.0, 1.0/3.0], 6))
hm_rhythm_choices.extend(rep_n(nths(4)))
hm_rhythm_choices.extend(rep_n([1.0,0.5,0.5],4))
hm_rhythm_choices.extend(rep_n([0.5,0.5,1.0],4))
hm_rhythm_choices.extend(rep_n([0.5,1.0,0.5],4))
hm_rhythm_choices.extend(rep_n(nths(2),4))
	
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
        self.motif_generator = MotifGenerator(key)

    def create_phrase(self, dur, chords):
    	notes = []
    	while dur > 4*MIN_PHRASE_LENGTH:
    		# This clause is for motif generation. In the interest of time, we have temporarily disabled
    		# it because it causes a bug with durations
    		if self.motif_generator.curr_motif is not None and random.random() > 0.5 and False:
    			motif_len = self.motif_generator.curr_motif_dur
    			dur1 = motif_len*random.randint(1, min(4,dur/motif_len))
    			dur -= dur1
    			prev_note = None
    			while dur1 > 0:
    				(first_chords, chords) = split_stream(chords, motif_len)
    				new_notes = self.motif_generator.generate_from_motif(prev_note, first_chords[0])
    				prev_notes = [n for n in new_notes if n.isNote]
    				prev_note = prev_notes[-1] if len(prev_notes) else None
    				notes.extend(new_notes)
    				dur1 -= motif_len
    		else:	
    			dur1 = 4*random.randint(MIN_PHRASE_LENGTH, min(MAX_PHRASE_LENGTH, dur/4.0))
    			(first_chords, chords) = split_stream(chords, dur1)
    			dur = dur - dur1
    			notes1 = self.normal_phrase(dur1, first_chords)
    			notes.extend(notes1)
    			if self.motif_generator.curr_motif is None:
    				self.motif_generator.generate_motif(notes,4.0)
    	final_rhythm = self.get_rhythm(dur)
    	notes.extend(self.get_pitches(final_rhythm, chords))
    	return notes

    def normal_phrase(self, dur, chords):
    	rhythm = self.get_rhythm(dur)
    	notes = self.get_pitches(rhythm, chords)
    	return notes

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
    	notes = []
    	curr_dur = 0 # tracks the progress through the song
    	chord_idx = 0 # index in the chord progression
    	offset = lambda n: chords[n].offset - chords[0].offset
    	for i in range(len(rhythm)):
    		if prev_note is None:
	    		prev_note = note.Note(chords[0].root()).transpose(12) # HACKY!!!!
    		curr_rhythm = rhythm[i]
    		# first decide a direction at random
    		direction = Direction.decide(prev_note)
    		# next decide what type of tone we'd like to select
    		tone_type = ToneType.decide(curr_rhythm)
    		if chord_idx < len(chords) - 1 and offset(chord_idx + 1) < curr_dur:
    			chord_idx += 1
    		curr_chord = chords[chord_idx]
    		n = self.compute_next_note(prev_note, direction, tone_type, curr_chord)
    		n.duration = duration.Duration(curr_rhythm)
    		notes.append(n)
    		if n.isNote:
    			prev_note = n
    		else:
    			prev_note = None
    		curr_dur += curr_rhythm
    	return notes

    def compute_next_note(self, prev_note, direction, tone_type, chord):
    	"""
    	Use the arguments to determine the next note to play.
    	User must specify duration
    	"""
    	if random.random() < 0.1: # 5% chance of rest
    		return note.Rest()
    	# case on the tone_type
    	if tone_type == ToneType.AccidentalTone:
    		return prev_note.transpose(direction)
    	elif tone_type == ToneType.ChordTone:
    		return nearest_chord_note(prev_note, chord, direction)
    	elif tone_type == ToneType.ScaleTone:
    		scale = self.key.getScale().getPitches()
    		# remove the actual tone from the scale, with high probability
    		scale = [n for n in scale if n.pitchClass != prev_note.pitchClass]
    		while min([n.midi for n in scale]) > prev_note.midi:
    			scale = [n.transpose(-12) for n in scale]
    		while max([n.midi for n in scale]) < prev_note.midi:
    			scale = [n.transpose(12) for n in scale]
    		if Direction.UP == direction:
    			scale = [n if n.midi >= prev_note.midi else n.transpose(12) for n in scale]
    		else:
    			scale = [n if n.midi <= prev_note.midi else n.transpose(-12) for n in scale]
    		selectedTone = min(scale, key=lambda n:abs(n.midi - prev_note.midi))
    		ret = note.Note()
    		ret.midi = selectedTone.midi 
    		return ret
    	else:
    		assert False, "Unknown Tone Type"

class MotifGenerator:
	"""
	Stores previously played lines and
	re-generate them later
	"""
	def __init__(self, key):
		self.key = key
		self.curr_motif = None

	def generate_motif(self, notes, dur = 8.0):
		"""
		looks through notes and picks a 
		motif. Stores that in the curr_motif field.
		Returns True if it could find a motif of appropriate
		length, False 
		otherwise
		"""
		all_possible_motifs = []
		start_idx = 0
		notes_len = len(notes)
		while start_idx < notes_len:
			t = 0 # current duration
			end_index = start_idx
			while t < dur and end_index < notes_len:
				t += notes[end_index].duration.quarterLength
				end_index += 1
			# check if the total time is equal to the duration,
			# end_index is in bounds, and the average note is
			# faster than a quarter note
			if dur == t and end_index < notes_len and end_index +1 - start_idx > dur:
				all_possible_motifs.append(notes[start_idx:end_index + 1])
			start_idx += 1
		if len(all_possible_motifs) == 0:
			return False
		self.curr_motif = all_possible_motifs[random.randint(0, len(all_possible_motifs) - 1)]
		self.curr_motif_dur = dur
		return True

	def generate_from_motif(self, start_note, start_chord):
		if start_note == None:
			start_note = note.Note()
			start_note.midi = start_chord.pitches[0].midi
		else:
			start_note = nearest_chord_note(start_note, start_chord, Direction.UP)
		delta = start_note.midi - self.curr_motif[0].midi
		ret_notes = []
		for n in self.curr_motif:
			if n.isNote:
				ret_notes.append(n.transpose(delta))
			else: # is rest
				r = note.Rest()
				r.duration = duration.Duration(n.duration.quarterLength)
				ret_notes.append(r)
		print "ret_notes len {} and motif len {}".format(len(ret_notes), len(self.curr_motif))
		return ret_notes


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
