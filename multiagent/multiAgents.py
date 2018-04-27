# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print newScaredTimes
        
        "*** YOUR CODE HERE ***"
        
        currentFood=currentGameState.getFood()
        listOfFoodCoord=currentFood.asList()
        
        maxNum=float('inf')
        foodScore=0
        
        # Calculate the minimum food Distance from new position
        listOfDist=[]
        for foodPos in listOfFoodCoord:
            listOfDist+=[manhattanDistance(newPos,foodPos)]
        minDistFromFood=min(listOfDist)
        if (minDistFromFood!=0 ):
            foodScore = -1*minDistFromFood
            
        ghostScore=0
        
        # Calculate the ghost distance from new position
        for ghostState in newGhostStates:
            dist=manhattanDistance(newPos, ghostState.getPosition())
            if dist<1:
                ghostScore-= maxNum

    
        actionScore=0
        
        # If new action is Stop
        if action==Directions.STOP:
            actionScore = -10
            

        
        powerFoodScore=0     
        
        # Calculate distance from power food
        distFromPowerFood=[]
        for powerFood in successorGameState.getCapsules():
            distFromPowerFood+=[manhattanDistance(newPos, powerFood)]
        if len(distFromPowerFood) > 0:
            minDistFromPowerFood=min(distFromPowerFood)
            if minDistFromPowerFood==0:
                powerFoodScore=maxNum
            else:
                powerFoodScore=1/minDistFromPowerFood
             
            
        return powerFoodScore+actionScore+ghostScore+foodScore+currentGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        noOfAgents=gameState.getNumAgents()
        # actions for max agent
        maxActions=[]
        
        def value(state,agentNum):
            if state.isWin() or state.isLose() or agentNum>=noOfAgents*self.depth:
                return self.evaluationFunction(state)    
            if agentNum%noOfAgents==0:
                return maxValue(state,agentNum)
            else:
                return minValue(state,agentNum)
        
        # Agent : Ghosts    
        def minValue(state,agentNum):
            val=float('inf')
            currAgent=agentNum%noOfAgents
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                val=min(val,value(successorState,agentNum+1))
            return val
        
        # Agent : Pacman
        def maxValue(state,agentNum):
            val=-1*float('inf')
            currAgent=agentNum%noOfAgents
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                val=max(val,value(successorState,agentNum+1))
                if agentNum==0:
                    maxActions.append((val,actions)) 
            return val
        
        # method call to value fn    
        value(gameState,0)
        maxVal=-1*float('inf')
        resultAction=''
        # calculate the action with maximum value
        for actVal in  maxActions:
            v,a=actVal
            if v > maxVal:
                resultAction=a
                maxVal=v
        
        return resultAction
        
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        noOfAgents=gameState.getNumAgents()
        # actions for max agent
        maxActions=[]
        
        def value(state,agentNum,alpha,beta):
            if state.isWin() or state.isLose() or agentNum>=noOfAgents*self.depth:
                return self.evaluationFunction(state)    
            if agentNum%noOfAgents==0:
                return maxValue(state,agentNum,alpha,beta)
            else:
                return minValue(state,agentNum,alpha,beta)
        
        # Agent : Ghosts    
        def minValue(state,agentNum,alpha,beta):
            val=float('inf')
            currAgent=agentNum%noOfAgents
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                val=min(val,value(successorState,agentNum+1,alpha,beta))
                if val < alpha:
                    return val
                beta=min(beta,val)
            return val
        
        # Agent : Pacman
        def maxValue(state,agentNum,alpha,beta):
            val=-1*float('inf')
            currAgent=agentNum%noOfAgents
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                val=max(val,value(successorState,agentNum+1,alpha,beta))
                if val > beta:
                    return val
                alpha=max(alpha,val)
                if agentNum==0:
                    maxActions.append((val,actions)) 
            return val
        inf=float('inf') 
        # method call to value fn ( alpha as -ve inifinty and beta as +ve infinity)   
        print(value(gameState,0,-1*inf,inf))
        maxVal=-1*float('inf')
        resultAction=''
        # calculate the action with maximum value
        for actVal in  maxActions:
            v,a=actVal
            if v > maxVal:
                resultAction=a
                maxVal=v
        print resultAction
        
        return resultAction
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        # number of agents
        noOfAgents=gameState.getNumAgents()
        # actions for max agent
        maxActions=[]
        
        def value(state,agentNum):
            if state.isWin() or state.isLose() or agentNum>=noOfAgents*self.depth:
                return self.evaluationFunction(state)    
            if agentNum%noOfAgents==0:
                return maxValue(state,agentNum)
            else:
                return expValue(state,agentNum)
        
        # Agent : Ghosts   
        def expValue(state,agentNum):
            currAgent=agentNum%noOfAgents
            val=0
            noOfActions=len(state.getLegalActions(currAgent))
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    noOfActions-=1
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                # probable values
                val+=value(successorState,agentNum+1)/float(noOfActions)
            return val
        
        # Agent : Pacman 
        def maxValue(state,agentNum):
            val=-1*float('inf')
            currAgent=agentNum%noOfAgents
            for actions in state.getLegalActions(currAgent):
                if actions==Directions.STOP:
                    continue
                successorState=state.generateSuccessor(currAgent,actions)
                val=max(val,value(successorState,agentNum+1))
                if agentNum==0:
                    maxActions.append((val,actions)) 
            return val
        
        # method call to value fn    
        value(gameState,0)
        maxVal=-1*float('inf')
        resultAction=''
        # calculate the action with maximum value
        for actVal in  maxActions:
            v,a=actVal
            if v > maxVal:
                resultAction=a
                maxVal=v
        
        return resultAction
        
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
        
    currentFood=currentGameState.getFood()
    currentPos=currentGameState.getPacmanPosition()
    listOfGhostStates=currentGameState.getGhostStates()
    listOfFoodCoord=currentFood.asList()
    distFoodScore=0
    distGhostScore=0
    distPowerFoodScore=0
            
    # Calculate the max of reciprocal of food Distance from current position
    listOfFoodDist=[]
    for foodPos in listOfFoodCoord:
        listOfFoodDist+=[1.0/float(manhattanDistance(currentPos,foodPos))]
    if len(listOfFoodDist)>0:
        distFoodScore=max(listOfFoodDist)
           
    
    # Calculate the minimum ghost distance from current position
     
    listOfGhostDist=[]
    for ghostState in listOfGhostStates:
        listOfGhostDist+=[(manhattanDistance(currentPos, ghostState.getPosition()),ghostState.scaredTimer)]   
    for items in listOfGhostDist:
        dist,scaredTime=items
        if dist!=0:
            if scaredTime>0:
                distGhostScore+=(1.0/dist)*10
            else:
                distGhostScore-=(1.0/dist)*10
    
    
               
    # Calculate distance from power food
    distFromPowerFood=[]
    for powerFood in currentGameState.getCapsules():
        distFromPowerFood+=[(1.0/float(manhattanDistance(currentPos, powerFood)))]
    if len(distFromPowerFood) > 0:
        distPowerFoodScore=max(distFromPowerFood)
    
    
            
    return distFoodScore+distPowerFoodScore+distGhostScore+currentGameState.getScore()
    

# Abbreviation
better = betterEvaluationFunction

