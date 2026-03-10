# Grind polyculture with max drones

from polyculture import farm_polyculture

def grind_polyculture():
	while True:
		farm_polyculture()

clear()
for _ in range(max_drones()):
	spawn_drone(grind_polyculture)

grind_polyculture()
