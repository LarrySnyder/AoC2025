import numpy as np
import time
import tqdm
import functools
import networkx as nx


DAY = 1
PART = 1
SAMPLE = True
if SAMPLE:
	FILENAME = f'day{DAY}/aoc_day{DAY}_sample.txt'
else:
	FILENAME = f'day{DAY}/aoc_day{DAY}.txt'

def read_data():
	with open(FILENAME) as f:
		codes = f.read().splitlines() # splitlines gets rid of \n at end of lines
	return codes



def solve_aoc():
	result = None
	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
