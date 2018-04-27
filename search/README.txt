*******************************************************************************
*******************************************************************************
********This file contains details about the heuristic for Q6 and Q7.**********
*******************************************************************************
*******************************************************************************

Pacman movement is restricted to only four directions that is : North, South,
East and West.
So if there are no walls in the space then the shortest distance will be the
Manhattan distance between two points.

********************************************************************************

Q6> In CornersProblem the goal state is a state when the pacman has visited
all the four corners in the space.

So one of the suitable heuristic for the problem would be the sum of Manhattan 
distance from the current state to the closest unvisited corner and from that 
corner to the other closest unvisited corner, till it reaches the goal state 
i.e. all corners has been covered.

Since the Manhattan distance is the shortest distance in the space the 
admissibility of the heuristic is automatically established.

Similarly the shortest distance between two states is the Manhattan distance 
between those states,which also proves the consistency of heuristic.

*********************************************************************************

Q7> For the FoodSearchProblem the goal state is a state when the pacman has eaten 
all the food present in the space.

For this problem the heuristic selected is sum of Manhattan distance from
start point to the closest food and the actual distance (maze distance) from that 
food point to the farthest food point.

The combination of Manhattan distance and Maze distance provide an admissible and 
consistent heuristic and the runtime for the calculation of heuristic is balanced 
since calculation of maze distance (actual shortest path ) can be slow based on the 
space given.(i.e. with large no. of walls).

***********************************************************************************

Time spent on the Assignment : 20 hrs.







