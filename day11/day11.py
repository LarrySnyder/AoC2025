
import numpy as np
import time
#import tqdm
import functools
import networkx as nx
#import typing
import matplotlib.pyplot as plt


DAY = 11
PART = 2
SAMPLE = False
if SAMPLE:
	FILENAME = f'day{DAY}/aoc_day{DAY}_sample_input_part{PART}.txt'
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

@functools.lru_cache(maxsize=None)
def num_paths_from_device(G: nx.DiGraph, start_device: str, end_device: str = 'out'):
	"""Return number of paths from start_device to 'out'."""
	if start_device == end_device:
		return 1
	else:
		num_paths = 0
		for e in G.out_edges(start_device):
			num_paths += num_paths_from_device(G, e[1], end_device)
		return num_paths

def part1(device_outputs):

	# Build digraph.
	G = nx.DiGraph()
	G.add_nodes_from(device_outputs.keys())
	for d1 in device_outputs.keys():
		for d2 in device_outputs[d1]:
			G.add_edge(d1, d2)

	# Confirm it's a tree.
	try:
		nx.find_cycle(G)
	except:
		print('It\'s a tree!')
	else:
		print('Not a tree!')

	# Count paths.
	result = num_paths_from_device(G, 'you')

	return result

def part2(device_outputs):

	# Build digraph.
	G = nx.DiGraph()
	G.add_nodes_from(device_outputs.keys())
	for d1 in device_outputs.keys():
		for d2 in device_outputs[d1]:
			G.add_edge(d1, d2)

	# svr -> ... -> dac -> ... -> fft -> ... out
	try:
		# Count paths from 'svr' to 'dac' that do not pass through 'fft'. 
		# Do this by removing 'fft' from the graph.
		temp_G = G.copy()
		temp_G.remove_node('fft')
		num_paths_svr_to_dac = num_paths_from_device(temp_G, 'svr', 'dac')
		print(f'{num_paths_svr_to_dac} paths from svr to dac')
		# Count paths from 'dac' to 'fft' (in G, not temp_G).
		num_paths_dac_to_fft = num_paths_from_device(G, 'dac', 'fft')
		print(f'{num_paths_dac_to_fft} paths from dac to fft')
		# Count paths from 'fft' to 'out' that do not pass through 'dac'.
		temp_G = G.copy()
		temp_G.remove_node('dac')
		num_paths_fft_to_out = num_paths_from_device(temp_G, 'fft', 'out')
		print(f'{num_paths_fft_to_out} paths from fft to out')
		num_paths = num_paths_svr_to_dac * num_paths_dac_to_fft * num_paths_fft_to_out
	except:
		num_paths = 0
	finally:
		pass

	# svr -> ... -> fft -> ... -> dac -> ... out
	try:
		# Count paths from 'svr' to 'fft' that do not pass through 'dac'. 
		# Do this by removing 'dac' from the graph.
		temp_G = G.copy()
		temp_G.remove_node('dac')
		num_paths_svr_to_fft = num_paths_from_device(temp_G, 'svr', 'fft')
		print(f'{num_paths_svr_to_fft} paths from svr to fft')
		# Count paths from 'fft' to 'dac'.
		num_paths_fft_to_dac = num_paths_from_device(G, 'fft', 'dac')
		print(f'{num_paths_fft_to_dac} paths from fft to dac')
		# Count paths from 'dac' to 'out' that do not pass through 'fft'.
		temp_G = G.copy()
		temp_G.remove_node('fft')
		num_paths_dac_to_out = num_paths_from_device(temp_G, 'dac', 'out')
		print(f'{num_paths_dac_to_out} paths from dac to out')
		num_paths += num_paths_svr_to_fft * num_paths_fft_to_dac * num_paths_dac_to_out
	except:
		num_paths += 0
	finally:
		pass

	# # Get paths.
	# all_paths = all_paths_from_device(G, 'svr')
	# # Count how many contain dac and fft.
	# result = sum([1 for p in all_paths if 'dac' in p and 'fft' in p])

	result = num_paths
	return result
		
def solve_aoc():
	data = read_data()

	device_outputs = {}
	for row in data:
		device, outputs = row.split(': ')
		device_outputs[device] = outputs.split()

	if PART == 1:
		result = part1(device_outputs)
	else:
		result = part2(device_outputs)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
