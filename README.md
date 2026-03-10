<img width="460" height="215" alt="TFWR game banner" src="https://github.com/user-attachments/assets/e77f183e-a371-49af-9a7b-c82b5f72f7eb" />

# The Farmer Was Replaced solutions
In The Farmer Was Replaced (TFWR), the challenge is to program an autonomous drone to manage a farm using quite a restricted Python environment.

In my opinion, the limitations of the game's coding environment is what makes the solutions interesting and abnormal.
Sometimes the optimizations that should be made in this game, wouldn't ever make sense nor optimize anything in the real world, which is
mostly thanks to the way the program environment handles timing and ticks.

Naturally, my approach was to immediately abstract all low-level drone functions to more readable and manageable higher-level ones. Most of my time in this game was spent on trying to
optimize and code a good dinosaur (snake) game solution. Usually, the A* pathfinding algorithm works wonders, but in this game, heavy array access is severely punished. After many days of trying
different approaches, I came to the right conclusion that the hamiltonian path with shortcuts is surprisingly the fastest method. I also spent quite a bit of time tick-optimizing code, but
there are still many clever optimizations to be made.

I wouldn't recommend copy-pasting my solutions, but to rather find your own ways, because that's what makes the game interesting.

## Lessons learned
* The most common best solution to a problem isn't always the best one.
* Abstracting code helps a lot, but may cause bad performance.
* Always code with the documentation open.

## Repository structure

* Abstractions:
  * ```farming.py``` - Abstract the farming mechanics to a single function: ```farm(Entities.Carrot)```
  * ```movement.py``` - Abstract drones' movement to a manageable ```farm_rectangle(types, bottom_left, top_right, ...)```
  * ```utils.py``` - All kinds of helpful utilities from randint to function benchmarking.
* Algorithm/data structure implementations:
  * ```a_star.py``` - Implement the A* pathfinding algorithm. (pretty useless in this game)
  * ```deque.py``` - Implement a double-ended queue. (useful, but remains too slow for good leaderboard times)
  * ```heap_queue.py``` - Implement a priority queue. (works, but too slow)
* Snake game attempts:
  * ```dino_hyper_hamiltons.py``` - Use a hamiltonian path with shortcuts to beat the snake game. The best approach, but needs to be optimized methodically to get a good leaderboard time.
  * ```attempt_dino_astar.py``` - Attempt at using the A* pathfinding algorithm to beat the snake game. Way too slow, the game punishes array access a lot.
  * ```attempt_dino_floodfl.py``` - Attempt at using floodfill to go greedy, but not trap the snake, but also too slow.
* Important implementations:
  * ```polyculture.py``` - Use the game's polyculture mechanic to multiply yields.
  * ```maze_normal.py``` - Solve mazes.
  * ```grind_cacti.py``` - Sort a field of cacti.
  * ```grind_crop.py``` - Plant and harvest the entire field with a crop.
