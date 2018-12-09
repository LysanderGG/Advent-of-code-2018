from collections import defaultdict


def read_input(filepath):
	with open(filepath) as f:
		return [x for line in f]


def solve(nb_players, last_marble):
	state = [0, 1]
	curr_val = 2
	curr_idx = 1
	player = 0
	scores = defaultdict(int)

	while curr_val <= last_marble:
		if  curr_val % 1000 == 0:
			print(curr_val)

		if curr_val % 23 == 0:
			curr_idx = (curr_idx - 7) % len(state)
			rm_val = state[curr_idx]
			scores[player] += curr_val + rm_val
			del state[curr_idx]
		else:
			new_idx = (curr_idx + 2) % len(state)
			if new_idx == 0:
				new_idx = len(state)
			curr_idx = new_idx
			state.insert(new_idx, curr_val)

		curr_val += 1
		player = (player + 1) % nb_players

	return max(scores.values())


def get_indexes(state, global_idx):
	for i in range(len(state)):
		if global_idx < len(state[i]):
			return i, global_idx
		global_idx -= len(state[i])

	return i, len(state[i])

def solve2(nb_players, last_marble):
	state = [0, 16,  8, 17,  4, 18,  9, 19,  2, 20, 10, 21,  5, 22, 11,  1, 12,  6, 13,  3, 14,  7, 15]
	curr_val = 23
	curr_idx = state.index(22)
	nb_marbels = len(state)
	state = [[x] for x in state]
	player = 0
	scores = defaultdict(int)

	while curr_val <= last_marble:
		if  curr_val % 1000 == 0:
			print(curr_val)

		if curr_val % 23 == 0:
			curr_idx = (curr_idx - 7) % nb_marbels
			i, j = get_indexes(state, curr_idx)
			rm_val = state[i][j]
			scores[player] += curr_val + rm_val
			del state[i][j]
			nb_marbels -= 1

		else:
			new_idx = (curr_idx + 2) % nb_marbels
			if new_idx == 0:
				new_idx = nb_marbels

			curr_idx = new_idx
			i, j = get_indexes(state, curr_idx)
			state[i].insert(j, curr_val)
			nb_marbels += 1

		curr_val += 1
		player = (player + 1) % nb_players

	return max(scores.values())


if __name__ == "__main__":
	ans = solve(424, 71482)
	print(f"Part1: {ans}")

	ans = solve2(424, 7148200)
	print(f"Part2: {ans}")
