from music21 import *
import melody, harmony
import sample_input
from copy import deepcopy

#Grabs a deep copy of the given stream, while going as little over the given duration
#as possible.  Also returns a deep copy of the 
def extractDuration(inStream, inDuration):
	endIndex = 1
	totalDuration = 0
	while (totalDuration <= inDuration and endIndex < len(inStream)-1):
		totalDuration = totalDuration + inStream[endIndex].duration.quarterLength
		endIndex = endIndex + 1
	return (melody.dcStream(inStream[:endIndex]), melody.dcStream(inStream[endIndex:]))
def makeSolo(melodyInput, harmonyInput):
	key = melodyInput[0]
	kgram = melody.KGramSong(harmonyInput, melodyInput)
	kgram.makeDS()
	harmonyMaker = harmony.HarmonyPhrase(key)
	qbs = 64 #16 measures before each switch
	useMelody = True
	generatedSong = stream.Score()
	generatedMelody = stream.Part()
	remainderStream = harmonyInput
	while (len(remainderStream) != 0):
		(curStream, remainderStream) = extractDuration(remainderStream, qbs)
		if useMelody:
			generatedMelody.append(kgram.generate(curStream))
		else:
			generatedMelody.append(harmonyMaker.create_phrase(curStream.duration.quarterLength, curStream))
		useMelody = not useMelody
			
	generatedSong.append(generatedMelody.flat)
	generatedSong.append(harmonyInput)
	return generatedSong

def IGotRhythm():
	(harmony, melody) = sample_input.IGotRhythm()
	return makeSolo(melody, harmony)

def WithMelody(song):
	(harmony, melody) = song()
	soloPart = makeSolo(melody, harmony)[0]
	harmonyPart = stream.Part()
	harmonyPart.append(harmony)
	harmonyPart.append(deepcopy(harmony))
	harmonyPart = harmonyPart.flat
	lead = stream.Part()
	lead.append(melody)
	lead.append(soloPart)
	lead = lead.flat
	song = stream.Score()
	song.append(lead)
	song.append(harmonyPart)
	return song


def IGotRhythmWithMelody():
	return WithMelody(sample_input.IGotRhythm)

def AutumnLeavesWithMelody():
	return WithMelody(sample_input.AutumnLeaves)

if __name__ == '__main__':
	song = IGotRhythmWithMelody()
	song.show("midi")