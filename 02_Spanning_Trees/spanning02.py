file = open("USA-highway-miles.in")

n = 128
cities = []
distances = []
forest = []
edges = []
size = []
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
size = [1 for i in range(n)]

distances.sort(key=lambda d: d[2])

def root(i):
	while i != forest[i]:
		forest[i] = forest[forest[i]]
		i = forest[i]
	return i

def find(u, v):
	return root(u) == root(v)

def union(u, v):
	i = root(u)
	j = root(v)
	if size[i] < size[j]:
		forest[i] = j
		size[j] += size[i]
	else:
		forest[j] = i
		size[i] = size[j]

while True:
	if len(distances) == 0: break
	
	edge = distances.pop(0)

	if not find(edge[0], edge[1]):
		mst += edge[2]
		union(edge[0], edge[1])

print(mst)
# Output 16598 in ~200ms