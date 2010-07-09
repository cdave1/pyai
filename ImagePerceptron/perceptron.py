# Copyright David Petrie 2008
#
# Perceptron
import sys
import random
from copy import copy



# Represents data in the input file
class image:
	def __init__(self, imageClass, width, height, imageData):
		self.imageClass = imageClass
		self.width = width
		self.height = height
		self.imageData = imageData



	def getPixel(self, x, y):
		return int(self.imageData[(y * 10) + x])



	def printImage(self):
		s = ""
		for x in range(10):
			for y in range(10):
				if self.getPixel(x,y) == 0: s+=' '
				else: s+='O'
			s += '\n'
		print s
			


class perceptron:
	# On instatiation, create a set of random weights and features
	def __init__(self, epochLimit=100):
		self.features = []
		self.weights = []
		self.epochLimit = epochLimit
		self.length = 50
		for i in range(self.length):
			self.weights.append(random.choice([1, -1]))
			self.features.append(feature(i))



	# Weighted match, including the dummy weight
	def isMatch(self, image):
		w = [self.weights[i] * self.features[i].match(image) for i in range(self.length)]
		return 1 + sum(w)
		


	def addWeights(self, image):
		for i in range(self.length):
			self.weights[i] += self.features[i].match(image)



	def subtractWeights(self, image):
		for i in range(self.length):
			self.weights[i] -= self.features[i].match(image)



	# Train the perceptron to accept any images in the class imageClass
	# and reject any not in that class.
	def train(self, images, imageClass):
		correct, epoch = 0, 0
		while (correct < len(images)) and (epoch < self.epochLimit):
			for img in images:
				if img.imageClass == imageClass:
					if self.isMatch(img) <= 0: 
						self.addWeights(img)
				else:
					if self.isMatch(img) > 0:
						self.subtractWeights(img)
			correct = 0
			for img in images:
				if self.test(img) == img.imageClass: correct += 1
			epoch += 1
		
		if correct == len(images): 
			print "Completely correct for all images after %d epochs." % epoch
		else: 
			print "Reached epoch limit (%d) - some images not classified correctly." % self.epochLimit



	def test(self, image):
		if self.isMatch(image) > 0: return "#Yes"
		return "#other"



class feature:
	# On instantiation, create a set of four pixels.
	def __init__(self, seed=-1):
		self.pixels = []
		if seed == -1: random.seed()
		else: random.seed(seed)

		for i in range(4):
			self.pixels.append([random.choice(range(10)), 
					random.choice(range(10)), 
					random.choice(range(2))])



	def printPixels(self, image):
		print [image.getPixel(p[0], p[1]) for p in self.pixels]



	def match(self, image):
		f = lambda p: image.getPixel(p[0], p[1]) == p[2]
		return len(filter(f, self.pixels)) > 2



# Handles loading of images, training percepton, and then
# testing the training data against the perceptron.
def main(argv):
	print "Loading Images:"
	images = loadImages(argv[0])

	print "Training:"
	if len(argv) >= 2: p = perceptron(int(argv[1]))
	else: p = perceptron()
	p.train(images, "#Yes")
	print "Features [x, y, true/false]:"
	for f in p.features: print f.pixels
	print "Final weights:"
	print p.weights
	print "Testing training data against perceptron:"
	getResults(images, p)
	
	print "\nTesting:"


	if len(argv) == 3: 
		testingImages = loadImages(argv[2])
		getResults(testingImages, p)



def getResults(images, perceptron):
	correct = 0
	for img in images:
		if img.imageClass == perceptron.test(img): correct += 1
	if correct < len(images): 
		print "%3.1f%% were correctly classified." % (float(correct*100)/len(images))
	else:
		print "100% were correctly classified."
	
	

def loadImages(imageFile):
	f = open(imageFile, "r")
	raw = [line for line in f.readlines() if line != '\n']
	images = []

	# for each instance of "P1" get the next four lines from
	# the raw data. Clean the data up while doing this.
	for i in range(len(raw)):
		if "P1" in raw[i]:
			wh = raw[i+2].split(" ")
			w, h = int(wh[0]), int(wh[1])
			width = raw[i+2]
			images.append(image(raw[i+1].strip('\n'), w, h, 
				raw[i+3].strip('\n') + raw[i+4].strip('\n')))
	print "%d images were loaded." % len(images)
	return images
	


if __name__ == "__main__":
	main(sys.argv[1:])
