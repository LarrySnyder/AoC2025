#import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx


DAY = 1
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

def turn_dial(curr_pos, move):
	new_pos = (curr_pos + move) % 100
	if PART == 1:
		num_zeros = 1 if new_pos == 0 else 0
	else:
		# Count number of full rotations.
		num_zeros = (abs(move) // 100)
		# Adjust for first partial rotation.
		dir = -1 if move < 0 else 1
		num_clicks = abs(move)
		partial_move = dir * (num_clicks % 100)
		if curr_pos != 0 and curr_pos + partial_move <= 0 or curr_pos + partial_move >= 100:
			num_zeros += 1
	return new_pos, num_zeros

def turn_dial_brute_force(curr_pos, move):
	num_zeros = 0
	pos = curr_pos
	dir = -1 if move < 0 else 1
	for _ in range(abs(move)):
		pos += dir
		if pos == -1:
			pos = 99
		elif pos == 100:
			pos = 0
		if pos == 0:
			num_zeros += 1
	return pos, num_zeros

def solve_aoc():
	data = read_data()

	pos = 50
	print(f'The dial starts by pointing at {pos}.')

	with open('day1/temp.txt', 'w') as f:

		total_num_zeros = 0
		for rotation in data:
			dir = -1 if rotation[0] == 'L' else 1
			move = dir * int(rotation[1:])
			# new_pos, num_zeros = turn_dial_brute_force(pos, move)
			new_pos, num_zeros = turn_dial(pos, move)
			result_str = f'The dial is rotated {rotation} to point at {new_pos}. During this rotation, it points at zero {num_zeros} times.'
			print(result_str)
			f.write(result_str + '\n')
			pos = new_pos
			total_num_zeros += num_zeros

	result = total_num_zeros
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
