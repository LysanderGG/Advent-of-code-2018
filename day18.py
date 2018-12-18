import itertools
from collections import Counter


SIZE = 50


def read_input(filepath):
	res = {}
	with open(filepath) as f:
		y = 0
		for line in f:
			x = 0
			for c in line.strip():
				res[x, y] = c
				x += 1
			y += 1

	return res


def adj(x, y):
	for offx, offy in itertools.product([-1, 0, 1], repeat=2):
		if offx == 0 and offy == 0:
			continue

		newx = x+offx
		newy = y+offy
		if 0 <= newx < SIZE and 0 <= newy < SIZE:
			yield x+offx, y+offy


def adjacent_resources(state, x, y):
	return Counter(state[xx,yy] for xx, yy in adj(x, y))


def compute_next_state(state):
	next_state = {}
	for (x, y), c in state.items():
		adj_res = adjacent_resources(state,x ,y)
		if c == '.':
			next_state[x,y] = '|' if adj_res['|'] >= 3 else '.'
		elif c == '|':
			next_state[x,y] = '#' if adj_res['#'] >= 3 else '|'
		elif c == '#':
			next_state[x,y] = '#' if adj_res['#'] >= 1 and adj_res['|'] >= 1 else '.'

	return next_state


def debug_print(state):
	for y in range(SIZE):
		for x in range(SIZE):
			print(state[x,y], end="")
		print("")


def nb_resources(state):
	c = Counter(state.values())
	return c['#'] * c['|']


def solve1(state):
	for _ in range(10):
		state = compute_next_state(state)
	return nb_resources(state)


def solve2(state):
	for i in range(1_000_000_000):
		if i % 1000 == 0:
			print(i, nb_resources(state))
			# debug_print(state)

		state = compute_next_state(state)

	return nb_resources(state)


if __name__ == "__main__":
	input = read_input("day18.txt")
	print(f"Part1: {solve1(input)}")
	print(f"Part2: {solve2(input)}")
