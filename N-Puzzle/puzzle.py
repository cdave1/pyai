# Copyright David Petrie 2008
#
# To solve a random 15-puzzle:
# usage: python puzzle.py
#
from random import randint
from copy import copy
import sys

LineLength = 4

UP = -LineLength
DOWN = LineLength
LEFT = -1
RIGHT = 1

trail = {}



# Represents a state of the puzzle.
class state:
	def __init__(self, old, grid, empty):
		self.oldState = old
		self.grid = grid
		self.emptyCell = empty
		self.cost = 0
		if self.oldState:
			self.cost = self.oldState.cost + 1



	def printGrid(self):
		print "Step:", self.cost
		for i in range(len(self.grid)):
			if len(str(self.grid[i])) == 1: print "",
			print self.grid[i],
			if (i+1) % LineLength == 0: print ''


	
	# Signature of the state so we can check for duplicates.
	def sig(self):
		s = ""
		for i in self.grid:
			s += "_" + str(i)
		return s



	def misplacedDistance(self):
		m = 0
		for i in range(len(self.grid)):
			if i != self.grid[i]: m += 1
		return m



	def manhattanDistance(self):
		m = 0
		for i in range(len(self.grid)):
			j = self.grid[i]
			m += (abs(i/LineLength - j/LineLength) + abs(i%LineLength - j%LineLength))
		return m



	def h1(self):
		return self.misplacedDistance() + self.cost



	def h2(self):
		return self.manhattanDistance() + self.cost



# Creates a randomised grid, starting from the goal position,
# and then makes a number of random moves. This will guarantee
# our puzzles are always solvable. Also ensures that a move cannot
# reverse a previous move (0.25 chance of happening per move).
def randomisedStartState(depth):
	grid = range(LineLength * LineLength)
	s = state(None, grid, 0)
	d = 0
	move = -1
	keys = []
	while d < depth:
		move = randint(0, 3)
		if move == 0:
			next = nextNode(s, UP)
		elif move == 1:
			next = nextNode(s, DOWN)
		elif move == 2:
			next = nextNode(s, LEFT)
		elif move == 3:
			next = nextNode(s, RIGHT)
		if next != False:
			if next.sig() not in keys:
				s = next
				keys.append(s.sig())
				d += 1
	s.cost = 0
	s.oldState = None
	return s
			


def isGoal(state):
	for i in range(LineLength * LineLength):
		if state.grid[i] != i: return False
	return True



# Creates a new grid by swapping elements in state's grid at oldPos and newPos
def swap(oldPos, newPos, state):
	g = copy(state.grid)
	tmp = g[newPos]
	g[newPos] = g[oldPos]
	g[oldPos] = tmp
	return g
	


# Get the next state when moving node in direction.
def nextNode(node, direction):
	oldPos = node.emptyCell
	newPos = newPos = oldPos + direction
	if direction == UP:
		if newPos < 0: return False;	
	elif direction == DOWN:
		if newPos > (LineLength * LineLength) - 1: return False;
	elif direction == LEFT:
		if newPos % LineLength >= oldPos % LineLength: return False;
	elif direction == RIGHT:
		if newPos % LineLength <= oldPos % LineLength: return False;
	s = state(node, swap(oldPos, newPos, node), newPos)
	if trail.has_key(s.sig()) in trail: return False
	return s



def printGoalMessage(node, comparisons):
	print "Solved!"
	print "Steps:"
	while (node != None):
		node.printGrid()
		node = node.oldState


# Simple uninformed tree search.
# If we have looked at a node already, we ignore it.
#
# Norvig mentions that there are 9!/2 = 181,400 reachable states for the 8-puzzle.
#
# Consequently, there are 1.05 * 10^13 reachable states for the 15-puzzle, meaning that
# coming up with a solution via uninformed graph search is basically intractable.
def GraphSearch(startState):
	trail = {}
	fringe = []
	comparisons = 0
	fringe.append(startState)
	while len(fringe) > 0:
		comparisons += 1
		node = fringe.pop(0)
		if isGoal(node): 
			printGoalMessage(node, comparisons)
			break
		if trail.has_key(node.sig()):
			pass
		else:
			trail[node.sig()] = node
			nodes = [nextNode(node,UP), 
				nextNode(node, DOWN), 
				nextNode(node, LEFT),
				nextNode(node, RIGHT)]

			nodes = filter(isNodeValid, nodes)
			for n in nodes:
				fringe.append(n)
	return False



def isNodeValid(n):
	return n != False



# AStarSearch
#
# Similar to graph search, except the nodes are sorted
# by a heuristic (sortFunc).
def AStarSearch(startState, sortFunc):
	trail = {}
	fringe = []
	comparisons = 0
	fringe.append(startState)
	while len(fringe) > 0:
		comparisons += 1
		node = fringe.pop()
		if isGoal(node): 
			printGoalMessage(node, comparisons)
			break
		if trail.has_key(node.sig()):
			pass
		else:
			trail[node.sig()] = node
			nodes = [nextNode(node,UP), 
				nextNode(node, DOWN), 
				nextNode(node, LEFT),
				nextNode(node, RIGHT)]

			nodes = filter(isNodeValid, nodes)

			nodes.sort(sortFunc)

			for n in nodes:
				fringe.append(n)
	return False



# Misplaced heuristic comparer
def compareNodesH1(x, y):
	if x.h1() < y.h1():
		return 1;
	elif x.h1() == y.h1():
		return 0;
	else:
		return -1



# Manhatten heuristic comparer
def compareNodesH2(x, y):
	if x.h2() < y.h2():
		return 1;
	elif x.h2() == y.h2():
		return 0;
	else:
		return -1



def solve():
	print "Solving:"
	s = randomisedStartState(10)
	s.printGrid()
	GraphSearch(s)



# Runs each algorithm 50 times for each depth to 15.
def startExperiment():
	for depth in range(15):
		print "=============================================="
		print "Depth", depth
		for i in range(50):
			#
			s = randomisedStartState(depth)
		
			#print "Graph Search"
			GraphSearch(copy(s))

			# Misplaced distance heuristic
			AStarSearch(copy(s), compareNodesH1)

			# Manhatten distance heuristic
			AStarSearch(copy(s), compareNodesH2)



solve()
