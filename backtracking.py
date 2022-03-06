from heuristics import mrv, lcv, static_ordering, unordered_domain_values
from inference import maintain_arc_consistency

"""
This module contains the main backtracking algorithm implementations.
The functions in this module are based on the algorithms as described in class slides
and in the textbook `Artificial Intelligence: A Modern Approach (Prentice Hall 2020)`:

function BACKTRACKING-SEARCH(csp) returns a solution or failure
    return BACKTRACK(csp, {})

function BACKTRACK(csp, assignment) returns a solution or failure
    if assignment is complete then return assignment
    var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
        if value is consistent with assignment then
            add {var = value} to assignment
            inferences <- INFERENCE(csp, var, assignment)
            if inferences != failure then
                add inferences to csp
                result <- BACKTRACK(csp, assignment)
                if result != failure then return result
                remove inferences from csp
            remove {var = value} from assignment
    return failure
"""
def backtracking_search(csp, verbose=True, select_unassigned_variable=mrv, order_domain_values=lcv, inference=maintain_arc_consistency):
    """
    Function that runs the backtracking search. All this function does is 
    wrap the backtrack method and passes it an initial empty assignment.
    It also prints the problem if needed (verbose=True).
    """
    if verbose:
        print_problem(select_unassigned_variable, order_domain_values, inference)
    if inference is None:
        return backtrack_no_inference(csp, {}, select_unassigned_variable, order_domain_values)
    return backtrack(csp, {}, select_unassigned_variable=select_unassigned_variable, order_domain_values=order_domain_values, inference=inference)

def backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference):
    """
    This function is the implementation of the backtracking algorithm. The corresponding
    lines from the pseudocode are included as comments above the actual code.
    arguments:
        :assignment: - A dictionary representing the assignments {var = value} thus far
        :select_unassigned_variable: - A function representing the variable ordering heuristic (e.g., mrv)
        :order_domain_values: - A function representing the value ordering heuristic (e.g., lcv)
        :inference: - A function representing the inference method (e.g., forward checking, mac/ac3)
    """
    # if assignment is complete then return assignment
    if csp.valid_solution(assignment): # Base case
        return assignment
    # var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    variable = select_unassigned_variable(csp, assignment)
    # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
    for value in order_domain_values(csp, variable, assignment):
        # if value is consistent with assignment then
        if csp.is_consistent(variable, {variable: value, **assignment}):
            # add {var = value} to assignment
            csp.assign(variable, value, assignment)
            csp.add_assignment(variable, value)
            # inferences <- INFERENCE(csp, var, assignment)
            inferences = inference(csp, variable, assignment)
            # if inferences != failure then
            if inferences != 'failure':
                # add inferences to csp
                csp.add_inferences(inferences)
                # result <- BACKTRACK(csp, assignment)
                result = backtrack(csp, assignment, select_unassigned_variable, order_domain_values, inference)
                # if result != failure then return result
                if result: return result
                # remove inferences from csp
                csp.remove_inferences(inferences)
            # remove {var = value} from assignment
            del assignment[variable]
    return None

def backtrack_no_inference(csp, assignment, select_unassigned_variable, order_domain_values):
    """
    Function that runs simple backtracking without inference. This method is a simpler variation of the 
    one with inference, where we simply add the next value to an assignment and check if the assignment
    is consistent rather than trying different inferences.
    """
    # if assignment is complete then return assignment
    if csp.valid_solution(assignment): # Base case
        return assignment
    # var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    variable = select_unassigned_variable(csp, assignment)
    # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
    for value in order_domain_values(csp, variable, assignment):
        local_assignment = assignment.copy()
        local_assignment[variable] = value
        # If assignment is consistent, we recurse
        if csp.is_consistent(variable, local_assignment):
            result = backtrack_no_inference(csp, local_assignment, select_unassigned_variable, order_domain_values)
            # if result != failure then return result
            if result is not None:
                return result
    return None

def print_problem(variable_heuristic, value_heuristic, inference):
    """
    Utility function to display the heuristics and inference method used in a CSP problem.
    """
    print("CSP problem attributes: ")
    for type_, function in {"Variable ordering heuristic": variable_heuristic, "Value ordering heuristic": value_heuristic, "Inference type": inference}.items():
        print(f"\t{type_} -> {function.__name__ if function else None}")
    print()