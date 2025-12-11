
import numpy as np
import time
import tqdm
#import functools
#import networkx as nx
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

DAY = 9
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

def print_diagram(diagram):
	max_x = max([key[0] for key in diagram.keys()])
	max_y = max([key[1] for key in diagram.keys()])
	for y in range(max_y + 1): 
		row_str = ''
		for x in range(max_x + 1):
			if diagram[(x, y)] is None:
				row_str += '. '
			else:
				row_str += f'{diagram[(x, y)]} '
		print(row_str)

def part1(red_tiles):

	max_area = 0
	for i in range(len(red_tiles) - 1):
		for j in range(i + 1, len(red_tiles)):
			area = abs((red_tiles[i][0] - red_tiles[j][0] + 1) * (red_tiles[i][1] - red_tiles[j][1] + 1))
			if area > max_area:
				max_area = area
				
	result = max_area
	return result

def part2(red_tiles):

	# Find min and max coordinates.
	x_vals = [tile[0] for tile in red_tiles]
	y_vals = [tile[1] for tile in red_tiles] 
	min_x = 0
	max_x = max(x_vals)
	min_y = 0
	max_y = max(y_vals)
	x_vals = list(range(min_x, max_x - min_x + 3))
	y_vals = list(range(min_y, max_y - min_y + 3))

	# Build polygon.
	polygon = Polygon(red_tiles)

	# Build diagram.
	print('building diagram ...')
	diagram = {} # {(x, y): None for x in x_vals for y in y_vals}
	pbar = tqdm.tqdm(total=len(x_vals)*len(y_vals))
	for t, tile in enumerate(red_tiles):
		pbar.update()
		diagram[tuple(tile)] = 'R'
		if t < len(red_tiles) - 1:
			next_tile = red_tiles[t+1]
		else:
			next_tile = red_tiles[0]
		if tile[0] == next_tile[0]:
			# Same x.
			if tile[1] < next_tile[1]:
				edge_ys = range(tile[1] + 1, next_tile[1])
			else:
				edge_ys = range(next_tile[1] + 1, tile[1])
			for y in edge_ys:
				diagram[(tile[0], y)] = 'E' # edge
		else:
			# Same y.
			if tile[0] < next_tile[0]:
				edge_xs = range(tile[0] + 1, next_tile[0])
			else:
				edge_xs = range(next_tile[0] + 1, tile[0])
			for x in edge_xs:
				diagram[(x, tile[1])] = 'E'

	# Determine interior points.
	print('determining interior points ...')
	is_interior = {}
	for x in x_vals:
		for y in y_vals:
			is_interior[(x, y)] = diagram.get((x, y), None) in ('R', 'E') or polygon.contains(Point(x, y))
	
	if SAMPLE:
		print_diagram(diagram)
		print()
		diagram2 = {(x, y): 'I' if is_interior[(x, y)] else '.' for x in x_vals for y in y_vals}
		print_diagram(diagram2)

	# Loop through pairs of red tiles and see whether rectangle is entirely interior.
	pbar = tqdm.tqdm(total=int(len(red_tiles)*(len(red_tiles) - 1) / 2))
	max_area = 0
	for i in range(len(red_tiles) - 1):
		for j in range(i + 1, len(red_tiles)):
			pbar.update()
			tile_i = red_tiles[i]
			tile_j = red_tiles[j]
			if tile_i[0] < tile_j[0]:
				rect_x_vals = list(range(tile_i[0], tile_j[0] + 1))
			else:
				rect_x_vals = list(range(tile_j[0], tile_i[0] + 1))
			if tile_i[1] < tile_j[1]:
				rect_y_vals = list(range(tile_i[1], tile_j[1] + 1))
			else:
				rect_y_vals = list(range(tile_j[1], tile_i[1] + 1))
			rect_xy_vals = [(x, y) for x in rect_x_vals for y in rect_y_vals]
			if not all([is_interior[(x, y)] for (x, y) in rect_xy_vals]):
				break
			
			area = abs((red_tiles[i][0] - red_tiles[j][0] + 1) * (red_tiles[i][1] - red_tiles[j][1] + 1))
			if area > max_area:
				max_area = area

	result = max_area
	return result
		
def solve_aoc():
	data = read_data()

	red_tiles = [data[r].split(',') for r in range(len(data))]
	red_tiles = [np.array((int(red_tiles[r][0]), int(red_tiles[r][1]))) for r in range(len(red_tiles))]

	if PART == 1:
		result = part1(red_tiles)
	else:
		result = part2(red_tiles)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
