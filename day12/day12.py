
import numpy as np
import time
import tqdm
import gurobipy as gp
from gurobipy import GRB


DAY = 12
PART = 1
SAMPLE = False		# <-- set to True to use sample input file, False to use real input
OTHER_FILE = True	# <-- set to True to use specific filename instead, specified below
if OTHER_FILE:
	FILENAME = 'day12/aoc_day12_other1_input.txt'
elif SAMPLE:
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

def part1(shapes, regions, region_strs):

	# Each part has 8 orientations:
	# 	- 0-3: rotate 0, 90, 180, 270 degrees clockwise
	# 	- 4-7: flip left-right, then rotate 0, 90, 180, 270 degrees clockwise
	orientations = list(range(8))
	orientation_map = {(s, o): orientation(shapes[s], o) for s in range(len(shapes)) for o in orientations}
	# Eliminate symmetric orientations.
	for s in range(len(shapes)):
		for o1 in orientations[:-1]:
			for o2 in orientations[o1+1:]:
				if orientation_map[(s, o1)] == orientation_map[(s, o2)]:
					orientation_map[(s, o2)] = None

	# Calculate a_somn parameters.
	a = {}
	for s in range(len(shapes)):
		for o in orientations:
			for m in range(3):
				for n in range(3):
					if orientation_map[(s,o)] is not None and orientation_map[(s,o)][m][n] == '#':
						a[(s,o,m,n)] = 1
					else:
						a[(s,o,m,n)] = 0

	total_fits = 0
	fits = []
	times = []
	pbar = tqdm.tqdm(total = len(regions))
	for r, region in enumerate(regions):
		pbar.update()
		start_time = time.time()

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

		with gp.Env(empty=True) as env:
			env.setParam('OutputFlag', 0)		# suppress output
			env.start()
			with gp.Model(env=env, name=f'region_{r}') as model:
				# Build model and decision variables.
				x = {}
				for s in range(len(shapes)):
					for o in orientations:
						if orientation_map[(s, o)] is not None:
							for i in range(rgn_width - 2):
								for j in range(rgn_height - 2):
									x[(s, o, i, j)] = model.addVar(vtype=GRB.BINARY, name=f'x_{s},{o},{i},{j}')
				soij_set = set(x.keys())

				# Constraint: Use the required # of each shape.
				for s in range(len(shapes)):
					model.addConstr(gp.quicksum(x[(s, o, i, j)] for o in orientations for i in range(rgn_width-2) for j in range(rgn_height-2) if (s,o,i,j) in soij_set) == region['shapes'][s], name=f'shape_count_{s}')
				# No overlaps.
				for i in range(rgn_width):
					for j in range(rgn_height):
						model.addConstr(gp.quicksum(a[(s,o,m,n)] * x[(s,o,i-m,j-n)] for s in range(len(shapes)) for o in orientations \
										for m in range(max(0, i-rgn_width+3), min(2, i)+1) \
										for n in range(max(0, j-rgn_height+3), min(2, j)+1) \
										if (s,o,i-m,j-n) in soij_set) <= 1, \
											name=f'overlap_{i},{j}')

				# Constraint: Solve.
				model.optimize()
				if model.Status == GRB.OPTIMAL:
					total_fits += 1

				fits.append(model.Status == GRB.OPTIMAL)
				times.append(time.time() - start_time)

				model.close()
			env.close()

	with open(FILENAME.replace('input', 'output'), 'w') as f:
		for r, region in enumerate(regions):
			f.write(f'{r:4} : {region_strs[r]:{max(len(rs) for rs in region_strs)}} : {'YES' if fits[r] else ' NO'} ({times[r]:.3f} seconds)\n')
		f.write('\n')
		f.write(f'avg time = {np.average(times):.3f}\n')
		f.write(f'max time = {np.max(times):.3f}\n')

	result = total_fits
	return result

def part2():

	return result

def solve_aoc():
	data = read_data()

	# Read shapes. Assumnes all shapes are 3x3.
	shapes = []
	s = 0
	done = False
	while not done:
		shape = data[5 * s + 1 : 5 * s + 4]
		shapes.append(shape)
		s += 1
		if 'x' in data[5 * s]:
			done = True

	# Read regions.
	regions = []
	for row in data[5 * len(shapes):]:
		pt1, pt2 = row.split(': ')
		size = tuple(map(int, pt1.split('x')))
		region_shapes = tuple(map(int, pt2.split()))
		region = {
			'size': size,
			'shapes': region_shapes
		}
		regions.append(region)

	if PART == 1:
		result = part1(shapes, regions, data[5 * len(shapes):])
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
