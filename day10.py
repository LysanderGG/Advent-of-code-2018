import re


def read_input(filepath):
	with open(filepath) as f:
		res = []
		r1 = re.compile("position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>")
		for line in f:
			x, y, vx, vy = (int(x) for x in r1.match(line.strip()).groups())
			res += [(x, y, vx, vy)]
		return res


def grid_extrema(grid):
	min_x = min(t[0] for t in grid)
	min_y = min(t[1] for t in grid)
	max_x = max(t[0] for t in grid) + 1
	max_y = max(t[1] for t in grid) + 1
	return min_x, min_y, max_x, max_y


def draw_grid(grid):
	min_x, min_y, max_x, max_y = grid_extrema(grid)

	grid = sorted(grid, key=lambda element: (element[1], element[0]))

	for j in range(min_y, max_y, 1):
		for i in range(min_x, max_x, 1):
			x, y, _, _ = grid[0]
			if x == i and y == j:
				print("#", end= " ")
				grid = grid[1:]
				while len(grid) > 0 and grid[0][0] == x and grid[0][1] == y:
					grid = grid[1:]
				if not grid:
					print("")
					print("")
					return
			else:
				print(".", end= " ")
		print()


def evolve(grid):
	new_grid = []
	for x, y, vx, vy in grid:
		new_grid += [(x + vx, y + vy, vx, vy)]
	return new_grid

import time
def solve(grid):
	sec = 0
	while(1):
		if sec % 1000 == 0:
			print("Sec ", sec)

		min_x, min_y, max_x, max_y = grid_extrema(grid)
		if max_x - min_x < 200 and max_y - min_y < 30:
			print("Sec ", sec)
			draw_grid(grid)
			time.sleep(2)

		grid = evolve(grid)
		sec += 1
	return 0

if __name__ == "__main__":
	input = read_input("day10.txt")

	ans = solve(input)
	print(f"Part1: {ans}")
