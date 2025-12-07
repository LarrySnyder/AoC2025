
#import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx


DAY = 4
PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = f'day{DAY}/aoc_day{DAY}_sample_input.txt'
else:
	FILENAME = f'day{DAY}/aoc_day{DAY}_input.txt'

def read_data():
	with open(FILENAME) as f:
		data = f.read().splitlines() # splitlines gets rid of \n at end of lines
	return data

def adjecents(data, r, c):
	adjs = []
	for r_delta in (-1, 0, 1):
		for c_delta in (-1, 0, 1):
			if not(r_delta == c_delta == 0) and (0 <= r + r_delta < len(data)) and (0 <= c + c_delta < len(data[r])):
				adjs.append(data[r+r_delta][c+c_delta])
	return adjs

def print_grid(grid):
	for row in grid:
		print(''.join(row))

def find_accessible(data):
	accessible = [list(row) for row in data]
	num_accessible = 0
	for r, row in enumerate(data):
		for c, cell in enumerate(row):
			if cell == '@':
				adjs = adjecents(data, r, c)
				if sum([1 for a in adjs if a == '@']) < 4:
					num_accessible += 1
					accessible[r][c] = 'x'

	return accessible, num_accessible

def solve_aoc():
	data = read_data()
	grid = [list(row) for row in data]

	if PART == 1:
		accessible, num_accessible = find_accessible(grid)
		result = num_accessible
	else:
		num_removed = 0
		accessible, num_accessible = find_accessible(grid)
		while num_accessible > 0:
			# remove accessible rolls
			for r, row in enumerate(grid):
				for c, cell in enumerate(row):
					if accessible[r][c] == 'x':
						grid[r][c] = '.'
						num_removed += 1
			# check again for accessible rolls
			accessible, num_accessible = find_accessible(grid)
		result = num_removed

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
