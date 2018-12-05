def read_input(filepath):
	with open(filepath) as f:
		return [line.strip() for line in f][0]


def solve(input):
	v = ""  # validated
	r = input  # rest
	while 1:
		if len(r) == 1:
			v += r[0]
			break
		
		if r[0].lower() == r[1].lower() and r[0] != r[1]:
			r = (v[-1] if len(v) > 0 else "") + r[2:]
			v = v[:-1]
		else:
			v += r[0]
			r = r[1:]

	return len(v)


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
