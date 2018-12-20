import exrex


def read_input(filepath):
	with open(filepath) as f:
		regex = [line.strip() for line in f if line.strip()]

	return regex[0][1:len(regex[0]) - 1]


# def extract_group(regex):
# 	n = 0
# 	for i, c in enumerate(regex):
# 		if c == '(':
# 			n += 1
# 		if c == ')':
# 			n -= 1
# 			if n == 0:
# 				return regex[1:i-1], regex[i:]
# 	return regex, None


def extract_conditions(regex):
	if '|' not in regex:
		yield regex
	else:
		print("extract_conditions", regex)
		n = 0
		for i, c in enumerate(regex):
			if c == '|':
				yield regex[:i]
				yield from extract_conditions(regex[i+1:])
		yield regex


# def append_routes(routes, regex):
# 	# print("append_routes", routes, regex)
# 	if not regex:
# 		return routes

# 	if '(' in regex:
# 		add_routes = get_routes([""], regex)

# 	new_routes = []
# 	for cond in extract_conditions(regex):

# 		for r in routes:
# 			new_routes += [r + cond]

# 	# print(new_routes)
# 	return new_routes


# def get_routes(routes, regex):
# 	if not regex:
# 		return routes

# 	# print("get_routes", routes, regex)
# 	try:
# 		i = regex.index('(')
# 		start = regex[:i]
# 		regex = regex[i+1:len(regex) - 1]
# 	except ValueError:
# 		start = regex
# 		regex = None

# 	routes = append_routes(routes, start)
# 	routes = append_routes(routes, regex)

# 	return routes



def get_groups(regex):
	print("get_groups", regex)
	if '(' in regex:
		open_parenthesis = None
		close_parenthesis = -1
		n = 0
		for i, c in enumerate(regex):
			if c == '(':
				if n == 0:
					yield from get_groups(regex[close_parenthesis+1: i])
					open_parenthesis = i
				n += 1
			elif c == ')':
				n -= 1
				close_parenthesis = i
				if n == 0:
					yield from get_groups(regex[open_parenthesis+1: i])
	else:
		yield regex


def get_routes(routes, regex):
	for group in get_groups(regex):
		print(group)


dir_dict = {
	'S': (0, 1),
	'N': (0, -1),
	'W': (-1, 0),
	'E': (1, 0)
}


def make_grid(regex):
	routes = list(exrex.generate(regex))
	# print(routes)
	grid = {}

	for r in routes:
		x, y = (0, 0)
		for c in r:
			dx, dy = dir_dict[c]
			x, y = x + dx, y + dy
			grid[x,y] = '|'
			x, y = x + dx, y + dy
			grid[x,y] = '.'

	return grid


def adj(grid, x, y):
	for p in dir_dict.values():
		if (x+p[0], y+p[1]) in grid:
			yield x+2*p[0], y+2*p[1]


def paths_reachable(grid, fr):
	already_been = {fr}
	paths = [[fr]]

	while True:
		new_paths = []
		for path in paths:
			s = path[-1]
			for pos in adj(grid, s[0], s[1]):
				if pos in already_been:
					continue

				already_been.add(pos)
				new_paths += [path + [pos]]

		if len(new_paths) == 0:
			return paths

		paths = new_paths

	return new_paths


def print_grid(grid):
	min_y = min(y for _, y in grid)
	max_y = max(y for _, y in grid)
	min_x = min(x for x, _ in grid)
	max_x = max(x for x, _ in grid)

	for y in range(min_y, max_y+1):
		for x in range(min_x, max_x+1):
			c = x, y
			if c == (0, 0):
				print('X', end="")
			elif c in grid:
				print(grid[c], end="")
			else:
				print("#", end="")
		print("")

def solve1(regex):
	print(regex)
	grid = make_grid(regex)
	paths = paths_reachable(grid, (0, 0))
	print(paths)
	longuest = max(len(p) for p in paths)
	print_grid(grid)
	return longuest - 1


def solve2(state):

	return 0


if __name__ == "__main__":
	state = read_input("day20.txt")
	print(f"Part1: {solve1(state)}")
	print(f"Part2: {solve2(state)}")
