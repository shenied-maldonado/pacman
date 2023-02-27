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
    return [s, s, w, s, w, w, s, w]


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
    visited = set()

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier.push((start, []))  # (state, path) --> tuple[tuple[int: x, int: y], list[string]: path]

    while not frontier.isEmpty():
        current, path = frontier.pop()
        visited.add(current)

        if problem.isGoalState(current):
            return path

        for successor in problem.getSuccessors(current):
            position = successor[0]

            if position not in visited:
                new_path = path + [successor[1]]
                frontier.push((position, new_path))


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier = util.Queue()
    visited = set()

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    frontier.push((start, []))  # (state, path) --> tuple[tuple[int: x, int: y], list[string]: path]

    while not frontier.isEmpty():
        current, path = frontier.pop()
        visited.add(current)

        if problem.isGoalState(current):
            return path

        for successor in problem.getSuccessors(current):
            position = successor[0]

            if position not in visited:
                new_path = path + [successor[1]]
                frontier.push((position, new_path))


def uniformCostSearch(problem: SearchProblem):
    """Search the node of the least total cost first."""
    "*** YOUR CODE HERE ***"
    return aStarSearch(problem, heuristic=nullHeuristic)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()

    all_costs = {}
    all_paths = {}
    visited = set()

    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    all_costs[start] = 0.
    all_paths[start] = []
    frontier.push(start, 0. + heuristic(start, problem))

    while not frontier.isEmpty():
        current = frontier.pop()

        if problem.isGoalState(current):  # reached goal
            return all_paths[current]

        for successor in problem.getSuccessors(current):
            position = successor[0]  # tuple[int: x, int: y]: (x, y)
            direction = successor[1]  # string: 'direction'
            cost = successor[2]  # int: path_cost

            if position not in visited:  # unexplored node
                new_cost = all_costs[current] + cost
                new_path = all_paths[current] + [direction]

                if position in all_costs:  # known path_cost
                    if new_cost < all_costs[position]:
                        all_paths[position] = new_path
                        frontier.update(position, new_cost)

                else:  # unknown cost
                    all_costs[position] = new_cost
                    all_paths[position] = new_path
                    frontier.push(position, all_costs[position] + heuristic(position, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
