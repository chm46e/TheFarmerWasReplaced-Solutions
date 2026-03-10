# A bunch of drone movement related functions.

from farming import farm
from utils import (is_even, decide_closest_rectangle_corner,
	calculate_distance_toroidal_space, get_random_position)
from farming import decide_pumpkin_harvest
from utils import sleep, WORLD_SIZE, xor, random_element

# Move to position (x;y)
# x: int, target x coordinate
# y: int, target y coordinate
# loopable: bool, allow toroidal space
# returns: True if reached pos, else False
def move_to_pos(x, y, loopable = False):
	current_x, current_y = get_pos_x(), get_pos_y()
	
	# This is very over-optimized for every tick, but I love it.
	
	# normalize to [0, world_size-1]. Also works with negative values!
	x %= WORLD_SIZE
	y %= WORLD_SIZE
		
	if current_x != x:	
		if loopable:
			distance_x = calculate_distance_toroidal_space(x, current_x, WORLD_SIZE)
		else:
			distance_x = x - current_x
		
		if distance_x > 0:
			for _ in range(distance_x):
				move(East)
		else:
			for _ in range(-distance_x):
				move(West)
			
	if current_y != y:
		if loopable:
			distance_y = calculate_distance_toroidal_space(y, current_y, WORLD_SIZE)
		else:
			distance_y = y - current_y		
		if distance_y > 0:
			for _ in range(distance_y):
				move(North)
		else:
			for _ in range(-distance_y):
				move(South)
			
	if not loopable:		
		if get_pos_x() != x or get_pos_y() != y:
			quick_print("move_to_pos failed: something is blocking the way...")
			return False
		return True
		
			
def move_to_closest_rectangle_corner(bottom_left, top_right):
	closest_corner = decide_closest_rectangle_corner(bottom_left, top_right)
	
	if closest_corner == "bottom_left":
		move_to_pos(bottom_left[0], bottom_left[1], True)
	elif closest_corner == "bottom_right":
		move_to_pos(top_right[0], bottom_left[1], True)
	elif closest_corner == "top_left":
		move_to_pos(bottom_left[0], top_right[1], True)
	elif closest_corner == "top_right":
		move_to_pos(top_right[0], top_right[1], True)	
	else:
		quick_print("Invalid corner")
		
# Move to any random open space next to the drone
# Returns: True if moved, False if fully stuck
def move_to_any_open():
	moveable = []
	if can_move(North):
		moveable.append(North)
	if can_move(East):
		moveable.append(East)
	if can_move(West):
		moveable.append(West)
	if can_move(South):
		moveable.append(South)
	
	if not moveable:
		return False
	return move(random_element(moveable))
	
move_to_any_open()
	
def move_to_random_position():
	position = get_random_position()
	move_to_pos(position[0], position[1])

def determine_type_with_algorithm(algorithm, position, types):
	if len(types) == 0:
		return Entities.Grass
	
	x, y = position
	
	if algorithm == "fill":
		return types[0]
	elif algorithm == "checkered":
		if is_even(x):
			if is_even(y):
				return types[0]
			if len(types) > 1:
				return types[1]
			return Entities.Grass
		else:
			if is_even(y):
				if len(types) > 1:
					return types[1]
				return Entities.Grass
			return types[0]
	else:
		print("Unknown algorithm")
		return types[0]
		
def determine_standing_type_with_algorithm(algorithm, types):
	x, y = get_pos_x(), get_pos_y()
	return determine_type_with_algorithm(algorithm, [x, y], types)
				
# Farm a column of types with algorithm
# types: array of Entities
# position: array[x, y], starting position
# length: int, column will go up this many spaces
# algorithm: fill | checkered
def farm_column(types, position, length = get_world_size(), algorithm="fill", reversed = False):
	x, y = position
	pumpkin_counter = 0
	
	if reversed:
		move_to_pos(x, y + length - 1, True)
	else:
		move_to_pos(x, y, True)
		
	correct_pumpkin_measure = measure()
	
	for i in range(length):
		if reversed:
			move_to_pos(x, y + length - 1 - i, True)
		else:
			move_to_pos(x, y + i, True)
			
		farm(determine_standing_type_with_algorithm(algorithm, types))
		
		# Pumpkin checks
		pumpkin_counter = decide_pumpkin_harvest(types, pumpkin_counter, correct_pumpkin_measure, length)
		if pumpkin_counter == length:
			harvest()
			farm_column(types, position, length, algorithm, reversed)

