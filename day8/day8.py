
import numpy as np
import time
#import tqdm
#import functools
import networkx as nx
import typing


DAY = 8
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

def part1(network: nx.Graph, coords, dist_matrix, num_pairs_to_connect, product_size_to_return):

	# Sort distance matrix.
	dist_sorted = sorted(dist_matrix.items(), key=lambda item: item[1])

	for n in range(num_pairs_to_connect):
		# Get closest pair.
		closest_pair = dist_sorted[n][0]
		# Add edge.
		network.add_edge(*closest_pair)
		# Update distasnces.
		dist_matrix[closest_pair] = np.inf
		dist_matrix[closest_pair[::-1]] = np.inf

		num_components = nx.number_connected_components(network)
		components = nx.connected_components(network)
		component_sizes = sorted([len(c) for c in components], reverse=True)
		unique_component_sizes, unique_component_size_counts = np.unique(component_sizes, return_counts=True)
		print(f'After connecting boxes {coords[closest_pair[0]]} and {coords[closest_pair[1]]}, there are {num_components} components with sizes {unique_component_size_counts} {unique_component_sizes}')

	result = 1
	for s in range(product_size_to_return):
		result *= component_sizes[s]

	return result

def part2(network: nx.Graph, coords, dist_matrix):

	# Sort distance matrix.
	dist_sorted = sorted(dist_matrix.items(), key=lambda item: item[1])

	n = 0
	while nx.number_connected_components(network) > 1:
		# Get closest pair.
		closest_pair = dist_sorted[n][0]
		n += 1
		# Add edge.
		network.add_edge(*closest_pair)
		# Update distasnces.
		dist_matrix[closest_pair] = np.inf
		dist_matrix[closest_pair[::-1]] = np.inf

		# num_components = nx.number_connected_components(network)
		# components = nx.connected_components(network)
		# component_sizes = sorted([len(c) for c in components], reverse=True)
		# unique_component_sizes, unique_component_size_counts = np.unique(component_sizes, return_counts=True)
		# print(f'After connecting boxes {coords[closest_pair[0]]} and {coords[closest_pair[1]]}, there are {num_components} components with sizes {unique_component_size_counts} {unique_component_sizes}')

	result = coords[closest_pair[0]][0] * coords[closest_pair[1]][0]

	return result
		
def solve_aoc():
	data = read_data()

	num_boxes = len(data)
	coords = [tuple(data[r].split(',')) for r in range(num_boxes)]
	coords = [tuple(int(coord[n]) for n in range(3)) for coord in coords]

	network = nx.Graph()
	network.add_nodes_from(list(range(num_boxes)))

	# Build distance matrix.
	dist_matrix = {(i,j): np.linalg.norm(np.array(coords[i]) - np.array(coords[j])) \
				for i in range(num_boxes) for j in range(num_boxes) if i < j}

	if PART == 1:
		result = part1(network, coords, dist_matrix, num_pairs_to_connect=10 if SAMPLE else 1000, product_size_to_return=3)
	else:
		result = part2(network, coords, dist_matrix)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
