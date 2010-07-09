# Copyright David Petrie 2008
#
# Decision Tree
import sys
from math import log
from copy import copy

baseline = ""



# Represents a set of attributes and corresponding values
class instance:
	def __init__(self,attributes,values,classType):
		self.attributes = attributes
		self.values = values
		self.classType = classType



	def printVals(self):
		print self.attributes
		print self.values
		print self.classType



	# Might be better to do this in a hash table, but too much
	# glue code needed - assume list orders don't change :)
	def getAttributeValue(self, attribute):
		for i in range(len(self.attributes)):
			if self.attributes[i] == attribute: return self.values[i]



# Represents a node in the decision tree
class node:
	def __init__(self):
		self.classType = "noclass"
		self.attribute = "leaf"
		self.nodes = {}



	def setNode(self, key, node):
		self.nodes[key] = node



	def setClassType(self, classType):
		self.classType = classType



	def printNodes(self, indent = ""):
		if len(self.nodes) == 0:
			print indent, "=> Class:", self.classType, "(prob: 100%)"
		else:
			for k, v in self.nodes.iteritems():
				print indent, self.attribute, "=", k
				v.printNodes(indent + "   ")



	def getChildNode(self, instance):
		key = instance.getAttributeValue(self.attribute)
		if self.nodes.has_key(key):
			return self.nodes[key]



def main(argv):
	print "Training"
	root = train(argv[0])

	print "Training complete. Tree looks like this:"
	root.printNodes()
	if len(argv) == 2:
		print "\nTesting Results:"
		test(root, argv[1])



# Build the tree
def train(fileName):
	instances = []
	f = open(fileName, "r")
	classes = getList(f.readline())
	attributes = getList(f.readline())

	for l in f.readlines():
		vals = getList(l)
		instances.append(instance(attributes, vals[1:], vals[0]))

	global baseline
	baseline = GetClassMajority(instances, classes)

	print "Classes:", classes
	print "Attributes:", attributes
	print "Number of instances:", len(instances)
	print "Baseline classifier:", baseline

	node = BuildNode(instances, attributes, classes)
	
	return node



def test(node, fileName):
	f = open(fileName, "r")
	classes = getList(f.readline())
	attributes = getList(f.readline())
	instances = []

	for l in f.readlines():
		vals = getList(l)
		instances.append(instance(attributes, vals[1:], vals[0]))

	correct = 0
	correctBaseline = 0
	for i in instances:
		if testInstance(node, i): correct += 1
		if i.classType == baseline: correctBaseline += 1
	print "Tree prediction accuracy: %3.1f%%" % (float(correct*100)/len(instances))
	print "Baseline prediction accuracy (%s):" % baseline,
	print "%3.1f%%" % (float(correctBaseline*100)/len(instances))



def testInstance(node, instance):
	while(len(node.nodes) > 0):
		node = node.getChildNode(instance)
	return instance.classType == node.classType



# Builds a tree of nodes for the decision tree.
def BuildNode(instances, attributes, classes):
	n = node()
	if len(instances) == 0:
		n.setClassType(baseline)
		return n
	elif IsPure(instances,classes):
		n.setClassType(GetClassMajority(instances, classes))
		return n
	elif len(attributes) == 0:
		n.setClassType(GetClassMajority(instances, classes))
		return n
	else:
		bestAttr = FindBestAttribute(instances,attributes,classes)
		trueInstances = GetAttributeInstances(instances, bestAttr, 'true')
		falseInstances = GetAttributeInstances(instances, bestAttr, 'false')
		n.attribute = bestAttr
		tmpAttr = copy(attributes)
		tmpAttr.remove(bestAttr)

		n.setNode('true', BuildNode(trueInstances, tmpAttr, classes))
		n.setNode('false', BuildNode(falseInstances, tmpAttr, classes))
		return n



def getList(line):
	filterInput = lambda string: string != '\n' and string != ''
	return filter(filterInput, line.split())



# Returns a list showing number of instances under each class
def GetClassInstances(instances, classType):
	inClass = lambda instance: instance.classType == classType
	return filter(inClass, instances)



# Returns all instances that have an attribute value == value
def GetAttributeInstances(instances, attr, value):
	f = lambda instance: instance.getAttributeValue(attr) == value
	return filter(f, instances)
	


def IsPure(instances,classes):
	lengths = [len(GetClassInstances(instances, c)) for c in classes]
	total = sum(lengths)
	for l in lengths:
		if l == total: return True
	return False



# Find class with the largest number of instances
def GetClassMajority(instances,classes):
	maxLen = 0
	maxClass = ""
	for c in classes:
		classInstances = GetClassInstances(instances, c)
		if len(classInstances) >= maxLen: 
			maxLen = len(classInstances)
			maxClass = c
	return maxClass



# Finds the best available attribute by looking at the weighted
# impurity measure.
def FindBestAttribute(instances,attributes,classes):
	maxImpurity = 1
	# bestAttribute = attributes[0]
	for a in attributes:
		imp = WeightedImpurity(instances, a, classes)
		
		if imp <= maxImpurity:
			maxImpurity = imp
			bestAttribute = a
	return bestAttribute



# Weighted impurity of the node
#
# Sigma_i[P(node_i) * impurity(node_i)]
def WeightedImpurity(instances, attr, classes):
	t = GetAttributeInstances(instances, attr, 'true')
	f = GetAttributeInstances(instances, attr, 'false')
	lt, lf = len(t), len(f)
	pt = float(lt)/float(lt+lf)
	pf = float(lf)/float(lt+lf)

	return (pt * Impurity(t, classes)) + (pf * Impurity(f, classes))



# Impurity measure from lecture notes
def Impurity(instances, classes):
	a = len(GetClassInstances(instances, classes[0]))
	b = len(GetClassInstances(instances, classes[1]))

	if (a + b) == 0: return 0
	return float(a*b) / float(pow((a + b), 2))



if __name__ == "__main__":
	main(sys.argv[1:])
