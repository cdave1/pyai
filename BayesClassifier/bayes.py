# Copyright David Petrie 2008
#
# Naive Bayes Classifier.
import sys
from operator import mul



# So filter has something to use
def notEmpty(s): return len(s) != 0
# Checks if last item is 1
def isSpam(l): return l[-1:][0] == 1
# Opposite of isSpam (assuming possible values are 0 and 1)
def isNotSpam(l): return not isSpam(l)



# Gets the files and trains with first, tests with second.
def main(argv):
	print "Training"
	classifier = classify(argv[0])

	print ""
	print "Testing Results (Indicates chance of not being spam)"
	test(classifier, argv[1])             



# Creates a classifier based on training data in the supplied file.
#
# The classifier returned is just a dictionary of items.
def classify(file):
	classifier = {}
	f = open(file, "r")

	# read each line from the file, split by spaces and convert each entry to an int.
	v = [map(int, filter(notEmpty, line.split(" "))) for line in f.readlines() if line != '\n']

	spamEntries = filter(isSpam, v)
	nonSpamEntries = filter(isNotSpam, v)
	
	spam = getRatios(spamEntries)
	nonSpam = getRatios(nonSpamEntries)
	all = getRatios(v)

	print "Total entries in training set:"
	print len(v)
	print "Entries marked as spam:"
	print len(spamEntries)
	print "Entries marked as non-spam:"
	print len(nonSpamEntries)
	print "Feature occurences in sets marked as spam:"
	print spam
	print "Feature occurences in sets marked non-spam:"
	print nonSpam
	print "Feature occurences in both:"
	print all

	classifier["spam"] = spam
	classifier["nonSpam"] = nonSpam
	classifier["all"] = all
	classifier["pSpam"] = float(len(spamEntries)) / float(len(v))
	classifier["pNonSpam"] = float(len(nonSpamEntries)) / float(len(v))

	return classifier



# Gets the occurences of each feature in the class, divided by number of entries.
def getRatios(entries):
	print len(entries)
	probs = [1 for i in range(len(entries[0])-1)]
	for e in entries:
		for i in range(len(e)-1):
			if e[i] == 1: probs[i] += 1
	f = lambda x: float(x) / float(len(entries))
	return map(f, probs)



# Tests all items in the testFile against data in the classifier. 
def test(classifier, testFile):
	f = open(testFile, "r")
	testSet = [map(int, filter(notEmpty, line.split(" "))) for line in f.readlines() if line != '\n']

	# For each feature in the test set, take the number, and then get the probability from
	# classifier
	for t in testSet:
		print t
		pSpam = getProbability(t, classifier['spam'], classifier['all'], classifier['pSpam'])
		pNonSpam = getProbability(t, classifier['nonSpam'], classifier['all'], classifier['pNonSpam'])
		print "Spam probability: %0.3f" % pSpam
		print "Non-spam probability: %0.3f" % pNonSpam
		print 



# Returns the Bayesian probability that testData belongs to
# the class represented by classFeatures.
#
# Returned values are capped at 1.0.
def getProbability(testData, classFeatures, allFeatures, classRatio):
	pSpam = []
	pAll = []

	for i in range(len(classFeatures)):
		if testData[i] == 1: 
			pSpam.append(classFeatures[i])
			pAll.append(allFeatures[i])
		else: 
			pSpam.append(1.0 - classFeatures[i])
			pAll.append(1.0 - allFeatures[i])

	p = (reduce(mul, pSpam) * classRatio) / reduce(mul, pAll)
	return min(1, p)



if __name__ == "__main__":
	main(sys.argv[1:])
