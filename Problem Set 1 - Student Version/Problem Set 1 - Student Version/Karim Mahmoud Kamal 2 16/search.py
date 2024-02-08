from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
from typing import List, Tuple, Optional, Set

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

#==> This function returns the cost of the node based on the algorithm
def CostFunction( algorithm : str, index: int, cost: int, problem: Problem[S, A],
                  state: S, child:S, action: A, heuristic: HeuristicFunction)       -> int:

    # ==> if the algorithm is BreadthFirstSearch, then the cost increases as level increase 
    if algorithm == 'BreadthFirst':
        return index

    # ==> if the algorithm is DepthFirstSearch, then the cost increases as level decrease
    elif algorithm == 'DepthFirst':
        return -1 * index
    
    # ==> if the algorithm is UniformCostSearch, then the cost is the cumulative cost of the path
    elif algorithm == 'UniformCost':
        return problem.get_cost(state, action) + cost 
    
    # ==> if the algorithm is AStarSearch, then the cost is the cumulative cost of the path + the heuristic value
    # ==> the heuristic value is the estimated cost from the current state to the goal state
    elif algorithm == 'AStar':
        return cost - heuristic(problem, state) + problem.get_cost(state, action)+ heuristic(problem, child) 

    # ==> if the algorithm is BestFirstSearch, then the cost is the heuristic value
    elif algorithm == 'BestFirst':
        return heuristic(problem, child)
    
    # ==> if the algorithm is not one of the above algorithms, then raise an exception
    else:
        raise Exception("Unknown algorithm")


# ==> GraphSearch function thaw will be used by all search algorithms
def GraphSearch (frontier: list, problem: Problem[S, A], algorithm: str, heuristic: HeuristicFunction) -> Solution:
    
    # ==> Initialize the index of the node
    index = 0
    
    # ==> Initialize the explored set to be empty
    explored = set()                  
    
    # ==> While the frontier is not empty
    while frontier: 
        
        # ==> Pop the shallowest node from the frontier
        cost, (temp_not_used, state), path = heapq.heappop(frontier) 
        # ==> if the node was not already explored before
        if state not in explored:
            
            # ==> if the node contains a goal state then return the corresponding solution
            if problem.is_goal(state):
                return path
            
            # ==> Add the node to the explored set
            explored.add(state) 
            
            # ==> For each action in the problem, we expand the chosen node
            # ==> for each action, we calculate the cost of the node and push it to the frontier
            for action in problem.get_actions(state): 

                # ==> get the child node
                child = problem.get_successor(state, action)
                
                # ==> increase the index
                index+=1

                # ==> calculate the cost of the child node based on the algorithm
                child_cost = CostFunction(algorithm, index, cost, problem, state, child, action, heuristic)

                # ==> if the child node was not already explored and not in the frontier, then push it to the frontier
                if child not in explored and child not in frontier:
                    # ==> check if the child node is a goal state and the algorithm is BreadthFirst
                    # ==> if the child node is a goal state and the algorithm is BreadthFirst, then return the corresponding solution
                    if problem.is_goal(child) and algorithm == 'BreadthFirst':
                        return path + [action] 
                    
                    # ==> push the child node to the frontier
                    heapq.heappush(frontier, (child_cost,(index, child), path + [action])) 

    # ==> if no solution was found, then return None
    return None


# ==> The following comment for BFS and DFS:
    # ==> each node in the frontier is a tuple of ( (index, node) , path)
    # ==> We used an index to differentiate between nodes with the same state but different parents

# ==> BreadthFirstSearch
def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier = [(0, (0, initial_state), [])] 
    return GraphSearch(frontier, problem, 'BreadthFirst', None)

# ==> DepthFirstSearch
def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier = [(0, (0, initial_state), [])] 
    return GraphSearch(frontier, problem, 'DepthFirst', None)
    
# ==> The following comment for UCS and AStar and BestFirst:
    # ==> each node in the frontier is a tuple of ( cumulative_path_cost, (index, node), path)
    # ==> We used an index to differentiate between nodes with the same state but different parents

# ==> UniformCostSearch
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier = [(0, (0, initial_state), [])]
    return GraphSearch(frontier, problem, 'UniformCost', None)

# ==> AStarSearch
def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    frontier = [(heuristic(problem, initial_state) + 0, (0, initial_state), [])] 
    return GraphSearch(frontier, problem, 'AStar', heuristic)

# ==> BestFirstSearch
def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    frontier = [(heuristic(problem, initial_state), (0, initial_state), [])] 
    return GraphSearch(frontier, problem, 'BestFirst', heuristic)
