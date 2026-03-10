# Example of how I earlier in the playthrough divided the farm into rectangles,
# so I could grow all crops at the same time, but actually it appears to be faster to do one crop at a time.

from movement import (farm_rectangle, farm_square, move_to_pos,
	bubble_sort_cacti, farm_cacti_rectangle)
	
def pumpkin_drone1():
	while True:
		farm_square([Entities.Pumpkin], [0, 0], 11)
		
def pumpkin_drone2():
	while True:
		farm_square([Entities.Pumpkin], [11, 11], 11)		

def cacti_drone():
	while True:
		farm_cacti_rectangle([0, 17], [10, 21])
		
def carrot_drone1():
	while True:
		farm_rectangle([Entities.Carrot], [11, 0], [18, 10])
		
def carrot_drone2():
	move_to_pos(18, 10, True)
	while True:
		farm_rectangle([Entities.Carrot], [11, 0], [18, 10])
		
def tree_drone1():
	while True:
		farm_rectangle([Entities.Tree, Entities.Grass], [0, 11], [10, 16], "checkered")
		
def tree_drone2():
	move_to_pos(10, 11, True)
	while True:
		farm_rectangle([Entities.Tree, Entities.Grass], [0, 11], [10, 16], "checkered")	
		
clear()
spawn_drone(pumpkin_drone1)
spawn_drone(pumpkin_drone2)
spawn_drone(cacti_drone)
spawn_drone(carrot_drone1)
spawn_drone(carrot_drone2)
spawn_drone(tree_drone1)
spawn_drone(tree_drone2)

while True:
	farm_rectangle([Entities.Sunflower], [19, 0], [21, 10])
