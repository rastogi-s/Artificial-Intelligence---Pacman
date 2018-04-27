# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from multiprocessing import active_children


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    #stack used as frontier
    stack=util.Stack()
    stack.push(problem.getStartState())
    path={problem.getStartState():[]}
    visited_nodes=[]
    
    # loop till stack is empty 
    while not stack.isEmpty():
        parent=stack.pop()
        dist=path[parent]
        visited_nodes+=[parent]
        
        # check if the current state is goal state.
        if problem.isGoalState(parent):
            return dist
        
        for child in problem.getSuccessors(parent):
            child_coord=child[0] # coordinates for the child node.
            child_action=child[1] # direction for the child node.
            
            # check if the child state is already visited.
            if child_coord not in visited_nodes:
                stack.push(child_coord)
                path[child_coord]=dist+[child_action]
                
    return dist
    
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    #queue used as frontier
    queue=util.Queue()
    path={problem.getStartState():[]}
    queue.push(problem.getStartState())
    visited_nodes=[problem.getStartState()]
    
    while not queue.isEmpty():
        parent=queue.pop()
        dist=path[parent]
        
        # check if the current state is goal state.
        if problem.isGoalState(parent):
            return dist
        
        for child in problem.getSuccessors(parent):
            child_coord=child[0] # coordinates for the child node.
            child_action=child[1] # direction for the child node.
            
            # check if the child state is already visited.
            if child_coord not in visited_nodes:
                queue.push(child_coord)
                visited_nodes+=[child_coord]
                path[child_coord]=dist+[child_action]

    return dist

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    #priority queue used as frontier
    queue=util.PriorityQueue()
    firstNode=problem.getStartState()
    cost=0
    path={firstNode:([],cost)}
    queue.push(firstNode,cost)
    visited_nodes=[]
    
    # loop till the queue is empty
    while not queue.isEmpty():
        parent=queue.pop()
        dist,cost=path[parent]
        #print(cost)
        # check if the current state is goal state.
        if problem.isGoalState(parent):
            return dist
           
        # check if the parent state is already visited.   
        if parent not in visited_nodes:
            visited_nodes+=[parent]
        else:
            continue
        
        for child in problem.getSuccessors(parent):
            child_coord,child_action,child_cost=child  
            # total cost including the cost of path from start state
            # to the current state.
            total_cost=cost+child_cost
            # check if the child state is already visited.  
            if child_coord not in visited_nodes:
                if child_coord in path:
                    oldCost=path[child_coord][1]
                    if oldCost > total_cost:
                        path[child_coord]=(dist+[child_action],total_cost)
                        queue.update(child_coord,total_cost)
                else:
                    path[child_coord]=(dist+[child_action],total_cost)
                    queue.push(child_coord,total_cost)
                  
                
    return dist    
    
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    
    #priority queue used as frontier
    queue=util.PriorityQueue()
    
    firstNode=problem.getStartState()
    cost=0
    path={firstNode:([],cost)}
    queue.push(firstNode,cost+heuristic(firstNode,problem))
    visited_nodes=[]
    # loop till the queue is empty
    while not queue.isEmpty():
        parent=queue.pop()
        dist,cost=path[parent]
        
        # check if the current state is goal state.
        if problem.isGoalState(parent):
            return dist
        
        # check if the parent state is already visited.      
        if parent not in visited_nodes:
            visited_nodes+=[parent]
        else:
            continue
        
        for child in problem.getSuccessors(parent):
            child_coord,child_action,child_cost=child
            # total cost including heuristic.  
            total_cost=cost+child_cost+heuristic(child_coord,problem)
            
            if child_coord not in visited_nodes:
                if child_coord in path:
                    oldCost=path[child_coord][1]
                    if oldCost > total_cost:
                        path[child_coord]=(dist+[child_action],cost+child_cost)
                        queue.update(child_coord,total_cost)
                else:
                    path[child_coord]=(dist+[child_action],cost+child_cost)
                    queue.push(child_coord,total_cost)
            
    return dist   
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
