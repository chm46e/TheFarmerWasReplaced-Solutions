# A bunch of different utility functions thrown together into one file.

WORLD_SIZE = get_world_size()
MAX_TILE_SIZE = WORLD_SIZE * WORLD_SIZE

# Function to update the world_size safely
# Use this rather than set_world_size() directly.
# This is bad coding practise, but the best way to optimize for ticks elsewhere.
def update_world_size(size):
	global WORLD_SIZE
	global MAX_TILE_SIZE
	
	set_world_size(size)
	WORLD_SIZE = get_world_size()
	MAX_TILE_SIZE = WORLD_SIZE * WORLD_SIZE

def is_even(x):
	return not x % 2
	
# Measure distance from drone to position
# Assumes toroidal space.
# position: array[x, y]
def distance_to_pos(position):
	x, y = get_pos_x(), get_pos_y()
	return (abs(calculate_distance_toroidal_space(position[0], x, WORLD_SIZE)) +
		abs(calculate_distance_toroidal_space(position[1], y, WORLD_SIZE)))
	
def manhattan_distance(position1, position2):
	return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
	
# Decide which corner to move to when rectangle farming
# bottom_left: array[x, y], position of bottom_left corner
# top_right: array[x, y], position of top_right corner
# Returns: string, bottom_left | bottom_right | top_left | top_right
def decide_closest_rectangle_corner(bottom_left, top_right):
	bottom_left_corner = distance_to_pos([bottom_left[0], bottom_left[1]])
	bottom_right_corner = distance_to_pos([top_right[0], bottom_left[1]])
	top_left_corner = distance_to_pos([bottom_left[0], top_right[1]])
	top_right_corner = distance_to_pos([top_right[0], top_right[1]])
	
	closest_corner = min(bottom_left_corner, bottom_right_corner, top_left_corner, top_right_corner)
	
	if closest_corner == bottom_left_corner:
		return "bottom_left"
	elif closest_corner == bottom_right_corner:
		return "bottom_right"
	elif closest_corner == top_left_corner:
		return "top_left"
	elif closest_corner == top_right_corner:
		return "top_right"
	else:
		return "bottom_left"
	
def get_opposite_direction(direction):
	if direction == North:
		return South
	elif direction == South:
		return North
	elif direction == East:
		return West
	elif direction == West:
		return East

DIRECTIONS = [North, South, East, West]
DIRECTIONS_WITH_COORDS = [(North, 0, 1), (South, 0, -1), (East, 1, 0), (West, -1, 0)]
DIRECTIONS_TO_COORDS = {North: (0, 1), South: (0, -1), East: (1, 0), West: (-1, 0)}

def convert_direction_to_pos_diff(direction):
	return DIRECTIONS_TO_COORDS[direction]

def get_pos_from_direction(direction):
	x, y = get_pos_x(), get_pos_y()
	diff = convert_direction_to_pos_diff(direction)
	return (diff[0] + x, diff[1] + y)
		
# Sleep synchronously on the same thread
# Not super accurate +-0.5s, but looks cooler
# seconds: int, time in seconds to wait
def sleep(seconds):
	start = get_time()
	
	while get_time() - start < seconds:
		do_a_flip()
		
# Sleep synchronously for ticks
# Accuracy +-1 tick, use only if accuracy matters
# ticks: int, ticks to sleep on the thread	
def sleep_ticks(ticks):
	# TODO: consider more precise waiting with pass
	start = get_tick_count()
	
	while get_tick_count() - start < ticks:
		pass

# Returns: True if any open spots, False if fully stuck
def can_move_anywhere():
	if (can_move(North) or can_move(East)) or (can_move(West) or can_move(South)):
		return True
	else:
		return False
		
