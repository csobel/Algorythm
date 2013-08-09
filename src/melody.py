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

def absReduce(x,y):
	if abs(x) < abs(y):
		return x
	else:
		return y
		
def absReduceMax(x,y):
	if abs(x) > abs(y):
		return x
	else:
		return y	
		
def getDuration(istream):
	return dcStream(istream).duration.quarterLength
	#if (len(istream) == 0):
		#return 0
	#return istream[len(istream)-1].offset - istream[0].offset + istream[0].duration.quarterLength
def dcStream(istream):
	strlen = len(istream)
	retStream = stream.Part()
	i = 0
	while (i < strlen):
		curNote = copy.deepcopy(istream[i])
		retStream.append(curNote)
		i = i+1
	return retStream.flat
	
def countCs(chordStream):
	dupStr = dcStream(chordStream)
	return dupStr.duration.quarterLength
	
	
class KGramSong:
	def __init__(self, harmony, melody):
		self.harmony = harmony.notesAndRests #a stream.Part
		self.melody = melody.notesAndRests #stream.Part
		self.minBeats = 4 #If the requested number of beats is below this, rest
		self.maxBeats = 6 #Upper bound on length of k-gram; will split into multiple parts if necessary
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
				#print getDuration(self.melody[startIndex:curIndex])
				#print dcStream(self.melody[startIndex:curIndex]).duration.quarterLength
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
			print i, len(self.ds[i-self.minBeats])
			#j=0
			#while (j < len(self.ds[i-self.minBeats])):
			#	print self.ds[i-self.minBeats][j].duration
			#	j = j + 1
			i=i+1
	def carve(self,inDur,start,end):
		lst = self.melody#self.ds[duration-self.minBeats]
		#lst.show('text')
		if (getDuration(lst[start:end]) == inDur):
			return copy.deepcopy(lst[start:end]).flat
		else:
			diff = dcStream(lst[start:(end-1)]).duration.quarterLength - inDur.quarterLength#lst[start:(end-1)].duration.quarterLength
			shortenedNote = copy.deepcopy(lst[end])
			#shortenedNote.show('text')
			oldDuration = shortenedNote.duration.quarterLength
			shortenedNote.duration = duration.Duration(-1 * diff)
			dcop = dcStream(lst[start:(end-1)])
			#print dcop.duration.quarterLength
			dcop.append(shortenedNote)
			#print inDur.quarterLength, diff, dcop.duration.quarterLength, shortenedNote.duration.quarterLength, oldDuration
			return dcop.flat
	def splitGen(self,cs,ind):
		#print ind
		print len(cs), ind
		p1 = self.generate(dcStream(cs[ind:]))
		p2 = self.generate(dcStream(cs[:ind]))
		#offSet = p1[len(p1)-1].duration
		#oldLen = len(p1)
		#p2 = map(lambda thing: thing.offset = thing.offset - offSet, p2)
		p1.append(p2)
		#i = oldLen
		return p1.flat
	def generate(self,chordStream):
		chordsOnly = chordStream.notesAndRests #Should only contain chords
		if len(chordsOnly) == 0:
			return stream.Part()
		retStream = stream.Part()
		#dur = getDuration(chordStream)
		ccsi = 0
		repeatLast = False
		while (ccsi < len(chordStream)):
			ccse = ccsi
			dur = 0
			while (dur < self.minBeats and ccse < len(chordStream)):
				dur = dur + chordStream[ccse].duration.quarterLength
				ccse = ccse + 1
			if (dur < self.minBeats):
				break
			#dur = chordStream[0].duration
			curChord = chordStream[ccsi]
			
			#TEMPORARY: Greedily assume best music comes from a k-gram between chords.
			#Try to generate a full-length k-gram.
			if (dur > self.maxBeats):
				return self.splitGen(chordStream, len(chordStream)/2)
			extraResting = dur #Add rests to this!
			dur = int(dur)
			print dur-self.minBeats
			rnd = int(random.random() * len(self.ds[dur-self.minBeats]))
			
			targInd = dur-self.minBeats
			if (len(self.ds[targInd]) != 0):
				i=0
				if not repeatLast:
					maxDiff = 1000
					actualDiff = 0
					bestIndex = 0
					while (i < len(self.ds[targInd])):
						curMelFrag = self.ds[targInd][i]
						#possDiff = min(curChord.pitches, key=lambda curPitch: abs((curPitch.midi - curMelFrag[0].midi) % 12))
						diffMappings = map(lambda curPitch: (curPitch.midi % 12)- (curMelFrag[0].midi % 12), curChord.pitches)
						possDiff = reduce(absReduce, diffMappings)
						rndNum = random.random()
						if (abs(possDiff) <= maxDiff):
							rndVar = random.random()
							if (abs(possDiff) < maxDiff or rndVar > 0.95):
								#print possDiff, maxDiff, rndVar
								maxDiff = abs(possDiff)
								actualDiff = possDiff
								bestIndex = i
						#if (random.random() > 0.9):
						#	maxDiff = abs(possDiff)
						#	actualDiff = possDiff
						#	bestIndex = i
							#print "THUNDERDOME'D"
						#print maxDiff, possDiff
						#for chordPitch in curChord.pitches:
						#	if (chordPitch == curMelFrag[0].pitch):
						#		return dcStream(self.ds[targInd][i])
						i=i+1
				retMel = dcStream(self.ds[targInd][bestIndex])
				print "Picked index ", targInd, bestIndex
				#return copy.deepcopy(self.ds[targInd][rnd]).flat
				#return dcStream(self.ds[targInd][bestIndex])
				if (repeatLast or random.random() > 0.9):
					if (repeatLast):
						actualDiff = actualDiff - int((random.random() - 0.5) * 6)
					#print "Transposing by ", actualDiff
					retMel = retMel.transpose(actualDiff)
				retStream.append(retMel)
				#retStream = retStream.flat
				extraResting = extraResting - self.ds[targInd][bestIndex].duration.quarterLength
			#else:
			if (extraResting != 0.0):
				print "Making rest"
				restStr = stream.Part()
				#restNote = note.Rest(targInd)
				restNote = note.Rest(extraResting)
				restStr.append(restNote)
				retStream.append(restStr)
				retStream = retStream.flat
				#return restStr
			#return self.splitGen(chordStream, len(chordStream)/2)
			#Just generate a k-gram based on the first and last chords.
			#Otherwise, we actually have to generate some melody :D
			ccsi = ccse
			repeatLast = False
			if (random.random() > 0.9):
				repeatLast = True
			
		return retStream

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
	print "Finished making DS!"
	coolmel = testkgs.generate(har)
	prod = stream.Score()
	prod.append(coolmel)
	#coolmel.show('text')
	prod.append(har)
	return (prod, testkgs)
	#mainStream = stream.Score()
	
	#Build k-gram data structure from melody using harmony info
	#mainStream.append(har) #Harmony will always be present