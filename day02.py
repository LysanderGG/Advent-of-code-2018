from collections import Counter


def read_input(filepath):
	with open(filepath) as f:
		return [line.strip() for line in f]


def solve(input):
	counts = [Counter(x for x in row) for row in input]
	nb_2 = sum(2 in c.values() for c in counts)
	nb_3 = sum(3 in c.values() for c in counts)
	return nb_2 * nb_3


def solve2(input):
	already_known = set()
	for word in input:
		word_minus_letter = {word[:i] + word[i+1:] for i in range(len(word))}
		for w in word_minus_letter: 
			if w in already_known:
				return w 
		for w in word_minus_letter: 
			already_known.add(w)


if __name__ == "__main__":
	input = read_input("day02.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
