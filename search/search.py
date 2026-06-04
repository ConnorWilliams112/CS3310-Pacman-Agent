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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from queue import PriorityQueue

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

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        children = []
        for successor, action, stepCost in problem.getSuccessors(self.state):
            new_cost = self.path_cost + stepCost
            child_node = Node(successor, self, action, new_cost)
            children.append(child_node)
        return children

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal.

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    start_state = problem.getStartState()
    frontier.push((start_state, []))
    explored = set()
    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions
        if state not in explored:
            explored.add(state)
            for child in problem.getSuccessors(state):
                if child[0] not in explored:
                    frontier.push((child[0], actions + [child[1]]))
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    start_state = problem.getStartState()
    frontier.push((start_state, []))
    explored = set()
    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state not in explored:
            explored.add(state)
            for child in problem.getSuccessors(state):
                successor_state = child[0]
                successor_action = child[1]
                if successor_state not in explored:
                    frontier.push((successor_state, actions + [successor_action]))
    return None 

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # To do this i started with BFS code becuase it is very similiary in the fact that it is on a queue
    frontier = util.PriorityQueue()            
    start_state = problem.getStartState()  
    start_item = (start_state, [], 0)
    start_priority = 0
    frontier.push((start_state,[]), start_priority)
    explored = set()                     
    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if problem.isGoalState(state):
            return actions
        if state not in explored:
            explored.add(state)
            for child in problem.getSuccessors(state):           
                successor_state = child[0]                       
                successor_action = child[1]                     
                if successor_state not in explored:   
                    next_actions = actions + [successor_action]
                    item = (successor_state, next_actions)
                    priority = problem.getCostOfActions(next_actions)
                    frontier.update(item, priority)
    return None 


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = PriorityQueue()
    explored = set()
    
    initial_node = Node(problem.getStartState())
    frontier.put((heuristic(initial_node.state, problem), initial_node))
    
    while not frontier.empty():
        priority, node = frontier.get()
        if problem.isGoalState(node.state):
            return node.solution()
        if node.state not in explored:
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored:
                    f = child.path_cost + heuristic(child.state, problem)
                    frontier.put((f, child))
    return []

def h1(state, problem):

    x1, y1 = state
    x2, y2 = problem.goal

    if not hasattr(problem, "walls"):
        return abs(x1 - x2) + abs(y1 - y2)

    walls = problem.walls
    manhattan = abs(x1 - x2) + abs(y1 - y2)

    def pathIsClear(horizontalFirst):
        x, y = state

        if horizontalFirst:
            while x != x2:
                x += 1 if x2 > x else -1
                if walls[x][y]:
                    return False
            while y != y2:
                y += 1 if y2 > y else -1
                if walls[x][y]:
                    return False
        else:
            while y != y2:
                y += 1 if y2 > y else -1
                if walls[x][y]:
                    return False
            while x != x2:
                x += 1 if x2 > x else -1
                if walls[x][y]:
                    return False

        return True

    wallPenalty = 0
    if not pathIsClear(True) and not pathIsClear(False):
        wallPenalty = 2

    return manhattan + wallPenalty

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
