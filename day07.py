from collections import defaultdict


def read_input(filepath):
	with open(filepath) as f:
		res = []
		for line in f:
			s1 = line[len("Step ")]
			s2 = line[len("Step C must be finished before step ")]
			res += [(s1, s2)]
		return res


def available_steps(input):
	all_steps = sorted({t[0] for t in input} | {t[1] for t in input})

	for step in all_steps:
		if all(t[1] != step for t in input):
			yield step


def solve(input):
	sequence = []
	last_step = None

	while len(input) > 0:
		last_step = input[0]
		for step in available_steps(input):
			sequence += step
			input = list(filter(lambda p: p[0] != step, input))
			break

	return ''.join(map(str, sequence)) + last_step[1]


def solve2(input):
	NB_WORKERS = 5
	CONST_TIME = 60
	time = 0

	input = [(s1, s2, ord(s1) - ord('A') + 1 + CONST_TIME) for s1, s2 in input]
	in_work_steps = set()

	while len(input) > 0:
		last_step = input[0]
		av_steps = list(filter(lambda s: s not in in_work_steps, available_steps(input)))

		for step in in_work_steps:
			input = list(map(lambda p: (p[0], p[1], p[2] - 1) if p[0] == step else p, input))

		for i in range(min(len(av_steps), NB_WORKERS - len(in_work_steps))):
			step = av_steps[i]
			in_work_steps.add(step)
			input = list(map(lambda p: (p[0], p[1], p[2] - 1) if p[0] == step else p, input))

		time += 1
		for i in input:
			if i[2] == 0 and i[0] in in_work_steps:
				in_work_steps.remove(i[0])

		input = list(filter(lambda p: p[2] != 0, input))

	return time + ord(last_step[1]) - ord('A') + 1 + CONST_TIME


if __name__ == "__main__":
	input = read_input("day07.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
