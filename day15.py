def read_input(filepath):
	with open(filepath) as f:
		the_map = {}
		characters = []
		y = 0
		for line in f:
			x = 0
			for c in line.strip():
				the_map[x, y] = c
				if c in 'GE':
					characters += [(x, y, c, 200, False)]  # (x, y, 'E' or 'G', health points, has been processed this turn)
				x += 1
			y += 1

	return the_map, characters


adj_pos = [
	(0, -1),
	(-1, 0),
	(1, 0),
	(0, 1)
]

def adj(x, y):
	for p in adj_pos:
		yield x+p[0], y+p[1]


def enemy(c):
	if c == 'E': return 'G'
	elif c == 'G': return 'E'
	else: 'no'


def path_reachable(the_map, fr, to):
	already_been = {fr}
	paths = [[fr]]
	while len(paths) > 0:
		new_paths = []
		for path in paths:
			s = path[-1]
			for pos in adj(s[0], s[1]):
				if the_map[pos] != '.' or pos in already_been:
					continue

				if pos[0] == to[0] and pos[1] == to[1]:
					return path[1:] + [pos]

				already_been.add(pos)
				new_paths += [path + [pos]]
		paths = new_paths

	return None


def move(the_map, characters, c):
	# if enemy already in range do not move
	for pos in adj(c[0], c[1]):
		if pos in the_map and the_map[pos] == enemy(c[2]):
			characters = [x for x in characters if c[0] != x[0] or c[1] != x[1]]
			characters += [(c[0], c[1], c[2], c[3], True)]
			return the_map, characters, c, False

	# identify targets
	targets = [k for (k, v) in the_map.items() if v == enemy(c[2])]
	if not targets:
		return the_map, characters, c, True

	#identifies all of the open squares (.) that are in range of each target
	open_squares = []
	for target in targets:
		for pos in adj(target[0], target[1]):
			if pos in the_map and the_map[pos] == '.':
				open_squares += [pos]

	# reachables + nearest
	reachables = []
	for pos in open_squares:
		path = path_reachable(the_map, (c[0], c[1]), pos)
		if path and len(path) > 0:
			reachables += [(pos[0], pos[1], path)]

	if reachables:
		min_dist = min(len(r[2]) for r in reachables)
		reachables = [r for r in reachables if len(r[2]) == min_dist]

		# chosen enemy
		reachables = sorted(reachables, key=lambda e: (e[1], e[0]))
		target = reachables[0]

		target_pos = target[2][0]

		# update the_map and characters
		the_map[c[0],c[1]] = '.'
		characters = [x for x in characters if c[0] != x[0] or c[1] != x[1]]

		the_map[target_pos] = c[2]
		characters += [(target_pos[0], target_pos[1], c[2], c[3], True)]

		c = (target_pos[0], target_pos[1], c[2], c[3])

		return the_map, characters, c, False

	characters = [x for x in characters if c[0] != x[0] or c[1] != x[1]]
	characters += [(c[0], c[1], c[2], c[3], True)]
	return the_map, characters, c, False


def fight(the_map, characters, char, elf_attack=3):
	targets = []
	for pos in adj(char[0], char[1]):
		for enemy in characters:
			if enemy[0] == pos[0] and enemy[1] == pos[1] and char[2] != enemy[2]:
				targets += [enemy]

	if targets:
		target = sorted(targets, key=lambda e: (e[3], e[1], e[0]))[0]

		characters = [c for c in characters if c[0] != target[0] or c[1] != target[1]]
		attack = 3 if char[2] == 'G' else elf_attack
		if target[3] > attack:
			characters += [(target[0], target[1], target[2], target[3] - attack, target[4])]
		else:
			the_map[target[0], target[1]] = '.'

	return the_map, characters


def turn(the_map, characters, elf_attack=3):
	# clear all flags
	characters = [(c[0], c[1], c[2], c[3], False) for c in characters]

	characters = sorted(characters, key=lambda e: (e[1], e[0]))
	while not all(c[4] for c in characters):
		characters = sorted(characters, key=lambda e: (e[1], e[0]))
		char = next(c for c in characters if not c[4])

		the_map, characters, char, is_end = move(the_map, characters, char)
		if is_end:
			return the_map, characters, is_end

		the_map, characters = fight(the_map, characters, char, elf_attack)

	return the_map, characters, False


def solve1(the_map, characters):
	nb_turns = 0

	while 1:
		the_map, characters, is_end = turn(the_map, characters)
		characters = sorted(characters, key=lambda e: (e[1], e[0]))
		if is_end:
			return nb_turns * sum(c[3] for c in characters)

		nb_turns += 1


def solve2(the_map, characters):
	nb_turns = 0
	m = the_map.copy()
	c = characters.copy()
	elf_attack = 4
	nb_elfs = sum(x[2] == 'E' for x in characters)

	while 1:
		m, c, is_end = turn(m, c, elf_attack)

		if is_end:
			if nb_elfs == sum(x[2] == 'E' for x in c):
				return nb_turns * sum(x[3] for x in c)

			elf_attack += 1
			m = the_map.copy()
			c = characters.copy()
			nb_turns = 0
			continue

		nb_turns += 1


if __name__ == "__main__":
	the_map, characters = read_input("day15.txt")
	print(f"Part1: {solve1(the_map, characters)}")
	the_map, characters = read_input("day15.txt")
	print(f"Part2: {solve2(the_map, characters)}")
