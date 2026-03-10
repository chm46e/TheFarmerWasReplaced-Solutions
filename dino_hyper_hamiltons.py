# Attempt to optimize the snake game with hamiltonian and shortcuts as much as possible.
# Currently, shortcuts too little, which is why it takes 30min to fill a 32x32 board.
# This should be very possible to optimize to 15min or less, but for that it has to shortcut well into the late game.
# Also cutting down movement between shortcut movements would also help.
# Without using game glitches, this should be the fastest algorithm to solve the snake game in this game.

# Not sure if taking multiple seconds in the start to prefill the hamiltonian path is faster or not.
# It does then take only 2 ticks to find the next step, but not sure if the savings are worth it.


from utils import is_even, WORLD_SIZE, DIRECTIONS_WITH_COORDS, MAX_TILE_SIZE
from deque import *

WORLD_SIZE_MINUS_ONE = WORLD_SIZE - 1

DINOSAUR = deque_create(MAX_TILE_SIZE)
OLD_TAIL_RANK = 0

def update_dinosaur_queue(new_rank, ate_apple):
	deque_append_fast(DINOSAUR, new_rank)
	
	global OLD_TAIL_RANK
	if not ate_apple:
		OLD_TAIL_RANK = deque_popleft_fast(DINOSAUR)
	# if ate an apple, keep the tail

def get_next_hamiltonian_step(x, y):
	if not y:
		if x:
			return West
		return North
	
	if is_even(x):
		if y < WORLD_SIZE_MINUS_ONE:
			return North
		return East
	else:
		if y > 1:
			return South
		elif y and x == 31:
			return South
		return East

def prefill_hamiltonian_path():
	# TODO: range() takes 1 tick, but maybe for x in [0, 1, 2, 3, 4, 5, etc] is faster?
	for y in range(WORLD_SIZE):
		HAMILTONIAN_PATH.append([])
		for x in range(WORLD_SIZE):
			HAMILTONIAN_PATH[y].append(get_next_hamiltonian_step(x, y))
			
def calculate_hamiltonian_rank(x, y):
	if not x:
		rank = y
	elif y:
		if not is_even(x):
			# x(size - 1) + size - 1 - y + 1
			rank = x * WORLD_SIZE_MINUS_ONE + (WORLD_SIZE - y)
		else:
			rank = x * WORLD_SIZE_MINUS_ONE + y
	else:
		# size * (size - 1) + size - 1 - x + 1
		# WORLD_SIZE ** 2 - x
		rank = MAX_TILE_SIZE - x
	return rank
			
def prefill_hamiltonian_ranks():
	# TODO: range() takes 1 tick, but maybe for x in [0, 1, 2, 3, 4, 5, etc] is faster?
	for y in range(WORLD_SIZE):
		HAMILTONIAN_RANKS.append([])
		for x in range(WORLD_SIZE):
			HAMILTONIAN_RANKS[y].append(calculate_hamiltonian_rank(x, y))

# 2D array HAMILTONIAN_PATH[y][x] = next_direction	
HAMILTONIAN_PATH = []
# 2D array HAMILTONIAN_RANKS[y][x] = rank
HAMILTONIAN_RANKS = []
prefill_hamiltonian_path()
prefill_hamiltonian_ranks()

# costs: 2 + 200 ticks if success, 3 ticks otherwise
def move_next_hamiltonian_step(x, y):
	return move(HAMILTONIAN_PATH[y][x])

# costs: 2 ticks	
def get_hamiltonian_rank(x, y):
	return HAMILTONIAN_RANKS[y][x]

def move_next_snake_step(length, apple_position, x, y):
	apple_x, apple_y = apple_position
	
	if length >= MAX_TILE_SIZE * 0.15: # 0.15
		return move_next_hamiltonian_step(x, y)
		
	head_rank = get_hamiltonian_rank(x, y)
	apple_rank = get_hamiltonian_rank(apple_x, apple_y)
	
	best_direction = None
	best_rank = head_rank
	
	if apple_rank < head_rank:
		if length < 8:
			apple_rank = get_hamiltonian_rank(1, 0)
		elif length < 32:
			apple_rank = get_hamiltonian_rank(31, 0)
		elif length < 64:
			apple_rank = get_hamiltonian_rank(31, 31)
		elif length < 96:
			apple_rank = get_hamiltonian_rank(30, 1)
		elif length < 128:
			apple_rank = get_hamiltonian_rank(29, 31)
			
	for direction in DIRECTIONS_WITH_COORDS:
		dir, dir_x, dir_y = direction
		if not can_move(dir):
			continue
			
		neighbor_rank = get_hamiltonian_rank(x + dir_x, y + dir_y)
		if (neighbor_rank > head_rank and neighbor_rank <= apple_rank) and neighbor_rank > best_rank:
			best_rank = neighbor_rank
			best_direction = dir
	if best_direction:
		return move(best_direction)
	else:
		return move_next_hamiltonian_step(x, y)		
		
def execute_hyper_hamiltonian_with_shortcuts():
	while True:
		clear()
		change_hat(Hats.Dinosaur_Hat)
		apple_pos = (0, 0)
		length = 1
		ate_apple = False
		fully_stuck = False
		
		while True:
			if fully_stuck:
				change_hat(Hats.Straw_Hat)
				break
				
			x, y = get_pos_x(), get_pos_y()
			update_dinosaur_queue(get_hamiltonian_rank(x, y), ate_apple)
			if ate_apple:
				ate_apple = False
				
			if get_entity_type() == Entities.Apple:
				apple_pos = measure()
				length += 1
				ate_apple = True
			
			fully_stuck = not move_next_snake_step(length, apple_pos, x, y)
				
execute_hyper_hamiltonian_with_shortcuts()
