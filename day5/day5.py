
#import numpy as np
import time
import tqdm
#import functools
#import networkx as nx


DAY = 5
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

def solve_aoc():
	data = read_data()
	
	fresh_ranges = []
	avail = set()
	now_avail = False
	for row in data:
		if row == '':
			now_avail = True
			continue
		if now_avail:
			avail.add(int(row))
		else:
			id_range = row.split('-')
			fresh_ranges.append((int(id_range[0]), int(id_range[1])))

	num_fresh = 0
	if PART == 1:
		for id in avail:
			for fr in fresh_ranges:
				if fr[0] <= id <= fr[1]:
					num_fresh += 1
					break
	else:
		pbar = tqdm.tqdm(total=len(fresh_ranges))
		# Sort fresh_ranges by first element.
		fresh_ranges.sort(key=lambda x: x[0])
		# Loop through fresh_ranges.
		current_id = 0
		for fr in fresh_ranges:
			pbar.update()
			if current_id > fr[1]:
				# we are already past the endpoint of this range
				continue
			num_fresh += fr[1] + 1 - max(current_id, fr[0])
			current_id = fr[1] + 1

	result = num_fresh

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
