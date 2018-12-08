def read_input(filepath):
	with open(filepath) as f:
		return [int(x) for line in f for x in line.split()]


class Node():
	def __init__(self, nb_child_nodes, nb_meta):
		self.nb_child_nodes = nb_child_nodes
		self.nb_meta = nb_meta
		self.children = []
		self.meta = []

	def add_child(self, node):
		self.children += [node]

	def meta_sum(self):
		s = sum(self.meta)
		for c in self.children:
			s += c.meta_sum()
		return s

	def meta_value(self):
		if not self.children:
			return sum(self.meta)

		s = 0
		for m in self.meta:
			if m == 0:
				continue
			if m <= len(self.children):
				s += self.children[m-1].meta_value()
		return s


def next_node(input, parent=None):
	nb_child_nodes = input[0]
	nb_meta = input[1]
	node = Node(nb_child_nodes, nb_meta)
	if parent:
		parent.add_child(node)

	for _ in range(nb_child_nodes):
		_, input = next_node(input[2:], node)

	node.meta = input[2:nb_meta+2]
	return node, input[nb_meta:]


def solve(input):
	node, _ = next_node(input)
	return node.meta_sum()


def solve2(input):
	node, _ = next_node(input)
	return node.meta_value()


if __name__ == "__main__":
	input = read_input("day08.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
