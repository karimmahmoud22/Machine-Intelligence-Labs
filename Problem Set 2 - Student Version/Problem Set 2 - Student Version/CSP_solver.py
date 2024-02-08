from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    
    # for each binary constraint that involve the assigned variable
    for constraint in problem.constraints:
        
        if isinstance(constraint, BinaryConstraint):
            if assigned_variable in constraint.variables:
                other_variable = constraint.get_other(assigned_variable)
                
                # Skip constraints involving assigned variables
                if other_variable not in domains:
                    continue
                
                # Copy the domain to modify and check for consistency
                new_domain = domains[other_variable].copy()
                
                # set to store the values to remove from the domain
                to_remove = set()

                # loop over the values in the domain of the other variable
                for value in new_domain:

                    # create an assignment for the variables in the constraint
                    assignment = {assigned_variable: assigned_value, other_variable: value}

                    # check if the assignment satisfies the constraint
                    if not constraint.is_satisfied(assignment):

                        # if it does not, add the value to the set of values to remove
                        to_remove.add(value)

                # remove the values from the domain of the other variable
                new_domain -= to_remove

                domains[other_variable] = new_domain

                # check if the domain of the other variable is empty
                if len(new_domain) == 0:

                    # if it is, return False
                    return False
                
    
    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.

# This function should return the number of values in the domain of the given variable that are ruled out by the constraints involving the given variable.
def count_constrained_values(problem: Problem, variable_to_assign: str, value: Any, domains: Dict[str, set]) -> int:
    
    # Count the number of choices that are ruled out for the other variables
    count = 0
    
    # for each binary constraint that involve the assigned variable
    for constraint in problem.constraints:

        # Check if the constraint involves the assigned variable
        if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:

            # Get the other involved variable
            other_variable = constraint.variables[0] if constraint.variables[1] == variable_to_assign else constraint.variables[1]

            # Skip constraints involving assigned variables
            if other_variable not in domains:
                continue

            # Count the number of choices that are ruled out for the other variable
            for other_value in domains[other_variable]:
                if not constraint.condition(value, other_value):
                    count += 1

    return count

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:

    # create a dictionary to store the removed values for each value in the domain of the variable to assign
    removed_values = {}

    # Initialize the dictionary with the values in the domain of the variable to assign
    for value in domains[variable_to_assign]:
        removed_values[value] = 0

    # loop over the values in the domain of the variable to assign
    for value in domains[variable_to_assign]:

        # for each binary constraint that involve the assigned variable
        for constraint in problem.constraints:

            # check if the constraint involves the assigned variable
            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:

                # get the other involved variable
                other_variable = constraint.get_other(variable_to_assign)

                # skip constraints involving assigned variables
                if other_variable not in domains:
                    continue

                # count the number of choices that are ruled out for the other variable
                for other_value in domains[other_variable]:

                    # create an assignment for the variables in the constraint
                    assignment = {variable_to_assign: value, other_variable: other_value}

                    # check if the assignment satisfies the constraint
                    if not constraint.is_satisfied(assignment):

                        # if it does not, increment the number of removed values for the value in the domain of the variable to assign
                        removed_values[value] += 1

    # return the sorted removed values based on the number of removed values and the value itself
    return sorted(removed_values, key=lambda x: (removed_values[x], x))


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.

def solve(problem: Problem) -> Optional[Assignment]:

    # do the 1-consistency check
    if not one_consistency(problem):

        # if the problem is not 1-consistent, return None
        return None

    # create initial empty assignment for the variables
    assignment = {}

    # recursive search function to solve the problem
    def recursive_search(assignment: Assignment, domains: Dict[str, set]) -> Optional[Assignment]:
        
        # check if the assignment is complete
        if problem.is_complete(assignment):
            return assignment

        # get the variable to assign using the minimum remaining values heuristic
        variable = minimum_remaining_values(problem, domains)

        # get the least restraining values for the variable to assign
        for value in least_restraining_values(problem, variable, domains):
            
            # create a copy of the assignment to use in the forward checking
            new_assignmet = assignment.copy()

            # assign the value to the variable
            new_assignmet[variable] = value

            # create a copy of the domains to use in the forward checking
            new_domains = domains.copy()

            # remove the variable from the domains
            del new_domains[variable]

            # check if the assignment is consistent using the forward checking
            if forward_checking(problem, variable, value, new_domains):

                # if it is, call the recursive search with the new assignment and the new domains
                result = recursive_search(new_assignmet, new_domains)

                # check if the result is not None (a solution was found)
                if result is not None:
                    return result

        # if no solution was found,
        return None

    # call the recursive search with the initial assignment and the initial domains
    return recursive_search(assignment, problem.domains)
   