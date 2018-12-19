def read_input(filepath):
	with open(filepath) as f:
		tmp = [line.strip() for line in f if line.strip()]

	ip = int(tmp[0].split(" ")[1])
	instr = []
	for l in tmp[1:]:
		a,b,c = (int(x) for x in l[5:].split())
		instr += [(l[:4], a, b, c)]

	return ip, instr


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


def solve1(ip_reg, instr):
	registers = [0] * 6
	ip = 0

	while 1:
		opcode, a, b, c = instr[ip]

		registers[c] = g_operators[opcode](registers, a, b)

		registers[ip_reg] += 1
		ip = registers[ip_reg]

		if ip >= len(instr):
			return registers[0]


if __name__ == "__main__":
	ip, instr = read_input("day19.txt")
	print(f"Part1: {solve1(ip, instr)}")
