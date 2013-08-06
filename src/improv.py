from music21 import *

def createHarmony(chordStrs, num_repeats = 1):
    """
    Test method to create some chords.
    Each chord will last for 1/2 a measure
    """
    s = stream.Part()
    for _ in range(num_repeats):
        chords = map(harmony.ChordSymbol, chordStrs)
        for c in chords:
            c.duration = duration.Duration(1.5)
            r = note.Rest()
            r.duration = duration.Duration(0.5)
            s.append(c)
            s.append(r)
    return s

def closestPitch(mchord, mnote):
    """
    finds the pitch in mchord that is closest to mnote
    """
    mnoteInt = mnote.octave*12 + mnote.pitchClass
    mpitches = mchord.pitches
    pitchInts = [mpitch.octave*12 + mpitch.pitchClass for mpitch in mpitches]
    pitchInts = [p for p in pitchInts if p != mnoteInt]
    print "chord: {} and note: {}".format(pitchInts, mnoteInt)
    retInt = min(pitchInts, key=lambda x:abs(x-mnoteInt))
    retPitch = pitch.Pitch()
    retPitch.pitchClass = retInt % 12
    retPitch.octave = retInt / 12
    return retPitch
    

def createSolo(chordProg, num_measures):
    """
    Test method to create a super simple solo.
    Still will assume, for now, that each chord
    lasts for 2 beats (half a measure)
    """
    solo = stream.Part()
    if type(chordProg[0]) == type(''):
        chordProg = map(harmony.ChordSymbol, chordProg)
    curr_note = None # for now
    for measure_num in range(num_measures):
        for i in range(4): # iterate by quater note
            curr_chord = chordProg[(2*measure_num + i/2) % len(chordProg)]
            next_note = note.Note()
            if curr_note is None:
                next_note.pitch = curr_chord.root()
            else:
                next_note.pitch = closestPitch(curr_chord, curr_note)
            next_note.duration = duration.Duration(1.0)
            solo.append(next_note)
            curr_note = next_note
    return solo
                
        
