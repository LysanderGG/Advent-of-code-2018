from collections import defaultdict


def power_level(x, y, serial):
	rackId = x + 10
	power_lvl = (rackId * y + serial) * rackId
	power_lvl = (power_lvl % 1000) // 100
	power_lvl -= 5
	return power_lvl


def init_grid(serial):
	grid = {}
	for x in range(1, 301):
		for y in range(1, 301):
			grid[x, y] = power_level(x, y, serial)
	return grid


def square_power(grid, x, y, size):
	return sum(grid[i,j] for i in range(x, x+size) for j in range(y, y+size))


def solve(serial):
	grid = init_grid(serial)
	max_coords = (0, 0)
	max_pwr = 0
	for x in range(1,298):
		for y in range(1, 298):
			pwr = square_power(grid, x, y, 3)
			if pwr > max_pwr:
				max_pwr = pwr
				max_coords = x, y

	return max_coords


def solve2(serial):
	grid = init_grid(serial)
	max_coords = (0, 0, 0)
	max_pwr = 0
	for size in range(1, 300):
		print(size, max_coords)
		for x in range(1,301-size):
			pwr = square_power(grid, x, 1, size)
			for y in range(2, 301-size):
				for i in range(x, x+size):
					pwr -= grid[i, y - 1]
					pwr += grid[i, y + size - 1]

				if pwr > max_pwr:
					max_pwr = pwr
					max_coords = x, y, size

	return max_coords


if __name__ == "__main__":
	input = 3214

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
