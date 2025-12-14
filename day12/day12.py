
import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx
import gurobipy as gp
from gurobipy import GRB


DAY = 12
PART = 1
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

def orientation(shape, o):
	# o = 0, 1, 2, 3, 4, 5, 6, 7
	# 	- 0-3: rotate 0, 90, 180, 270 degrees clockwise
	# 	- 4-7: flip left-right, then rotate 0, 90, 180, 270 degrees clockwise
	if o >= 4:
		shape = [row[::-1] for row in shape]
		o -= 4
	for _ in range(o):
		shape = [''.join(row) for row in zip(*shape[::-1])]
	return shape

def print_shape(shape):
	for row in shape:
		print(row)

def part1(shapes, regions):

	# Each part has 8 orientations:
	# 	- 0-3: rotate 0, 90, 180, 270 degrees clockwise
	# 	- 4-7: flip left-right, then rotate 0, 90, 180, 270 degrees clockwise
	orientations = list(range(8))
	orientation_map = {(s, o): orientation(shapes[s], o) for s in range(len(shapes)) for o in orientations}
	
	for o in range(8):
		print(f'Shape 0 Orientation {o}:')
		print_shape(orientation(shapes[0], o))
		print('')

	total_fits = 0
	for r, region in enumerate(regions):
		# Optimization problem:
		# 	min 	0
		#	s.t.	sum {o,i,j} x_soij = r_s 						{forall s}
		#			sum {s,o,m,n} a_somn * x_so{i-m}{j-n} <= 1		{forall i,j} 
		# where	x_soij = 1 if an instance of shape s is in orientation o and its top-left corner is at (i,j)
		#			(top-left before rotation/flipping)
		# 		r_s = required # of shape s
		#		a_somn = 1 if shape s in orientation o placed at some (i,j) covers (i+m,j+n), 0 o/w, for
		#			m, n in {0, 1, 2}
		
		rgn_width = region['size'][0]
		rgn_height = region['size'][1]

		# Calculate a_somn parameters.
		a = {}
		for s in range(len(shapes)):
			for o in orientations:
				for m in range(3):
					for n in range(3):
						a[(s,o,m,n)] = 1 if orientation_map[(s,o)][m][n] == '#' else 0

		# Build model and decision variables.
		model = gp.Model(f'region_{r}')
		x = {}
		for s in range(len(shapes)):
			for o in orientations:
				for i in range(rgn_width - 2):
					for j in range(rgn_height - 2):
						x[(s, o, i, j)] = model.addVar(vtype=GRB.BINARY, name=f'x_{s},{o},{i},{j}')
		
		# Build constraints.
		# Use the required # of each shape.
		for s in range(len(shapes)):
			model.addConstr(gp.quicksum(x[(s, o, i, j)] for o in orientations for i in range(rgn_width-2) for j in range(rgn_height-2)) == region['shapes'][s], name=f'shape_count_{s}')
		# No overlaps.
		for i in range(rgn_width):
			for j in range(rgn_height):
				model.addConstr(gp.quicksum(a[(s,o,m,n)] * x[(s,o,i-m,j-n)] for s in range(len(shapes)) for o in orientations \
								for m in range(max(0, i-rgn_width+3), min(2, i)+1) \
								for n in range(max(0, j-rgn_height+3), min(2, j)+1)) <= 1, \
									name=f'overlap_{i},{j}')

# 0 <= i-m <= width-3, m <= 2
# m <= min(2, i), m >= i - width + 3

		# Solve.
		model.optimize()
		if model.Status == GRB.OPTIMAL:
			total_fits += 1
			for soij in x.keys():
				if x[soij].X == 1:
					print(f'x_{soij} = 1')

	result = total_fits
	return result

def part2():

	return result
		
def solve_aoc():
	data = read_data()

	# Read shapes.
	# Both sample and real input have 6 shapes. All shapes are 3x3.
	shapes = []
	for s in range(6):
		shape = data[5 * s + 1 : 5 * s + 4]
		shapes.append(shape)

	# Read regions.
	regions = []
	for row in data[30:]:
		pt1, pt2 = row.split(': ')
		size = tuple(map(int, pt1.split('x')))
		region_shapes = tuple(map(int, pt2.split()))
		region = {
			'size': size,
			'shapes': region_shapes
		}
		regions.append(region)

	if PART == 1:
		result = part1(shapes, regions)
	else:
		result = part2()

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
