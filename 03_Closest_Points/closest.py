from math import sqrt

# O(nlogn)
def parse(path):
	file = open(path)
	
	for line in file:
		if line.strip() == "NODE_COORD_SECTION": break
	
	points = []
	
	for line in file:
		if len(line.strip()) == 0 or line.strip() == "EOF": continue;
		name, x, y = line.strip().split()
		points.append((name, float(x), float(y)))

	# O(n log(n))
	points.sort(key=lambda x: x[1])
	
	return points

# constant
def distance(a, b):
	return sqrt(pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))

# n
def refine(points, coordinate, since, until):
	ret = []
	
	for point in points:
		if point[coordinate] > since:
			if point[coordinate] > until: break
			ret.append(point)
	
	return ret

# n log(n)
def find_closest(points):	
	if len(points) < 2: return float('inf')
	if len(points) == 2: return distance(points[0], points[1])
	if len(points) == 3: return min(distance(points[0], points[1]), distance(points[1], points[2]), distance(points[0], points[2]))
	
	pivot = round(len(points) / 2)
	subset1 = points[:pivot]
	subset2 = points[pivot:]
	
	# (n/2)log(n/2)
	d1 = find_closest(subset1)
	# (n/2)log(n/2)
	d2 = find_closest(subset2)

	closest = min(d1, d2)
	
	# n
	stripeY = refine(points, 1, points[pivot][1] - closest, points[pivot][1] + closest)
	
	# n
	count = len(stripeY)

	# o(nlogn)
	stripeY.sort(key=lambda x: x[2])
	
	# n
	for i, A in enumerate(stripeY):
		# c
		for j in range(1,4):
			try:
				B = stripeY[i + j]
				closest = min(closest, distance(A, B))
			except IndexError:
				continue
				
	return closest

# check against closest-pair.out
file = open("ALL_tsp/closest-pair.out")

tests = 0
passed = 0

for line in file:
	tests += 1
	path, dimension, expected_result = line.split()
	file = path.replace("../data", "ALL_tsp").strip(":")
	
	points = parse(file)
	result = find_closest(points)
	
	if round(result, 7) == round(float(expected_result), 7):
		print("Passed " + file)
		passed += 1
	else:
		print("Failed " + file + " with " + str(dimension) + " points\n\tWas:\t\t" + str(result) + "\n\tExpected:\t" + str(expected_result))

print("\n\nPassed " + str(passed) + " / " + str(tests) + " (" + str(round(100 * passed / tests, 2)) + "%)")

#points = parse("ALL_tsp/close-pairs-6.in")
##print(len(points))
#print(find_closest(points))