# eightpuzzle.py
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


import search
import random
import statistics
import automate
# Module Classes

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):

        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range( 3 ):
            self.cells.append( [] )
            for col in range( 3 ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the eight puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in EIGHT_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print loadEightPuzzle(0)
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.

    """
    puzzle = EightPuzzleState([0,1,2,3,4,5,6,7,8])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

#/*=====Start Change Task 2 and 3=====*/
def heuristicTests(pzl, glstate):

    #prints out the hueristics
    h1 = search.h1test(pzl, glstate)
    print("h1: " + str(h1))

    h2 = search.h2test(pzl, glstate)
    print("h2: " + str(h2))

    h3 = search.h3test(pzl, glstate)
    print("h3: " + str(h3))

    h4 = search.h4test(pzl, glstate)
    print("h4: " + str(h4))
    print()

    return


if __name__ == '__main__':

    goal_state = EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8])

    h1_values_Astar = []
    h2_values_Astar = []
    h3_values_Astar = []
    h4_values_Astar = []
    h3_values = []

    path_lengths_Astar = []
    path_lengths_bfs = []
    path_lengths_dfs = []
    path_lengths_ucs = []

    AstarMaxFringes = []
    bfsMaxFringes = []
    dfsMaxFringes = []
    ucsMaxFringes = []

    AstarMaxDepths = []
    bfsMaxDepths = []
    dfsMaxDepths = []
    ucsMaxDepths = []

    AstarExploredNodes = []
    bfsExploredNodes = []
    dfsExploredNodes = []
    ucsExploredNodes = []

    n = 0
    num = 100
    num_moves = 20
    # creates n amount of puzzles and appends the h1 to 4 values to the lists

    while n <  num:

        puzzle = createRandomEightPuzzle(num_moves)
        problem = EightPuzzleSearchProblem(puzzle)

        path_Astar = search.aStarSearch(problem)
        path_lengths_Astar.append(len(path_Astar[0]))
        AstarMaxFringes.append(path_Astar[1])
        AstarMaxDepths.append(path_Astar[2])
        AstarExploredNodes.append(path_Astar[3])

        h1_values_Astar.append(search.h1test(puzzle, goal_state) - len(path_Astar))
        h2_values_Astar.append(search.h2test(puzzle, goal_state) - len(path_Astar))
        h3_values_Astar.append(search.h3test(puzzle, goal_state) - len(path_Astar))
        h4_values_Astar.append(search.h4test(puzzle, goal_state) - len(path_Astar))

        h3_values.append(search.h3test(puzzle, goal_state))

        path_bfs = search.breadthFirstSearch(problem)
        path_lengths_bfs.append(len(path_bfs[0]))
        bfsMaxFringes.append(path_bfs[1])
        bfsMaxDepths.append(path_bfs[2])
        bfsExploredNodes.append(path_bfs[3])


        path_dfs = search.depthFirstSearch(problem)
        if (path_dfs[4] == 1):
            path_lengths_dfs.append(len(path_dfs[0]))
            dfsMaxFringes.append(path_dfs[1])
            dfsMaxDepths.append(path_dfs[2])
            dfsExploredNodes.append(path_dfs[3])

        path_ucs = search.uniformCostSearch(problem)
        path_lengths_ucs.append(len(path_ucs[0]))
        ucsMaxFringes.append(path_ucs[1])
        ucsMaxDepths.append(path_ucs[2])
        ucsExploredNodes.append(path_ucs[3])



        n += 1

    # Calculate the average absolute differences
    avg_diff_h1_Astar = statistics.mean(h1_values_Astar)
    avg_diff_h2_Astar = statistics.mean(h2_values_Astar)
    avg_diff_h3_Astar = statistics.mean(h3_values_Astar)
    avg_diff_h4_Astar = statistics.mean(h4_values_Astar)

    avg_h3 = statistics.mean(h3_values)
    avg_Astar = statistics.mean(path_lengths_Astar)
    avg_bfs = statistics.mean(path_lengths_bfs)
    avg_dfs = statistics.mean(path_lengths_dfs)
    avg_ucs = statistics.mean(path_lengths_ucs)

    astarAvgMaxFringe = statistics.mean(AstarMaxFringes)
    bfsAvgMaxFringe = statistics.mean(bfsMaxFringes)
    dfsAvgMaxFringe = statistics.mean(dfsMaxFringes)
    ucsAvgMaxFringe = statistics.mean(ucsMaxFringes)

    astarAvgMaxDepth = statistics.mean(AstarMaxDepths)
    bfsAvgMaxDepth = statistics.mean(bfsMaxDepths)
    dfsAvgMaxDepth = statistics.mean(dfsMaxDepths)
    ucsAvgMaxDepth = statistics.mean(ucsMaxDepths)

    astarAvgExploredNodes = statistics.mean(AstarExploredNodes)
    bfsAvgExploredNodes= statistics.mean(bfsExploredNodes)
    dfsAvgExploredNodes = statistics.mean(dfsExploredNodes)
    ucsAvgExploredNodes = statistics.mean(ucsExploredNodes)

    # prints the average absolute differences of h1 to h4
    print()
    print("average absolute difference of heuristics from A* path length using " + str(num) + " puzzles with " + str(
        num_moves) + " random moves")
    print("------------------------------------------------------------")
    print("h1: " + str(abs(avg_diff_h1_Astar)))
    print("h2: " + str(abs(avg_diff_h2_Astar)))
    print("h3: " + str(abs(avg_diff_h3_Astar)))
    print("h4: " + str(abs(avg_diff_h4_Astar)))
    print()

    print("Average maximum size of the fringe for each search algorithm using " + str(num) + " puzzles with " + str(
        num_moves) + " random moves")
    print("------------------------------------------------------------")
    print("A Star: " + str(astarAvgMaxFringe))
    print("Breadth First Search: " + str(bfsAvgMaxFringe))
    print("Depth First Search: " + str(dfsAvgMaxFringe))
    print("Uniform Cost Search: " + str(ucsAvgMaxFringe))
    print()

    print("Average maximum depth for each search algorithm using " + str(num) + " puzzles with " + str(
        num_moves) + " random moves")
    print("------------------------------------------------------------")
    print("A Star: " + str(astarAvgMaxDepth))
    print("Breadth First Search: " + str(bfsAvgMaxDepth))
    print("Depth First Search: " + str(dfsAvgMaxDepth))
    print("Uniform Cost Search: " + str(ucsAvgMaxDepth))
    print()

    print("Average number of expanded nodes for each search algorithm using " + str(num) + " puzzles with " + str(
        num_moves) + " random moves")
    print("------------------------------------------------------------")
    print("A Star: " + str(astarAvgExploredNodes))
    print("Breadth First Search: " + str(bfsAvgExploredNodes))
    print("Depth First Search: " + str(dfsAvgExploredNodes))
    print("Uniform Cost Search: " + str(ucsAvgExploredNodes))
    print()

    print("Average path length for h3 and each algorithm using  " + str(num) + " puzzles with " + str(
        num_moves) + " random moves")
    print("------------------------------------------------------------")
    print("h3: " + str(avg_h3))
    print("A Star: " + str(avg_Astar))
    print("Breadth First Search: " + str(avg_bfs))
    print("Depth First Search: " + str(avg_dfs))
    print("Uniform Cost Search: " + str(avg_ucs))
    print()

    load_puzzles = automate.load_csv("scenarios.csv")
    generate_puzzles = automate.create_puzzles_from_csv(load_puzzles)

    answer = input("Would you like to run scenarios.csv? (yes/no): ")

    if answer.lower() == "yes":
        for i in generate_puzzles:
            print(i)
            prob = EightPuzzleSearchProblem(i)
            pat = search.aStarSearch(prob)
            print("A* found a path of " + str(len(pat)) + " moves.")
            print(pat)
    print()

    puzzle = createRandomEightPuzzle(25)
    print('A random puzzle:')
    print(puzzle)
    print()

    problem = EightPuzzleSearchProblem(puzzle)
    path= search.aStarSearch(problem)    

    path2 = search.breadthFirstSearch(problem)

    print('A* found a path of %d moves: %s' % (len(path[0]), str(path[0])))
    print(path2)

    heuristicTests(puzzle, goal_state)

    curr = puzzle
    i = 1
    for a in path[0]:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))

        heuristicTests(curr, goal_state)

        print(curr)

        input("Press return for the next state...") # wait for key stroke
        print()
        i += 1

#*=====End Change Task 2 and 3=====*/
