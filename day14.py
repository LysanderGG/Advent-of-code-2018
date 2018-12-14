def solve1(input):
	chocos = [3, 7]
	elfs = [0, 1]

	for _ in range(input+10):
		new_chocos = [int(c) for c in str(sum(chocos[e] for e in elfs))]
		chocos += new_chocos
		elfs = [(e + chocos[e] + 1) % len(chocos) for e in elfs]

	return chocos[input:input+10]


def solve2(input):
	chocos = [3, 7]
	elfs = [0, 1]
	last_6 = 0

	while True:
		new_chocos = [int(c) for c in str(sum(chocos[e] for e in elfs))]
		chocos += new_chocos
		elfs = [(e + chocos[e] + 1) % len(chocos) for e in elfs]

		nl = 0
		for n in new_chocos:
			last_6 = (last_6 % 100000) * 10 + n
			nl += 1
			if last_6 == input:
				return len(chocos) - 6 - len(new_chocos) + nl


if __name__ == "__main__":
	input = 864801
	print(f"Part1: {solve1(input)}")
	print(f"Part2: {solve2(input)}")
