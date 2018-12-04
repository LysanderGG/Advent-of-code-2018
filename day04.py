from collections import defaultdict
import re
import moment
import operator


def read_input(filepath):
	with open(filepath) as f:
		res = []
		for line in f:
			r1 = re.compile("\[1518-(\d+-\d+ \d+:\d+)\] (.*)")
			date, s = r1.match(line.strip()).groups()
			res += [(moment.date(date, '%m-%d %H:%M'), s)]

	return sorted(res, key=lambda tup: tup[0])


def minutes_between(d1, d2):
	delta = d2 - d1
	return int(str(delta).split(":")[1])


def gen_minutes_between(d1, d2):
	i = d1.minutes
	while i < d2.minutes or i > d2.minutes and i <= 60:
		yield i
		i += 1
		if i == 60:
			i = 0


def solve(input):
	id = None
	data = defaultdict(int)
	for date, s in input:
		if s.startswith("Guard"):
			id = int(s.split(" ")[1][1:])
		elif s.startswith("falls asleep"):
			prev_date = date
		elif s.startswith("wakes up"):
			data[id] += minutes_between(prev_date, date)

	best_sleeper = max(data.items(), key=operator.itemgetter(1))[0]

	minutes = defaultdict(int)
	for date, s in input:
		if s.startswith(f"Guard #"):
			id = int(s.split(" ")[1][1:])
		else:
			if id != best_sleeper:
				continue

			if s.startswith("falls asleep"):
				prev_date = date
			elif s.startswith("wakes up"):
				for m in gen_minutes_between(prev_date, date):
					minutes[m] += 1

	best_minute = max(minutes.items(), key=operator.itemgetter(1))[0]
	return best_minute * best_sleeper


def solve2(input):
	minutes = {}
	for date, s in input:
		if s.startswith(f"Guard #"):
			id = int(s.split(" ")[1][1:])
			if id not in minutes:
				minutes[id] = defaultdict(int)
		elif s.startswith("falls asleep"):
			prev_date = date
		if s.startswith("wakes up"):
			for m in gen_minutes_between(prev_date, date):
				minutes[id][m] += 1

	max_id = None
	max_times = 0
	max_min = 0
	for id, m_dict in minutes.items():
		if len(m_dict) == 0:
			continue

		minute, max_for_id = max(m_dict.items(), key=operator.itemgetter(1))
		if max_for_id > max_times:
			max_times = max_for_id
			max_id = id
			max_min = minute

	return max_id * max_min


if __name__ == "__main__":
	input = read_input("day04.txt")

	ans = solve(input)
	print(f"Part1: {ans}")

	ans = solve2(input)
	print(f"Part2: {ans}")
