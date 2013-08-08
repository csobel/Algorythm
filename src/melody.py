# contains simple functions to test improv code
import improv
import sample_input
from music21 import *

import copy
import random
#Parses information about the melody/harmony of a song
#Note: k-gram must start and end on a note, not a rest

#Can't do a delta between start/end... different chords!
#Brute force solution?

def getDuration(stream):
	if (len(stream) == 0):
		return 0
	return stream[len(stream)-1].offset - stream[0].offset# + stream[0].duration.quarterLength
def dcStream(istream):
	strlen = len(istream)
	retStream = stream.Part()
	i = 0
	while (i < strlen):
		curNote = copy.deepcopy(istream[i])
		retStream.append(curNote)
		i = i+1
	return retStream
	
class KGramSong:
	def __init__(self, harmony, melody):
		self.harmony = harmony.notesAndRests #a stream.Part
		self.melody = melody.notesAndRests #stream.Part
		self.minBeats = 4 #If the requested number of beats is below this, rest
		self.maxBeats = 16 #Upper bound on length of k-gram; will split into multiple parts if necessary
	def makeDS(self): #Assumes it's been init'd properly
		#For all beats counts between min and max, calculate the ending note
		self.ds = []
		i = self.minBeats
		while (i <= self.maxBeats):
			self.ds.append([])
			i = i + 1
		melLen = len(self.melody)
		print melLen
		i = 0
		#self.melody.show('text')
		while (i < melLen):
			startIndex = i
			curIndex = startIndex
			j = self.minBeats
			while (j <= self.maxBeats and curIndex < melLen and not self.melody[startIndex].isRest):
				while (getDuration(self.melody[startIndex:curIndex]) < j and curIndex < melLen):
					curIndex = curIndex + 1
				if (curIndex < melLen and not (self.melody[curIndex].isRest)):
					roflmao = self.carve(duration.Duration(j),startIndex,curIndex)
					#print len(roflmao), roflmao.duration, getDuration(roflmao)
					self.ds[j-self.minBeats].append(roflmao)
					#self.ds[j-self.minBeats].append((startIndex, curIndex))
				j = j + 1
			i = i+1
			#print i, melLen
		i=self.minBeats
		while (i <= self.maxBeats):
			#print i, len(self.ds[i-self.minBeats])
			i=i+1
	def carve(self,inDur,start,end):
		lst = self.melody#self.ds[duration-self.minBeats]
		#lst.show('text')
		if (getDuration(lst[start:end]) == inDur):
			return copy.deepcopy(lst[start:end]).flat
		else:
			diff = inDur.quarterLength - lst[start:(end-1)].duration.quarterLength
			shortenedNote = copy.deepcopy(lst[end])
			#shortenedNote.show('text')
			shortenedNote.duration = duration.Duration(diff)
			dcop = dcStream(lst[start:(end-1)])
			dcop.append(shortenedNote)
			return dcop.flat
	def splitGen(self,cs,ind):
		#print ind
		p1=self.generate(dcStream(cs[ind:]))
		p2 = self.generate(dcStream(cs[:ind]))
		#print p1,p2
		#print len(p1),len(p2)
		#p1.show('text')
		#p2.show('text')
		p1.append(p2)
		return p1.flat
	def generate(self,chordStream):
		retStream = stream.Part()
		dur = getDuration(chordStream)
		if (dur < self.minBeats): #Just rest
			fullRest = note.Rest()
			fullRest.duration = duration.Duration(dur)
			retStream.append(fullRest)
			return copy.deepcopy(retStream.flat)
		
		#TEMPORARY: Greedily assume best music comes from a k-gram between chords.
		#Try to generate a full-length k-gram.
		if (dur > self.maxBeats):
			return self.splitGen(chordStream, len(chordStream)/2)
		dur = int(dur)
		rnd = int(random.random() * len(self.ds[dur-self.minBeats]))
		print rnd, len(self.ds[dur-self.minBeats])
		if (len(self.ds[dur-self.minBeats]) != 0):
			return copy.deepcopy(self.ds[dur-self.minBeats][rnd]).flat
		else:
			restStr = stream.Part()
			restNote = note.Rest(dur)
			restStr.append(restNote)
			return restStr
		#return self.splitGen(chordStream, len(chordStream)/2)
		#Just generate a k-gram based on the first and last chords.
		#Otherwise, we actually have to generate some melody :D
		
			
		

def test_on_prog(chordStrs):
    num_measures = 4
    s = stream.Score()
    harm = improv.createHarmony(chordStrs, num_measures/2)
    solo = improv.createSolo(chordStrs, num_measures)
    s.append(solo)
    s.append(harm)
    return s
	
def load_sample():
	(har,mel) = sample_input.IGotRhythm()
	testkgs = KGramSong(har,mel)
	testkgs.makeDS()
	coolmel = testkgs.generate(har)
	prod = stream.Score()
	prod.append(coolmel)
	coolmel.show('text')
	prod.append(har)
	return prod
	#mainStream = stream.Score()
	
	#Build k-gram data structure from melody using harmony info
	#mainStream.append(har) #Harmony will always be present