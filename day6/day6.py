
#import numpy as np
import time
#import tqdm
#import functools
#import networkx as nx


DAY = 6
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
	
	rows = [row.split() for row in data]
	grand_total = 0
	if PART == 1:
		num_problems = len(rows[0])
		for p in range(num_problems):
			prob_type = rows[-1][p]
			if prob_type == '+':
				running_total = 0
			else:
				running_total = 1
			for r in range(len(rows) - 1):
				if prob_type == '+':
					running_total += int(rows[r][p])
				else:
					running_total *= int(rows[r][p])
			grand_total += running_total
	else:
		grand_total = 0
		c = len(data[0]) - 1
		while c >= 0:
			nums = []
			done = False
			while not done:
				nums.append(int(''.join([data[r][c] for r in range(len(data)-1)])))
				if data[-1][c] in ('+', '*'):
					done = True
				c -= 1 
			# c is now the index of the blank column to the left of the problem
			prob_type = data[-1][c+1]
			if prob_type == '+':
				running_total = sum(nums)
			else:
				running_total = 1
				for num in nums:
					running_total *= num
			grand_total += running_total
			# move one more left
			c -= 1

	result = grand_total
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
