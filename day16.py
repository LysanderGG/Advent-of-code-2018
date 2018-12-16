def read_input(filepath):
	with open(filepath) as f:
		tmp = [line.strip() for line in f if line.strip()]

	res = []
	for i in range(0, len(tmp), 3):
		res += [(
			[int(x) for x in tmp[i][len("Before: ["):].split("]")[0].split(",")],
			[int(x) for x in tmp[i+1].split(' ')],
			[int(x) for x in tmp[i+2][len("After:  ["):].split("]")[0].split(",")]
		)]

	return res


def read_input_2(filepath):
	with open(filepath) as f:
		return [[int(x) for x in line.strip().split()] for line in f]


g_operators = {
	"addr": lambda registers, a, b: registers[a] + registers[b],
	"addi": lambda registers, a, b: registers[a] + b,
	"mulr": lambda registers, a, b: registers[a] * registers[b],
	"muli": lambda registers, a, b: registers[a] * b,
	"banr": lambda registers, a, b: registers[a] & registers[b],
	"bani": lambda registers, a, b: registers[a] & b,
	"borr": lambda registers, a, b: registers[a] | registers[b],
	"bori": lambda registers, a, b: registers[a] | b,
	"setr": lambda registers, a, b: registers[a],
	"seti": lambda registers, a, b: a,
	"gtir": lambda registers, a, b: int(a > registers[b]),
	"gtri": lambda registers, a, b: int(registers[a] > b),
	"gtrr": lambda registers, a, b: int(registers[a] > registers[b]),
	"eqir": lambda registers, a, b: int(a == registers[b]),
	"eqri": lambda registers, a, b: int(registers[a] == b),
	"eqrr": lambda registers, a, b: int(registers[a] == registers[b]),
}


def behave_like(before, instructions, after):
	_, a, b, c = instructions
	possible_opcodes = []

	for op, func in g_operators.items():
		registers = before.copy()
		registers[c] = func(registers, a, b)
		if registers == after:
			possible_opcodes += [op]

	return set(possible_opcodes)


def solve1(input):
	return sum(len(behave_like(*t)) >= 3 for t in input)


def solve2(input, sample_pg):
	# Find possible functions per opcode
	opcodes = {i: set(g_operators.keys()) for i in range(16)}
	for before, instructions, after in input:
		possible_opcodes = behave_like(before, instructions, after)
		opcodes[instructions[0]] &= possible_opcodes

	# Reduce to only 1 operation per opcode
	definitive_opcodes = {}
	while len(definitive_opcodes) < 16:
		to_remove = []
		for i, opcode in opcodes.items():
			if len(opcode) == 1:
				val = opcode.pop()
				definitive_opcodes[i] = val
				to_remove += [val]

		# Remove the opcode from all sets in opcodes.
		for rm in to_remove:
			for i in opcodes:
				if rm in opcodes[i]:
					opcodes[i].remove(rm)

	# Run sample program
	registers = [0] * 4
	for opcode, a, b, c in sample_pg:
		registers[c] = g_operators[definitive_opcodes[opcode]](registers, a, b)

	return registers[0]


if __name__ == "__main__":
	input = read_input("day16.txt")
	print(f"Part1: {solve1(input)}")
	sample_pg = read_input_2("day16-2.txt")
	print(f"Part2: {solve2(input, sample_pg)}")
