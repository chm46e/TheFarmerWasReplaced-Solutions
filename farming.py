# Abstract entire farming mechanic to farm(Entities.crop)

from utils import random_element

# Turn most plants into infected, gives Weird Substance
FERTILIZE_ALL = False

def farm_grass():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)

def farm_bush():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)	

def farm_carrot():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Carrot:
		if (num_items(Items.Hay) > 0
			and num_items(Items.Wood) > 0):
			plant(Entities.Carrot)
	if num_items(Items.Water) > 0:
		if get_water() == 0:
			use_item(Items.Water, 3)
		elif get_water() <= 0.5:
			use_item(Items.Water, 1)
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)
				
def farm_tree():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	if get_entity_type() != Entities.Tree:
		plant(Entities.Tree)
	if num_items(Items.Water) > 0:
		if get_water() == 0:
			use_item(Items.Water, 3)
		elif get_water() <= 0.5:
			use_item(Items.Water, 1)
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)	

def farm_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() == Entities.Dead_Pumpkin:
		plant(Entities.Pumpkin)
	if get_entity_type() != Entities.Pumpkin:
		plant(Entities.Pumpkin)
	if num_items(Items.Water) > 0:
		if get_water() == 0:
			use_item(Items.Water, 3)
		elif get_water() <= 0.5:
			use_item(Items.Water, 1)
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)	

# Decides, when to harvest pumpkin
# Entire row of length must be filled with pumpkins.
#
# return:  -1 for invalid row,
# 			1 to (length - 1) counter,
# 			length, when all good to harvest
def decide_pumpkin_harvest(types, counter, first_measure, length):
	if types[0] == Entities.Pumpkin and counter != -1:
		if measure() == first_measure:
			counter += 1
		else:
			return -1 # nope
	else:
		return -1 # nope
			
	if counter == length:
		if can_harvest():
			return counter
		return -1 # counting went wrong
	else:
		return counter
	
def _farm_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	if can_harvest():
		harvest()
	if get_entity_type() != Entities.Sunflower:
		plant(Entities.Sunflower)
	if num_items(Items.Water) > 0:
		if get_water() == 0:
			use_item(Items.Water, 3)
		elif get_water() <= 0.5:
			use_item(Items.Water, 1)
	
		
def _farm_cactus():
	if get_ground_type() != Grounds.Soil:
		till()
	if get_entity_type() != Entities.Cactus:
		plant(Entities.Cactus)
	if FERTILIZE_ALL:
		use_item(Items.Fertilizer)	

# Deal with farming the given type of plant under the drone.
# type : from Entities
def farm(type):
	if type == Entities.Grass:
		farm_grass()
	elif type == Entities.Bush:
		farm_bush()
	elif type == Entities.Carrot:
		farm_carrot()
	elif type == Entities.Tree:
		farm_tree()
	elif type == Entities.Pumpkin:
		farm_pumpkin()
	elif type == Entities.Sunflower:
		_farm_sunflower()
	elif type == Entities.Cactus:
		_farm_cactus()

# Give it an entities list and it will pick a random element to farm under the drone.
def farm_random_from_list(entities):
	farm(random_element(entities))
