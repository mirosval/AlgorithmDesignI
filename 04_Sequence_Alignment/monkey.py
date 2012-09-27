

def read_input(name):
	file = open(name)
	
	sequences = []
	name = ""
	sequence = ""
	for line in file:
		if line.startswith(">"):
			if name != "":
				sequences.append((name,sequence))
			sequence = ""
			name = line.strip().strip('>')
		else:
			sequence += line.strip()

	sequences.append((name,sequence))
	
	return sequences

def read_blosum(name):
	file = open(name)

	blosum = dict()
	letters = []
	for line in file:
		if line.startswith("#"): continue
		
		if line.startswith(" "):
			letters = line.strip().split()
			for letter in letters:
				blosum[letter] = dict()
		else:
			row = line.strip().split()
			column = row[0]
			row = row[1:]
			for index, value in enumerate(row):
				blosum[column][letters[index]] = int(value)
	
	return blosum

def align(sequenceA, sequenceB, blosum):
	m = len(sequenceA) + 1
	n = len(sequenceB) + 1
	matrix = [[0 for i in range(n)] for j in range(m)]
	for i in range(m):
		matrix[i][0] = i * -4

	for j in range(n):
		matrix[0][j] = j * -4
	
	for j in range(1, n):
		for i in range(1, m):
			a = sequenceA[i - 1]
			b = sequenceB[j - 1]
			ma = max(blosum[a][b] + matrix[i - 1][j - 1], blosum[a]['*'] + matrix[i - 1][j], blosum['*'][b] + matrix[i][j - 1])
			matrix[i][j] = ma
	
	t = trace(matrix, sequenceA, sequenceB, blosum)
	
	return (matrix[m-1][n-1], t[0], t[1])

def trace(matrix, sequenceA, sequenceB, blosum):
	alignedA = ''
	alignedB = ''
	i = len(sequenceA)
	j = len(sequenceB)
	while i > 0 and j > 0:
		score = matrix[i][j]
		diagonalScore = matrix[i - 1][j - 1]
		topScore = matrix[i][j - 1]
		leftScore = matrix[i - 1][j]
		if score == diagonalScore + blosum[sequenceA[i - 1]][sequenceB[j - 1]]:
			alignedA = sequenceA[i - 1] + alignedA
			alignedB = sequenceB[j - 1] + alignedB
			i -= 1
			j -= 1
		elif score == leftScore - 4:
			alignedA = sequenceA[i - 1] + alignedA
			alignedB = '-' + alignedB
			i -= 1
		else:
			alignedA = '-' + alignedA
			alignedB = sequenceB[j - 1] + alignedB
			j -= 1
	
	while i > 0:
		alignedA = sequenceA[i - 1] + alignedA
		alignedB = '-' + alignedB
		i -= 1
	
	while j > 0:
		alignedA = '-' + alignedA
		alignedB = sequenceA[j - 1] + alignedB
		j -= 1
	
	return (alignedA, alignedB)

#sequences = read_input("Toy_FASTAs.in")
sequences = read_input("HbB_FASTAs.in")
blosum = read_blosum("BLOSUM62.txt")

for i, s1 in enumerate(sequences):
	for j, s2 in enumerate(sequences):
		if i <= j: continue
		
		a = align(s1[1], s2[1], blosum)
		print(s1[0], "--", s2[0], ": ", a[0])
		print(a[1])
		print(a[2])