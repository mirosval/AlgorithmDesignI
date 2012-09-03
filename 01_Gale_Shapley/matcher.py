import math
import sys

try:
	file = open(sys.argv[1]);
except IOError:
	print("File {0} does not exist".format(sys.argv[1]))
	exit()
except IndexError:
	print("Usage: python3 matcher.py filename.in")
	exit()

people = []
preferences = []
menPrefs = []
men = []
womenPrefs = []
women = []
pairs = []

for line in file:
	if line.startswith("#"):
		continue
	
	if line.startswith("n="):
		n = int(line.replace("n=", ""))
		continue
	
	if line.strip() == "":
		break
	
	people.append(line.split(" ")[1].strip())

for line in file:
	prefs = line.strip().split(": ")[1].split(" ")
	prefs = [math.ceil(int(pref) / 2 - 1) for pref in prefs]
	preferences.append(prefs)

for i in range(n*2):
	if i % 2 == 0:
		men.append(people[i])
		menPrefs.append(preferences[i])
	else:
		women.append(people[i])
		womenPrefs.append(preferences[i])

pairs = [-1 for x in range(n)]

while True:
	if -1 not in pairs: break

	man = pairs.index(-1)
	prefs = menPrefs[man]
	if not prefs: break

	woman = prefs.pop(0)
	if woman not in pairs:
		pairs[man] = woman
	else:
		mPrime = pairs.index(woman)
		wPrefs = womenPrefs[woman]
		if(wPrefs.index(man) < wPrefs.index(mPrime)):
			pairs[man] = woman
			pairs[mPrime] = -1

for woman in pairs:
	print("{0} -- {1}".format(men[pairs.index(woman)], women[woman]))