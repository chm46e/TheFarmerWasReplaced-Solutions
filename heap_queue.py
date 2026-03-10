# Priority queue implemented using a binary heap.
# Not optimized for ticks at all, but it was fun to figure out how to implement it.

from utils import merge_two_dictionaries

def default_min_comparator(heapq, a, b):
	return a < b

# Create a priority queue object
# Min-first: comparator should return true if a < b
# Max-first: comparator should return true if a > b
# comparator: function, takes heapq, a and b as arguments and returns a boolean
# comparator_values: dict, merged into heapq, needed for advanced comparators
def heapq_create(comparator = default_min_comparator, comparator_values = {}):
	return merge_two_dictionaries({
		"tree": [],
		"compare": comparator,
		"membership": {},
	}, comparator_values)
	
def heapq_length(heapq):
	return len(heapq["tree"])
	
def heapq_push(heapq, value):
	#start_tick_count = get_tick_count()
	
	heapq["tree"].append(value)
	_bubble_up(heapq, heapq_length(heapq) - 1)
	
	if value in heapq["membership"]:
		heapq["membership"][value] += 1
	else:
		heapq["membership"][value] = 1
		
	#end_tick_count = get_tick_count()
	#took_ticks = end_tick_count - start_tick_count
	#quick_print("push:", took_ticks)
	
def _bubble_up(heapq, index):
	data = heapq["tree"]
	compare = heapq["compare"]
	
	while index > 0:
		parent = (index - 1) // 2
		if compare(heapq, data[index], data[parent]):
			data[index], data[parent] = data[parent], data[index]
			index = parent
		else:
			break

def heapq_pop(heapq):
	data = heapq["tree"]
	if not data:
		return None
	if len(data) == 1:
		heapq["membership"][heapq_get_best(heapq)] -= 1
		return data.pop()
	
	removed_val = data[0]
	data[0] = data.pop()
	_bubble_down(heapq, 0, data)
	
	heapq["membership"][removed_val] -= 1
	
	return removed_val
	
def heapq_get_best(heapq):
	data = heapq["tree"]
	if not data:
		return None
	return data[0]

def _bubble_down(heapq, index, data):
	#start_tick_count = get_tick_count()

	compare = heapq["compare"]
	length = len(data)
	
	while True:
		best = index
		left = 2 * index + 1
		right = 2 * index + 2
		
		if left < length and compare(heapq, data[left], data[best]):
			best = left
		if right < length and compare(heapq, data[right], data[best]):
			best = right
			
		if best != index:
			data[index], data[best] = data[best], data[index]
			index = best
		else:
			break
			
	#end_tick_count = get_tick_count()
	#took_ticks = end_tick_count - start_tick_count
	#quick_print("pop:", took_ticks)
			
def heapq_contains(heapq, value):
	if not value in heapq["membership"]:
		return False
	return heapq["membership"][value] > 0