def get_random_position():
	return (random() * WORLD_SIZE // 1, random() * WORLD_SIZE // 1)
		
# Calculate distance in a looping donut world
# target: int, x or y
# current: int, x or y
# world_size: int, get_world_size()
# returns: int, + means east, - means west
def calculate_distance_toroidal_space(target, current, world_size):
	# I didn't come up with it myself, but the logic is simple:
	# first it calculates raw_distance = target - current
	# if raw_distance is small, it simplifies back to raw_distance
	# if raw_distance >= 0.5world, then distance goes negative
	return (target - current + world_size + world_size // 2) % world_size - world_size // 2
		
# Simulate file execution with current items and unlocks		
def simulate_with_current(file, speed = 4, globals = {}, seed = 1):
	unlocks = {
		Unlocks.Cactus: num_unlocked(Unlocks.Cactus),
		Unlocks.Carrots: num_unlocked(Unlocks.Carrots),
		Unlocks.Trees: num_unlocked(Unlocks.Trees),
		Unlocks.Sunflowers: num_unlocked(Unlocks.Sunflowers),
		Unlocks.Pumpkins: num_unlocked(Unlocks.Pumpkins),
		Unlocks.Grass: num_unlocked(Unlocks.Grass),
		Unlocks.Speed: num_unlocked(Unlocks.Speed),
		Unlocks.Expand: num_unlocked(Unlocks.Expand),
		Unlocks.Plant: num_unlocked(Unlocks.Plant),
		Unlocks.Polyculture: num_unlocked(Unlocks.Polyculture),
		Unlocks.Fertilizer: num_unlocked(Unlocks.Fertilizer),
		Unlocks.Watering: num_unlocked(Unlocks.Watering),
		Unlocks.Dinosaurs: num_unlocked(Unlocks.Dinosaurs),
		Unlocks.Megafarm: num_unlocked(Unlocks.Megafarm),
		Unlocks.Senses: num_unlocked(Unlocks.Senses),
		Unlocks.Mazes: num_unlocked(Unlocks.Mazes)
	}

	items = {
		Items.Hay: num_items(Items.Hay), 
		Items.Wood: num_items(Items.Wood),
		Items.Carrot: num_items(Items.Carrot), 
		Items.Pumpkin: num_items(Items.Pumpkin),
		Items.Cactus: num_items(Items.Cactus), 
		Items.Weird_Substance: num_items(Items.Weird_Substance),
		Items.Gold: num_items(Items.Gold), 
		Items.Water: num_items(Items.Water) ,
		Items.Fertilizer: num_items(Items.Fertilizer), 
		Items.Power: num_items(Items.Power)
	}

	simulate(file, unlocks, items, globals, seed, speed)
	
# Simulate file execution with a ton of items and all unlocks
def simulate_with_perfection(file, speed = 4, globals = {}, seed = 1):
	items = {
		Items.Hay: 1000000000, 
		Items.Wood: 1000000000,
		Items.Carrot: 1000000000, 
		Items.Pumpkin: 1000000000,
		Items.Cactus: 1000000000, 
		Items.Weird_Substance: 1000000000,
		Items.Gold: 1000000000, 
		Items.Water: 1000000000,
		Items.Fertilizer: 1000000000, 
		Items.Power: 1000000000
	}

	simulate(file, Unlocks, items, globals, seed, speed)

def random_element(list):
	return list[random() * len(list) // 1]
	
# Return a number between a and b (both included)	
def randint(a, b):
	return (random() * (b - a + 1) // 1) + a
	
def xor(a, b):
	# This is much cooler:
	# return not (a and b) and not (not a and not b)
	return a != b
	
# Write dict_b into dict_a
# dict_b overwrites dict_a values, destroying dict_a
# dict_a: first dict, will be overwritten
# dict_b: second dict, won't be overwritten
# returns: reference to first dict
def merge_two_dictionaries(dict_a, dict_b):
	for key in dict_b:
		dict_a[key] = dict_b[key]
	return dict_a
		
def _default_sort_key_fn(elem):
	return elem
			
def _bubble_sort(list, key_fn = _default_sort_key_fn, reverse = False):
	n = len(list)
	for i in range(n):
		for j in range(n - 1 - i):
			a = key_fn(list[j])
			b = key_fn(list[j+1])
			if not reverse:
				if a > b:
					temp = list[j]
					list[j] = list[j+1]
					list[j+1] = temp
			else:
				if a < b:
					temp = list[j]
					list[j] = list[j+1]
					list[j+1] = temp
	return list
	
def _insertion_sort(list, key_fn = _default_sort_key_fn, reverse = False):
	n = len(list)
	for i in range(1, n):
		current_val = list[i]
		j = i - 1
		
		while j >= 0:
			key_j = key_fn(list[j])
			key_curr = key_fn(current_val)
			
			should_swap = False
			if reverse:
				if key_j < key_curr:
					should_swap = True
			else:
				if key_j > key_curr:
					should_swap = True
			if should_swap:
				list[j + 1] = list[j]
				j -= 1
			else:
				break
		list[j + 1] = current_val
	return list
	
def sort(list, key_fn = _default_sort_key_fn, reverse = False, sorting_alg = _insertion_sort):
	return sorting_alg(list, key_fn, reverse)
	
def benchmark_fn(fn, args = None):
	start_tick_count = get_tick_count()
	start_s_count = get_time()
	overhead = 0
	
	if not args:
		res = fn()
		overhead = 2
	else:
		n = len(args)
		if n == 1:
			res = fn(args[0])
			overhead = 6
		elif n == 2:
			res = fn(args[0], args[1])
			overhead = 9
		elif n == 3:
			res = fn(args[0], args[1], args[2])
			overhead = 12
		elif n == 4:
			res = fn(args[0], args[1], args[2], args[3])
			overhead = 15
		
	end_tick_count = get_tick_count()
	end_s_count = get_time()
	quick_print(fn, "- Took", end_tick_count - start_tick_count - overhead, "ticks =", end_s_count - start_s_count, "seconds. Returned", res)
	
	return res
