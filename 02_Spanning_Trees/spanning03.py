import copy
from timeit import Timer

file = open("USA-highway-miles.in")

n = 128
cities = []
distances = []

for i in range(n):
	line = file.readline()
	
	cities.append(line.strip().strip('"'))

for line in file:
	endpoints, distance = line.strip().split(" [")
	city1, city2 = [x.strip('"') for x in endpoints.split("--")]
	distance = int(distance.rstrip(']'))
	distances.append((cities.index(city1), cities.index(city2), distance))

distances.sort(key=lambda d: d[2])

class UnionFind:
	def __init__(self, n):
		self.forest = [x for x in range(n)]
		self.size = [1 for i in range(n)]
		
	def root(self, i):
		while i != self.forest[i]:
			self.forest[i] = self.forest[self.forest[i]]
			i = self.forest[i]
		
		return i

	def find(self, u, v):
		return self.root(u) == self.root(v)

	def union(self, u, v):
		i = self.root(u)
		j = self.root(v)
		
		if self.size[i] < self.size[j]:
			self.forest[i] = j
			self.size[j] += self.size[i]
		else:
			self.forest[j] = i
			self.size[i] = self.size[j]

def mst():
	mst = 0
	dists = copy.deepcopy(distances)
	unionFind = UnionFind(n)
	
	while True:
		if len(dists) == 0: break
		
		edge = dists.pop(0)

		if not unionFind.find(edge[0], edge[1]):
			mst += edge[2]
			unionFind.union(edge[0], edge[1])
	
	return mst

t = Timer("mst()", "from __main__ import mst")
print(t.timeit(100) / 100)
# Output 16598 in ~200ms