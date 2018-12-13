def rail(c):
	if c in 'v^': return '|'
	elif c in '><': return '-'
	elif c in '\\/-|+': return c
	else: return ' '


def read_input(filepath):
	with open(filepath) as f:
		tracks = {}
		cars = []
		y = 0
		for line in f:
			x = 0
			for c in line:
				if c in 'v^<>':
					cars += [(x, y, c, 0)]
				
				c = rail(c)
				if c != ' ':
					tracks[x, y] = c
				x += 1
			y += 1

	return tracks, cars


dir_dict = {
	'v': (0, 1),
	'^': (0, -1),
	'<': (-1, 0),
	'>': (1, 0)
}

def collision(cars, x, y):
	return any((x == c[0] and y == c[1]) for c in cars)


def new_dir(track, dir, state):
	if track in '-|':
		return dir, state
	if track == '\\':
		if dir == 'v': return '>', state
		elif dir == '^': return '<', state
		elif dir == '>': return 'v', state
		else: return '^', state
	elif track == '/':
		if dir == 'v': return '<', state
		elif dir == '^': return '>', state
		elif dir == '>': return '^', state
		else: return 'v', state
	else:
		if state == 0:
			if dir == 'v': return '>', 1
			elif dir == '^': return '<', 1
			elif dir == '>': return '^', 1
			else: return 'v', 1
		elif state == 1:
			return dir, 2
		else:
			if dir == 'v': return '<', 0
			elif dir == '^': return '>', 0
			elif dir == '>': return 'v', 0
			else: return '^', 0


def next_tick(tracks, cars):
	new_cars = []
	for x, y, dir, state in cars:
		if collision(new_cars, x, y):
			return "collision", (x, y)

		dx, dy = dir_dict[dir]
		x, y = x + dx, y + dy
		
		if collision(new_cars, x, y):
			return "collision", (x, y)

		dir, state = new_dir(tracks[x, y], dir, state)
		new_cars += [(x, y, dir, state)]
	return "ok", new_cars


def solve1(tracks, cars):
	while 1:
		ok, res = next_tick(tracks, cars)
		if ok == "collision":
			return res
		cars = res


def remove_crash(cars, x, y):
	new_cars = [c for c in cars if x != c[0] or y != c[1]]
	return len(cars) != len(new_cars), new_cars


def next_tick2(tracks, cars):
	new_cars = []
	for x, y, dir, state in cars:
		col, new_cars = remove_crash(new_cars, x, y)
		if col:
			continue
		
		dx, dy = dir_dict[dir]
		x, y = x + dx, y + dy

		dir, state = new_dir(tracks[x, y], dir, state)

		col, new_cars = remove_crash(new_cars, x, y)
		if col:
			continue

		new_cars += [(x, y, dir, state)]

	return new_cars


def solve2(tracks, cars):
	while 1:
		cars = sorted(cars, key=lambda element: (element[1], element[0]))
		cars = next_tick2(tracks, cars)
		if len(cars) == 1:
			return cars[0][:2]


if __name__ == "__main__":
	tracks, cars = read_input("day13.txt")
	print(f"Part1: {solve1(tracks, cars)}")
	print(f"Part2: {solve2(tracks, cars)}")
