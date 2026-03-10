# Solution to the maze puzzle using recursion.
# Not optimized, but does prioritize getting closer to the treasure.

# The next step should be to use A* to find the treasure path, keep track of MAZE global and memorize shortcuts.
# I assume it thinking for a few seconds and immediately going for the treasure is faster than exploring the whole maze.

from utils import get_opposite_direction, manhattan_distance

VISITED = {}

def solve_maze():
	if get_entity_type() == Entities.Treasure:
		return True
	
	x, y = get_pos_x(), get_pos_y()	
	key = x * 100 + y
	VISITED[key] = True
	
	treasure_x, treasure_y = measure()
	
	directions = [(North, 0, 1), (South, 0, -1), (East, 1, 0), (West, -1, 0)]
	order = [0, 1, 2, 3]
	
	# optimization: bubble sort directions
	for i in range(4):
		for j in range(3 - i):
			dist1 = manhattan_distance([x + directions[order[j]][1], y + directions[order[j]][2]],
				[treasure_x, treasure_y])
			dist2 = manhattan_distance([x + directions[order[j+1]][1], y + directions[order[j+1]][2]],
				[treasure_x, treasure_y])
			if dist1 > dist2:
				temp = order[j]
				order[j] = order[j+1]
				order[j+1] = temp
			
	for i in order:
		next_x, next_y = get_pos_x() + directions[i][1], get_pos_y() + directions[i][2]
		next_key = next_x * 100 + next_y
		
		moveable = can_move(directions[i][0])
		
		if moveable and next_key not in VISITED:
			move(directions[i][0])
			if solve_maze() == True:
				return True
				
			move(get_opposite_direction(directions[i][0]))
	return False
		
def farm_maze():
	global VISITED
	VISITED = {}
	
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	solve_maze()
	if can_harvest():
		harvest()

clear()
while True:
	farm_maze()
	clear()
