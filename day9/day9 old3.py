
import numpy as np
import time
import tqdm
#import functools
#import networkx as nx

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

def point_in_rect(min_x, max_x, min_y, max_y, pt):
	if min_x <= pt[0] <= max_x and min_y <= pt[1] <= max_y:
		return True
	else:
		return False
	
def neighbors(red_tiles, red_tile_index):
	red_tile = red_tiles[red_tile_index]
	red_nbr_1 = red_tiles[red_tile_index-1 if red_tile_index>0 else len(red_tiles)-1]
	red_nbr_2 = red_tiles[red_tile_index+1 if red_tile_index<len(red_tiles)-1 else 0]
	nbrs = []
	for red_nbr in (red_nbr_1, red_nbr_2):
		if red_nbr[0] == red_tile[0]:
			if red_nbr[1] < red_tile[1]:
				nbr = (red_tile[0], red_tile[1] - 1)
			else:
				nbr = (red_tile[0], red_tile[1] + 1)
		else:
			if red_nbr[0] < red_tile[0]:
				nbr = (red_tile[0] - 1, red_tile[1])
			else:
				nbr = (red_tile[0] + 1, red_tile[1])
		nbrs.append(nbr)

	return nbrs

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

	pbar = tqdm.tqdm(total=len(red_tiles) * (len(red_tiles) - 1) / 2)
	max_area = 0
	for i in range(len(red_tiles) - 1):
		for j in range(i + 1, len(red_tiles)):
			pbar.update()
			# Determine rectangle corners
			tile_i, tile_j = red_tiles[i], red_tiles[j]
			min_x = min(tile_i[0], tile_j[0])
			max_x = max(tile_i[0], tile_j[0])
			min_y = min(tile_i[1], tile_j[1])
			max_y = max(tile_i[1], tile_j[1])
			# Check whether there area any red tiles inside the rectangle.
			ok = True
			for t, tile in enumerate(red_tiles):
				if (tuple(tile) != tuple(tile_i) and tuple(tile) != tuple(tile_j) # tile is not i or j
					and tuple(tile) not in (tuple((tile_i[0], tile_j[1])), tuple((tile_j[0], tile_i[1]))) # tile is not one of the other corners
					and point_in_rect(min_x, max_x, min_y, max_y, tile)):
					# Check whether *neighbors* of this tile are also in the rect --
					# if so, no good.
					nbrs = neighbors(red_tiles, t)
					if all(point_in_rect(min_x, max_x, min_y, max_y, nbr) for nbr in nbrs):
						ok = False
						break
				if not ok:
					break
			if ok:
				area = (max_x - min_x + 1) * (max_y - min_y + 1)
				if area > max_area:
					max_area = area
					print(f'New max area {max_area} from tiles {tile_i} and {tile_j}')

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
