#import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx


DAY = 2
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

def id_is_invalid(id):

	id_str = str(id)
	len_id_str = len(id_str)

	if PART == 1:
		factors = [2]
	else:
		# Get factors of len_id_str.
		factors = [n for n in range(1, (len_id_str // 2) + 1) if len_id_str % n == 0]

	for f in factors:
		if all([id_str[f * t:f * (t + 1)] == id_str[f * (t + 1): f * (t + 2)] for t in range(len_id_str // f - 1)]):
			return True

	return False

def solve_aoc():
	data = read_data()[0]

	# Split data at commas.
	range_strs = data.split(',')
	# Split ranges into start and end numbers.
	ranges = []
	for r in range_strs:
		[range_min, range_max] = r.split('-')
		ranges.append((int(range_min), int(range_max)))

	# Loop through ranges.
	sum_invalid = 0
	for r in ranges:
		invalid_ids = []
		for id in range(r[0], r[1] + 1):
			if id_is_invalid(id):
				sum_invalid += id
				invalid_ids.append(id)
		range_output = f'{r[0]}-{r[1]} invalid IDs: '
		for id in invalid_ids:
			range_output += f'{id} '
		print(range_output)

	result = sum_invalid

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
