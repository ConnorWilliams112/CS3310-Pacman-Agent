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
from pacman import GameState

#Reflex agent ONLY uses current game state. No searching multiple moves ahead.
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        score = successorGameState.getScore()

        # penalize for stopping
        if action == Directions.STOP:
            score -= 10

        # reward for being close to food
        foodList = newFood.asList()
        if foodList:
            closestFood = min(manhattanDistance(newPos, food) for food in foodList)
            score += 10 / max(closestFood, 1)

        # reward / penalty based on ghost state
        for i in range(len(newGhostStates)):
            ghostState = newGhostStates[i]
            scaredTime = newScaredTimes[i]

            ghostPos = ghostState.getPosition()
            ghostDist = manhattanDistance(newPos, ghostPos)

            # if ghost is scared, add points. More points for being closer to ghost (max(ghostDist,1))
            if scaredTime > 0:
                score += 20 / max(ghostDist, 1)

            # ghost is not scared, subtract points for being next to it (Dist <=1)
            elif ghostDist <= 1:
                score -= 100

            # ghost is not scared, subtract points the closer you are to it
            else:
                score -= 2 / ghostDist

        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        #Returns action for the top-level call, score for recursive calls
        actions = gameState.getLegalActions(0)
        return max(actions, key=lambda action: self.minimax(gameState.generateSuccessor(0, action), self.depth, 1))
    
    def minimax(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Recursive minimax function that explores the game tree.
        
        Args:
            gameState: The current game state to evaluate
            depth: Current depth in the search tree (decrements to 0)
            agentIndex: Index of the agent whose turn it is (0=Pacman, >=1=ghosts)
        
        Returns:
            The minimax value (score) for the current state

        - Check terminal states (win/lose) and depth limit
        - If MAX layer (Pacman's turn):
            - Try all legal actions, recurse with agentIndex+1
            - Return max value and corresponding action
        - If MIN layer (ghost's turn):
            - Try all legal actions, recurse with agentIndex+1 (wrapping around)
            - Return min value
        """
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0: #Pacman's turn (maximizing agent)
            return self.maxValue(gameState, depth, agentIndex)
        else:
            return self.minValue(gameState, depth, agentIndex)
        
    
    def maxValue(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Computes the maximum value achievable for Pacman (maximizing agent).
        Called when it's Pacman's turn (agentIndex == 0).
        
        Args:
            gameState: The current game state
            depth: Current depth in the search tree
            agentIndex: Should be 0 (Pacman)
        
        Returns:
            The maximum score Pacman can achieve from this state
        """
        numAgents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        maxScore = float('-inf')
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            score = self.minimax(successor, nextDepth, nextAgent)
            maxScore = max(maxScore, score)
        return maxScore

    
    def minValue(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Computes the minimum value (from Pacman's perspective) achievable by ghosts (minimizing agents).
        Called when it's a ghost's turn (agentIndex >= 1).
        
        Args:
            gameState: The current game state
            depth: Current depth in the search tree
            agentIndex: Index of the ghost (1, 2, 3, ...)
        
        Returns:
            The minimum score (best for ghosts, worst for Pacman) from this state
        """
        numAgents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        minScore = float('inf')
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            score = self.minimax(successor, nextDepth, nextAgent)
            minScore = min(minScore, score)
        return minScore
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #Returns action for the top-level call, score for recursive calls
        actions = gameState.getLegalActions(0)
        return max(actions, key=lambda action: self.expectimax(gameState.generateSuccessor(0, action), self.depth, 1)) # Genmini 3.1 Pro helped me debug this line as I was calling something wrong in another class
    
    def expectimax(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Recursive expectimax function that explores the game tree with expected values for ghosts.
        
        Args:
            gameState: The current game state to evaluate
            depth: Current depth in the search tree (decrements to 0)
            agentIndex: Index of the agent whose turn it is (0=Pacman, >=1=ghosts)
        
        Returns:
            The expectimax value (expected score) for the current state
        """
        "*** YOUR CODE HERE ***"
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0: #Pacman's turn ( Now its expectimax instead of just max)
            return self.maxValue(gameState, depth, agentIndex)  # I had a bug here Gemeni 3.1 AI helped me fix it 
        else:
            return self.expectValue(gameState, depth, agentIndex)
    
    def maxValue(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Computes the maximum value achievable for Pacman (maximizing agent).
        Called when it's Pacman's turn (agentIndex == 0).
        
        Args:
            gameState: The current game state
            depth: Current depth in the search tree
            agentIndex: Should be 0 (Pacman)
        
        Returns:
            The maximum score Pacman can achieve from this state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        maxScore = float('-inf')
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            score = self.expectimax(successor, nextDepth, nextAgent)
            maxScore = max(maxScore, score)
        return maxScore
    
    def expectValue(self, gameState: GameState, depth: int, agentIndex: int):
        """
        Computes the expected value when ghosts choose uniformly at random (minimizing agents).
        Called when it's a ghost's turn (agentIndex >= 1).
        
        Args:
            gameState: The current game state
            depth: Current depth in the search tree
            agentIndex: Index of the ghost (1, 2, 3, ...)
        
        Returns:
            The expected score (average of all possible ghost moves) from this state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        actions = gameState.getLegalActions(agentIndex)
        expectScore = 0 # AI Gemeni 3.1 Pro helped me debug this line. I had float and it was causing error. 
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth - 1 if nextAgent == 0 else depth
            expectScore += self.expectimax(successor, nextDepth, nextAgent) #Gemeni 3.1 Pro AI helped me figure out the + sign on this line
        return expectScore / len(actions)    ##Gemeni 3.1 Pro AI helped me figure out the divide by len(actions)
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        actions = gameState.getLegalActions(0)

        bestAction = None
        bestScore = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            score = self.alphabeta(successor, self.depth, 1, alpha, beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            alpha = max(alpha, bestScore)

        return bestAction

    def alphabeta(self, gameState, depth, agentIndex, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.minValue(gameState, depth, agentIndex, alpha, beta)

    def maxValue(self, gameState, depth, agentIndex, alpha, beta):

        value = float("-inf")

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                nextDepth = depth -1
            else:
                nextDepth = depth

            value = max(value, self.alphabeta(successor, nextDepth, nextAgent, alpha, beta))

            if value > beta:
                return value

            alpha = max(alpha, value)

        return value

    def minValue(self, gameState, depth, agentIndex, alpha, beta):

        value = float("inf")

        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action)

            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            if nextAgent == 0:
                nextDepth = depth -1
            else:
                nextDepth = depth

            value = min(value, self.alphabeta(successor, nextDepth, nextAgent, alpha, beta))

            if value < alpha:
                return value

            beta = min(beta, value)

        return value


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: First just used the previous evaluation function 
    and changed the actions to state problem. I got Help from Gemini Pro 3.1 to help with the transistion from the Action problem to state problem.
    At first I just wanted to incentive food. Then I messed with Ghosts and tunning those values. I realized there is almost alwasys time to eat the Ghost and a big
    factor in determining score so there needs to be an incentive to eating the power capsule and then eating the scared Ghosts """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsules = currentGameState.getCapsules() # AI Gemeni 3.1 Pro helped me realize that this could be used to tune since they are worth more points

    score = currentGameState.getScore()

    # reward for being close to food
    foodList = newFood.asList()
    if foodList:
        closestFood = min(manhattanDistance(newPos, food) for food in foodList) # This autofilled in with my AI Claude that I had in my browser. I messed with tuning values
        score += 10 / max(closestFood, 1) # This autofilled in with my AI Claude that I had in my VS. I messed with tuning values
        score += -0.5 * len(foodList) # This autofilled in with my AI Claude that I had in my VS I messed with tuning values. I messed with tuning values
    
    if capsules:
        closestCapsule = min(manhattanDistance(newPos, capsule) for capsule in capsules)
        score += 10 / (max(closestCapsule, 1)+1)
        score += -5 * len(capsules)


    # reward / penalty based on ghost state
    for i in range(len(newGhostStates)):
        ghostState = newGhostStates[i]
        scaredTime = newScaredTimes[i]

        ghostPos = ghostState.getPosition()
        ghostDist = manhattanDistance(newPos, ghostPos)

        # if ghost is scared, add points. More points for being closer to ghost (max(ghostDist,1))
        if scaredTime > 0 and scaredTime > ghostDist-1:
            score += 200 / max(ghostDist, 1)

        # ghost is not scared, subtract points for being next to it (Dist <=1)
        elif ghostDist <= 1:
            score -= 1000

        # ghost is not scared, subtract points the closer you are to it
        else:
            score -= 1 / ghostDist
    return score    

        
    
# Abbreviation
better = betterEvaluationFunction