from expand import expand
# import heapq as heapMethods
from queue import PriorityQueue as PQ
from collections import deque

class Node:
	def __init__(self,name,parent=None): # ,goalName,time_map,dis_map):
		self.name = name
		self.g = 0 # parent and time_map[parent.name][name] or 0
		self.h = 0 # dis_map[name][goalName]
		self.f = 0
		self.parentNode = parent
	
	def __repr__(self):
		return "Node // Name: "+self.name+" | f: "+str(self.f)

	def __lt__(self,o):
		return self.f < o.f

	def __eq__(self,o):
		return self.f == o.f

	def __gt__(self,o):
		return not (self < o or self == o)

	def __ge__(self,o):
		return not (self < o)

	def __le__(self,o):
		return not (self > o)

	def calcF(self):
		self.f = self.g + self.h

# f(n) = h(n) + g(n) -- used in the PQ
# dist map: h(n)
# time map: g(n)
# return path from landmark start to landmark end
def a_star_search (dis_map, time_map, start, end):
	#avoiding errors
	if start not in dis_map or start not in time_map:
		return []
	if end not in dis_map[start]:
		return []

	path = [] #output
	pq = PQ() #for organizing
	poppedNodes = [] #bookkeeping for graph search

	startNode = Node(start)
	startNode.g = 0
	startNode.h = dis_map[start][end]
	startNode.calcF()

	#add start to popped list
	currentNode = startNode
	poppedNodes.append(currentNode.name)
	while currentNode.name != end:
		
		neighbors = expand(currentNode.name,time_map)
		""" print(currentNode.name + "'s neighbors:")
		print(neighbors) """
		for n in neighbors:
			if not (n in poppedNodes):
				node = Node(n,currentNode)
				node.g = time_map[node.parentNode.name][n] + node.parentNode.g

				#avoiding errors
				if n in dis_map and end in dis_map[n]:
					node.h = dis_map[n][end]
				else:
					return []

				node.calcF()
				pq.put((node,node.name))
		
		#if pq is empty, the node has no neighbors to help it reach the goal (NO PATH)
		if not pq.empty():
			pair = pq.get()
			currentNode = pair[0]
			poppedNodes.append(currentNode.name)
		else:
			return []

	#go up from currentNode and push to front of a list, creating path
	path = deque(path)
	#pathTime = currentNode.f
	while currentNode is not None:
		path.appendleft(currentNode.name)
		currentNode = currentNode.parentNode
	path = list(path)
	return path #,pathTime

def main():
	pq = PQ()
	node1 = Node("tost",None)
	node2 = Node("testing",None)
	pq.put((node1,node1.name))
	pq.put((node2,node2.name))

	print(pq)

	while not pq.empty():
		print(pq.get()[0])
