# This is an attempt of solving the dinosaur (snake) game with a smart greedy and then hamiltonian with shortcuts.
# The simple greedy algorithm tends to suicide a lot, which I tried to solve first with counting free neighbors.
# That helped, but still the same problem, that is only solvable with flood fill checking, which fixed the suicides.
# But calculating flood fill every step takes too long (goes up from 0.5s/step), so this script was abandoned.
# It isn't optimized, deemed it worthless.

from movement import move_to_pos, move_to_any_open
from utils import (is_even, can_move_anywhere, update_world_size, WORLD_SIZE, DIRECTIONS_WITH_COORDS, manhattan_distance,
	MAX_TILE_SIZE, sort, get_pos_from_direction, benchmark_fn)
from deque import *

MAZE = []
for y in range(WORLD_SIZE):
	MAZE.append([])
	for x in range(WORLD_SIZE):
		MAZE[y].append(0)
DINOSAUR = deque_create(MAX_TILE_SIZE)

# Update MAZE and DINOSAUR after movement
# new_position: (x, y), of the head
# ate_apple: boolean, moved off of the apple?
def update_dinosaur_queue_and_maze(new_position, ate_apple):
	deque_append(DINOSAUR, new_position)
	MAZE[new_position[1]][new_position[0]] = 1
	
	if not ate_apple:
		old_tail = deque_popleft(DINOSAUR)
		MAZE[old_tail[1]][old_tail[0]] = 0
	# if ate an apple, keep the tail

def calculate_hamiltonian_rank(position):
	x, y = position
	rank = 0
	
	if x == 0:
		rank = y
	elif y != 0:
		if not is_even(x):
			# x(size - 1) + size - 1 - y + 1
			rank = x * (WORLD_SIZE - 1) + (WORLD_SIZE - y)
		else:
			rank = x * (WORLD_SIZE - 1) + y
	else:
		# size * (size - 1) + size - 1 - x + 1
		rank = WORLD_SIZE ** 2 - x
		
	return rank

def move_next_hamiltonian_step():
	x, y = get_pos_x(), get_pos_y()
	
	if y == 0 and can_move(West):
		return move(West)
	elif is_even(x) and can_move(North):
		return move(North)
	elif y == 1 and not is_even(x) and can_move(East):
		return move(East)
	elif y > 1 and not is_even(x) and can_move(South):
		return move(South)
	elif x == get_world_size() - 1 and can_move(South):
		return move(South)
	elif is_even(x) and y == WORLD_SIZE - 1 and can_move(East):
		return move(East)
	else:
		return False

def move_next_snake_step(length, apple_position):
	if length >= WORLD_SIZE ** 2 * 0.4:
		return move_next_hamiltonian_step()
	
	directions = [(North, 0, 1), (East, 1, 0), (South, 0, -1), (West, -1, 0)]
	x, y = get_pos_x(), get_pos_y()
	head_rank = calculate_hamiltonian_rank([x, y])
	apple_rank = calculate_hamiltonian_rank(apple_position)
	
	best_direction = None
	best_rank = head_rank
	
	for direction in directions:
		if not can_move(direction[0]):
			continue
			
		neighbor_rank = calculate_hamiltonian_rank([x + direction[1], y + direction[2]])
		
		if (neighbor_rank > head_rank and neighbor_rank <= apple_rank) and neighbor_rank > best_rank:
			best_rank = neighbor_rank
			best_direction = direction[0]
	
	if best_direction != None and can_move(best_direction):
		return move(best_direction)
	else:
		return move_next_hamiltonian_step()
		
def _count_free_neighbors(target_x, target_y):
	c = 0
	for direction in DIRECTIONS_WITH_COORDS:
		y = target_y + direction[2]
		x = target_x + direction[1]
		if 0 <= y < WORLD_SIZE and 0 <= x < WORLD_SIZE and not MAZE[y][x]:
			c += 1
	return c
	
def _directions_key_fn(elem):
	return elem[1]

def _has_enough_space(start_x, start_y, required_space):
	start = (start_x, start_y)
	
	queue = deque_create(MAX_TILE_SIZE)
	deque_append(queue, start)
	
	visited = {}
	visited[start] = True
	
	count = 0
	while deque_length(queue) > 0:
		curr_x, curr_y = deque_popleft(queue)
		count += 1
		
		if count >= required_space:
			return True
			
		for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
			neighbor = (curr_x + dx, curr_y + dy)
			nx, ny = neighbor
			if 0 <= nx < WORLD_SIZE and 0 <= ny < WORLD_SIZE and not MAZE[ny][nx] and not neighbor in visited:
				visited[neighbor] = True
				deque_append(queue, neighbor)		
	return False
	
def move_next_greedy_step(length, apple_pos):
	x, y = get_pos_x(), get_pos_y()
	apple_x, apple_y = apple_pos
	
	x_to_apple = abs(x - apple_x)
	y_to_apple = abs(y - apple_y)
	
	north_dist = x_to_apple + abs((y + 1) - apple_y)
	south_dist = x_to_apple + abs((y - 1) - apple_y)
	east_dist = abs((x + 1) - apple_x) + y_to_apple
	west_dist = abs((x - 1) - apple_x) + y_to_apple
	
	directions = sort([(North, north_dist), (South, south_dist), (East, east_dist),
		(West, west_dist)], _directions_key_fn)
	
	for direction in directions:
		best_dir = direction[0]
		if can_move(best_dir):
			target_x, target_y = get_pos_from_direction(best_dir)
			if length > 20:
				if benchmark_fn(_has_enough_space, [target_x, target_y, length]):
					return move(best_dir)
			else:
				if _count_free_neighbors(target_x, target_y) >= 2 or (target_x == apple_x and target_y == apple_y):
					return move(best_dir)
		
	return False


def execute_greedy_hamiltonian_with_shortcuts():
	while True:
		change_hat(Hats.Dinosaur_Hat)
		apple_pos = (0, 0)
		length = 1
		ate_apple = False
		fully_stuck = False
		
		while True:
			if fully_stuck:
				change_hat(Hats.Straw_Hat)
				break
				
			new_position = (get_pos_x(), get_pos_y())
			update_dinosaur_queue_and_maze(new_position, ate_apple)
			if ate_apple:
				ate_apple = False
				
			if get_entity_type() == Entities.Apple:
				measurement = measure()
				if measurement != None:
					apple_pos = measurement
				length += 1
				ate_apple = True
			
			if length < MAX_TILE_SIZE // 2:
				fully_stuck = not move_next_greedy_step(length, apple_pos)
			else:
				fully_stuck = not move_next_snake_step(length, apple_pos)
				
clear()				
execute_greedy_hamiltonian_with_shortcuts()
