from music21 import *
import melody, harmony

#Grabs a deep copy of the given stream, while going as little over the given duration
#as possible.  Also returns a deep copy of the 
def extractDuration(inStream, inDuration):
	endIndex = 0
	totalDuration = 0
	while (totalDuration <= inDuration and endIndex < len(inStream)-1):
		totalDuration = totalDuration + inStream[endIndex].duration.quarterLength
		endIndex = endIndex + 1
	return (melody.dcStream(inStream[:endIndex]), melody.dcStream(inStream[endIndex:]))
def makeSolo(melodyInput, harmonyInput):
	key = melodyInput[0]
	kgram = melody.KGramSong(melodyInput, harmonyInput)
	harmonyMaker = HarmonyPhrase(key)
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
			generatedMelody.append(curStream.duration, curStream)
		useMelody = not useMelody
			
	generatedSong.append(generatedMelody)
	generatedSong.append(harmonyInput)