from music21 import *
import random

def createHarmony(chordStrs, num_repeats = 1):
    """
    Test method to create some chords.
    Each chord will last for 1/2 a measure
    """
    s = stream.Part()
    for _ in range(num_repeats):
        chords = map(harmony.ChordSymbol, chordStrs)
        longRest = True
        for c in chords:
            c.duration = duration.Duration(1.0 if longRest else 1.5)
            r = note.Rest()
            r.duration = duration.Duration(1.0 if longRest else 0.5)
            s.append(c)
            s.append(r)
            longRest = not longRest
    return s

def scaleInRange(lower, upper, keyStr = "C"):
    """
    returns all the pitches in key k between lower and upper
    """
    return scale.MajorScale(keyStr).getPitches(lower, upper)

def closestPitch(mchord, mnote):
    """
    finds the pitch in mchord that is closest to mnote,
    but not equal to mnote
    """
    mpitches = mchord.pitches
    pitchInts = [i*12 + mpitch.pitchClass for i in range(5,8) for mpitch in mpitches]
    pitchInts = [p for p in pitchInts if p != mnote.midi]
    retInt = min(pitchInts, key=lambda x:abs(x-mnote.midi))
    retPitch = pitch.Pitch()
    if retPitch.midi < 12*4:
        print "BAD {}".format(retPitch)
    retPitch.midi = retInt
    return retPitch
    
def pickPitch(curr_note, dest_chord):
    """
    given a current note, curr note and
    the chord we need to end up on. Pick
    a pitch from that chord.
    """
    # just uniformly pick something in a one octave range
    # surronding the note
    delta = random.randint(-6, 6)
    trans_note = curr_note.transpose(delta)
    result = closestPitch(dest_chord, trans_note)
    return result
    

def next(part, curr_note, next_chord):
    """
    given a current note and a destination chord,
    advances the piece by 2 notes. Updates part
    to include these two notes and returns the next 
    recommended note to play
    """
    print "next input {}".format(curr_note.midi)
    part.append(curr_note)
    target = note.Note()
    target.duration = duration.Duration(1.0)
    target.pitch = pickPitch(curr_note, next_chord)
    intermediate = note.Note()
    intermediate.duration = duration.Duration(1.0)
    if abs(target.midi - curr_note.midi) < 2:
        intermediate.pitch = closestPitch(next_chord, target)
    else:
        if random.randint(0,1):
            delta = -1 if curr_note.midi < target.midi else 1
            intermediate.pitch = target.pitch.transpose(delta)
        else:
            if curr_note.midi < target.midi:
                pitchChoices = scaleInRange(curr_note, target)
            else:
                pitchChoices = scaleInRange(target, curr_note)
            if len(pitchChoices) > 0:
                intermediate.pitch = pitchChoices[random.randint(0,len(pitchChoices)-1)]
            else:
                intermediate.pitch = target.pitch # TODO, this is kinda arbitrary, but fixes bug!
    part.append(intermediate)
    print "next output {} \n".format(target.pitch.midi)
    return target # return next note to play


def createSolo(chordProg, num_measures):
    """
    Test method to create a super simple solo.
    Still will assume, for now, that each chord
    lasts for 2 beats (half a measure)
    """
    solo = stream.Part()
    if type(chordProg[0]) == type(''):
        chordProg = map(harmony.ChordSymbol, chordProg)
    curr_note = note.Note()
    curr_note.duration = duration.Duration(1.0)
    curr_note.pitch = chordProg[0].root().transpose(12)
    for measure_num in range(num_measures):
        for i in range(2): #iterate by half note
            next_chord = chordProg[(1 + 2*measure_num + i) % len(chordProg)]
            curr_note = next(solo, curr_note, next_chord)
    return solo
                
        
