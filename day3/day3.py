
#import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx


DAY = 3
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

	num_to_turn_on = 12 if PART == 2 else 2

	total_joltage = 0
	for bank in data:
		joltages = [int(j) for j in bank]
		digits = []
		slot = -1
		for b in range(num_to_turn_on):
			# Find largest digit not among the last (num_to_turn_on - b - 1) slots.
			end_slot = None if b == num_to_turn_on - 1 else -(num_to_turn_on - b - 1)
			digits.append(max(joltages[slot+1:end_slot]))
			slot = joltages.index(digits[b], slot+1)
		# Update total
		digits_as_str = ''.join(str(d) for d in digits)
		print(f'{bank}: {digits_as_str}')
		total_joltage += int(digits_as_str)

	result = total_joltage
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
