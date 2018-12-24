import re
import itertools

immune_system_str = """
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3
"""

infection_str = """
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""

immune_system_str = """
9936 units each with 1739 hit points (weak to slashing, fire) with an attack that does 1 slashing damage at initiative 11
2990 units each with 9609 hit points (weak to radiation; immune to fire, cold) with an attack that does 31 cold damage at initiative 1
2637 units each with 9485 hit points (immune to cold, slashing; weak to bludgeoning) with an attack that does 26 radiation damage at initiative 13
1793 units each with 2680 hit points (weak to bludgeoning; immune to cold) with an attack that does 13 bludgeoning damage at initiative 10
8222 units each with 6619 hit points (immune to fire, slashing) with an attack that does 6 bludgeoning damage at initiative 12
550 units each with 5068 hit points with an attack that does 87 radiation damage at initiative 19
950 units each with 8681 hit points (weak to radiation) with an attack that does 73 slashing damage at initiative 17
28 units each with 9835 hit points with an attack that does 2979 bludgeoning damage at initiative 3
3799 units each with 2933 hit points with an attack that does 7 slashing damage at initiative 16
35 units each with 8999 hit points (weak to bludgeoning; immune to radiation) with an attack that does 2505 cold damage at initiative 6
"""

infection_str = """
1639 units each with 28720 hit points with an attack that does 27 cold damage at initiative 8
4968 units each with 16609 hit points (immune to slashing, bludgeoning, radiation) with an attack that does 6 fire damage at initiative 2
3148 units each with 48970 hit points (weak to fire, bludgeoning) with an attack that does 29 slashing damage at initiative 20
1706 units each with 30069 hit points (immune to cold, bludgeoning) with an attack that does 29 fire damage at initiative 7
496 units each with 39909 hit points (immune to cold; weak to radiation) with an attack that does 133 bludgeoning damage at initiative 4
358 units each with 17475 hit points with an attack that does 82 bludgeoning damage at initiative 5
120 units each with 53629 hit points with an attack that does 807 fire damage at initiative 15
402 units each with 44102 hit points (weak to slashing) with an attack that does 185 bludgeoning damage at initiative 14
468 units each with 11284 hit points (weak to fire) with an attack that does 43 radiation damage at initiative 18
4090 units each with 23075 hit points (immune to radiation) with an attack that does 10 bludgeoning damage at initiative 9
"""

class Group():
	def __init__(self, faction, group_id, nb_units, hit_points, weakness, immunity, attack_dmg, attack_type, initiative):
		self.faction = faction
		self.group_id = group_id
		self.nb_units = nb_units
		self.hit_points = hit_points
		self.weakness = weakness
		self.immunity = immunity
		self.attack_dmg = attack_dmg
		self.attack_type = attack_type
		self.initiative = initiative

		self.attacker = None
		self.target = None

	def __repr__(self):
		return f"{self.faction}[{self.group_id}] {self.nb_units}"

	def effective_power(self):
		return self.nb_units * self.attack_dmg

	def count_damages(self, other):
		if self.attack_type in other.immunity:
			return 0
		return self.effective_power() * (2 if self.attack_type in other.weakness else 1)

	def attack(self):
		if not self.target or self.nb_units < 1:
			return 0
		
		dmg = self.count_damages(self.target)
		self.target.nb_units -= dmg // self.target.hit_points

		return dmg // self.target.hit_points


def read_input(s, faction, boost=0):
	res = []
	r = re.compile("^(\d+) units each with (\d+) hit points (?:\((.*?)\) )?with an attack that does (\d+) (\D+) damage at initiative (\d+)$")
	group_id = 1
	for line in s.split('\n'):
		if not line:
			continue

		nb_units, hit_points, weakness_immunity, attack_dmg, attack_type, initiative = r.match(line.strip()).groups()
		nb_units = int(nb_units)
		hit_points = int(hit_points)
		attack_dmg = int(attack_dmg) + boost
		initiative = int(initiative)

		weakness = []
		immunity = []
		if weakness_immunity:
			for wi in weakness_immunity.split('; '):
				if wi.startswith('weak'):
					weakness = [x.strip() for x in wi[len("weak to "):].split(', ')]
				else:
					immunity = [x.strip() for x in wi[len("immune to "):].split(', ')]
		
		res += [Group(faction, group_id, nb_units, hit_points, weakness, immunity, attack_dmg, attack_type, initiative)]
		group_id += 1

	return res


def effective_power(group):
	return group.nb_units * group.attack_dmg


def target_selection(groups):
	sorted_groups = sorted(groups, key=lambda g: (-g.effective_power(), -g.initiative))

	for g in sorted_groups:
		g.attacker = None
		g.target = None

	for g in sorted_groups:
		try:
			target = max((x
				for x in groups
				if x.faction != g.faction and not x.attacker and g.count_damages(x) > 0),
				key=lambda x: (g.count_damages(x), x.effective_power(), x.initiative)
			)
		except ValueError as e:
			continue

		g.target = target
		target.attacker = g


def attack(groups):
	sorted_groups = sorted(groups, key=lambda g: -g.initiative)

	dmg = 0
	for g in sorted_groups:
		dmg += g.attack()

	remaining_groups = [g for g in groups if g.nb_units > 0]
	return remaining_groups, dmg


def winner(groups):
	return all(g.faction == groups[0].faction for g in groups)


def fight(boost=0):
	immune_system = read_input(immune_system_str, 'immune', boost)
	infection = read_input(infection_str, 'infection')
	groups = immune_system + infection

	while not winner(groups):
		target_selection(groups)
		groups, total_kills = attack(groups)

		if total_kills == 0:
			return None

	return groups


def solve1():
	groups = fight()
	return sum(g.nb_units for g in groups)


def solve2():
	boost = 1
	while 1:
		winner = fight(boost)

		if winner and winner[0].faction == 'immune':
			return sum(g.nb_units for g in winner)

		boost += 1


if __name__ == "__main__":
	print(f"Part1: {solve1()}")
	print(f"Part2: {solve2()}")
