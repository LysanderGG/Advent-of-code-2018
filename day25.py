import itertools


def read_input(filepath):
	res = []
	with open(filepath) as f:
		return [
			tuple(int(x.strip())
			for x in line.strip().split(','))
			for line in f
		]


def dist(p1,p2):
	return sum(abs(x - y) for x,y in zip(p1,p2))


def solve1(state):
	constellations = {x: i for i,x in enumerate(state)}

	while True:
		has_changed = False
		for c1, c2 in itertools.combinations(constellations, 2):
			cid1, cid2 = constellations[c1], constellations[c2]
			if cid1 == cid2:
				continue

			if dist(c1, c2) <= 3:
				for k, v in constellations.items():
					if v == cid2:
						constellations[k] = cid1
						has_changed = True

		if not has_changed:
			break

	return len(set(constellations.values()))


if __name__ == "__main__":
	state = read_input("day25.txt")
	print(f"Part1: {solve1(state)}")
