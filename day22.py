from functools import lru_cache
from heapq import heappush, heappop


depth = 11817
target = (9,751)


@lru_cache(None)
def geo_index(x,y):
	if (x,y) == (0,0):
		return 0
	elif (x,y) == target:
		return 0
	elif y == 0:
		return 16807 * x
	elif x == 0:
		return 48271 * y
	
	return erosion_lvl(x-1,y) * erosion_lvl(x,y-1)


def erosion_lvl(x,y):
	return (geo_index(x,y) + depth) % 20183


def geo_risk(x,y):
	return erosion_lvl(x, y) % 3


def risk_lvl(x,y,tx,ty):
	return sum(	geo_risk(i,j) for i in range(x, tx+1) for j in range(y, ty+1))


def solve1():
	return risk_lvl(0, 0, target[0], target[1])


ok_tools = {
	0: {'gear', 'torch'},
	1: {'gear', 'neither'},
	2: {'torch', 'neither'}
}

adj_pos = [
	(0, -1),
	(-1, 0),
	(1, 0),
	(0, 1)
]

def adj(x, y, tool, grid):
	for dx, dy in adj_pos:
		nx, ny = x + dx, y + dy
		if 0 <= nx and 0 <= ny and tool in ok_tools[grid[nx, ny]]:
			yield nx, ny


def solve2():
	grid = {}
	for i in range(target[0] + 101):
		for j in range(target[1] + 101):
			grid[i,j] = geo_risk(i,j)

	states = [(0, 0, 0, 'torch')]  # [(time, x, y, tool)], heap by time
	already_been = {(0, 0, 'torch'): 0}  # (x, y, tool): time
	while states:
		curr_time, x, y, curr_tool = heappop(states)
		if (x, y, curr_tool) == (target[0], target[1], 'torch'):
			return curr_time

		if x >= target[0] + 100 or y >= target[1] + 100: 
			continue
		if already_been.get((x, y, curr_tool)) < curr_time: 
			continue

		# Change tool
		for new_tool in ok_tools[grid[x, y]]:
			if new_tool != curr_tool:
				new_time = curr_time + 7
				heappush(states, (new_time, x, y, new_tool))
				if new_time < already_been.get((x, y, new_tool), 999999): 
					already_been[x, y, new_tool] = new_time

		# Move with current tool
		for nx, ny in adj(x, y, curr_tool, grid):
			new_time = curr_time + 1
			if new_time < already_been.get((nx, ny, curr_tool), 999999):
				already_been[nx, ny, curr_tool] = new_time
				heappush(states, (new_time, nx, ny, curr_tool))


if __name__ == "__main__":
	print(f"Part1: {solve1()}")
	print(f"Part2: {solve2()}")
