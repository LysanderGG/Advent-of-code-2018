import re
from collections import defaultdict


min_y = max_y = min_x = max_x = 0


def read_input(filepath):
	r = re.compile("(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)")
	res = set()
	with open(filepath) as f:
		for line in f:
			c1, v1, _, v2, v3 = r.match(line.strip()).groups()
			v1, v2, v3 = (int(x) for x in [v1, v2, v3])
			if c1 == 'x':
				for y in range(v2, v3+1):
					res.add((v1, y))
			else:
				for x in range(v2, v3+1):
					res.add((x, v1))

	return res


def propagate_v(ground, water, x, y):
	has_changed = False

	new_water = water.copy()
	while (x, y) not in ground and y <= max_y:
		if (x, y) not in new_water:
			new_water[x, y] = '|'
			has_changed = True
		y += 1

	return new_water, has_changed


def propagate_h(ground, water, x, y):
	has_changed = False
	new_coords = set()
	xl, xr = x, x
	while (xr, y) not in ground and ((xr, y+1) in ground or ((xr, y+1) in water and water[(xr, y+1)] == '~')):
		new_coords.add((xr, y))
		xr += 1

	while (xl, y) not in ground and ((xl, y+1) in ground or ((xl, y+1) in water and water[(xl, y+1)] == '~')):
		new_coords.add((xl, y))
		xl -= 1

	h_water = (xl, y) in ground and (xr, y) in ground
	new_water = water.copy()
	for c in new_coords:
		new_val = '~' if h_water else '|'
		if c in new_water and new_water[c] == new_val:
			pass
		else:
			new_water[c] = '~' if h_water else '|'
			has_changed = True

	# vertical fall down when '.' under xl or xr
	if not h_water:
		for x in [xl, xr]:
			if (x, y+1) not in water and (x, y+1) not in ground:
				if not ((x, y) in new_water and new_water[x, y] == '|'):
					new_water[(x, y)] = '|'
					has_changed = True

	return new_water, has_changed


def debug_print(ground, water):
	print(ground)
	for y in range(min_y, max_y+1):
		for x in range(min_x, max_x+1):
			c = x, y
			if c in water:
				print(water[c], end="")
			elif c in ground:
				print("#", end="")
			else:
				print(".", end="")
		print("")


def fill(ground):
	global min_x, min_y, max_x, max_y

	min_y = min(y for _, y in ground)
	max_y = max(y for _, y in ground)
	min_x = min(x for x, _ in ground)
	max_x = max(x for x, _ in ground)

	water = {(500, 0): '|'}
	while 1:
		new_water = water.copy()
		has_changed = False

		water_to_use = [coords for coords, char in water.items() if char == '|']
		water_to_use = [(x, y) for x, y in water_to_use if not ((x+1, y) in water and water[x+1, y] == '|' and (x-1, y) in water and water[x-1, y] == '|' and ((x, y+1) in water or (x, y+1) in ground))]
		water_to_use = sorted(water_to_use, key=lambda e: (e[1], e[0]))[::-1]

		for (wx, wy) in water_to_use:
			down = (wx, wy+1)
			if down in ground:
				new_water, has_changed = propagate_h(ground, new_water, wx, wy)
			elif down in water and water[down] == '~':
				new_water, has_changed = propagate_h(ground, new_water, wx, wy)
			elif down not in ground and down not in water:
				new_water, has_changed = propagate_v(ground, new_water, wx, wy)

			if has_changed:
				break

		if not has_changed:
			return new_water

		water = new_water.copy()

	return water


def solve1(water):
	return sum(1 for _, y in water.keys() if min_y <= y <= max_y)


def solve2(water):
	return sum(1 for (_, y), c in water.items() if min_y <= y <= max_y and c== '~')


if __name__ == "__main__":
	ground = read_input("day17.txt")
	water = fill(ground)
	print(f"Part1: {solve1(water)}")
	print(f"Part2: {solve2(water)}")
