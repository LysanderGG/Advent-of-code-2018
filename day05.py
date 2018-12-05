def read_input(filepath):
	with open(filepath) as f:
		return [line.strip() for line in f][0]


def react(a, b):
	return a.lower() == b.lower() and a != b


def solve(input):
	i = 0
	while i < len(input) - 1:
		if react(input[i], input[i+1]):
			input = input[:i] + input[i+2:]
			i = max(i - 1, 0)
		else:
			i += 1

	return len(input)


def solve2(input):
	chars = {x.lower() for x in input}
	return min(solve(input.replace(c, "").replace(c.upper(), "")) for c in chars)


if __name__ == "__main__":
	input = read_input("day05.txt")
	# input = "dabAcCaCBAcCcaDA"

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
