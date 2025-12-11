
import numpy as np
import time
import tqdm
#import functools
#import networkx as nx
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

DAY = 9
PART = 2
SAMPLE = True
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
	# returns -1 if strictly outside, 0 if on border, 1 if strictly inside
	if min_x < pt[0] < max_x and min_y < pt[1] < max_y:
		return 1
	elif min_x < pt[0] < max_x and (pt[1] == min_y or pt[1] == max_y):
		return 0
	elif min_y < pt[1] < max_y and (pt[0] == min_x or pt[0] == max_x):
		return 0
	else:
		return -1
	
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

def polygon_border_points(red_tiles):
	border_points = set()
	prev_tile = np.array(red_tiles[-1])
	for r in range(len(red_tiles)):
		tile = np.array(red_tiles[r])
		direction = (tile - prev_tile) / (int(abs(tile[0] - prev_tile[0])) + int(abs(tile[1] - prev_tile[1])))
		pt = prev_tile
		while not (pt == tile).all():
			border_points.add(tuple((int(pt[0]), int(pt[1]))))
			pt = pt + direction
		prev_tile = tile

	return border_points

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

	# using idea here: https://www.reddit.com/r/adventofcode/comments/1phywvn/comment/ntagqh5/
	# 1. All corners of the rectangle must be within the polygon.
	# 2. No edges of the polygon can extend to the inside of the rectangle. (Extending to the edge of the rectangle is okay.)
	# 3. If you shrink the rectangle by one tile on all four sides, all corners of the shrunken rectangle must be within the polygon.

	# Build polygon.
	polygon = Polygon(red_tiles)
	# Get border points.
	border_points = polygon_border_points(red_tiles)

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
			corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
			# Check that all corners are within the polygon.
			all_corners_inside = all([corner in border_points or polygon.contains(Point(corner)) for corner in corners])
			if not all_corners_inside:
				continue
			# Check that all corners are within the polygon if we move each side in by 1 unit.
			corners = [(min_x+1, min_y+1), (min_x+1, max_y-1), (max_x-1, min_y+1), (max_x-1, max_y-1)]
			all_corners_inside = all([corner in border_points or polygon.contains(Point(corner)) for corner in corners])
			if not all_corners_inside:
				continue

			# Check that every edge is either fully inside or fully outside the rectangle.
			prev_tile = red_tiles[-1]
			prev_is_inside = point_in_rect(min_x, max_x, min_y, max_y, prev_tile)
			ok = True
			for t, tile in enumerate(red_tiles):
				tile_is_inside = point_in_rect(min_x, max_x, min_y, max_y, tile)
				if (prev_is_inside == -1 and tile_is_inside == 1) or \
					(prev_is_inside == 0 and tile_is_inside == 1) or \
					(prev_is_inside == 1 and tile_is_inside in (0, -1)):
					ok = False
					break
				else:
					prev_tile = tile
					prev_is_inside = tile_is_inside
			
			if not ok:
				continue

			if ok:
				area = (max_x - min_x + 1) * (max_y - min_y + 1)
				if area > max_area:
					max_area = area
#					print(f'New max area {max_area} from tiles {tile_i} and {tile_j}')

	result = max_area
	return result
		
def part2_notme(puzzle_input):
	# from https://github.com/mgtezak/Advent_of_Code/blob/master/2025/09/p2.py
    corners = [tuple(map(int, line.split(','))) for line in puzzle_input.splitlines()]
    n = len(corners)

    def get_size(x1, y1, x2, y2):
        x = abs(x1 - x2) + 1
        y = abs(y1 - y2) + 1
        return x * y

    edges = []
    sizes = []
    for i in range(n):
        edges.append(sorted((corners[i], corners[i-1])))
        for j in range(i+1, n):
            c1, c2 = sorted((corners[i], corners[j]))
            sizes.append((get_size(*c1, *c2), c1, c2))

    edges.sort(reverse=True, key=lambda e: get_size(*e[0], *e[1]))
    sizes.sort(reverse=True)

    for size, (x1, y1), (x2, y2) in sizes:
        y1, y2 = sorted((y1, y2))
        if not any(
            (x4 > x1 and x3 < x2 and y4 > y1 and y3 < y2)
            for (x3, y3), (x4, y4) in edges
        ):
            return size
		
def solve_aoc():
	data = read_data()

	red_tiles = [data[r].split(',') for r in range(len(data))]
	red_tiles = [np.array((int(red_tiles[r][0]), int(red_tiles[r][1]))) for r in range(len(red_tiles))]

	if PART == 1:
		result = part1(red_tiles)
	else:
		red_tiles_temp = [f'{int(tile[0])},{int(tile[1])}' for tile in red_tiles]
		red_tiles_str = '\n'.join(red_tiles_temp)
		result = part2_notme(red_tiles_str)
#		result = part2(red_tiles)

	return result

if __name__ == "__main__":
    start_time = time.time()
    result = solve_aoc()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Result: {result}")
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
