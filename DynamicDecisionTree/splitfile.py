import sys
import random



def getList(line):
	filterInput = lambda string: string != '\n' and string != ''
	return filter(filterInput, line.split())



def main(argv):
	f = open(argv[0], "r")
	prefix = argv[0].split('.')[0]
	ext = argv[0].split('.')[1]
	splitCount = int(argv[1])

	suffix = argv[2]

	instances = []
	classes = f.readline()
	attributes = f.readline()
	instances = [l for l in f.readlines()]
	random.shuffle(instances)

	trainFile = open(prefix +"-train"+ suffix + "."+ext, "w")
	trainFile.write(classes)
	trainFile.write(attributes)
	for l in instances[:splitCount]:
		trainFile.write(l)
	trainFile.close()

	testFile = open(prefix +"-test"+ suffix + "."+ext, "w")
	testFile.write(classes)
	testFile.write(attributes)
	for l in instances[splitCount:]:
		testFile.write(l)
	testFile.close()





if __name__ == "__main__":
	main(sys.argv[1:])
