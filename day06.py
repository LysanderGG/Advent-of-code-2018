from collections import defaultdict


def read_input(filepath):
	with open(filepath) as f:
		res = []
		for line in f:
			x, y = line.strip().split(",")
			res += [(int(x), int(y))]
		return res


def manhattan_distance(x, y, xx, yy):
	return abs(x - xx) + abs(y - yy)

def solve(input):
	coord_offset = 10
	x_max = max(x for x, _ in input)
	y_max = max(y for _, y in input)

	inf_areas = set()
	area = defaultdict(int)
	for x in range(-coord_offset, x_max + coord_offset):
		for y in range(-coord_offset, y_max + coord_offset):
			distances = [manhattan_distance(x, y, i[0], i[1]) for i in input]
			min_d = min(distances)
			if distances.count(min_d) == 1:
				idx = distances.index(min_d)
				area[idx] += 1
			if x <= 0 or x >= x_max or y <= 0 or y >= y_max:
				for i in range(len(distances)):
					if distances[i] == min_d:
						inf_areas.add(i)

	# remove infinite areas
	print(area)
	print(inf_areas)
	for inf in inf_areas:
		area[inf] = 0

	return max(area.values())


def solve2(input):
	return 0


if __name__ == "__main__":
	input = read_input("day06.txt")
	# input = [[1, 1],[1, 6],[8, 3],[3, 4],[5, 5],[8, 9]]

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
