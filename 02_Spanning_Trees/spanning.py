file = open("USA-highway-miles.in")

cities = []
distances = dict()

for i in range(128):
	if i == 128: break
	line = file.readline()
	
	cities.append(line.strip().strip('"'))

for line in file:
	endpoints, distance = line.strip().split(" [")
	city1, city2 = [x.strip('"') for x in endpoints.split("--")]
	distance = int(distance.rstrip(']'))
	distances.insert(distance, (city1, city2))
	
print(distances[485])