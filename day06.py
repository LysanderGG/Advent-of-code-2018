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
	x_max = max(x for x, _ in input)
	y_max = max(y for _, y in input)

	inf_areas = set()
	area = defaultdict(int)
	for x in range(x_max + 1):
		for y in range(y_max + 1):
			distances = [manhattan_distance(x, y, xi, yi) for xi, yi in input]
			min_d = min(distances)
			if distances.count(min_d) == 1:
				idx = distances.index(min_d)
				area[idx] += 1
				if x <= 0 or x >= x_max or y <= 0 or y >= y_max:
					inf_areas.add(idx)

	# remove infinite areas
	for inf in inf_areas:
		area[inf] = 0

	return max(area.values())


def solve2(input):
	x_max = max(x for x, _ in input)
	y_max = max(y for _, y in input)

	area = 0
	for x in range(x_max + 1):
		for y in range(y_max + 1):
			distances = [manhattan_distance(x, y, xi, yi) for xi, yi in input]
			sum_d = sum(distances)
			if sum_d <= 10000:
				area += 1

	return area


if __name__ == "__main__":
	input = read_input("day06.txt")
	# input = [[1, 1],[1, 6],[8, 3],[3, 4],[5, 5],[8, 9]]

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
