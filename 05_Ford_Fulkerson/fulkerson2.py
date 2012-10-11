from pprint import pprint

class Edge(object):
	def __init__(self, source, target, capacity):
		self.source = source
		self.target = target
		self.capacity = capacity
	
	def __repr__(self):
		return "%s->%s @ %s" % (self.source, self.target, self.capacity)

class Fulkerson(object):
	def __init__(self):
		self.nodes = {}
		self.flow = {}
	
	def add_node(self, node):
		self.nodes[node] = []
	
	def add_edge(self, source, target, capacity):
		edge = Edge(source, target, capacity)
		residual_edge = Edge(target, source, capacity)
		
		edge.residual = residual_edge
		residual_edge.residual = edge
		
		self.nodes[source].append(edge)
		self.nodes[target].append(residual_edge)
		
		self.flow[edge] = 0
		self.flow[residual_edge] = 0
	
	def find_path(self, source, target, path = []):
		if source == target:
			return path
		
		for edge in self.nodes[source]:
			residual = edge.capacity - self.flow[edge]
			
			if (residual > 0 or residual == -1) and not (edge, residual) in path:
				res = self.find_path(edge.target, target, path + [(edge, residual)])
				if res != None:
					return res
		
	def calculate_flow(self, source, target):
		self.source = source
		self.target = target
		path = self.find_path(source, target)
		while path != None:				
			path_max_flow = min(residual for edge, residual in path if residual > -1)
			pprint(path_max_flow)
			for edge, res in path:
				self.flow[edge] += path_max_flow
				self.flow[edge.residual] -= path_max_flow
			path = self.find_path(source, target)
	
	def get_max_flow(self):
		return sum(self.flow[edge] for edge in self.nodes[self.source])
	
	def __repr__(self):
		return repr(self.nodes) + repr(self.flow)
	def __str__(self):
		return str(self.nodes) + "\n" + str(self.flow)

network = Fulkerson()

file = open("rail.txt")
n = int(file.readline().strip())
for i in range(0, n):
	node = file.readline().strip()
	network.add_node(i)
	
m = int(file.readline().strip())
arcs = dict()
residual = dict()
for i in range(0, m):
	nodeA, nodeB, capacity = file.readline().strip().split()
	nodeA = int(nodeA)
	nodeB = int(nodeB)
	capacity = int(capacity)
	
	network.add_edge(nodeA, nodeB, capacity)

network.calculate_flow(0, n - 1)
pprint(network.get_max_flow())

