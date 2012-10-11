from pprint import pprint

file = open("rail.txt")

n = int(file.readline().strip())
nodes = []
for i in range(0, n):
	node = file.readline().strip()
	nodes.append(node)
	
m = int(file.readline().strip())
arcs = dict()
residual = dict()
for i in range(0, m):
	nodeA, nodeB, capacity = file.readline().strip().split()
	nodeA = int(nodeA)
	nodeB = int(nodeB)
	capacity = int(capacity)
	if nodeA not in arcs:
		arcs[nodeA] = dict()
		residual[nodeA] = dict()
	if nodeB not in arcs:
		arcs[nodeB] = dict()
		residual[nodeB] = dict()
	arcs[nodeA][nodeB] = capacity
	#arcs[nodeB][nodeA] = capacity
	residual[nodeA][nodeB] = 0

#residual = arcs.copy()


def bfs(nodeA, nodeB, nodes, arcs):    
	queue = []
	queue.append([nodeA])

	while len(queue) > 0:
		path = queue.pop(0)
		n = path[-1]        
		if nodeB == n:
			return path
		
		for adjacent in arcs[n]:
			new_path = list(path)
			if arcs[n][adjacent] == 0: continue
			new_path.append(adjacent)
			queue.append(new_path)

def get_path_min(path):
	path_c = []
	minimum = float('inf')
	
	for i, node in enumerate(path):
		if i + 1 == len(path): break
		capacity = arcs[ path[i] ][ path[i + 1] ]
		path_c.insert(i, capacity)
		if capacity == -1: continue
		minimum = min(minimum, capacity)
	
	pprint(path_c)
	
	return minimum

# determine path capacity
while True:
	path = bfs(0, len(nodes) - 1, nodes, arcs)
	pprint(path)
	if path == None:
		print(sum(c for c in arcs[0]))
		break
	min_capacity = get_path_min(path)
	pprint(min_capacity)
	for i, node in enumerate(path):
		if i + 1 == len(path): break
		capacity = arcs[ path[i] ][ path[i + 1] ]
		if capacity > 0:
			arcs[ path[i] ][ path[i + 1] ] -= min_capacity
			residual[ path[i] ][ path[i + 1] ] += min_capacity

#pprint(nodes)
#pprint(arcs)