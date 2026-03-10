# Use the plant companion/polyculture system to have much greater returns on harvest.

from farming import farm, farm_random_from_list
from movement import move_to_pos, move_to_any_open, move_to_random_position
from utils import randint

#COMPANION_TYPES = [Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot]
COMPANION_TYPES = [Entities.Bush, Entities.Tree]

def farm_polyculture():
	harvestables = []
	move_to_random_position()
	farm_random_from_list(COMPANION_TYPES)
	
	for _ in range(30):
		harvestables.append((get_pos_x(), get_pos_y()))
		
		companion = get_companion()
		if companion != None:
			companion_type, (companion_x, companion_y) = companion
		else:
			companion_type, (companion_x, companion_y) = (Entities.Grass, (randint(0, 31), randint(0, 31)))
			quick_print("Failed to get companion: going to random")
		
		if (companion_x, companion_y) in harvestables:
			move_to_any_open()
			if can_harvest():
				harvest()
			farm_random_from_list(COMPANION_TYPES)
			continue
			
		move_to_pos(companion_x, companion_y, True)
		
		if get_entity_type() != companion_type:
			if can_harvest():
				harvest()
			farm(companion_type)
			
	for harvestable in harvestables:	
		move_to_pos(harvestable[0], harvestable[1], True)
		harvest()
		farm_random_from_list(COMPANION_TYPES)
