import re


def read_input(filepath):
	res = []
	r = re.compile("^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)$")
	with open(filepath) as f:
		for line in f:
			res += [tuple(int(x) for x in r.match(line.strip()).groups())]

	return res


def d(x,y,z, xx, yy, zz):
	return abs(x-xx) + abs(y-yy) + abs(z-zz)


def solve1(state):
	max_r = max(p[3] for p in state)
	sx,sy,sz,sr = next(p for p in state if p[3] == max_r)

	return sum(d(x,y,z,sx,sy,sz) <= sr for x, y, z, r in state)


# def in_range(px,py,pz,robots):
# 	return sum(d(px,py,pz,x,y,z) <= r for x,y,z,r in robots)


# def man_d(x,y,z):
# 	return sum(abs(k) for k in [x,y,z])
	
# def man_d_t(t):
# 	return sum(abs(k) for k in t)


# def solve2(state):
# 	min_x = min(p[0] for p in state)
# 	max_x = max(p[0] for p in state)
# 	min_y = min(p[1] for p in state)
# 	max_y = max(p[1] for p in state)
# 	min_z = min(p[2] for p in state)
# 	max_z = max(p[2] for p in state)
# 	min_r = min(p[3] for p in state)
# 	bests = []

# 	best_coords = (0,0,0)
# 	best_nb_in_range = 0
# 	dr = min_r // 2
# 	for x in range(min_x, max_x+1, dr):
# 		print(x)
# 		for y in range(min_y, max_y+1, dr):
# 			for z in range(min_z, max_z+1, dr):
# 				nb_r = in_range(x,y,z,state)
# 				bests += [(nb_r, (x,y,z))]
# 				if nb_r > best_nb_in_range:
# 					best_coords = (x,y,z)
# 					best_nb_in_range = nb_r
					

# 	bests = sorted(bests)[::-1][:8]
# 	best_best = best_coords
# 	best_best_nb = best_nb_in_range

# 	while(len(bests) > 0):
# 		b = bests.pop()
# 		best_nb_in_range = b[0]
# 		best_coords = b[1]
# 		print(bests)

# 		tr = min_r
# 		while tr > 0:
# 			dr = max(tr // 4, 1)
# 			tx, ty, tz = best_coords
# 			for x in range(tx-tr, tx+tr, dr):
# 				# print(x)
# 				for y in range(ty-tr, ty+tr, dr):
# 					for z in range(tz-tr, tz+tr, dr):
# 						nb_r = in_range(x,y,z,state)
# 						if nb_r > best_nb_in_range:
# 							best_coords = (x,y,z)
# 							best_nb_in_range = nb_r
# 						elif nb_r == best_nb_in_range and man_d(x,y,z) < man_d_t(best_coords):
# 							best_coords = (x,y,z)


# 			# print(best_coords, best_nb_in_range)
# 			tr //= 2

# 		if best_nb_in_range > best_best_nb:
# 			best_best_nb = best_nb_in_range
# 			best_best = best_coords
# 		elif nb_r == best_nb_in_range and man_d(x,y,z) < man_d_t(best_coords):
# 			best_coords = (x,y,z)

# 	print(best_coords, best_nb_in_range)

# 	return man_d_t(best_coords)

if __name__ == "__main__":
	state = read_input("day23.txt")
	print(f"Part1: {solve1(state)}")
	# print(f"Part2: {solve2(state)}")
