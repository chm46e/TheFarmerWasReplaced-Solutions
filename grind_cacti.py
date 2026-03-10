# Grind a full field of cacti.

from movement import bubble_sort_cacti, farm_row, move_to_pos
from utils import WORLD_SIZE, sleep_ticks

def grind_cacti_rows(root_drone = False):
	if root_drone:
		drone_id = 0
	else:
		drone_id = num_drones() - 1
		
	farm_row([Entities.Cactus], (0, drone_id), WORLD_SIZE)
	bubble_sort_cacti((0, drone_id), (WORLD_SIZE, drone_id))
	
def grind_cacti_columns(root_drone = False):
	if root_drone:
		drone_id = 0
	else:
		drone_id = num_drones() - 1
		
	bubble_sort_cacti((drone_id, 0), (drone_id, WORLD_SIZE))

while True:	
	clear()
	DRONES = []
		
	while num_drones() < max_drones():
		drone = spawn_drone(grind_cacti_rows)
		if not drone:
			break
		DRONES.append(drone)
		sleep_ticks(5)
	
	grind_cacti_rows(True)
	while len(DRONES):
		wait_for(DRONES[-1])
		DRONES.pop(-1)
		
	while num_drones() < max_drones():
		drone = spawn_drone(grind_cacti_columns)
		if not drone:
			break
		DRONES.append(drone)
		sleep_ticks(5)
	
	grind_cacti_columns(True)	
	while len(DRONES):
		wait_for(DRONES[-1])
		DRONES.pop(-1)
		
	move_to_pos(0, 0)
	harvest()
