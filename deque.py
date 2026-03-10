# A deque implementation using a circular buffer.
# I tick optimized the fast variants of the functions, but the regular ones are slow and safe.
# There are probably some smart ways to tick optimize this further, but I haven't thought/spoiled them to myself yet.
# Don't mix usage of fast (tick optimized) and regular functions for the same deque.

# Create a deque of capacity.
# capacity: int, >0, max size of deque
def deque_create(capacity):
	storage = []
	for _ in range(capacity):
		storage.append(None)
		
	return [storage, {}, 0, 0, 0, capacity, True]
	# 0 - storage
	# 1 - membership
	# 2 - head
	# 3 - tail
	# 4 - size
	# 5 - capacity
	# 6 - firstUse
	#
	#same as this dict, but faster:
	#{
		#"storage": storage,
		#"membership": {},
		#"head": 0,
		#"tail": 0,
		#"size": 0,
		#"capacity": capacity,
		#"firstUse": True
	#}

# Append a value at the head of a deque.
# dq: deque object
# value: any
def deque_append(dq, value):
	storage, membership, head, tail, size, capacity, firstUse = dq
	if not firstUse:
		head = (head + 1) % capacity
		dq[2] = head # increase head
	else:
		dq[6] = False # update firstUse
		
	storage[head] = value # update storage[head]
	dq[4] = size + 1 # increase size
	
	if value in membership:
		membership[value] += 1 # increase membership
	else:
		membership[value] = 1 # set membership

# Append a value at the head of a deque.
# Tick optimized implementation (cuts corners)
# costs: 5 ticks (3 first time)
#
# dq: deque object
# value: any
def deque_append_fast(dq, value):
	storage, _membership, head, tail, _size, capacity, firstUse = dq
	if not firstUse:
		head = (head + 1) % capacity
		dq[2] = head # increase head
	else:
		dq[6] = False # update firstUse
		
	storage[head] = value # update storage[head]

# Pop the left (tail) value off of the deque.
# dq: deque object
def deque_popleft(dq):
	storage, membership, head, tail, size, capacity, firstUse = dq
	if not size:
		return None
	value = storage[tail]
	
	dq[3] = (tail + 1) % capacity # increase tail
	dq[4] = size - 1 # decrease size
	
	membership[value] -= 1
	
	if not size:
		dq[2] = 0
		dq[3] = 0
		dq[6] = True
		dq[1] = {}
	return value

# Pop the left (tail) value off of the deque.
# Tick optimized implementation (cuts corners)
# costs: 4 ticks
#
# dq: deque object
def deque_popleft_fast(dq):
	storage, _membership, head, tail, _size, capacity, firstUse = dq
	dq[3] = (tail + 1) % capacity # increase tail
	return storage[tail]

# Get the value at index in the deque.
# dq: deque object
# index: int, head(0) to tail(-1)
def deque_get(dq, index):
	storage, membership, head, tail, size, capacity, firstUse = dq
	if not size:
		return None
	
	index %= size
	
	real_index = (head - index) % capacity
	return storage[real_index]

# Return the length of the deque.
# Do not use this in conjunction with fast functions.
# dq: deque object
def deque_length(dq):
	storage, membership, head, tail, size, capacity, firstUse = dq
	return size

# Return the length of the deque.
# To be used with fast functions (but it's slower than the normal variant, which is 0 ticks).
# costs: 3 ticks
#
# dq: deque object
def deque_length_fast(dq):
	storage, _membership, head, tail, _size, capacity, firstUse = dq
	return ((head - tail) % capacity) + 1

# Remove a value at index from the deque. Think carefully before using this.
# Very slow, prefer pop or popleft.
# dq: deque object
# index: int, index of deque to remove
def deque_remove(dq, index):
	storage, membership, head, tail, size, capacity, firstUse = dq
	if not size:
		return None
	
	index %= size
	
	removed_val = deque_get(dq, index)
	membership[removed_val] -= 1
	
	# shift elements to fill the gap
	current_logical = index
	while current_logical > 0:
		# The current position gets the value of the one closer to the head
		prev_logical = current_logical - 1
		
		# Convert logical indices to physical storage indices
		curr_physical = (head - current_logical) % capacity
		prev_physical = (head - prev_logical) % capacity
		
		storage[curr_physical] = storage[prev_physical]
		current_logical -= 1
	
	# shifting done, the old head is now redundant
	dq[2] = (head - 1) % capacity
	dq[4] -= 1 # update size
	
	if not size:
		dq[2] = 0
		dq[3] = 0
		dq[6] = True
		dq[1] = {}
	return removed_val

# Check if the deque contains specified value.
# Uses a membership dictionary for this, meaning no fast support.
# dq: deque object
# value: any
def deque_contains(dq, value):
	storage, membership, head, tail, size, capacity, firstUse = dq
	if not value in membership:
		return False
	return membership[value] > 0
