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
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
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

#/*=====Start Change Task 1=====*/

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""

    # states to be explored (LIFO). holds nodes in form (state, action)
    frontier = util.Stack()
    # previously explored states (for path checking), holds states
    exploredNodes = []
    #define start node
    startState = problem.getStartState()
    startNode = (startState, [])
    
    frontier.push(startNode)

    n = 1
    maxFringe = 0
    maxDepth = 0

    while not frontier.isEmpty():

        if (n>=maxFringe):
            maxFringe = n


        #begin exploring last (most-recently-pushed) node on frontier
        currentState, actions = frontier.pop()
        n -= 1

        if(len(actions) > maxDepth):
            maxDepth = len(actions)
        
        if currentState not in exploredNodes:
            if len(actions) < 10:
                #mark current node as explored
                exploredNodes.append(currentState)

                if problem.isGoalState(currentState):
                    return [actions, maxFringe, maxDepth, len(exploredNodes), 1]
                else:
                    #get list of possible successor nodes in
                    #form (successor, action, stepCost)
                    successors = problem.getSuccessors(currentState)

                    #push each successor to frontier
                    for succState, succAction, succCost in successors:
                        newAction = actions + [succAction]
                        newNode = (succState, newAction)
                        frontier.push(newNode)
                        n +=1

    return [actions, maxFringe, maxDepth, len(exploredNodes), 0]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    n = 0
    #to be explored (FIFO)
    frontier = util.Queue()
    
    #previously expanded states (for cycle checking), holds states
    exploredNodes = []
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    frontier.push(startNode)
    n += 1
    maxFringe = 0;
    maxDepth = 0;

    while not frontier.isEmpty():

        if(maxFringe < n):
            maxFringe = n

        #begin exploring first (earliest-pushed) node on frontier
        currentState, actions, currentCost = frontier.pop()
        n -= 1

        if (len(actions) > maxDepth):
            maxDepth = len(actions)

        if currentState not in exploredNodes:
            #put popped node state into explored list
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return [actions, maxFringe, maxDepth, len(exploredNodes)]
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    frontier.push(newNode)
                    n+=1

    return actions
        
def uniformCostSearch(problem):
    """Search the node of least total cost first."""


    #to be explored (FIFO): holds (item, cost)
    frontier = util.PriorityQueue()

    #previously expanded states (for cycle checking), holds state:cost
    exploredNodes = {}
    
    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)
    
    frontier.push(startNode, 0)

    n = 1
    maxFringe = 0
    maxDepth = 0

    while not frontier.isEmpty():

        if (maxFringe < n):
            maxFringe = n

        #begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost = frontier.pop()
        n -= 1

        if(len(actions) > maxDepth):
            maxDepth = len(actions)

        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            #put popped node's state into explored list
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                return [actions, maxFringe, maxDepth, len(exploredNodes)]
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)

                    frontier.update(newNode, newCost)
                    n += 1

    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    #to be explored (FIFO): takes in item, cost+heuristic
    frontier = util.PriorityQueue()

    exploredNodes = [] #holds (state, cost)

    startState = problem.getStartState()
    startNode = (startState, [], 0) #(state, action, cost)

    frontier.push(startNode, 0)

    n = 1
    maxFringe = 0
    maxDepth = 0

    while not frontier.isEmpty():

        if (maxFringe < n):
            maxFringe = n

        #begin exploring first (lowest-combined (cost+heuristic) ) node on frontier
        currentState, actions, currentCost = frontier.pop()
        n -= 1

        if(len(actions) > maxDepth):
            maxDepth = len(actions)

        #put popped node into explored list
        exploredNodes.append((currentState, currentCost))

        if problem.isGoalState(currentState):
            return [actions, maxFringe, maxDepth, len(exploredNodes)]

        else:
            #list of (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)

            #examine each successor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                newNode = (succState, newAction, newCost)

                #check if this successor has been explored
                already_explored = False
                for explored in exploredNodes:
                    #examine each explored node tuple
                    exploredState, exploredCost = explored

                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True

                #if this successor not explored, put on frontier and explored list
                if not already_explored:
                    frontier.push(newNode, newCost + heuristic(succState, problem))
                    exploredNodes.append((succState, newCost))
                    n += 1

    return actions


def h1test(current_state, glstate):

    count = 0
    for row in range(3):
        for col in range(3):
            if current_state.cells[row][col] == glstate.cells[row][col]:
                count += 1
    return 8-count


def h2test(current_state, glstate):
    total_distance = 0
    # Iterates through each tile
    for row in range(3):
        for col in range(3):
            current_tile = current_state.cells[row][col]
            if current_tile != 0:  # Skip the blank (empty) tile
                # iterates through the goal state to check how far away the current tile is from its proper state
                for goal_row in range(3):
                    for goal_col in range(3):
                        # subs the x and y coordinate of the goal state from the current state and finds the length of
                        # the hypotonuse (sqrt(a^2+b^2) = c)
                        if glstate.cells[goal_row][goal_col] == current_tile:
                            distance = math.sqrt((row - goal_row) ** 2 + (col - goal_col) ** 2)
                            total_distance += distance
    return total_distance


def h3test(current_state, glstate):
    total_distance = 0
    # iterates through each tile
    for row in range(3):
        for col in range(3):
            current_tile = current_state.cells[row][col]
            if current_tile != 0:
                # iterates through the goal state to check how far away the current tile is from its proper state
                for goal_row in range(3):
                    for goal_col in range(3):
                        # if the current tile belongs in the current goal state, the distance from the tile is set as
                        # abs(X(current)-X(goal)) + abs(Y(current)-Y(goal))
                        if glstate.cells[goal_row][goal_col] == current_tile:
                            distance = abs(row - goal_row) + abs(col - goal_col)
                            total_distance += distance
    return total_distance


def h4test(current_state, glstate):
    out_of_row_count = 0
    out_of_col_count = 0

    for row in range(3): # iterates through each tile
        for col in range(3):
            current_tile = current_state.cells[row][col] # sets the current tile
            if current_tile != 0: # Skip the blank (empty) tile
                inrow = 0
                # Iterates though the column again to check if the current tile is in it, if so, adds one to the count
                for c in range(3):
                    if current_tile == glstate.cells[row][c]:
                        inrow = 1
                if inrow == 0:
                    out_of_row_count +=1
                # Iterates though the column again to check if the current tile is in it, if so, adds one to the count
                incol = 0
                for r in range(3):
                    if current_tile == glstate.cells[r][col]:
                        incol = 1
                if incol == 0:
                    out_of_col_count += 1

    return out_of_row_count + out_of_col_count

#*=====End Change Task 1 =====*/

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
