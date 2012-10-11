import copy
import sys
import collections
from pprint import pprint

class Graph(object):
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges
	
	def draw(self):
		g = pgv.AGraph()
		
		for edge in self.edges:
			g.add_edge(edge.source, edge.target, capacity=edge.capacity)
		
		g.layout()
		
		print g.draw("a.dot")
	
	def __repr__(self):
		return "Graph:\nNodes: \n" + repr(self.nodes) + "\nEdges:\n" + repr(self.edges)

class Node(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.edges = []
	def __repr__(self):
		return "Node: %s %s Edges: %i" % (self.id, self.name, len(self.edges))
		
class Edge(object):
	def __init__(self, source, target, capacity):
		self.source = source
		self.target = target
		self.capacity = capacity
		self.flow = 0
		self.reverse = None
	
	def __repr__(self):
		return "%s->%s @ Capacity: %s Flow: %s Residual: %s" % (self.source, self.target, self.capacity, self.flow, self.capacity - self.flow)

def parse(f):
	file = open(f)
	nodes = []
	edges = []
	n = int(file.readline().strip())
	for i in range(0, n):
		node = file.readline().strip()
		node = Node(i, node)
		nodes.insert(i, node)
		
	m = int(file.readline().strip())
	arcs = dict()
	residual = dict()
	for i in range(0, m):
		nodeA, nodeB, capacity = file.readline().strip().split()
		nodeA = int(nodeA)
		nodeB = int(nodeB)
		capacity = int(capacity)
		
		if capacity == -1:
			capacity = sys.maxint
		
		edge = Edge(nodeA, nodeB, capacity)
		reverse = Edge(nodeB, nodeA, capacity)
		
		edge.reverse = reverse
		reverse.reverse = edge
		
		edges.append(edge)
		nodes[nodeA].edges.append(edge)
		nodes[nodeB].edges.append(reverse)
	
	return Graph(nodes, edges)

def bfs(graph, source, target):
	visited = []
	path = [source.id]
	
	queue = collections.deque()
	queue.append(path)
	
	while len(queue) > 0:
		path = queue.popleft()
		node = graph.nodes[path[-1]]
		visited.append(node.id)

		if node == target:
			return path
		
		for edge in node.edges:
			residual = edge.capacity - edge.flow
			if residual > 0 and edge.target not in visited:
				queue.append(path + [edge.target])

def edge_path(graph, path):
	ret = []
	for i, node in enumerate(path):
		if len(path) > i + 1:
			node = graph.nodes[node]
			ret.append(filter(lambda edge: edge.target == path[i + 1], node.edges)[0])
	return ret

def bottleneck(graph, path):
	return min(edge.capacity - edge.flow for edge in path)

def augment(graph, path):
	path = edge_path(graph, path)
	
	m = bottleneck(graph, path)
	
	for edge in path:
		edge.flow += m
		edge.reverse.flow -= m
		
	return m		

def cflow(graph):
	return sum(edge.flow for edge in graph.nodes[0].edges)

def min_cut(graph):
	cut = []
	visited = []
	path = []

	source = graph.nodes[0]
	target = graph.nodes[len(graph.nodes) - 1]
		
	q = collections.deque()
	q.append([source])
    
	while len(q) > 0:
		path = q.popleft()
		node = path[-1]
		visited.append(node.id)
		
		for edge in node.edges:
			if edge.target not in visited:
				if edge.capacity - edge.flow == 0:
					print("%s %s %s" % (edge.source, edge.target, edge.capacity - edge.flow))
				q.append(path + [graph.nodes[edge.target]])

def fulkerson(graph):
	flow = 0
	
	source = graph.nodes[0]
	target = graph.nodes[len(graph.nodes) - 1]
	
	path = bfs(graph, source, target)

	while path != None:
		flow += augment(graph, path)
		path = bfs(graph, source, target)
	
	return flow

graph = parse("rail.txt")
pprint(fulkerson(graph))
min_cut(graph)