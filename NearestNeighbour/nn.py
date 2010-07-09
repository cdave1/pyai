# Copyright David Petrie 2008
#
# Part 1: Nearest neighbour
import sys
from math import sqrt
from copy import copy

k = 1
testVals = []
trained = []
ranges = []



# Distance between two feature vectors
def distance(a, b):
	d = [((a[i] - b[i])**2)/ranges[i] for i in range(4)]
	return sqrt(sum(d))



# Creates a new list with the distance at the head.
def getDistance(r, t):
	l = copy(r);
	l.insert(0, distance(l, t))
	return l



# Sorts list of results by distance/
def sorter(a, b):
	if a[0] < b[0]: return 1
	elif a[0] == b[0]: return 0
	else: return -1



# Converts s to a float for map function
def toFloat(s):
	try: return float(s)
	except: return s



# Read each line in the file, create lists for all values, then convert to floats.
def trainedSet(trainingFile):
	f = open(trainingFile, "r")
	return [map(toFloat, line.split("  ")) for line in f.readlines() if line != '\n']



# Gets available ranges from the training data for each feature
def getRanges(dataSet):
	r = []
	for i in range(4):
		l = [data[i] for data in dataSet]
		r.append(max(l) - min(l))
	return r	



# Tests the testfile against the trained set of data
def test(trainedSet, testFile):
	f = open(testFile, "r")
	# Read each line in the file, create lists for all values, then convert to floats.
	testSet = [map(toFloat, line.split("  ")) for line in f.readlines() if line != '\n']

	correct = 0
	line = 1
	for t in testSet:
		nearest = []
		nearest = map(getDistance, trainedSet, [t for i in range(len(trainedSet))])
		nearest.sort(sorter)
		# Get top k items and find the most common
		winner = ""
		if k == 1:
			winner = nearest.pop().pop()
		else:
			nearest = [nearest.pop().pop() for i in range(k)]
			maj = 0

			for result in nearest:
				if nearest.count(result) > maj:
					maj = nearest.count(result)
					winner = result	

		expected = t.pop()
		if winner == expected: 
			correct += 1
			print "Line", line, " matched. Expected", expected, " and found", winner
		else: print "*** Mismatch on line", line, ". Expected", expected, " but found", winner
		line += 1
	print correct, "/", len(testSet)



trained = trainedSet(sys.argv[1])
if len(sys.argv) == 4: k = int(sys.argv[3])
ranges = getRanges(trained)
test(trained, sys.argv[2])
