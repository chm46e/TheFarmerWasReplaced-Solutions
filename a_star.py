# The A* pathfinding algorithm that is too slow for almost all uses in the game.
# This is one of the interesting ways the game forces you to not use usual solutions to problems.
# Even with a decent solution and a heapq, the calculations take several seconds.
# The game punishes for heavy list usage and arithmetic, which are operations that computers are usually very fast at.

from utils import manhattan_distance
from heap_queue import *

def _a_star_reconstruct_path(came_from, current):
	total_path = [current]
	while current in came_from:
		current = came_from[current]
		total_path.append(current)
	
	# return path in reverse, because pop() is much faster than pop(0)
	total_path.pop() # don't need the starting position
	return total_path
	
def _a_star_comparator(heapq, node_a, node_b):
	f_score = heapq["f_score"]
	return f_score[node_a] < f_score[node_b]

# A* algorithm
# Doesn't use toroidal space, can't use it anyway.
# Coordinates start from bottom_left as usual.
# maze: 2d array of booleans (wall), [y][x]
# start: (x, y), coords of the start position
# end: (x, y), coords of the end position
# returns: REVERSE array of move_to_pos coordinates or None
def a_star(maze, start, end):
	f_score = {start: manhattan_distance(start, end)}
	g_score = {start: 0}
	
	open = heapq_create(_a_star_comparator, {"f_score": f_score})
	heapq_push(open, start)
	
	came_from = {}
	maze_height = len(maze)
	maze_width = len(maze[0])
	end_x, end_y = end
	
	while heapq_length(open):
		current = heapq_pop(open)
		current_x, current_y = current
		
		if current == end:
			return _a_star_reconstruct_path(came_from, current)
			
		# check neighbors
		for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
			nx, ny = current_x + dx, current_y + dy
			neighbor = (nx, ny)
			if neighbor in came_from:
				continue
			
			if 0 <= nx < maze_width and 0 <= ny < maze_height and not maze[ny][nx]:
				tentative_g = g_score[current] + 1

				if neighbor not in g_score or tentative_g < g_score[neighbor]:
					# best path to this neighbor so far
					came_from[neighbor] = current
					g_score[neighbor] = tentative_g
					f_score[neighbor] = tentative_g + abs(nx - end_x) + abs(ny - end_y)
					
					if not heapq_contains(open, neighbor):
						heapq_push(open, neighbor)
						
	
	return None