# Farm a row of types with algorithm
# types: array of Entities
# position: array[x, y], starting position
# length: int, row will go right this many spaces
# algorithm: string, fill | checkered
def farm_row(types, position, length = get_world_size(), algorithm="fill", reversed = False):
	x, y = position
	pumpkin_counter = 0
	
	if reversed:
		move_to_pos(x + length - 1, y, True)
	else:
		move_to_pos(x, y, True)
	
	correct_pumpkin_measure = measure()
		
	for i in range(length):
		if reversed:
			move_to_pos(x + length - 1 - i, y, True)
		else:
			move_to_pos(x + i, y, True)
		
		farm(determine_standing_type_with_algorithm(algorithm, types))
		
		# Pumpkin checks
		pumpkin_counter = decide_pumpkin_harvest(types, pumpkin_counter, correct_pumpkin_measure, length)
		if pumpkin_counter == length:
			harvest()
			farm_row(types, position, length, algorithm, reversed)
			
		
# Farm a rectangle of types with algorithm
# types: array of Entities
# bottom_left: array[x, y], bottom left position
# top_right: array[x, y], top right position
# algorithm: string, fill | checkered
# rotate: bool, False is row, True is column
def farm_rectangle(types, bottom_left, top_right, algorithm="fill", rotate = False):
	closest_corner = decide_closest_rectangle_corner(bottom_left, top_right)
	height = abs(top_right[1] - bottom_left[1]) + 1
	width = abs(top_right[0] - bottom_left[0]) + 1
	if rotate:
		iterate = width
		length = height
		function = farm_column
		increase_y = 0
	else:
		iterate = height
		length = width
		function = farm_row
		increase_y = 1
		
	if closest_corner == "bottom_left":
		for i in range(iterate):
			function(types, [bottom_left[0] + i * xor(increase_y, 1), bottom_left[1] + i * increase_y], length, algorithm, i % 2 != 0)
	elif closest_corner == "bottom_right":
		for i in range(iterate):
			function(types, [bottom_left[0] - i * xor(increase_y, 1), bottom_left[1] + i * increase_y], length, algorithm, i % 2 == 0)
	elif closest_corner == "top_left":
		for i in range(iterate):
			function(types, [bottom_left[0] + i * xor(increase_y, 1), top_right[1] - i * increase_y], length, algorithm, i % 2 != 0)
	elif closest_corner == "top_right":
		for i in range(iterate):
			function(types, [bottom_left[0] - i * xor(increase_y, 1), top_right[1] - i * increase_y], length, algorithm, i % 2 == 0)		
	else:
		quick_print("Invalid corner")
		
# Farm a square of types with algorithm
# types: array of Entities
# bottom_left: array[x, y]. bottom left position
# length: int, length of the square
# algorithm: string, fill | checkered
# rotate: bool, False is row, True is column
def farm_square(types, bottom_left, length, algorithm="fill", rotate = False):
	top_right = [bottom_left[0] + length - 1, bottom_left[1] + length - 1]
	farm_rectangle(types, bottom_left, top_right, algorithm, rotate)
	
def bubble_sort_cacti(bottom_left, top_right):
	width = abs(top_right[0] - bottom_left[0]) + 1
	height = abs(top_right[1] - bottom_left[1]) + 1
	
	# Sort all rows
	for y in range(bottom_left[1], top_right[1] + 1):
		move_to_pos(bottom_left[0], y, True)
		swapped = False
		
		for i in range(width):
			swapped = False
			for j in range(width - 1):
				value = measure()
				east_value = measure(East)
				
				if value != None and east_value != None:
					if value > east_value and get_pos_x() != WORLD_SIZE - 1:
						swap(East)
						swapped = True
				move(East)
			move_to_pos(bottom_left[0], y, True)
			if not swapped:
				break

			
	# Sort all columns
	for x in range(bottom_left[0], top_right[0] + 1):
		move_to_pos(x, bottom_left[1], True)
		
		for i in range(height):
			swapped = False
			for j in range(height - 1):
				value = measure()
				north_value = measure(North)
				
				if value != None and north_value != None:
					if value > north_value and get_pos_y() != WORLD_SIZE - 1:
						swap(North)
						swapped = True
				move(North)
			move_to_pos(x, bottom_left[1], True)
			if not swapped:
				break
				
def farm_cacti_rectangle(bottom_left, top_right):
	move_to_closest_rectangle_corner(bottom_left, top_right)
	if get_entity_type() != Entities.Cactus or not can_harvest():
		sleep(1)
	
	bubble_sort_cacti(bottom_left, top_right)
	
	# can only be fully harvested from bottom_left corner
	move_to_pos(bottom_left[0], bottom_left[1], True)
	
	if can_harvest():
		harvest()
	farm_rectangle([Entities.Cactus], bottom_left, top_right)
	
def farm_cacti_square(bottom_left, length):	
	top_right = [bottom_left[0] + length - 1, bottom_left[1] + length - 1]	
	farm_cacti_rectangle(bottom_left, top_right)
