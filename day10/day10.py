
import numpy as np
import time
#import tqdm
#import functools
import networkx as nx
import itertools
import gurobipy as gp
from gurobipy import GRB


DAY = 10
PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = f'day{DAY}/aoc_day{DAY}_sample_input.txt'
else:
	FILENAME = f'day{DAY}/aoc_day{DAY}_input.txt'

RIGHT = np.array((0, 1))
LEFT = np.array((0, -1))
UP = np.array((-1, 0))
DOWN = np.array((1, 0))

def read_data():
	with open(FILENAME) as f:
		data = f.read().splitlines() # splitlines gets rid of \n at end of lines
	return data

def press_button(start_config, button):
	new_config = ''
	for l in range(len(start_config)):
		if l in button:
			new_config += '.' if start_config[l] == '#' else '#'
		else:
			new_config += start_config[l]

	return new_config

def part1(machines):

	total_presses = 0
	for m, machine in enumerate(machines):
		# Build network: each node corresponds to a light configuration, each
		# edge corresonds to a button press.
		light_configs = list(itertools.product('.#', repeat=len(machine['lights'])))
		light_configs = [''.join(lc) for lc in light_configs]
		G = nx.DiGraph()
		G.add_nodes_from(light_configs)
		for lc in light_configs:
			for b in machine['buttons']:
				G.add_edge(lc, press_button(lc, b))

		# Solve shortest path problem from initial configuration to target configuration.
		initial_config = '.' * len(machine['lights'])
		target_config = machine['lights']
		presses = nx.shortest_path_length(G, initial_config, target_config)

		print(f'Machine {m:3}: {presses} button presses')
		total_presses += presses

	result = total_presses
	return result

def part2(machines):

	total_presses = 0
	for m, machine in enumerate(machines):
		# Optimization problem:
		#   min  sum {b in BUTTONS} x_b
		#   s.t. a_bc * x_b = l_c {c in COUNTERS}
		# where	x_b = # of times button b is pressed
		#		a_bc = 1 if button b increases the joltage of counter c, 0 o/w
		#		l_c = desired joltage level of counter c
		model = gp.Model(f'machine_{m}')
		button_vars = {}
		for b_idx, b in enumerate(machine['buttons']):
			button_vars[b_idx] = model.addVar(vtype=GRB.INTEGER, name=f'button_{b_idx}', lb=0)
		model.setObjective(gp.quicksum(button_vars[b_idx] for b_idx in button_vars), GRB.MINIMIZE)
		a = {(b, c): 1 if c in machine['buttons'][b] else 0 for b in range(len(machine['buttons'])) for c in range(len(machine['joltages']))}
		# Constraints: for each counter, the sum of the contributions from each button
		# must equal the target joltage.
		for c_idx, target_joltage in enumerate(machine['joltages']):
			model.addConstr(gp.quicksum(a[(b, c_idx)] * button_vars[b] for b in range(len(machine['buttons']))) == target_joltage,
						name=f'counter_{c_idx}')		
		model.optimize()
		presses = int(model.objVal)

		print(f'Machine {m:3}: {presses} button presses')
		total_presses += presses

	result = total_presses
	return result
		
def solve_aoc():
	data = read_data()
	machines = []
	for row in data:
		pieces = row.split(' ')
		lights = pieces[0].partition('[')[2].partition(']')[0]
		button_strs = pieces[1:-1]
		buttons = []
		for b in button_strs:
			tuple_str = b[b.find('(')+1 : b.find(')')]
			lights_triggered = [int(l) for l in tuple_str.split(',')]
			buttons.append(lights_triggered)
		joltage_str = pieces[-1].partition('{')[2].partition('}')[0]
		joltages = [int(j) for j in joltage_str.split(',')]
		machine = {
			'lights': lights,
			'buttons': buttons,
			'joltages': joltages
		}
		machines.append(machine)

	if PART == 1:
		result = part1(machines)
	else:
		result = part2(machines)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
