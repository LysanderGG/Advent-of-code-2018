def read_input(filepath):
	with open(filepath) as f:
		return [int(line) for line in f]


def solve(input):
	return sum(i for i in input)


def solve2(input):
	s = set([0])
	curr_sum = 0
	while 1:
		for i in range(len(input)):
			curr_sum += input[i]
			if curr_sum in s:
				return curr_sum
			s.add(curr_sum)

if __name__ == "__main__":
	input = read_input("day01.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
