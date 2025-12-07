
import numpy as np
import time
#import tqdm
import functools
#import networkx as nx


DAY = 7
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

def part1(manifold, entry_pt):
	# Track beams.
	beams = set([tuple(entry_pt + DOWN)])
	num_splits = 0
	for row in range(1, len(data) - 1):
		new_beams = set()
		for beam in beams:
			# Is beam about to hit a splitter?
			if manifold[tuple(beam + DOWN)] == '^':
				# Split beams.
				num_splits += 1
				new_beams.add(tuple(beam + DOWN + LEFT))
				new_beams.add(tuple(beam + DOWN + RIGHT))
			else:
				# Continue beam.
				new_beams.add(tuple(beam + DOWN))
		beams = new_beams

	return num_splits

def part2(manifold, entry_pt):

	num_rows = max([point[0] for point in manifold])

	@functools.lru_cache(maxsize=None)
	def num_paths_from_point(point):
		if point[0] == num_rows - 1:
			return 1
		elif manifold[tuple(np.array(point) + DOWN)] == '^':
			return num_paths_from_point(tuple(np.array(point) + DOWN + LEFT)) + num_paths_from_point(tuple(np.array(point) + DOWN + RIGHT))
		else:
			return num_paths_from_point(tuple(np.array(point) + DOWN))
		
	return num_paths_from_point(tuple(entry_pt))
		
def solve_aoc():
	data = read_data()

	manifold = {(r, c): data[r][c] for r in range(len(data)) for c in range(len(data[0]))}
	
	# Find entry point.
	entry_pt = np.array((0, data[0].find('S')))

	if PART == 1:
		result = part1(manifold, entry_pt)
	else:
		result = part2(manifold, entry_pt)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
