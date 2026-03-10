# Grind a full field of specified crop.

from movement import farm_row
from utils import WORLD_SIZE, sleep_ticks

#CROPS = [Entities.Grass]
#ALGORITHM = "fill"

#CROPS = [Entities.Tree, Entities.Bush]
#ALGORITHM = "checkered"

#CROPS = [Entities.Carrot]
#ALGORITHM = "fill"

CROPS = [Entities.Pumpkin]
ALGORITHM = "fill"

#CROPS = [Entities.Sunflower]
#ALGORITHM = "fill"

ALIGN_DRONES = True

def grind_crop(root_drone = False):
	if root_drone:
		drone_id = 0
	else:
		drone_id = num_drones() - 1
		
	if ALIGN_DRONES:	
		# make pattern more beautiful
		while num_drones() < max_drones():
			pass
		
	while True:
		farm_row(CROPS, (0, drone_id), WORLD_SIZE,
			ALGORITHM)

clear()
while spawn_drone(grind_crop):
	sleep_ticks(5)
grind_crop(True)
