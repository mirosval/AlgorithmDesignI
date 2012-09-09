file = open("USA-highway-miles.in")

n = 128
cities = []
distances = []
forest = []
edges = []
mst = 0

for i in range(n):
	line = file.readline()
	
	cities.append(line.strip().strip('"'))

for line in file:
	endpoints, distance = line.strip().split(" [")
	city1, city2 = [x.strip('"') for x in endpoints.split("--")]
	distance = int(distance.rstrip(']'))
	distances.append((cities.index(city1), cities.index(city2), distance))

forest = [x for x in range(n)]

distances.sort(key=lambda d: d[2])

def find(u, v):
	return forest[u] == forest[v]

def union(u, v):
	pid = forest[u]
	for i, val in enumerate(forest):
		if forest[i] == pid: forest[i] = forest[v]

while True:
	if len(distances) == 0: break
	
	edge = distances.pop(0)

	if not find(edge[0], edge[1]):
		mst += edge[2]
		union(edge[0], edge[1])

print(mst)
# Output 16598 in ~200ms