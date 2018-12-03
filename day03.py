from collections import Counter
import re


def read_input(filepath):
	r = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
	with open(filepath) as f:
		return [tuple(int(x) for x in r.match(line.strip()).groups()) for line in f]


def solve(input):
	claim_map = dict()
	for (id, x, y, w, h) in input:
		for u in range(x, x + w):
			for v in range(y, y + h):
				claim_map[(u, v)] = claim_map.get((u, v), 0) + 1
	return sum(x > 1 for x in claim_map.values())


def solve2(input):
	claim_map = dict()
	all_ids = {id for (id, x, y, w, h) in input}
	overlap_ids = set()
	for (id, x, y, w, h) in input:
		for u in range(x, x + w):
			for v in range(y, y + h):
				curr = claim_map.get((u, v), [])
				claim_map[(u, v)] = curr + [id]
				if curr != []:
					for x in claim_map[(u, v)]:
						overlap_ids.add(x) 

	return all_ids - overlap_ids


if __name__ == "__main__":
	input = read_input("day03.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
