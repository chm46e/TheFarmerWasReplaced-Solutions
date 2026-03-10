# This is an attempt at implementing A* algorithm into the dinosaur (snake) game.
# Abandoned, because a_star takes too long to compute even after optimizations. (up to 10s)
# Apparently A* is not always the best pathfinding algorithm.
# Going back to optimizing greedy + hamiltonian with shortcuts.

from a_star import a_star
from utils import WORLD_SIZE, MAX_TILE_SIZE, can_move_anywhere
from deque import *
from movement import move_to_pos, move_to_any_open

MAZE = []
for y in range(WORLD_SIZE):
	MAZE.append([])
	for x in range(WORLD_SIZE):
		MAZE[y].append(0)

# DINOSAUR.pop(0) with a queue takes too long, so deque it is.
DINOSAUR = deque_create(MAX_TILE_SIZE)
OLD_TAIL = None # previous tail position that now is empty

# Update MAZE and DINOSAUR after movement
# new_position: (x, y), of the head
# ate_apple: boolean, moved off of the apple?
def update_dinosaur_queue_and_maze(new_position, ate_apple):
	global OLD_TAIL
	
	deque_append(DINOSAUR, new_position)
	MAZE[new_position[1]][new_position[0]] = 1
	
	if not ate_apple:
		OLD_TAIL = deque_popleft(DINOSAUR)
		MAZE[OLD_TAIL[1]][OLD_TAIL[0]] = 0
	# if ate an apple, keep the tail

def execute_dinosaur_astar_with_fallback():
	while True:
		clear()
		change_hat(Hats.Dinosaur_Hat)
		apple_pos = (0, 0)
		length = 1
		path = []
		waiting_path = []
		ate_apple = False
		
		while True:
			if not can_move_anywhere():
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
				path = a_star(MAZE, new_position, apple_pos)
			
			if path and len(path) > 0:
				success = move_to_pos(path[-1][0], path[-1][1])
				if not success:
					move_to_any_open()
					continue
				path.pop()
				waiting_path = []
			else:
				if (not waiting_path or len(waiting_path) == 0) and OLD_TAIL != None:
					waiting_path = a_star(MAZE, new_position, OLD_TAIL)
				
				if waiting_path:
					move_to_pos(waiting_path[-1][0], waiting_path[-1][1])
					waiting_path.pop()
				else:
					move_to_any_open()
								
execute_dinosaur_astar_with_fallback()				
		
		
	