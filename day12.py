NB_GENERATIONS = 20
OFFSET = NB_GENERATIONS + 2


def read_input(filepath):
	with open(filepath) as f:
		initial_state = None
		grammar_dict = {}
		for line in f:
			if not initial_state:
				initial_state = line.strip()[len("initial state: "):]
			else:
				grammar_dict[line[:5]] = line[9]

	return initial_state, grammar_dict


def evolve(state, grammar_dict):
	new_state = '..'
	for i in range(2, 2 * OFFSET + 100 - 2):
		s = state[i-2: i+3]
		new_state += grammar_dict[s]

	return new_state + '..'


def solve(initial_state, grammar_dict):
	state = '.'*OFFSET + initial_state + '.'*OFFSET

	for _ in range(NB_GENERATIONS):
		state = evolve(state, grammar_dict)

	score = 0
	for i in range(-OFFSET, 100+OFFSET):
		score += i if state[0] == '#' else 0
		state = state[1:]

	return score


def solve2():
	state_100 = '....................#....#....#....#....#....#....#....#....#....#....#....#....#....#....#....#....#....#...#....#...#...#...#....#....#....#....#....#....#....#...#...#....#...#....#....#....#....#.........................................................................................................................'
	indexes = [50000000000 - 100 + i for i in range(len(state_100)) if state_100[i] == '#']
	return sum(indexes)


if __name__ == "__main__":
	initial, grammar = read_input("day12.txt")

	print(f"Part1: {solve(initial, grammar)}")
	print(f"Part2: {solve2()}")
